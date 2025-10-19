"""
Train a real Transformer model on the bentrevett/multi30k dataset
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from datasets import load_dataset
import numpy as np
from tqdm import tqdm
import os
import json
from loguru import logger

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

class TranslationDataset(Dataset):
    def __init__(self, texts, targets, tokenizer, max_length=128):
        self.texts = texts
        self.targets = targets
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        target = str(self.targets[idx])
        
        # Tokenize inputs
        inputs = self.tokenizer(
            text, 
            max_length=self.max_length, 
            padding='max_length', 
            truncation=True, 
            return_tensors='pt'
        )
        
        # Tokenize targets
        targets = self.tokenizer(
            target, 
            max_length=self.max_length, 
            padding='max_length', 
            truncation=True, 
            return_tensors='pt'
        )
        
        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': targets['input_ids'].squeeze()
        }

def load_and_preprocess_data():
    """Load and preprocess the multi30k dataset"""
    logger.info("Loading bentrevett/multi30k dataset...")
    
    # Load dataset
    dataset = load_dataset("bentrevett/multi30k")
    
    # Get English-German pairs
    train_data = dataset['train']
    val_data = dataset['validation']
    test_data = dataset['test']
    
    logger.info(f"Train samples: {len(train_data)}")
    logger.info(f"Validation samples: {len(val_data)}")
    logger.info(f"Test samples: {len(test_data)}")
    
    # Extract English and German texts
    train_en = [item['en'] for item in train_data]
    train_de = [item['de'] for item in train_data]
    
    val_en = [item['en'] for item in val_data]
    val_de = [item['de'] for item in val_data]
    
    test_en = [item['en'] for item in test_data]
    test_de = [item['de'] for item in test_data]
    
    # Load tokenizer
    logger.info("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained("t5-small")
    
    # Add special tokens for different languages
    special_tokens = {
        "additional_special_tokens": ["<en>", "<de>", "<fr>", "<es>"]
    }
    tokenizer.add_special_tokens(special_tokens)
    
    return {
        'train': (train_en, train_de),
        'val': (val_en, val_de),
        'test': (test_en, test_de),
        'tokenizer': tokenizer
    }

def create_data_loaders(data, tokenizer, batch_size=32):
    """Create data loaders for training"""
    train_en, train_de = data['train']
    val_en, val_de = data['val']
    
    # Create datasets
    train_dataset = TranslationDataset(train_en, train_de, tokenizer)
    val_dataset = TranslationDataset(val_en, val_de, tokenizer)
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader

def train_model():
    """Train the Transformer model"""
    logger.info("Starting model training...")
    
    # Load and preprocess data
    data = load_and_preprocess_data()
    tokenizer = data['tokenizer']
    
    # Create data loaders with smaller batch size
    train_loader, val_loader = create_data_loaders(data, tokenizer, batch_size=4)
    
    # Load model
    logger.info("Loading T5 model...")
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
    model.resize_token_embeddings(len(tokenizer))
    model = model.to(device)
    
    # Training parameters
    num_epochs = 1  # Reduced for faster training
    learning_rate = 1e-4  # Smaller learning rate
    
    # Optimizer and loss function
    optimizer = optim.AdamW(model.parameters(), lr=learning_rate)
    criterion = nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
    
    # Training loop
    model.train()
    for epoch in range(num_epochs):
        logger.info(f"Epoch {epoch + 1}/{num_epochs}")
        
        total_loss = 0
        # Limit training to first 100 batches for faster training
        limited_loader = list(train_loader)[:100]
        
        for batch_idx, batch in enumerate(tqdm(limited_loader, desc="Training")):
            # Move to device
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            # Forward pass
            optimizer.zero_grad()
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            total_loss += loss.item()
            
            # Backward pass
            loss.backward()
            optimizer.step()
            
            if batch_idx % 10 == 0:
                logger.info(f"Batch {batch_idx}, Loss: {loss.item():.4f}")
        
        avg_loss = total_loss / len(limited_loader)
        logger.info(f"Epoch {epoch + 1} Average Loss: {avg_loss:.4f}")
        
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
                val_loss += outputs.loss.item()
        
        val_loss = val_loss / len(val_loader)
        logger.info(f"Validation Loss: {val_loss:.4f}")
        model.train()
    
    # Save model and tokenizer
    logger.info("Saving model...")
    model_save_path = "trained_translation_model"
    os.makedirs(model_save_path, exist_ok=True)
    
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    
    logger.info(f"Model saved to {model_save_path}")
    
    return model, tokenizer

def test_translation(model, tokenizer, text, target_lang="de"):
    """Test translation with the trained model"""
    model.eval()
    
    # For T5, we need to format as a translation task
    if target_lang == "de":
        input_text = f"translate English to German: {text}"
    elif target_lang == "fr":
        input_text = f"translate English to French: {text}"
    elif target_lang == "es":
        input_text = f"translate English to Spanish: {text}"
    else:
        input_text = f"translate English to English: {text}"
    
    # Tokenize
    inputs = tokenizer(
        input_text,
        max_length=128,
        padding=True,
        truncation=True,
        return_tensors='pt'
    ).to(device)
    
    # Generate translation
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=128,
            num_beams=4,
            early_stopping=True,
            do_sample=False
        )
    
    # Decode
    translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translation

if __name__ == "__main__":
    logger.info("Starting real model training...")
    
    # Train model
    model, tokenizer = train_model()
    
    # Test translation
    logger.info("Testing translation...")
    test_texts = [
        "Hello, how are you?",
        "I love programming",
        "The weather is beautiful today",
        "Can you help me with this?",
        "Thank you very much"
    ]
    
    for text in test_texts:
        translation = test_translation(model, tokenizer, text, "de")
        logger.info(f"EN: {text}")
        logger.info(f"DE: {translation}")
        logger.info("---")
    
    logger.info("Training completed!")
