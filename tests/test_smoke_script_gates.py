import os
import runpy


def test_gated_live_decision_smoke_skips_by_default(capsys) -> None:
    os.environ.pop("ENABLE_GATED_LIVE_SMOKE", None)
    module = runpy.run_path("scripts/gated_live_decision_smoke.py")
    module["main"]()
    assert "gated live decision smoke skipped" in capsys.readouterr().out


def test_free_provider_smoke_skips_by_default(capsys) -> None:
    os.environ.pop("ENABLE_FREE_PROVIDER_SMOKE", None)
    module = runpy.run_path("scripts/free_provider_smoke.py")
    module["main"]()
    assert "free provider smoke skipped" in capsys.readouterr().out


def test_gated_live_decision_smoke_requires_finnhub_key_when_enabled(monkeypatch, capsys) -> None:
    monkeypatch.setenv("ENABLE_GATED_LIVE_SMOKE", "1")
    monkeypatch.delenv("FINNHUB_API_KEY", raising=False)
    module = runpy.run_path("scripts/gated_live_decision_smoke.py")
    module["main"]()
    assert "gated live decision smoke skipped: FINNHUB_API_KEY is not set" in capsys.readouterr().out


def test_free_provider_smoke_requires_finnhub_key_when_enabled(monkeypatch, capsys) -> None:
    monkeypatch.setenv("ENABLE_FREE_PROVIDER_SMOKE", "1")
    monkeypatch.delenv("FINNHUB_API_KEY", raising=False)
    module = runpy.run_path("scripts/free_provider_smoke.py")
    module["main"]()
    assert "free provider smoke skipped: FINNHUB_API_KEY is not set" in capsys.readouterr().out
