# src/approver_god/policy/thresholds.py
# This file defines the strict thresholds for promoting a hypothesis from the
# "Universe" (provisional) to "Earth" (approved truth).

THRESHOLDS = {
    # The minimum confidence score from the model generating the hypothesis.
    "min_model_confidence": 0.9,

    # The minimum score for factual precision when checked against the Motherboard's knowledge.
    "min_factual_precision": 0.95,

    # The minimum score for matching citations to trusted sources.
    "min_citation_match": 0.98,

    # The maximum rate of contradiction with existing "Earth" truths.
    "max_contradiction_rate": 0.01,

    # The pass rate for any code or unit tests generated as part of the validation plan.
    "min_code_tests_pass_rate": 0.98,

    # A score for the novelty or groundbreaking nature of the hypothesis.
    # We want to reward new ideas, but they must still pass the other checks.
    "min_novelty_score": 0.3,
}

def meets_thresholds(metrics: dict) -> bool:
    """
    Checks if a given set of metrics meets the defined thresholds.
    """
    return (
        metrics.get("model_confidence", 0.0) >= THRESHOLDS["min_model_confidence"] and
        metrics.get("factual_precision", 0.0) >= THRESHOLDS["min_factual_precision"] and
        metrics.get("citation_match", 0.0) >= THRESHOLDS["min_citation_match"] and
        metrics.get("contradiction_rate", 1.0) <= THRESHOLDS["max_contradiction_rate"] and
        metrics.get("code_tests_pass_rate", 0.0) >= THRESHOLDS["min_code_tests_pass_rate"] and
        metrics.get("novelty_score", 0.0) >= THRESHOLDS["min_novelty_score"]
    )
