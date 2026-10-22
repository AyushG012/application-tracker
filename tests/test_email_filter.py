from gmail_client import is_excluded_email


def test_excludes_tutorchase_sender():
    assert is_excluded_email("newsletter@tutorchase.com")


def test_excludes_prosple_sender():
    assert is_excluded_email("updates@prosple.com")


def test_keeps_normal_recruiter_email():
    assert not is_excluded_email("recruiter@example.com")


def test_excludes_name_in_subject():
    assert is_excluded_email(
        "newsletter@example.com",
        "Prosple internship opportunities",
    )
