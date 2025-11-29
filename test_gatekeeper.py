from src.approver_god.gating.gatekeeper import process_request
from src.approver_god.intake.request_schema import IntakeRequest

def test_gatekeeper_pipeline():
    """
    Tests the full Approver GOD pipeline from request to promotion.
    """
    request = IntakeRequest(domain="test_domain", objective="A test objective")
    
    approved_facts = process_request(request)
    
    assert isinstance(approved_facts, list)
    assert len(approved_facts) > 0, "The gatekeeper should have approved at least one fact."
    assert "fact_id" in approved_facts[0]