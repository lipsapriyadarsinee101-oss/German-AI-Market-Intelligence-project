USE_CASES = {
    "Biometric social scoring": ("Prohibited / unacceptable risk", "Social scoring and certain biometric practices may be prohibited.", "Stop deployment and obtain specialist legal review."),
    "Recruitment ranking": ("Potential high risk", "AI used for employment decisions can fall into a high-risk category.", "Perform conformity, data-governance, human-oversight, and impact assessments."),
    "Credit scoring": ("Potential high risk", "Systems affecting access to essential private services may be high risk.", "Document purpose, test bias, ensure human review, and obtain legal assessment."),
    "Medical diagnosis support": ("Potential high risk", "Medical AI may be covered by product-safety and high-risk rules.", "Apply clinical validation, quality management, monitoring, and specialist legal review."),
    "Customer-service chatbot": ("Transparency risk", "Users generally need to know when they are interacting with AI.", "Add clear disclosure, escalation to a person, logging, and content safeguards."),
    "Predictive maintenance": ("Usually limited/minimal risk", "Industrial optimisation is often lower risk unless it controls safety-critical infrastructure.", "Document intended use, monitor performance, and review safety dependencies."),
}


def classify_use_case(use_case: str) -> dict[str, str]:
    risk, reason, action = USE_CASES.get(
        use_case,
        ("Needs assessment", "The context is insufficient for classification.", "Document the use case and seek qualified review."),
    )
    return {"risk_level": risk, "reason": reason, "action": action}

