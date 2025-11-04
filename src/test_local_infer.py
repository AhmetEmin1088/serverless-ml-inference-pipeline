import json, time
from lambda_handler import lambda_handler

def load_event(path="data/test_event.json"):
    import json
    return json.loads(open(path).read())

def run_cold():
    event = load_event()
    t0 = time.time()
    resp = lambda_handler(event, None)
    t1 = time.time()
    print("COLD RUN time: {:.3f}s".format(t1-t0))
    print("Response:", resp)

def run_warm():
    # simulate warm by calling twice (session may be cached inside handler module)
    event = load_event()
    for i in range(3):
        t0 = time.time()
        resp = lambda_handler(event, None)
        t1 = time.time()
        print(f"WARM run {i+1}: {t1-t0:.3f}s -> {resp}")

if __name__ == "__main__":
    print("=== Cold run ===")
    run_cold()
    print("\n=== Warm runs ===")
    run_warm()
