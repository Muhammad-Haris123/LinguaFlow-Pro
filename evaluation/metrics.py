"""
Evaluation metrics for Neural Machine Translation.
Implements BLEU, chrF, TER, and other standard NMT metrics.
"""

import re
import math
from collections import Counter
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from loguru import logger

try:
    import sacrebleu
    from sacrebleu.metrics import BLEU, CHRF
    SACREBLEU_AVAILABLE = True
except ImportError:
    SACREBLEU_AVAILABLE = False
    logger.warning("sacrebleu not available. Using fallback implementations.")

try:
    import nltk
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    logger.warning("nltk not available. Using fallback implementations.")


def tokenize(text: str) -> List[str]:
    """Simple tokenization for evaluation."""
    # Basic tokenization - split on whitespace and punctuation
    tokens = re.findall(r'\w+|[^\w\s]', text.lower())
    return tokens


def n_gram_precision(candidate: List[str], reference: List[str], n: int) -> float:
    """Calculate n-gram precision."""
    if len(candidate) < n:
        return 0.0
    
    candidate_ngrams = Counter(zip(*[candidate[i:] for i in range(n)]))
    reference_ngrams = Counter(zip(*[reference[i:] for i in range(n)]))
    
    overlap = sum((candidate_ngrams & reference_ngrams).values())
    total = sum(candidate_ngrams.values())
    
    return overlap / total if total > 0 else 0.0


def calculate_bleu_simple(candidate: str, reference: str, max_n: int = 4) -> float:
    """Calculate BLEU score using simple implementation."""
    candidate_tokens = tokenize(candidate)
    reference_tokens = tokenize(reference)
    
    if len(candidate_tokens) == 0:
        return 0.0
    
    # Calculate precision for each n-gram
    precisions = []
    for n in range(1, max_n + 1):
        prec = n_gram_precision(candidate_tokens, reference_tokens, n)
        precisions.append(prec)
    
    # Calculate brevity penalty
    if len(candidate_tokens) <= len(reference_tokens):
        bp = math.exp(1 - len(reference_tokens) / len(candidate_tokens))
    else:
        bp = 1.0
    
    # Calculate BLEU
    if min(precisions) == 0:
        return 0.0
    
    bleu = bp * math.exp(sum(math.log(p) for p in precisions) / len(precisions))
    return bleu


def calculate_bleu(candidates: List[str], references: List[List[str]], 
                  use_sacrebleu: bool = True) -> Dict[str, float]:
    """Calculate BLEU score for multiple candidates and references."""
    if use_sacrebleu and SACREBLEU_AVAILABLE:
        try:
            # Use sacrebleu for more accurate results
            bleu = BLEU()
            score = bleu.corpus_score(candidates, references)
            
            return {
                'bleu': score.score / 100.0,  # Convert to 0-1 scale
                'bleu_1': score.precisions[0] / 100.0,
                'bleu_2': score.precisions[1] / 100.0,
                'bleu_3': score.precisions[2] / 100.0,
                'bleu_4': score.precisions[3] / 100.0,
                'brevity_penalty': score.bp
            }
        except Exception as e:
            logger.warning(f"Sacrebleu failed: {e}. Using fallback implementation.")
    
    # Fallback implementation
    if isinstance(references[0], str):
        references = [[ref] for ref in references]
    
    bleu_scores = []
    bleu_1_scores = []
    bleu_2_scores = []
    bleu_3_scores = []
    bleu_4_scores = []
    
    for candidate, refs in zip(candidates, references):
        # Calculate BLEU against each reference and take the maximum
        max_bleu = 0.0
        max_bleu_1 = 0.0
        max_bleu_2 = 0.0
        max_bleu_3 = 0.0
        max_bleu_4 = 0.0
        
        for ref in refs:
            bleu = calculate_bleu_simple(candidate, ref)
            bleu_1 = n_gram_precision(tokenize(candidate), tokenize(ref), 1)
            bleu_2 = n_gram_precision(tokenize(candidate), tokenize(ref), 2)
            bleu_3 = n_gram_precision(tokenize(candidate), tokenize(ref), 3)
            bleu_4 = n_gram_precision(tokenize(candidate), tokenize(ref), 4)
            
            max_bleu = max(max_bleu, bleu)
            max_bleu_1 = max(max_bleu_1, bleu_1)
            max_bleu_2 = max(max_bleu_2, bleu_2)
            max_bleu_3 = max(max_bleu_3, bleu_3)
            max_bleu_4 = max(max_bleu_4, bleu_4)
        
        bleu_scores.append(max_bleu)
        bleu_1_scores.append(max_bleu_1)
        bleu_2_scores.append(max_bleu_2)
        bleu_3_scores.append(max_bleu_3)
        bleu_4_scores.append(max_bleu_4)
    
    return {
        'bleu': np.mean(bleu_scores),
        'bleu_1': np.mean(bleu_1_scores),
        'bleu_2': np.mean(bleu_2_scores),
        'bleu_3': np.mean(bleu_3_scores),
        'bleu_4': np.mean(bleu_4_scores),
        'brevity_penalty': 1.0  # Simplified
    }


