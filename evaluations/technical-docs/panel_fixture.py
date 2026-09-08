import argparse
import json
from pathlib import Path


def read_profile(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("profile must be an object")
    interval = data.get("refresh_seconds", 30)
    if type(interval) is not int or interval < 0:
        raise ValueError("refresh_seconds must be a non-negative integer")
    return {"refresh_seconds": interval}


class StatusPanel:
    def __init__(self, profile_path):
        self.profile_path = Path(profile_path)
        self.profile = read_profile(profile_path)
        self.last_error = None

    @property
    def automatic_refresh_enabled(self):
        return self.profile["refresh_seconds"] != 0

    def refresh_due(self, elapsed_seconds):
        return self.automatic_refresh_enabled and elapsed_seconds >= self.profile["refresh_seconds"]

    def reload(self):
        try:
            candidate = read_profile(self.profile_path)
        except (OSError, ValueError) as failure:
            self.last_error = str(failure)
            return False
        self.profile = candidate
        self.last_error = None
        return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["validate"])
    parser.add_argument("path")
    arguments = parser.parse_args()
    try:
        read_profile(arguments.path)
    except (OSError, ValueError) as failure:
        print(str(failure))
        return 1
    print("Profile valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
