import subprocess
import sys
from pathlib import Path


REPORT_PATH = Path("outputs/runs/demo_run/human_report.html")
STEPS = [
    "run_pipeline.py",
    "run_gigachat_comments.py",
    "run_investigations.py",
    "run_final_summary.py",
    "run_build_report.py",
]


def main() -> None:
    for step in STEPS:
        print(f"\n=== Running {step} ===", flush=True)
        subprocess.run([sys.executable, step], check=True)

    print("\nDemo completed.")
    print(f"Report: {REPORT_PATH.as_posix()}")


if __name__ == "__main__":
    main()