def calculate_chrf(candidates: List[str], references: List[List[str]], 
                  use_sacrebleu: bool = True) -> Dict[str, float]:
    """Calculate chrF score."""
    if use_sacrebleu and SACREBLEU_AVAILABLE:
        try:
            chrf = CHRF()
            score = chrf.corpus_score(candidates, references)
            
            return {
                'chrf': score.score / 100.0,  # Convert to 0-1 scale
                'chrf_1': score.precisions[0] / 100.0,
                'chrf_2': score.precisions[1] / 100.0,
                'chrf_3': score.precisions[2] / 100.0
            }
        except Exception as e:
            logger.warning(f"Sacrebleu chrF failed: {e}. Using fallback implementation.")
    
    # Fallback implementation
    if isinstance(references[0], str):
        references = [[ref] for ref in references]
    
    chrf_scores = []
    chrf_1_scores = []
    chrf_2_scores = []
    chrf_3_scores = []
    
    for candidate, refs in zip(candidates, references):
        max_chrf = 0.0
        max_chrf_1 = 0.0
        max_chrf_2 = 0.0
        max_chrf_3 = 0.0
        
        for ref in refs:
            # Character-level n-gram precision
            chrf_1 = n_gram_precision(list(candidate.lower()), list(ref.lower()), 1)
            chrf_2 = n_gram_precision(list(candidate.lower()), list(ref.lower()), 2)
            chrf_3 = n_gram_precision(list(candidate.lower()), list(ref.lower()), 3)
            
            # chrF is the harmonic mean of character n-gram precisions
            chrf = 2 * chrf_1 * chrf_2 / (chrf_1 + chrf_2) if (chrf_1 + chrf_2) > 0 else 0.0
            
            max_chrf = max(max_chrf, chrf)
            max_chrf_1 = max(max_chrf_1, chrf_1)
            max_chrf_2 = max(max_chrf_2, chrf_2)
            max_chrf_3 = max(max_chrf_3, chrf_3)
        
        chrf_scores.append(max_chrf)
        chrf_1_scores.append(max_chrf_1)
        chrf_2_scores.append(max_chrf_2)
        chrf_3_scores.append(max_chrf_3)
    
    return {
        'chrf': np.mean(chrf_scores),
        'chrf_1': np.mean(chrf_1_scores),
        'chrf_2': np.mean(chrf_2_scores),
        'chrf_3': np.mean(chrf_3_scores)
    }


def calculate_ter(candidates: List[str], references: List[List[str]]) -> Dict[str, float]:
    """Calculate Translation Error Rate (TER)."""
    if isinstance(references[0], str):
        references = [[ref] for ref in references]
    
    ter_scores = []
    
    for candidate, refs in zip(candidates, references):
        min_ter = float('inf')
        
        for ref in refs:
            # Simple TER calculation (edit distance / reference length)
            candidate_tokens = tokenize(candidate)
            ref_tokens = tokenize(ref)
            
            # Calculate edit distance (Levenshtein distance)
            edit_distance = levenshtein_distance(candidate_tokens, ref_tokens)
            ter = edit_distance / len(ref_tokens) if len(ref_tokens) > 0 else 1.0
            
            min_ter = min(min_ter, ter)
        
        ter_scores.append(min_ter)
    
    return {
        'ter': np.mean(ter_scores)
    }


