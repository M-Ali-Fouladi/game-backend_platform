import time
from matcher import find_matches

def run_worker():
    print("=== WORKER STARTED ===", flush=True)
    while True:
        find_matches()
        time.sleep(3)

if __name__ == "__main__":
    run_worker()