import base64, json
from pathlib import Path

img_path = Path("data/sample.png")
b64 = base64.b64encode(img_path.read_bytes()).decode('ascii')

event = {"body": json.dumps({"image_b64": b64})}

print(json.dumps(event)[:200] + "...")

Path("data/test_event.json").write_text(json.dumps(event))
print("Wrote data/test_event.json")
