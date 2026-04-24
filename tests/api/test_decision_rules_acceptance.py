from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def assert_meta(payload: dict) -> None:
    assert "meta" in payload
    assert "request_id" in payload["meta"]
    assert "api_version" in payload["meta"]
    assert "timestamp" in payload["meta"]


def test_decision_rules_list_is_ordered_and_has_required_fields() -> None:
    response = client.get("/api/v1/decision-rules")
    assert response.status_code == 200

    payload = response.json()
    assert_meta(payload)

    rules = payload["data"]
    assert isinstance(rules, list)
    assert len(rules) >= 3

    evaluation_orders = [rule["evaluation_order"] for rule in rules]
    assert evaluation_orders == sorted(evaluation_orders)

    required_fields = {
        "rule_id",
        "rule_version",
        "evaluation_order",
        "decision",
        "reason_code",
        "reason_label",
        "decision_summary",
        "eligibility_summary",
    }

    for rule in rules:
        assert required_fields.issubset(rule.keys())


def test_decision_rules_detail_known_rule() -> None:
    response = client.get("/api/v1/decision-rules/abcd_actionable_seed")
    assert response.status_code == 200

    payload = response.json()
    assert_meta(payload)

    rule = payload["data"]
    assert rule["rule_id"] == "abcd_actionable_seed"
    assert rule["rule_version"] == "decision_rules_v1"
    assert rule["decision"] == "actionable"


def test_decision_rules_detail_unknown_rule_returns_404() -> None:
    response = client.get("/api/v1/decision-rules/does_not_exist")
    assert response.status_code == 404

    payload = response.json()
    assert payload["error"]["error_code"] == "resource_not_found"
    assert payload["error"]["message"] == "Requested decision rule was not found."
    assert_meta(payload)


def test_decision_rules_filter_actionable() -> None:
    response = client.get("/api/v1/decision-rules", params={"decision": "actionable"})
    assert response.status_code == 200

    payload = response.json()
    assert_meta(payload)

    rules = payload["data"]
    assert len(rules) == 1
    assert rules[0]["rule_id"] == "abcd_actionable_seed"
    assert rules[0]["decision"] == "actionable"


def test_decision_rules_filter_watchlist() -> None:
    response = client.get("/api/v1/decision-rules", params={"decision": "watchlist"})
    assert response.status_code == 200

    payload = response.json()
    assert_meta(payload)

    rules = payload["data"]
    assert len(rules) == 1
    assert rules[0]["rule_id"] == "watchlist_passthrough"
    assert rules[0]["decision"] == "watchlist"


def test_decision_rules_filter_no_trade() -> None:
    response = client.get("/api/v1/decision-rules", params={"decision": "no_trade"})
    assert response.status_code == 200

    payload = response.json()
    assert_meta(payload)

    rules = payload["data"]
    assert len(rules) == 1
    assert rules[0]["rule_id"] == "no_trade_passthrough"
    assert rules[0]["decision"] == "no_trade"


def test_decision_rules_invalid_decision_returns_400() -> None:
    response = client.get("/api/v1/decision-rules", params={"decision": "invalid"})
    assert response.status_code == 400

    payload = response.json()
    assert payload["error"]["error_code"] == "invalid_parameter"
    assert payload["error"]["message"] == "decision must be actionable, watchlist, or no_trade."
    assert_meta(payload)


def test_decisions_latest_exposes_rule_traceability() -> None:
    response = client.get("/api/v1/decisions/latest")
    assert response.status_code == 200

    payload = response.json()
    assert_meta(payload)

    decisions = payload["data"]
    assert isinstance(decisions, list)
    assert len(decisions) >= 3

    for decision in decisions:
        assert "rule_id" in decision
        assert "rule_version" in decision

    by_ticker = {item["primary_ticker"]: item for item in decisions}

    assert by_ticker["ABCD"]["decision"] == "actionable"
    assert by_ticker["ABCD"]["rule_id"] == "abcd_actionable_seed"
    assert by_ticker["ABCD"]["rule_version"] == "decision_rules_v1"

    assert by_ticker["WXYZ"]["decision"] == "watchlist"
    assert by_ticker["WXYZ"]["rule_id"] == "watchlist_passthrough"
    assert by_ticker["WXYZ"]["rule_version"] == "decision_rules_v1"

    assert by_ticker["ZZZZ"]["decision"] == "no_trade"
    assert by_ticker["ZZZZ"]["rule_id"] == "no_trade_passthrough"
    assert by_ticker["ZZZZ"]["rule_version"] == "decision_rules_v1"


def test_decisions_are_consistent_with_decision_rules_registry() -> None:
    rules_response = client.get("/api/v1/decision-rules")
    assert rules_response.status_code == 200
    rules_payload = rules_response.json()
    assert_meta(rules_payload)

    registry = {
        item["rule_id"]: item["rule_version"]
        for item in rules_payload["data"]
    }

    decisions_response = client.get("/api/v1/decisions/latest")
    assert decisions_response.status_code == 200
    decisions_payload = decisions_response.json()
    assert_meta(decisions_payload)

    for decision in decisions_payload["data"]:
        rule_id = decision["rule_id"]
        rule_version = decision["rule_version"]

        assert rule_id in registry
        assert registry[rule_id] == rule_version
