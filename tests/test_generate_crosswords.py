import requests

# Remplace par l'URL de ton IA sur Render si besoin
aio_url = "https://ivox-ai.onrender.com/generate-crosswords"

def test_generate_crosswords():
    resp = requests.post(aio_url, json={"n": 5}, timeout=30)
    print("Status:", resp.status_code)
    print("Response:", resp.json())
    assert resp.status_code == 200
    results = resp.json().get("results", [])
    assert len(results) == 5
    for r in results:
        assert r["status"] == "ok"

if __name__ == "__main__":
    test_generate_crosswords()
