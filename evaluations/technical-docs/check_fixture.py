import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

from panel_fixture import StatusPanel, read_profile


def check_fixture():
    with tempfile.TemporaryDirectory(prefix="technical-docs-fixture-") as directory:
        profile_path = Path(directory) / "uploads" / "profile.json"
        profile_path.parent.mkdir()
        profile_path.write_text("{}", encoding="utf-8")
        assert read_profile(profile_path) == {"refresh_seconds": 30}
        panel = StatusPanel(profile_path)
        assert not panel.refresh_due(29)
        assert panel.refresh_due(30)
        profile_path.write_text('{"refresh_seconds": 0}', encoding="utf-8")
        assert panel.profile["refresh_seconds"] == 30
        assert panel.automatic_refresh_enabled
        assert panel.reload()
        assert not panel.automatic_refresh_enabled
        assert not panel.refresh_due(300)

        for invalid in (-1, None, "30", False):
            profile_path.write_text(json.dumps({"refresh_seconds": invalid}), encoding="utf-8")
            assert not panel.reload()
            assert panel.profile == {"refresh_seconds": 0}
            assert panel.last_error == "refresh_seconds must be a non-negative integer"

        profile_path.write_text('{"refresh_seconds": 10}', encoding="utf-8")
        script = Path(__file__).with_name("panel_fixture.py")
        result = subprocess.run(
            [sys.executable, str(script), "validate", str(profile_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "Profile valid"
        assert panel.profile == {"refresh_seconds": 0}
        assert panel.reload()
        assert panel.profile == {"refresh_seconds": 10}
        assert panel.last_error is None

        profile_path.write_text('{"refresh_seconds": -1}', encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(script), "validate", str(profile_path)],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1
        assert result.stdout.strip() == "refresh_seconds must be a non-negative integer"
        assert json.loads(profile_path.read_text(encoding="utf-8"))["refresh_seconds"] == -1
        assert panel.profile == {"refresh_seconds": 10}
    print("Fixture behavior checks pass")


if __name__ == "__main__":
    check_fixture()
