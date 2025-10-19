"""
Unit tests for the FastAPI backend.
"""

import pytest
import requests
import time
import subprocess
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


class TestTranslationAPI:
    """Test cases for the translation API."""
    
    @pytest.fixture(scope="class")
    def api_server(self):
        """Start the API server for testing."""
        # This would start the server in a separate process
        # For now, we'll assume it's running
        yield "http://localhost:8000"
    
    def test_health_check(self, api_server):
        """Test health check endpoint."""
        response = requests.get(f"{api_server}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "model_loaded" in data
    
    def test_get_languages(self, api_server):
        """Test languages endpoint."""
        response = requests.get(f"{api_server}/languages")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert "en" in data
        assert "de" in data
        assert "fr" in data
    
    def test_single_translation(self, api_server):
        """Test single text translation."""
        payload = {
            "text": "Hello, how are you?",
            "target_language": "de",
            "source_language": "en"
        }
        
        response = requests.post(f"{api_server}/translate", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "translated_text" in data
        assert "source_language" in data
        assert "target_language" in data
        assert "processing_time" in data
    
    def test_batch_translation(self, api_server):
        """Test batch translation."""
        payload = {
            "texts": [
                "Hello, how are you?",
                "This is a test.",
                "Good morning!"
            ],
            "target_language": "de",
            "source_language": "en"
        }
        
        response = requests.post(f"{api_server}/batch-translate", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "translations" in data
        assert "total_processing_time" in data
        assert "average_processing_time" in data
        assert len(data["translations"]) == 3
    
    def test_invalid_language(self, api_server):
        """Test translation with invalid language."""
        payload = {
            "text": "Hello, how are you?",
            "target_language": "invalid",
            "source_language": "en"
        }
        
        response = requests.post(f"{api_server}/translate", json=payload)
        assert response.status_code == 400
    
    def test_empty_text(self, api_server):
        """Test translation with empty text."""
        payload = {
            "text": "",
            "target_language": "de",
            "source_language": "en"
        }
        
        response = requests.post(f"{api_server}/translate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_model_info(self, api_server):
        """Test model information endpoint."""
        response = requests.get(f"{api_server}/model/info")
        assert response.status_code == 200
        
        data = response.json()
        assert "model_name" in data
        assert "supported_languages" in data
        assert "model_size" in data
        assert "is_loaded" in data
    
    def test_clear_cache(self, api_server):
        """Test cache clearing endpoint."""
        response = requests.delete(f"{api_server}/cache")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
    
    def test_metrics(self, api_server):
        """Test metrics endpoint."""
        response = requests.get(f"{api_server}/metrics")
        assert response.status_code == 200
        
        data = response.json()
        assert "total_translations" in data
        assert "cache_hit_rate" in data
        assert "average_response_time" in data


class TestDataPreprocessing:
    """Test cases for data preprocessing."""
    
    def test_preprocessor_initialization(self):
        """Test data preprocessor initialization."""
        from data.preprocessing import DataPreprocessor
        
        preprocessor = DataPreprocessor()
        assert preprocessor.model_name is not None
        assert preprocessor.max_length > 0
    
    def test_text_preprocessing(self):
        """Test text preprocessing functions."""
        from data.preprocessing import DataPreprocessor
        
        preprocessor = DataPreprocessor()
        
        # Test text normalization
        text = "  Hello,   world!  "
        processed = preprocessor.preprocess_text(text)
        assert processed == "Hello, world!"
    
    def test_dummy_dataset_creation(self):
        """Test dummy dataset creation."""
        from data.preprocessing import DataPreprocessor
        
        preprocessor = DataPreprocessor()
        datasets = preprocessor._create_dummy_dataset(['en', 'de', 'fr'])
        
        assert 'en-de' in datasets
        assert 'en-fr' in datasets
        assert 'train' in datasets['en-de']
        assert 'validation' in datasets['en-de']
        assert 'test' in datasets['en-de']


class TestEvaluationMetrics:
    """Test cases for evaluation metrics."""
    
    def test_bleu_calculation(self):
        """Test BLEU score calculation."""
        from evaluation.metrics import calculate_bleu
        
        candidates = ["Hello world", "Good morning"]
        references = [["Hallo Welt", "Guten Morgen"], ["Bonjour monde", "Bonjour"]]
        
        results = calculate_bleu(candidates, references)
        
        assert "bleu" in results
        assert "bleu_1" in results
        assert "bleu_2" in results
        assert "bleu_3" in results
        assert "bleu_4" in results
        assert 0 <= results["bleu"] <= 1
    
    def test_chrf_calculation(self):
        """Test chrF score calculation."""
        from evaluation.metrics import calculate_chrf
        
        candidates = ["Hello world", "Good morning"]
        references = [["Hallo Welt", "Guten Morgen"], ["Bonjour monde", "Bonjour"]]
        
        results = calculate_chrf(candidates, references)
        
        assert "chrf" in results
        assert "chrf_1" in results
        assert "chrf_2" in results
        assert "chrf_3" in results
        assert 0 <= results["chrf"] <= 1
    
    def test_ter_calculation(self):
        """Test TER calculation."""
        from evaluation.metrics import calculate_ter
        
        candidates = ["Hello world", "Good morning"]
        references = [["Hallo Welt", "Guten Morgen"], ["Bonjour monde", "Bonjour"]]
        
        results = calculate_ter(candidates, references)
        
        assert "ter" in results
        assert 0 <= results["ter"] <= 1
    
    def test_evaluate_translations(self):
        """Test comprehensive evaluation."""
        from evaluation.metrics import evaluate_translations
        
        candidates = ["Hello world", "Good morning"]
        references = [["Hallo Welt", "Guten Morgen"], ["Bonjour monde", "Bonjour"]]
        
        results = evaluate_translations(candidates, references, ['bleu', 'chrf', 'ter'])
        
        assert "bleu" in results
        assert "chrf" in results
        assert "ter" in results


if __name__ == "__main__":
    pytest.main([__file__])



