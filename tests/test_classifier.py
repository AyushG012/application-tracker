from classifier import classify_email


def test_offer_email():
    assert classify_email("Congratulations, job offer!") == "Offer"


def test_rejection_email():
    assert classify_email(
        "Application update",
        "We decided to pursue other candidates",
    ) == "Rejected"


def test_interview_email():
    assert classify_email("Interview invitation") == "Interview"


def test_assessment_email():
    assert classify_email("Complete the coding challenge") == "Assessment"


def test_application_confirmation():
    assert classify_email(
        "Application received",
    ) == "Applied"


def test_unrelated_email():
    assert classify_email("Weekend plans", "Dinner on Friday") is None