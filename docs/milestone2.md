=== Cold run ===
[INFO] LOCAL_TEST enabled → skipping S3 download.
[TIMING] Load: 0.58s | Preproc: 0.03s | Infer: 0.06s
COLD RUN time: 1.792s
Response: {'statusCode': 200, 'body': '{"pred_index": 841, "timings": {"model_load_s": 0.585, "preprocess_s": 0.028, "inference_s": 0.058}}'}

=== Warm runs ===
[INFO] LOCAL_TEST enabled → skipping S3 download.
[TIMING] Load: 0.22s | Preproc: 0.00s | Infer: 0.07s
WARM run 1: 0.304s -> {'statusCode': 200, 'body': '{"pred_index": 841, "timings": {"model_load_s": 0.221, "preprocess_s": 0.0, "inference_s": 0.07}}'}
[INFO] LOCAL_TEST enabled → skipping S3 download.
[TIMING] Load: 0.24s | Preproc: 0.00s | Infer: 0.06s
WARM run 2: 0.327s -> {'statusCode': 200, 'body': '{"pred_index": 841, "timings": {"model_load_s": 0.238, "preprocess_s": 0.0, "inference_s": 0.062}}'}
[INFO] LOCAL_TEST enabled → skipping S3 download.
[TIMING] Load: 0.25s | Preproc: 0.00s | Infer: 0.06s
WARM run 3: 0.323s -> {'statusCode': 200, 'body': '{"pred_index": 841, "timings": {"model_load_s": 0.246, "preprocess_s": 0.0, "inference_s": 0.063}}'}