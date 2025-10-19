"""
Unit tests for the Transformer model.
"""

import pytest
import torch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from models.transformer_model import TransformerNMT, create_model


class TestTransformerNMT:
    """Test cases for TransformerNMT model."""
    
    def test_model_creation(self):
        """Test model creation with default parameters."""
        model = TransformerNMT(
            src_vocab_size=1000,
            tgt_vocab_size=1000,
            d_model=128,
            n_heads=4,
            n_layers=2
        )
        
        assert model.src_vocab_size == 1000
        assert model.tgt_vocab_size == 1000
        assert model.d_model == 128
        assert model.get_model_size() > 0
    
    def test_forward_pass(self):
        """Test forward pass through the model."""
        model = TransformerNMT(
            src_vocab_size=1000,
            tgt_vocab_size=1000,
            d_model=64,
            n_heads=2,
            n_layers=1
        )
        
        batch_size = 2
        src_len = 10
        tgt_len = 8
        
        src = torch.randint(0, 1000, (batch_size, src_len))
        tgt = torch.randint(0, 1000, (batch_size, tgt_len))
        
        output = model(src, tgt)
        
        assert output.shape == (batch_size, tgt_len, 1000)
    
    def test_generation(self):
        """Test text generation."""
        model = TransformerNMT(
            src_vocab_size=1000,
            tgt_vocab_size=1000,
            d_model=64,
            n_heads=2,
            n_layers=1
        )
        
        batch_size = 1
        src_len = 5
        
        src = torch.randint(0, 1000, (batch_size, src_len))
        
        generated = model.generate(src, max_length=10)
        
        assert generated.shape[0] == batch_size
        assert generated.shape[1] <= 10
    
    def test_model_save_load(self):
        """Test model saving and loading."""
        model = TransformerNMT(
            src_vocab_size=1000,
            tgt_vocab_size=1000,
            d_model=64,
            n_heads=2,
            n_layers=1
        )
        
        # Save model
        model.save_model("test_model.pt")
        
        # Load model
        loaded_model = TransformerNMT.load_model("test_model.pt")
        
        assert loaded_model.src_vocab_size == model.src_vocab_size
        assert loaded_model.tgt_vocab_size == model.tgt_vocab_size
        assert loaded_model.d_model == model.d_model
        
        # Clean up
        import os
        os.remove("test_model.pt")
    
    def test_create_model_from_config(self):
        """Test model creation from configuration."""
        config = {
            'src_vocab_size': 1000,
            'tgt_vocab_size': 1000,
            'd_model': 64,
            'n_heads': 2,
            'n_layers': 1
        }
        
        model = create_model(config)
        
        assert model.src_vocab_size == 1000
        assert model.tgt_vocab_size == 1000
        assert model.d_model == 64
    
    def test_gpu_compatibility(self):
        """Test model works on GPU if available."""
        if not torch.cuda.is_available():
            pytest.skip("CUDA not available")
        
        model = TransformerNMT(
            src_vocab_size=1000,
            tgt_vocab_size=1000,
            d_model=64,
            n_heads=2,
            n_layers=1
        ).cuda()
        
        batch_size = 2
        src_len = 10
        tgt_len = 8
        
        src = torch.randint(0, 1000, (batch_size, src_len)).cuda()
        tgt = torch.randint(0, 1000, (batch_size, tgt_len)).cuda()
        
        output = model(src, tgt)
        
        assert output.device.type == 'cuda'
        assert output.shape == (batch_size, tgt_len, 1000)


if __name__ == "__main__":
    pytest.main([__file__])



