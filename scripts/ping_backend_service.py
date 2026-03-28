import sys
import time
from datetime import datetime, timezone

import requests

SERVICE_NAME = "IVOX Backend"
URL = "https://backend-q1iu.onrender.com/health"
INTERVAL_SECONDS = 120
TIMEOUT_SECONDS = 20


def ping_once() -> None:
    started = time.perf_counter()
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        response = requests.get(URL, timeout=TIMEOUT_SECONDS)
        elapsed_ms = (time.perf_counter() - started) * 1000
        print(
            f"[{timestamp}] {SERVICE_NAME} UP "
            f"status={response.status_code} latency_ms={elapsed_ms:.1f}",
            flush=True,
        )
    except requests.RequestException as error:
        elapsed_ms = (time.perf_counter() - started) * 1000
        print(
            f"[{timestamp}] {SERVICE_NAME} DOWN "
            f"error={error} latency_ms={elapsed_ms:.1f}",
            flush=True,
        )


def main() -> int:
    print(
        f"Starting monitor for {SERVICE_NAME} at {URL} "
        f"(every {INTERVAL_SECONDS}s)",
        flush=True,
    )
    while True:
        ping_once()
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Monitor stopped by user.", flush=True)
        sys.exit(0)
