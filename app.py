from src.approver_god.gating.gatekeeper import process_request
from src.babies.baby_science.respond import respond
from src.approver_god.intake.request_schema import IntakeRequest
from src.common.logging import get_logger

log = get_logger("app")

def main():
    """Main application entry point to run a full cycle of the system."""
    log.info("--- Starting AI Plantation Cycle ---")
    
    # 1. A scientist makes a request.
    request = IntakeRequest(domain="materials_science", objective="Develop a stronger, lightweight composite.")
    log.info("Submitting request to Approver GOD...")
    
    # 2. The Approver GOD processes it and promotes new facts.
    approved_facts = process_request(request)
    log.info(f"Approver GOD promoted {len(approved_facts)} new facts to Earth.")
    
    # 3. A Baby AI uses the new facts to provide a groundbreaking response.
    guidance = respond(request.model_dump())
    log.info(f"Baby Science responded: {guidance}")
    log.info("--- AI Plantation Cycle Complete ---")

if __name__ == "__main__":
    main()