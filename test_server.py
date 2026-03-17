import requests
import json

def test_predict():
    url = "http://localhost:8001/predict"
    # Mock payload with sample feature names (matchingTraining.csv)
    payload = {
        "features": {
            "Age of the girl": 5,
            "Is there a family history of autism or related neurodevelopmental conditions?": 1,
            "Did you experience any complications during pregnancy or childbirth?": 1,
            "At what age did your child first start to walk?": 2,
            "At what age did your child first start to speak in full words or phrases?": 2,
            # ... and so on. The server defaults missing features to 0.0
        }
    }
    
    print(f"Testing {url}...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Error connecting to server: {e}")
        print("Make sure to start the server first: uv run python server.py")

if __name__ == "__main__":
    test_predict()
