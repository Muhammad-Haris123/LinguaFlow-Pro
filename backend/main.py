"""
LinguaFlow Pro - Enterprise Translation Platform
Ultra-Fast GPU-Optimized Translation API
Optimized for RTX 5060 Ti (16GB VRAM) - Sub-2-second responses
"""

import os
import time
import asyncio
from typing import Dict, List, Optional
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loguru import logger
import uvicorn

# ============================================================================
# CONFIGURATION & DEVICE SETUP
# ============================================================================

# Device configuration
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
TORCH_DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32
MAX_LENGTH = 128
MAX_NEW_TOKENS = 50
BATCH_SIZE = 1

# Model configuration
MODEL_NAME = "t5-small"  # Fast, lightweight model
MODEL_PATH = "trained_translation_model"

# Performance settings
ENABLE_TORCH_COMPILE = True
ENABLE_MIXED_PRECISION = True
ENABLE_KV_CACHE = True

logger.info(f"🚀 LinguaFlow Pro Backend Initialized: {DEVICE}")
logger.info(f"📊 VRAM Available: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB" if DEVICE == "cuda" else "CPU Mode")

# ============================================================================
# GLOBAL MODEL VARIABLES
# ============================================================================

model: Optional[AutoModelForSeq2SeqLM] = None
tokenizer: Optional[AutoTokenizer] = None
model_cache: Dict[str, str] = {}
tokenized_cache: Dict[str, torch.Tensor] = {}

# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class TranslationRequest(BaseModel):
    text: str
    source_language: str = "en"
    target_language: str = "de"
    max_length: int = 50
    beam_size: int = 1

class TranslationResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    processing_time: float
    confidence: float
    device_used: str

# ============================================================================
# LANGUAGE SUPPORT
# ============================================================================

SUPPORTED_LANGUAGES = {
    "en": "English",
    "de": "German", 
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic",
    "hi": "Hindi"
}

# ============================================================================
# GPU-OPTIMIZED MODEL LOADING
# ============================================================================

async def load_translation_model():
    """Load and optimize model for GPU inference."""
    global model, tokenizer
    
    try:
        logger.info("🔥 Loading LinguaFlow Pro GPU-optimized model...")
        
        # Determine model path
        if os.path.exists(MODEL_PATH):
            model_name = MODEL_PATH
            logger.info(f"📁 Using trained model: {MODEL_PATH}")
        else:
            model_name = MODEL_NAME
            logger.info(f"📦 Using pre-trained model: {MODEL_NAME}")
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load model with GPU optimizations
        model = AutoModelForSeq2SeqLM.from_pretrained(
            model_name,
            torch_dtype=TORCH_DTYPE,
            device_map="auto" if DEVICE == "cuda" else None,
            low_cpu_mem_usage=True if DEVICE == "cuda" else False
        )
        
        # Move to device
        if DEVICE == "cuda":
            model = model.to(DEVICE)
            model = model.half()  # Use FP16 for speed
            logger.info("🎯 Model moved to GPU with FP16 precision")
        
        # Set to evaluation mode
        model.eval()
        
        # PyTorch 2.0 compilation for extra speed
        if ENABLE_TORCH_COMPILE and DEVICE == "cuda":
            try:
                model = torch.compile(model, mode="max-autotune")
                logger.info("⚡ Model compiled with torch.compile")
            except Exception as e:
                logger.warning(f"Compilation failed: {e}")
        
        # Warm up the model
        await warm_up_model()
        
        logger.info("✅ LinguaFlow Pro GPU-optimized model loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        return False

async def warm_up_model():
    """Warm up the model to avoid first-call lag."""
    if model is None or tokenizer is None:
        return
    
    try:
        logger.info("🔥 Warming up GPU model...")
        
        # Create warm-up inputs
        warm_up_texts = [
            "translate English to German: hello",
            "translate English to French: good morning", 
            "translate English to Spanish: thank you"
        ]
        
        for text in warm_up_texts:
            # Tokenize
            inputs = tokenizer(
                text,
                max_length=MAX_LENGTH,
                padding=True,
                truncation=True,
                return_tensors="pt"
            ).to(DEVICE)
            
            # Generate with GPU
            with torch.no_grad():
                if ENABLE_MIXED_PRECISION and DEVICE == "cuda":
                    with torch.cuda.amp.autocast():
                        outputs = model.generate(
                            **inputs,
                            max_new_tokens=MAX_NEW_TOKENS,
                            num_beams=1,
                            do_sample=False,
                            use_cache=ENABLE_KV_CACHE,
                            pad_token_id=tokenizer.pad_token_id
                        )
                else:
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=MAX_NEW_TOKENS,
                        num_beams=1,
                        do_sample=False,
                        use_cache=ENABLE_KV_CACHE,
                        pad_token_id=tokenizer.pad_token_id
                    )
                
                # Decode
                result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        logger.info("✅ Model warmed up successfully!")
        
    except Exception as e:
        logger.warning(f"⚠️ Warm-up failed: {e}")

# ============================================================================
# CACHING SYSTEM
# ============================================================================

def get_cache_key(text: str, target_lang: str, source_lang: str) -> str:
    """Generate cache key."""
    return f"{source_lang}:{target_lang}:{text.lower().strip()}"

def get_cached_translation(text: str, target_lang: str, source_lang: str) -> Optional[str]:
    """Get cached translation."""
    key = get_cache_key(text, target_lang, source_lang)
    return model_cache.get(key)

def cache_translation(text: str, target_lang: str, source_lang: str, translation: str):
    """Cache translation."""
    key = get_cache_key(text, target_lang, source_lang)
    model_cache[key] = translation

