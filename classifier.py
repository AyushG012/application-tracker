def classify_email(subject: str, snippet: str = "") -> str | None:
    text = f"{subject} {snippet}".lower()


    # use rules to clasify emails
    rules = [
        ("Offer", [
            "job offer", "offer letter", "pleased to offer",
            "offer of employment",
        ]),
        ("Rejected", [
            "unfortunately", "not moving forward",
            "decided to pursue other candidates",
            "will not be proceeding",
        ]),
        ("Interview", [
            "interview", "schedule a call", "phone screen",
            "technical screen",
        ]),
        ("Assessment", [
            "assessment", "coding challenge", "online test",
            "take-home assignment", "take home assignment",
        ]),
        ("Applied", [
            "application received", "thanks for applying",
            "thank you for applying", "application confirmation",
        ]),
    ]

    for category, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return category

    if any(word in text for word in [
        "application", "recruiter", "recruitment", "hiring"
    ]):
        return "Update"

    return None
