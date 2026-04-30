import subprocess
import sys


def test_check_live_smoke_report_readiness_script_passes_for_current_report() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_live_smoke_report_readiness.py"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "ok" in result.stdout
    assert "reason" in result.stdout
