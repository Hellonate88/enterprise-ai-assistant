import requests
import json

url = "http://localhost:8000/chat"
payload = {
    "question": "test question"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response Text: {response.text}")
    try:
        print(f"Response JSON: {json.dumps(response.json(), indent=2)}")
    except:
        pass
except Exception as e:
    print(f"Error: {e}")

