import os
import random
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(BASE_DIR, "attack_test_folder")
MARKER = ".simulator_marker"
PREFIX = "sim_file_"
NUM_FILES = 25
ATTACK_DELAY = 0.25
BASELINE_PAUSE = 3
FILE_SIZE = 4096
WORDS = ["report", "invoice", "meeting", "budget", "notes", "project",
         "schedule", "summary", "client", "draft", "review", "update"]


def _check_safe():
    real = os.path.realpath(TEST_DIR)
    if os.path.dirname(real) != os.path.realpath(BASE_DIR):
        sys.exit("Refusing to run: test folder is not next to the script.")
    if not os.path.isfile(os.path.join(real, MARKER)):
        sys.exit("Refusing to run: marker file not found.")


def _sim_file():
    return [f for f in os.listdir(TEST_DIR) if f.startswith(PREFIX)]


def setup():
    os.makedirs(TEST_DIR, exist_ok=True)
    with open(os.path.join(TEST_DIR, MARKER), "w") as m:
        m.write("created by simulator.py safe to delete\n")
    for i in range(NUM_FILES):
        text = " ".join(random.choice(WORDS) for _ in range(FILE_SIZE // 6))
        path = os.path.join(TEST_DIR, f"{PREFIX}{i:02d}.txt")
        with open(path, "w") as f:
            f.write(text[:FILE_SIZE])
    print(f"[setup] Created {NUM_FILES} files in {TEST_DIR}")


def _retry(action, tries=10, wait=0.2):
    """Run action(); if Windows says the file is busy, wait and try again."""
    for _ in range(tries):
        try:
            action()
            return True
        except PermissionError:
            time.sleep(wait)
    return False


def attack():
    _check_safe()
    files = sorted(f for f in _sim_file() if f.endswith(".txt"))
    if not files:
        print("[attack] No files found to attack. Run setup() first.")
        return
    print(f"[attack] Starting attack on {len(files)} files")
    for name in files:
        path = os.path.join(TEST_DIR, name)

        def scramble(path=path):
            with open(path, "wb") as f:
                f.write(os.urandom(FILE_SIZE))

        _retry(scramble)
        if not _retry(lambda: os.rename(path, path + ".locked")):
            print(f"[attack] could not rename {name} (file busy)")
        time.sleep(ATTACK_DELAY)
    print("[attack] done")


def cleanup():
    _check_safe()
    for name in _sim_file():
        _retry(lambda n=name: os.remove(os.path.join(TEST_DIR, n)))
    _retry(lambda: os.remove(os.path.join(TEST_DIR, MARKER)))
    try:
        os.rmdir(TEST_DIR)
    except OSError:
        pass
    print("[cleanup] test folder cleaned")


def run_simulation():
    setup()
    time.sleep(BASELINE_PAUSE)
    attack()


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "run"
    actions = {"run": run_simulation, "setup": setup,
               "attack": attack, "cleanup": cleanup}
    if action not in actions:
        sys.exit("Usage: python simulator.py [run|setup|attack|cleanup]")
    actions[action]()