# Training Guide

## Overview

This guide covers training the multilingual translation model using the Transformer architecture. The training pipeline supports GPU acceleration, mixed precision training, and comprehensive evaluation metrics.

## Prerequisites

### Hardware Requirements

**Minimum:**
- CPU: 4 cores, 8GB RAM
- GPU: 4GB VRAM (for small models)
- Storage: 10GB free space

**Recommended:**
- CPU: 8+ cores, 32GB+ RAM
- GPU: 8GB+ VRAM (RTX 3070, V100, A100)
- Storage: 50GB+ free space (SSD preferred)

### Software Requirements

- Python 3.8+
- CUDA 11.8+ (for GPU training)
- PyTorch 2.0+
- Transformers 4.30+
- Datasets 2.12+

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Basic Training

```bash
# Train with default configuration
python training/train.py

# Train with custom configuration
python training/train.py --config configs/custom_config.yaml

# Resume from checkpoint
python training/train.py --resume checkpoints/checkpoint_epoch_5.pt
```

### 3. Monitor Training

```bash
# View training logs
tail -f logs/training.log

# Monitor with TensorBoard
tensorboard --logdir runs/

# Monitor with Weights & Biases
wandb login
python training/train.py --config configs/wandb_config.yaml
```

## Configuration

### Configuration File Structure

```yaml
# Data configuration
languages: ['en', 'de', 'fr']
max_length: 128
cache_dir: './data/cache'
tokenizer_model: 'facebook/mbart-large-50'

# Model configuration
src_vocab_size: 10000
tgt_vocab_size: 10000
d_model: 512
n_heads: 8
n_layers: 6
d_ff: 2048
dropout: 0.1

# Training configuration
batch_size: 32
num_epochs: 10
learning_rate: 1e-4
gradient_clip: 1.0
warmup_steps: 4000
use_amp: true

# Logging and checkpointing
log_interval: 100
save_interval: 1000
checkpoint_dir: './checkpoints'
```

### Model Configurations

#### Small Model (Fast Training)
```yaml
d_model: 256
n_heads: 4
n_layers: 3
d_ff: 1024
batch_size: 64
```

#### Medium Model (Balanced)
```yaml
d_model: 512
n_heads: 8
n_layers: 6
d_ff: 2048
batch_size: 32
```

#### Large Model (Best Quality)
```yaml
d_model: 1024
n_heads: 16
n_layers: 12
d_ff: 4096
batch_size: 16
```

## Training Process

### 1. Data Preparation

The training pipeline automatically:

1. **Loads Multi30K Dataset**
   - Downloads from HuggingFace
   - Creates train/validation/test splits
   - Handles multiple language pairs

2. **Preprocesses Data**
   - Text normalization
   - Tokenization
   - Subword encoding
   - Data augmentation (optional)

3. **Creates Data Loaders**
   - PyTorch DataLoader
   - Batch processing
   - Parallel loading

### 2. Model Initialization

```python
from models.transformer_model import create_model

config = {
    'src_vocab_size': 10000,
    'tgt_vocab_size': 10000,
    'd_model': 512,
    'n_heads': 8,
    'n_layers': 6,
    'd_ff': 2048,
    'max_len': 5000,
    'dropout': 0.1
}

model = create_model(config)
```

### 3. Training Loop

The training process includes:

1. **Forward Pass**
   - Encoder processes source text
   - Decoder generates target text
   - Teacher forcing during training

2. **Loss Calculation**
   - Cross-entropy loss
   - Label smoothing
   - Ignore padding tokens

3. **Backward Pass**
   - Gradient computation
   - Gradient clipping
   - Parameter updates

4. **Optimization**
   - Adam optimizer
   - Learning rate scheduling
   - Mixed precision training

### 4. Validation

During training, the model is evaluated on:

- **Validation Loss**: Cross-entropy loss on validation set
- **BLEU Score**: Bilingual Evaluation Understudy
- **chrF Score**: Character n-gram F-score
- **TER Score**: Translation Error Rate

## Advanced Training

### Mixed Precision Training

```yaml
use_amp: true
```

Benefits:
- Faster training
- Lower memory usage
- Better GPU utilization

### Gradient Accumulation

```yaml
gradient_accumulation_steps: 4
effective_batch_size: 128
```

Useful for:
- Large models with limited GPU memory
- Simulating larger batch sizes

### Learning Rate Scheduling

```yaml
scheduler: 'cosine'
warmup_steps: 4000
max_lr: 1e-3
min_lr: 1e-6
```

Available schedulers:
- `cosine`: Cosine annealing
- `linear`: Linear warmup + decay
- `constant`: Constant learning rate

### Data Augmentation

```yaml
use_back_translation: true
augmentation_ratio: 0.1
noise_probability: 0.1
```

Augmentation techniques:
- Back translation
- Random noise injection
- Synonym replacement
- Paraphrasing

## Monitoring and Logging

### TensorBoard

```bash
# Start TensorBoard
tensorboard --logdir runs/

# View metrics
# - Loss curves
# - Learning rate
# - Gradient norms
# - Attention visualizations
```

