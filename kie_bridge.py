import os
import time
import requests
import argparse
import sys
import json

API_KEY = os.environ.get("KIE_API_KEY", "")
MARKET_URL = "https://api.kie.ai"
STORAGE_URL = "https://kiei.redpandaai.co"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

ENDPOINTS = [
    "/api/v1/jobs/createTask",
    "/api/v1/obs/createTask",
    "/v1/jobs/createTask",
    "/v1/obs/createTask",
    "/obs/createTask"
]

def find_working_endpoint():
    print("--- Probing Kie.ai Endpoints ---")
    for path in ENDPOINTS:
        url = f"{MARKET_URL}{path}"
        print(f"Probing {url}...", end=" ")
        try:
            res = requests.post(url, headers=HEADERS, json={"model": "test"}, timeout=5)
            if res.status_code != 404:
                print(f"✅ FOUND! ({res.status_code})")
                return path
            else:
                print("❌ 404")
        except Exception as e:
            print(f"❌ ERROR: {e}")
    print("Critical Error: No working endpoint found.")
    return None

WORKING_ENDPOINT = None

def upload_file(file_path):
    if not file_path or not os.path.exists(file_path):
        return None
    print(f"Uploading {file_path}...")
    upload_bases = [STORAGE_URL, MARKET_URL]
    upload_paths = ["/api/file-upload", "/api/v1/upload", "/upload"]
    for base in upload_bases:
        for path in upload_paths:
            url = f"{base}{path}"
            try:
                with open(file_path, "rb") as f:
                    files = {"file": f}
                    response = requests.post(url, headers={"Authorization": f"Bearer {API_KEY}"}, files=files, timeout=10)
                    if response.status_code == 200:
                        return response.json().get("url")
            except Exception:
                continue
    print(f"❌ Upload failed for {file_path}. Network block suspected.")
    return None

def generate_image(prompt, aspect_ratio="1:1", resolution="basic"):
    global WORKING_ENDPOINT
    if not WORKING_ENDPOINT:
        WORKING_ENDPOINT = find_working_endpoint()
        if not WORKING_ENDPOINT: sys.exit(1)
    print(f"Generating image: {prompt[:50]}...")
    url = f"{MARKET_URL}{WORKING_ENDPOINT}"
    payload = {
        "model": "seedream/5-lite-text-to-image",
        "input": {
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "quality": resolution,
            "output_format": "png",
            "nsfw_checker": False
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"Image request failed: {response.text}")
        return None
    data = response.json()
    if data.get("code") and data.get("code") != 200:
        print(f"API Error: {data.get('msg')}")
        return None
    task_id = data.get("data", {}).get("taskId") if isinstance(data.get("data"), dict) else data.get("taskId")
    if not task_id:
        print("Error: No taskId found in response body.")
        return None
    return poll_task(task_id)

def generate_video(prompt, start_image=None, end_image=None, duration=8):
    global WORKING_ENDPOINT
    if not WORKING_ENDPOINT:
        WORKING_ENDPOINT = find_working_endpoint()
        if not WORKING_ENDPOINT: sys.exit(1)
    print(f"Generating video: {prompt[:50]}...")
    first_frame = upload_file(start_image) if start_image else None
    last_frame = upload_file(end_image) if end_image else None
    url = f"{MARKET_URL}{WORKING_ENDPOINT}"
    payload = {
        "model": "kling/2.6-text-to-video", 
        "input": {
            "prompt": prompt,
            "duration": duration,
            "first_frame_url": first_frame,
            "last_frame_url": last_frame
        }
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 200:
        print(f"Video request failed: {response.text}")
        return None
    data = response.json()
    if data.get("code") and data.get("code") != 200:
        print(f"API Error: {data.get('msg')}")
        return None
    task_id = data.get("data", {}).get("taskId") if isinstance(data.get("data"), dict) else data.get("taskId")
    if not task_id:
        print("Error: No taskId found in response body.")
        return None
    return poll_task(task_id)

def poll_task(task_id):
    url = f"{MARKET_URL}/api/v1/jobs/recordInfo"
    params = {"taskId": task_id}
    while True:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code != 200:
            print(f"Polling failed: {response.text}")
            return None
        data = response.json()
        record = data.get("data", {})
        if not record: return None
        state = record.get("state")
        if state == "success":
            res_json = record.get("resultJson")
            if not res_json: return None
            try:
                res = json.loads(res_json) if isinstance(res_json, str) else res_json
                urls = res.get("resultUrls", [])
                return urls[0] if urls else None
            except: return None
        elif state == "fail":
            print(f"Task {task_id} failed: {record.get('failMsg')}")
            return None
        time.sleep(10)

def download_file(url, dest_path):
    print(f"Downloading to {dest_path}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["image", "video"], required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--start", help="Path to start image")
    parser.add_argument("--end", help="Path to end image")
    parser.add_argument("--out", required=True)
    parser.add_argument("--duration", type=int, default=8)
    args = parser.parse_args()
    if args.type == "image":
        url = generate_image(args.prompt)
    else:
        url = generate_video(args.prompt, args.start, args.end, args.duration)
    if url:
        download_file(url, args.out)
    else:
        sys.exit(1)