def levenshtein_distance(s1: List[str], s2: List[str]) -> int:
    """Calculate Levenshtein distance between two token sequences."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def calculate_meteor(candidates: List[str], references: List[List[str]]) -> Dict[str, float]:
    """Calculate METEOR score (simplified implementation)."""
    # This is a simplified METEOR implementation
    # For production use, consider using the official METEOR implementation
    
    meteor_scores = []
    
    for candidate, refs in zip(candidates, references):
        max_meteor = 0.0
        
        for ref in refs:
            candidate_tokens = set(tokenize(candidate))
            ref_tokens = set(tokenize(ref))
            
            # Calculate precision and recall
            matches = len(candidate_tokens & ref_tokens)
            precision = matches / len(candidate_tokens) if len(candidate_tokens) > 0 else 0.0
            recall = matches / len(ref_tokens) if len(ref_tokens) > 0 else 0.0
            
            # F-measure
            if precision + recall > 0:
                f_measure = 2 * precision * recall / (precision + recall)
            else:
                f_measure = 0.0
            
            # Simplified METEOR (in practice, METEOR is more complex)
            meteor = f_measure
            max_meteor = max(max_meteor, meteor)
        
        meteor_scores.append(max_meteor)
    
    return {
        'meteor': np.mean(meteor_scores)
    }


def evaluate_translations(candidates: List[str], references: List[List[str]], 
                         metrics: List[str] = ['bleu', 'chrf', 'ter']) -> Dict[str, float]:
    """Evaluate translations using multiple metrics."""
    results = {}
    
    if 'bleu' in metrics:
        bleu_results = calculate_bleu(candidates, references)
        results.update(bleu_results)
    
    if 'chrf' in metrics:
        chrf_results = calculate_chrf(candidates, references)
        results.update(chrf_results)
    
    if 'ter' in metrics:
        ter_results = calculate_ter(candidates, references)
        results.update(ter_results)
    
    if 'meteor' in metrics:
        meteor_results = calculate_meteor(candidates, references)
        results.update(meteor_results)
    
    return results


def print_evaluation_results(results: Dict[str, float]):
    """Print evaluation results in a formatted way."""
    logger.info("=== Evaluation Results ===")
    
    if 'bleu' in results:
        logger.info(f"BLEU: {results['bleu']:.4f}")
        logger.info(f"BLEU-1: {results['bleu_1']:.4f}")
        logger.info(f"BLEU-2: {results['bleu_2']:.4f}")
        logger.info(f"BLEU-3: {results['bleu_3']:.4f}")
        logger.info(f"BLEU-4: {results['bleu_4']:.4f}")
    
    if 'chrf' in results:
        logger.info(f"chrF: {results['chrf']:.4f}")
        logger.info(f"chrF-1: {results['chrf_1']:.4f}")
        logger.info(f"chrF-2: {results['chrf_2']:.4f}")
        logger.info(f"chrF-3: {results['chrf_3']:.4f}")
    
    if 'ter' in results:
        logger.info(f"TER: {results['ter']:.4f}")
    
    if 'meteor' in results:
        logger.info(f"METEOR: {results['meteor']:.4f}")


def main():
    """Test the evaluation metrics."""
    logger.info("Testing evaluation metrics")
    
    # Test data
    candidates = [
        "Hello, how are you?",
        "This is a test sentence.",
        "The weather is nice today."
    ]
    
    references = [
        ["Hallo, wie geht es dir?", "Hallo, wie geht's?"],
        ["Das ist ein Testsatz.", "Dies ist ein Test."],
        ["Das Wetter ist heute schön.", "Heute ist das Wetter schön."]
    ]
    
    # Evaluate
    results = evaluate_translations(candidates, references)
    print_evaluation_results(results)
    
    logger.info("Evaluation metrics test completed!")


if __name__ == "__main__":
    main()



