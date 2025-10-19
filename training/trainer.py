"""
Training pipeline for the Transformer NMT model.
Includes mixed precision training, checkpointing, and comprehensive logging.
"""

import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torch.cuda.amp import GradScaler, autocast
import wandb
from loguru import logger
from typing import Dict, Any, Optional, Tuple
import numpy as np
from tqdm import tqdm
import json

from models.transformer_model import TransformerNMT
from evaluation.metrics import calculate_bleu, calculate_chrf, calculate_ter


class NMTTrainer:
    """Trainer class for Neural Machine Translation model."""
    
    def __init__(self, model: TransformerNMT, config: Dict[str, Any], 
                 device: str = 'cuda' if torch.cuda.is_available() else 'cpu'):
        self.model = model.to(device)
        self.config = config
        self.device = device
        
        # Training parameters
        self.learning_rate = config.get('learning_rate', 1e-4)
        self.batch_size = config.get('batch_size', 32)
        self.num_epochs = config.get('num_epochs', 10)
        self.gradient_clip = config.get('gradient_clip', 1.0)
        self.warmup_steps = config.get('warmup_steps', 4000)
        
        # Mixed precision training
        self.use_amp = config.get('use_amp', True)
        self.scaler = GradScaler() if self.use_amp else None
        
        # Optimizer and scheduler
        self.optimizer = self._create_optimizer()
        self.scheduler = self._create_scheduler()
        
        # Loss function
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding tokens
        
        # Logging
        self.log_interval = config.get('log_interval', 100)
        self.save_interval = config.get('save_interval', 1000)
        
        # Checkpointing
        self.checkpoint_dir = config.get('checkpoint_dir', './checkpoints')
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        
        # Best metrics tracking
        self.best_bleu = 0.0
        self.best_epoch = 0
        
        logger.info(f"Initialized NMTTrainer on device: {device}")
        logger.info(f"Model parameters: {self.model.get_model_size():,}")
    
    def _create_optimizer(self) -> optim.Optimizer:
        """Create optimizer with different learning rates for different components."""
        # Different learning rates for different parts
        encoder_params = list(self.model.encoder.parameters())
        decoder_params = list(self.model.decoder.parameters())
        other_params = list(self.model.output_projection.parameters()) + \
                      list(self.model.language_embeddings.parameters())
        
        optimizer = optim.Adam([
            {'params': encoder_params, 'lr': self.learning_rate},
            {'params': decoder_params, 'lr': self.learning_rate},
            {'params': other_params, 'lr': self.learning_rate * 2}  # Higher LR for output layer
        ], betas=(0.9, 0.98), eps=1e-9)
        
        return optimizer
    
    def _create_scheduler(self) -> optim.lr_scheduler.LambdaLR:
        """Create learning rate scheduler with warmup."""
        def lr_lambda(step):
            if step < self.warmup_steps:
                return step / self.warmup_steps
            else:
                return (self.warmup_steps / step) ** 0.5
        
        return optim.lr_scheduler.LambdaLR(self.optimizer, lr_lambda)
    
    def train_epoch(self, train_loader: DataLoader, epoch: int) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        progress_bar = tqdm(train_loader, desc=f"Epoch {epoch}")
        
        for batch_idx, batch in enumerate(progress_bar):
            # Move batch to device
            input_ids = batch['input_ids'].to(self.device)
            attention_mask = batch['attention_mask'].to(self.device)
            labels = batch['labels'].to(self.device)
            target_attention_mask = batch['target_attention_mask'].to(self.device)
            
            # Prepare input and target for teacher forcing
            decoder_input = labels[:, :-1]  # Remove last token
            decoder_target = labels[:, 1:]  # Remove first token
            
            # Zero gradients
            self.optimizer.zero_grad()
            
            # Forward pass with mixed precision
            if self.use_amp:
                with autocast():
                    outputs = self.model(input_ids, decoder_input)
                    loss = self.criterion(
                        outputs.reshape(-1, outputs.size(-1)),
                        decoder_target.reshape(-1)
                    )
            else:
                outputs = self.model(input_ids, decoder_input)
                loss = self.criterion(
                    outputs.reshape(-1, outputs.size(-1)),
                    decoder_target.reshape(-1)
                )
            
            # Backward pass
            if self.use_amp:
                self.scaler.scale(loss).backward()
                self.scaler.unscale_(self.optimizer)
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.gradient_clip)
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), self.gradient_clip)
                self.optimizer.step()
            
            # Update scheduler
            self.scheduler.step()
            
            # Update metrics
            total_loss += loss.item()
            num_batches += 1
            
            # Update progress bar
            current_lr = self.scheduler.get_last_lr()[0]
            progress_bar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'avg_loss': f'{total_loss/num_batches:.4f}',
                'lr': f'{current_lr:.2e}'
            })
            
            # Logging
            if batch_idx % self.log_interval == 0:
                logger.info(f"Epoch {epoch}, Batch {batch_idx}, Loss: {loss.item():.4f}")
                
                if wandb.run is not None:
                    wandb.log({
                        'train/loss': loss.item(),
                        'train/learning_rate': current_lr,
                        'train/epoch': epoch,
                        'train/batch': batch_idx
                    })
            
            # Save checkpoint
            if batch_idx % self.save_interval == 0 and batch_idx > 0:
                self.save_checkpoint(epoch, batch_idx, loss.item())
        
        avg_loss = total_loss / num_batches
        return {'loss': avg_loss}
    
    def validate(self, val_loader: DataLoader, epoch: int) -> Dict[str, float]:
        """Validate the model."""
        self.model.eval()
        total_loss = 0.0
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for batch in tqdm(val_loader, desc="Validation"):
                # Move batch to device
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)
                
                # Prepare input and target
                decoder_input = labels[:, :-1]
                decoder_target = labels[:, 1:]
                
                # Forward pass
                if self.use_amp:
                    with autocast():
                        outputs = self.model(input_ids, decoder_input)
                        loss = self.criterion(
                            outputs.reshape(-1, outputs.size(-1)),
                            decoder_target.reshape(-1)
                        )
                else:
                    outputs = self.model(input_ids, decoder_input)
                    loss = self.criterion(
                        outputs.reshape(-1, outputs.size(-1)),
                        decoder_target.reshape(-1)
                    )
                
                total_loss += loss.item()
                
                # Generate predictions for evaluation
                predictions = self.model.generate(input_ids, max_length=50)
                all_predictions.extend(predictions.cpu().numpy())
                all_targets.extend(decoder_target.cpu().numpy())
        
        avg_loss = total_loss / len(val_loader)
        
        # Calculate metrics (simplified for now)
        # In practice, you'd need to decode tokens back to text
        metrics = {
            'val_loss': avg_loss,
            'val_bleu': 0.0,  # Placeholder
            'val_chrf': 0.0,  # Placeholder
            'val_ter': 0.0    # Placeholder
        }
        
        logger.info(f"Validation - Loss: {avg_loss:.4f}")
        
        if wandb.run is not None:
            wandb.log({
                'val/loss': avg_loss,
                'val/epoch': epoch
            })
        
        return metrics
    
    def train(self, train_loader: DataLoader, val_loader: Optional[DataLoader] = None):
        """Main training loop."""
        logger.info(f"Starting training for {self.num_epochs} epochs")
        
        for epoch in range(1, self.num_epochs + 1):
            start_time = time.time()
            
            # Train epoch
            train_metrics = self.train_epoch(train_loader, epoch)
            
            # Validate
            val_metrics = {}
            if val_loader is not None:
                val_metrics = self.validate(val_loader, epoch)
                
                # Check if this is the best model
                if val_metrics.get('val_bleu', 0) > self.best_bleu:
                    self.best_bleu = val_metrics['val_bleu']
                    self.best_epoch = epoch
                    self.save_checkpoint(epoch, 0, val_metrics['val_loss'], is_best=True)
            
            # Log epoch summary
            epoch_time = time.time() - start_time
            logger.info(f"Epoch {epoch} completed in {epoch_time:.2f}s")
            logger.info(f"Train Loss: {train_metrics['loss']:.4f}")
            if val_metrics:
                logger.info(f"Val Loss: {val_metrics.get('val_loss', 0):.4f}")
                logger.info(f"Val BLEU: {val_metrics.get('val_bleu', 0):.4f}")
            
            # Save regular checkpoint
            if epoch % 5 == 0:  # Save every 5 epochs
                self.save_checkpoint(epoch, 0, train_metrics['loss'])
        
        logger.info(f"Training completed! Best BLEU: {self.best_bleu:.4f} at epoch {self.best_epoch}")
    
    def save_checkpoint(self, epoch: int, batch_idx: int, loss: float, is_best: bool = False):
        """Save model checkpoint."""
        checkpoint = {
            'epoch': epoch,
            'batch_idx': batch_idx,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'loss': loss,
            'config': self.config
        }
        
        if self.scaler is not None:
            checkpoint['scaler_state_dict'] = self.scaler.state_dict()
        
        # Save regular checkpoint
        filename = f"checkpoint_epoch_{epoch}_batch_{batch_idx}.pt"
        filepath = os.path.join(self.checkpoint_dir, filename)
        torch.save(checkpoint, filepath)
        
        # Save best model
        if is_best:
            best_filepath = os.path.join(self.checkpoint_dir, "best_model.pt")
            torch.save(checkpoint, best_filepath)
            logger.info(f"New best model saved with BLEU: {self.best_bleu:.4f}")
        
        logger.info(f"Checkpoint saved: {filepath}")
    
    def load_checkpoint(self, filepath: str):
        """Load model checkpoint."""
        checkpoint = torch.load(filepath, map_location=self.device)
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        
        if self.scaler is not None and 'scaler_state_dict' in checkpoint:
            self.scaler.load_state_dict(checkpoint['scaler_state_dict'])
        
        logger.info(f"Checkpoint loaded from {filepath}")
        return checkpoint['epoch']


