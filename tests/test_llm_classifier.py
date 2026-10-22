
from unittest.mock import Mock, patch

from llm_classifier import classify_email_llm, classify_email_hybrid


def test_interview_classification():
    fake_result = {
        "status": "Interview",
        "company": "Acme",
        "role": "Software Engineering Intern",
        "confidence": 0.95,
        "reason": "The sender invites the recipient to an interview.",
    }

    fake_response = Mock()
    fake_response.text = (
        '{"status": "Interview", "company": "Acme", '
        '"role": "Software Engineering Intern", '
        '"confidence": 0.95, '
        '"reason": "The sender invites the recipient to an interview."}'
    )

    fake_client = Mock()
    fake_client.models.generate_content.return_value = fake_response

    with patch("llm_classifier.API_KEY", "test-key"), patch(
        "llm_classifier.genai.Client", return_value=fake_client
    ):
        result = classify_email_llm(
            "Interview invitation from Acme",
            "We would like to schedule an interview with you.",
        )

    assert result == fake_result
    fake_client.models.generate_content.assert_called_once()


def test_hybrid_falls_back_when_gemini_fails():
    with patch(
        "llm_classifier.classify_email_llm",
        side_effect=RuntimeError("Gemini unavailable"),
    ):
        result = classify_email_hybrid(
            "Interview invitation",
            "We would like to schedule an interview.",
        )

    assert result["status"] == "Interview"
    assert result["confidence"] == 0.0
