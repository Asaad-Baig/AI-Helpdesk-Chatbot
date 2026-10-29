import requests
import time
import concurrent.futures

URL = "http://localhost:5000/chat"
CONCURRENT_REQUESTS = 100
TEST_PAYLOAD = {"message": "What tenders are available?"}

def send_request(req_id):
    start = time.time()
    try:
        res = requests.post(URL, json=TEST_PAYLOAD, timeout=120)
        latency = round(time.time() - start, 2)
        return {"id": req_id, "status": res.status_code, "latency": latency}
    except Exception as e:
        return {"id": req_id, "status": "FAILED", "error": str(e)}

def run_stress_test():
    print(f"--- Starting Stress Test: {CONCURRENT_REQUESTS} Parallel Requests ---")
    start_total = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = [executor.submit(send_request, i) for i in range(CONCURRENT_REQUESTS)]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

    print(f"--- Stress Test Finished in {round(time.time() - start_total, 2)}s ---")

if __name__ == "__main__":
    run_stress_test()