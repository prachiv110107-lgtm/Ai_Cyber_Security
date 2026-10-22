import json
from app import app

def test_endpoints():
    client = app.test_client()

    print("\n--- 1. Testing GET / ---")
    res = client.get('/')
    print(res.status_code, res.get_json())
    assert res.status_code == 200

    print("\n--- 2. Testing POST /predict-url (Safe URL) ---")
    res = client.post('/predict-url', json={"url": "https://www.wikipedia.org"})
    print(res.status_code, json.dumps(res.get_json(), indent=2))
    assert res.get_json()['status'] == 'safe'

    print("\n--- 3. Testing POST /predict-url (Dangerous Phishing URL) ---")
    res = client.post('/predict-url', json={"url": "http://secure-paypal-login-verification-account.top/login.php"})
    print(res.status_code, json.dumps(res.get_json(), indent=2))
    assert res.get_json()['status'] == 'dangerous'

    print("\n--- 4. Testing POST /predict-sms (Dangerous Smishing) ---")
    res = client.post('/predict-sms', json={"message": "URGENT: Your Wells Fargo bank account is suspended due to unusual activity. Click http://wellsfarg0-online-security-token.club to restore access now."})
    print(res.status_code, json.dumps(res.get_json(), indent=2))
    assert res.get_json()['status'] == 'dangerous'

    print("\n--- 5. Testing POST /predict-email (Dangerous Email) ---")
    res = client.post('/predict-email', json={
        "sender": "admin@microsoft365-urgent-auth.pw",
        "subject": "CRITICAL: Password Expiration Notice",
        "content": "Dear Employee, Your corporate Microsoft 365 password expires in 2 hours. To maintain access, you must immediately renew your corporate credentials at http://microsoft-office365-urgent-password-reset.pw/auth."
    })
    print(res.status_code, json.dumps(res.get_json(), indent=2))
    assert res.get_json()['status'] == 'dangerous'

    print("\n--- 6. Testing GET /demo-samples ---")
    res = client.get('/demo-samples')
    print(res.status_code, f"Loaded {len(res.get_json()['urls'])} URL samples, {len(res.get_json()['sms'])} SMS samples")
    assert res.status_code == 200

    print("\n--- 7. Testing GET /challenge-questions ---")
    res = client.get('/challenge-questions')
    print(res.status_code, f"Loaded {len(res.get_json())} quiz questions")
    assert res.status_code == 200

    print("\n>>> ALL BACKEND API TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == '__main__':
    test_endpoints()
