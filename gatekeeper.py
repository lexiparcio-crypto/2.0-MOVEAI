from typing import Dict, Any, List
from src.common.logging import get_logger
from src.approver_god.intake.request_schema import IntakeRequest
from src.approver_god.retrieval.retrieve import retrieve_relevant_facts
from src.approver_god.hypothesis.generate import generate_hypotheses
from src.approver_god.validation.stats_tests import run_stats_tests
from src.approver_god.validation.contradiction_checks import check_for_contradictions
from src.approver_god.promotion.promote import promote_to_earth
from src.motherboard.api import add_universe_hypothesis

log = get_logger("gatekeeper")

def process_request(request: IntakeRequest) -> List[Dict[str, Any]]:
    """
    The main pipeline for the Approver GOD.
    It ingests a request, generates hypotheses, validates them, and promotes the approved ones.
    """
    log.info(f"Processing request for objective: {request.objective}")
    
    # 1. Retrieval
    relevant_facts = retrieve_relevant_facts(request.objective)
    
    # 2. Hypothesis Generation
    hypotheses = generate_hypotheses(request.objective, relevant_facts)
    
    approved_facts = []
    for hyp in hypotheses:
        add_universe_hypothesis(hyp)
        
        # 3. Validation
        confidence = run_stats_tests(hyp)
        is_consistent = check_for_contradictions(hyp, relevant_facts)
        
        # 4. Gating
        if confidence >= 0.95 and is_consistent:
            log.info(f"Hypothesis {hyp['hypothesis_id']} passed validation.")
            # 5. Promotion
            fact = promote_to_earth(hyp, hyp['hypothesis_id'], "approver_god_v1")
            approved_facts.append(fact)
        else:
            log.warn(f"Hypothesis {hyp['hypothesis_id']} failed validation.")
            
    return approved_facts