def main():
    """Test the trainer."""
    logger.info("Testing NMTTrainer")
    
    # Create a small model for testing
    from models.transformer_model import TransformerNMT
    
    model = TransformerNMT(
        src_vocab_size=10000,
        tgt_vocab_size=10000,
        d_model=128,
        n_heads=4,
        n_layers=2
    )
    
    # Training config
    config = {
        'learning_rate': 1e-4,
        'batch_size': 16,
        'num_epochs': 2,
        'use_amp': True,
        'checkpoint_dir': './test_checkpoints'
    }
    
    # Create trainer
    trainer = NMTTrainer(model, config)
    
    # Create dummy data loaders
    from torch.utils.data import DataLoader, TensorDataset
    
    # Dummy data
    batch_size = 16
    seq_len = 20
    
    dummy_data = TensorDataset(
        torch.randint(0, 10000, (100, seq_len)),  # input_ids
        torch.ones(100, seq_len),  # attention_mask
        torch.randint(0, 10000, (100, seq_len)),  # labels
        torch.ones(100, seq_len)   # target_attention_mask
    )
    
    train_loader = DataLoader(dummy_data, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(dummy_data, batch_size=batch_size, shuffle=False)
    
    # Test training
    logger.info("Starting test training...")
    trainer.train(train_loader, val_loader)
    
    logger.info("Trainer test completed successfully!")


if __name__ == "__main__":
    main()