### Weights & Biases

```python
# Initialize W&B
import wandb

wandb.init(
    project="multilingual-translation",
    config=config
)

# Log metrics
wandb.log({
    'train/loss': loss,
    'val/bleu': bleu_score,
    'learning_rate': lr
})
```

### Custom Logging

```python
from loguru import logger

# Configure logging
logger.add("logs/training.log", rotation="10 MB")

# Log custom metrics
logger.info(f"Epoch {epoch}, Loss: {loss:.4f}, BLEU: {bleu:.4f}")
```

## Checkpointing

### Automatic Checkpointing

The training pipeline automatically saves:

- **Regular Checkpoints**: Every N batches
- **Best Model**: Based on validation BLEU
- **Final Model**: At training completion

### Manual Checkpointing

```python
# Save checkpoint
trainer.save_checkpoint(epoch, batch_idx, loss)

# Load checkpoint
start_epoch = trainer.load_checkpoint("checkpoints/best_model.pt")
```

### Checkpoint Structure

```python
checkpoint = {
    'epoch': 5,
    'batch_idx': 1000,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'scheduler_state_dict': scheduler.state_dict(),
    'loss': 0.234,
    'bleu': 0.456,
    'config': config
}
```

## Evaluation

### Automatic Evaluation

The training pipeline evaluates on:

1. **Validation Set**: During training
2. **Test Set**: After training completion
3. **Custom Datasets**: For specific domains

### Manual Evaluation

```python
from evaluation.metrics import evaluate_translations

# Evaluate on custom data
candidates = ["Hello world", "Good morning"]
references = [["Hallo Welt"], ["Guten Morgen"]]

results = evaluate_translations(candidates, references)
print(f"BLEU: {results['bleu']:.4f}")
print(f"chrF: {results['chrf']:.4f}")
```

### Evaluation Metrics

- **BLEU**: Measures n-gram precision
- **chrF**: Character-level F-score
- **TER**: Translation Error Rate
- **METEOR**: Semantic similarity

## Troubleshooting

### Common Issues

#### Out of Memory (OOM)

**Solutions:**
- Reduce batch size
- Use gradient accumulation
- Enable mixed precision
- Use smaller model

```yaml
batch_size: 16
gradient_accumulation_steps: 4
use_amp: true
```

#### Slow Training

**Solutions:**
- Use GPU acceleration
- Increase batch size
- Optimize data loading
- Use mixed precision

```yaml
batch_size: 64
num_workers: 8
use_amp: true
```

#### Poor Convergence

**Solutions:**
- Adjust learning rate
- Use learning rate scheduling
- Add regularization
- Check data quality

```yaml
learning_rate: 5e-5
scheduler: 'cosine'
weight_decay: 0.01
label_smoothing: 0.1
```

### Debugging

#### Enable Debug Logging

```bash
python training/train.py --log-level DEBUG
```

#### Check Data Loading

```python
# Test data loader
for batch in train_loader:
    print(f"Batch shape: {batch['input_ids'].shape}")
    break
```

#### Monitor GPU Usage

```bash
# Monitor GPU
nvidia-smi -l 1

# Check memory usage
watch -n 1 nvidia-smi
```

## Best Practices

### 1. Data Quality

- Clean and normalize text
- Remove duplicates
- Balance language pairs
- Validate translations

### 2. Model Architecture

- Start with small models
- Gradually increase size
- Use proven architectures
- Experiment with hyperparameters

### 3. Training Strategy

- Use validation set for early stopping
- Monitor multiple metrics
- Save best checkpoints
- Regular evaluation

### 4. Resource Management

- Monitor GPU memory
- Use appropriate batch sizes
- Enable mixed precision
- Optimize data loading

## Production Deployment

### Model Optimization

```python
# Convert to TorchScript
model_scripted = torch.jit.script(model)
model_scripted.save("model_scripted.pt")

# Convert to ONNX
torch.onnx.export(model, dummy_input, "model.onnx")
```

### Model Serving

```python
# Load optimized model
model = torch.jit.load("model_scripted.pt")
model.eval()

# Fast inference
with torch.no_grad():
    output = model(input_ids)
```

## Performance Benchmarks

### Training Speed

| Model Size | GPU | Batch Size | Time/Epoch |
|------------|-----|------------|------------|
| Small (256) | RTX 3070 | 64 | 5 min |
| Medium (512) | RTX 3070 | 32 | 15 min |
| Large (1024) | A100 | 16 | 30 min |

### Memory Usage

| Model Size | GPU Memory | CPU Memory |
|------------|------------|------------|
| Small (256) | 4GB | 8GB |
| Medium (512) | 8GB | 16GB |
| Large (1024) | 16GB | 32GB |

### Quality Metrics

| Model Size | BLEU | chrF | TER |
|------------|------|------|-----|
| Small (256) | 0.25 | 0.45 | 0.60 |
| Medium (512) | 0.35 | 0.55 | 0.45 |
| Large (1024) | 0.42 | 0.62 | 0.35 |