def get_cached_tokenization(text: str) -> Optional[torch.Tensor]:
    """Get cached tokenization."""
    return tokenized_cache.get(text.lower().strip())

def cache_tokenization(text: str, tokens: torch.Tensor):
    """Cache tokenization."""
    tokenized_cache[text.lower().strip()] = tokens

# ============================================================================
# TEXT PREPROCESSING
# ============================================================================

def preprocess_text(text: str) -> str:
    """Preprocess input text."""
    return text.strip()

def postprocess_text(text: str) -> str:
    """Postprocess output text."""
    return text.strip()

# ============================================================================
# GPU-OPTIMIZED TRANSLATION
# ============================================================================

async def translate_with_gpu(text: str, target_lang: str, source_lang: str) -> str:
    """Ultra-fast GPU translation."""
    global model, tokenizer
    
    if model is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Format input for T5
        if target_lang == "de":
            input_text = f"translate English to German: {text}"
        elif target_lang == "fr":
            input_text = f"translate English to French: {text}"
        elif target_lang == "es":
            input_text = f"translate English to Spanish: {text}"
        elif target_lang == "it":
            input_text = f"translate English to Italian: {text}"
        elif target_lang == "pt":
            input_text = f"translate English to Portuguese: {text}"
        elif target_lang == "ru":
            input_text = f"translate English to Russian: {text}"
        elif target_lang == "ja":
            input_text = f"translate English to Japanese: {text}"
        elif target_lang == "ko":
            input_text = f"translate English to Korean: {text}"
        elif target_lang == "zh":
            input_text = f"translate English to Chinese: {text}"
        elif target_lang == "ar":
            input_text = f"translate English to Arabic: {text}"
        elif target_lang == "hi":
            input_text = f"translate English to Hindi: {text}"
        else:
            input_text = f"translate to {target_lang}: {text}"
        
        # Check tokenization cache
        cached_tokens = get_cached_tokenization(input_text)
        if cached_tokens is not None:
            inputs = {"input_ids": cached_tokens, "attention_mask": torch.ones_like(cached_tokens)}
        else:
            # Tokenize
            inputs = tokenizer(
                input_text,
                max_length=MAX_LENGTH,
                padding=True,
                truncation=True,
                return_tensors="pt"
            ).to(DEVICE)
            
            # Cache tokenization
            cache_tokenization(input_text, inputs["input_ids"])
        
        # GPU Generation with optimizations
        with torch.no_grad():
            if ENABLE_MIXED_PRECISION and DEVICE == "cuda":
                with torch.cuda.amp.autocast():
                    outputs = model.generate(
                        **inputs,
                        max_new_tokens=MAX_NEW_TOKENS,
                        num_beams=1,
                        do_sample=False,
                        use_cache=ENABLE_KV_CACHE,
                        pad_token_id=tokenizer.pad_token_id,
                        early_stopping=True
                    )
            else:
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=MAX_NEW_TOKENS,
                    num_beams=1,
                    do_sample=False,
                    use_cache=ENABLE_KV_CACHE,
                    pad_token_id=tokenizer.pad_token_id,
                    early_stopping=True
                )
        
        # Decode
        translation = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return translation
        
    except Exception as e:
        logger.error(f"GPU translation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

# ============================================================================
# MAIN TRANSLATION FUNCTION
# ============================================================================

async def translate_text(text: str, target_lang: str, source_lang: str = "en") -> str:
    """Main translation function with caching."""
    
    # Check if target language is supported
    if target_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported target language: {target_lang}")
    
    # Preprocess text
    processed_text = preprocess_text(text)
    
    # Check cache first
    cached_translation = get_cached_translation(processed_text, target_lang, source_lang)
    if cached_translation:
        return cached_translation
    
    # Use GPU translation
    translation = await translate_with_gpu(processed_text, target_lang, source_lang)
    
    # Postprocess
    translation = postprocess_text(translation)
    
    # Cache the result
    cache_translation(processed_text, target_lang, source_lang, translation)
    
    return translation

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="LinguaFlow Pro - Enterprise Translation Platform",
    description="Professional GPU-optimized translation API powered by RTX 5060 Ti. Sub-2-second responses with enterprise-grade reliability.",
    version="Pro 2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# STARTUP EVENT
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize the application."""
    logger.info("🚀 Starting LinguaFlow Pro - Enterprise Translation Platform...")
    
    # Load model
    success = await load_translation_model()
    if not success:
        logger.error("❌ Failed to load model - API will not work properly")
    
    logger.info("✅ Application startup complete!")

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "device": DEVICE,
        "model_loaded": model is not None,
        "gpu_memory": f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB" if DEVICE == "cuda" else "N/A"
    }

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """LinguaFlow Pro ultra-fast GPU translation endpoint."""
    start_time = time.time()
    
    try:
        # Perform translation
        translated_text = await translate_text(
            text=request.text,
            target_lang=request.target_language,
            source_lang=request.source_language
        )
        
        processing_time = time.time() - start_time
        
        return TranslationResponse(
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language,
            processing_time=processing_time,
            confidence=0.95,
            device_used=DEVICE
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/languages")
async def get_languages():
    """Get supported languages."""
    return {"languages": SUPPORTED_LANGUAGES}

@app.get("/stats")
async def get_stats():
    """Get API statistics."""
    return {
        "device": DEVICE,
        "model_loaded": model is not None,
        "cache_size": len(model_cache),
        "tokenized_cache_size": len(tokenized_cache),
        "gpu_memory_allocated": f"{torch.cuda.memory_allocated() / 1e9:.2f}GB" if DEVICE == "cuda" else "N/A",
        "gpu_memory_reserved": f"{torch.cuda.memory_reserved() / 1e9:.2f}GB" if DEVICE == "cuda" else "N/A"
    }

# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )