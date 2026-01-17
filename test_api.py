import requests

BASE_URL = "http://127.0.0.1:5000/api"

# Test Skills API
print("Testing Skills API...")
skills = requests.get(f"{BASE_URL}/skills").json()
print("Skills:", skills)

new_skill = {"name": "Machine Learning", "importance": 5}
response = requests.post(f"{BASE_URL}/skills", json=new_skill)
print("Added Skill:", response.json())

# Test Gap Analysis API
print("\nTesting Gap Analysis API...")
gaps = requests.get(f"{BASE_URL}/gap-analysis").json()
print("Skill Gaps:", gaps)

# Test Roadmap API
print("\nTesting Roadmap API...")
roadmap = requests.get(f"{BASE_URL}/roadmap").json()
print("Roadmap:", roadmap)