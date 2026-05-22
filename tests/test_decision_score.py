from app.decision_score import compute_decision_score


def test_compute_decision_score_without_risk_penalty() -> None:
    result = compute_decision_score(
        confidence=0.9,
        risk_flag_count=0,
    )

    assert result == 0.9


def test_compute_decision_score_applies_risk_penalty() -> None:
    result = compute_decision_score(
        confidence=0.9,
        risk_flag_count=2,
    )

    assert result == 0.7


def test_compute_decision_score_is_never_negative() -> None:
    result = compute_decision_score(
        confidence=0.1,
        risk_flag_count=5,
    )

    assert result == 0.0


def test_compute_decision_score_caps_penalty() -> None:
    result = compute_decision_score(
        confidence=1.0,
        risk_flag_count=20,
    )

    assert result == 0.5
