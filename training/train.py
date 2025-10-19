#!/usr/bin/env python3
"""
Main training script for the multilingual translation model.
"""

import os
import sys
import argparse
import yaml
import torch
from loguru import logger
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from data.preprocessing import DataPreprocessor
from models.transformer_model import TransformerNMT, create_model
from training.trainer import NMTTrainer
from evaluation.metrics import evaluate_translations


def load_config(config_path: str) -> dict:
    """Load training configuration from YAML file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration."""
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    logger.add(
        "logs/training.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="10 MB"
    )


def main():
    parser = argparse.ArgumentParser(description="Train multilingual translation model")
    parser.add_argument("--config", type=str, default="configs/base_config.yaml",
                       help="Path to configuration file")
    parser.add_argument("--resume", type=str, default=None,
                       help="Path to checkpoint to resume from")
    parser.add_argument("--log-level", type=str, default="INFO",
                       choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                       help="Logging level")
    
    args = parser.parse_args()
    
    # Setup logging
    os.makedirs("logs", exist_ok=True)
    setup_logging(args.log_level)
    
    logger.info("Starting multilingual translation model training")
    logger.info(f"Using configuration: {args.config}")
    
    # Load configuration
    config = load_config(args.config)
    logger.info(f"Configuration loaded: {config}")
    
    # Set device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Using device: {device}")
    
    # Initialize data preprocessor
    logger.info("Initializing data preprocessor...")
    preprocessor = DataPreprocessor(
        model_name=config.get('tokenizer_model', 'facebook/mbart-large-50'),
        max_length=config.get('max_length', 128),
        cache_dir=config.get('cache_dir', './data/cache')
    )
    
    # Load and preprocess data
    logger.info("Loading and preprocessing data...")
    datasets = preprocessor.load_multi30k_dataset(
        languages=config.get('languages', ['en', 'de', 'fr'])
    )
    
    if not datasets:
        logger.error("No datasets loaded. Exiting.")
        return
    
    # Create data loaders
    logger.info("Creating data loaders...")
    data_loaders = preprocessor.create_data_loaders(
        datasets,
        batch_size=config.get('batch_size', 32),
        num_workers=config.get('num_workers', 4)
    )
    
    # Create model
    logger.info("Creating model...")
    model_config = {
        'src_vocab_size': config.get('src_vocab_size', 10000),
        'tgt_vocab_size': config.get('tgt_vocab_size', 10000),
        'd_model': config.get('d_model', 512),
        'n_heads': config.get('n_heads', 8),
        'n_layers': config.get('n_layers', 6),
        'd_ff': config.get('d_ff', 2048),
        'max_len': config.get('max_len', 5000),
        'dropout': config.get('dropout', 0.1)
    }
    
    model = create_model(model_config)
    logger.info(f"Model created with {model.get_model_size():,} parameters")
    
    # Create trainer
    logger.info("Initializing trainer...")
    trainer_config = {
        'learning_rate': config.get('learning_rate', 1e-4),
        'batch_size': config.get('batch_size', 32),
        'num_epochs': config.get('num_epochs', 10),
        'gradient_clip': config.get('gradient_clip', 1.0),
        'warmup_steps': config.get('warmup_steps', 4000),
        'use_amp': config.get('use_amp', True),
        'checkpoint_dir': config.get('checkpoint_dir', './checkpoints'),
        'log_interval': config.get('log_interval', 100),
        'save_interval': config.get('save_interval', 1000)
    }
    
    trainer = NMTTrainer(model, trainer_config, device)
    
    # Resume from checkpoint if specified
    if args.resume:
        logger.info(f"Resuming from checkpoint: {args.resume}")
        start_epoch = trainer.load_checkpoint(args.resume)
        logger.info(f"Resumed from epoch {start_epoch}")
    
    # Start training
    logger.info("Starting training...")
    
    # Use the first language pair for training
    lang_pair = list(data_loaders.keys())[0]
    train_loader = data_loaders[lang_pair]['train']
    val_loader = data_loaders[lang_pair].get('validation')
    
    logger.info(f"Training on language pair: {lang_pair}")
    logger.info(f"Train batches: {len(train_loader)}")
    if val_loader:
        logger.info(f"Validation batches: {len(val_loader)}")
    
    # Train the model
    trainer.train(train_loader, val_loader)
    
    # Save final model
    logger.info("Saving final model...")
    final_model_path = os.path.join(trainer_config['checkpoint_dir'], 'final_model.pt')
    model.save_model(final_model_path)
    
    # Evaluate on test set if available
    if 'test' in data_loaders[lang_pair]:
        logger.info("Evaluating on test set...")
        test_loader = data_loaders[lang_pair]['test']
        
        # This is a simplified evaluation
        # In practice, you'd implement proper evaluation with BLEU, etc.
        model.eval()
        total_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch in test_loader:
                # Move to device
                input_ids = batch['input_ids'].to(device)
                labels = batch['labels'].to(device)
                
                # Forward pass
                decoder_input = labels[:, :-1]
                decoder_target = labels[:, 1:]
                
                outputs = model(input_ids, decoder_input)
                loss = trainer.criterion(
                    outputs.reshape(-1, outputs.size(-1)),
                    decoder_target.reshape(-1)
                )
                
                total_loss += loss.item()
                num_batches += 1
        
        avg_loss = total_loss / num_batches
        logger.info(f"Test loss: {avg_loss:.4f}")
    
    logger.info("Training completed successfully!")
    logger.info(f"Best model saved with BLEU: {trainer.best_bleu:.4f}")


if __name__ == "__main__":
    main()



