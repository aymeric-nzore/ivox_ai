import argparse
import time
from datetime import datetime, timezone

import requests

INTERVAL_SECONDS = 120
TIMEOUT_SECONDS = 20
SERVICES = [
    ("IVOX AI", "https://ivox-ai.onrender.com/health"),
    ("IVOX Backend", "https://backend-q1iu.onrender.com/health"),
]


def check_service(name: str, url: str) -> None:
    started = time.perf_counter()
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        elapsed_ms = (time.perf_counter() - started) * 1000
        print(
            f"[{timestamp}] {name} UP "
            f"status={response.status_code} latency_ms={elapsed_ms:.1f} url={url}",
            flush=True,
        )
    except requests.RequestException as error:
        elapsed_ms = (time.perf_counter() - started) * 1000
        print(
            f"[{timestamp}] {name} DOWN "
            f"error={error} latency_ms={elapsed_ms:.1f} url={url}",
            flush=True,
        )


def run_cycle() -> None:
    for name, url in SERVICES:
        check_service(name, url)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Monitor IVOX IA and backend services.",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run a single check cycle and exit.",
    )
    args = parser.parse_args()

    print(
        f"Starting dual-service monitor (interval={INTERVAL_SECONDS}s)",
        flush=True,
    )

    if args.once:
        run_cycle()
        return 0

    while True:
        run_cycle()
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    raise SystemExit(main())
