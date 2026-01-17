import requests
import sys

BASE_URL = "http://127.0.0.1:5000/api"

# Test Root Endpoint
def test_root():
    url = "http://localhost:8000/"
    response = requests.get(url)
    print(f"GET {url}")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    return response.status_code == 200

# Test Resume Analyze Endpoint
def test_resume_analyze(file_path, target_role):
    url = "http://localhost:8000/resume/analyze"
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'application/pdf' if file_path.endswith('.pdf') else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
        data = {'target_role': target_role}
        print(f"POST {url}")
        print(f"File: {file_path}")
        print(f"Target Role: {target_role}")
        response = requests.post(url, files=files, data=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"\nSkills found: {len(result.get('skills', []))}")
            print(f"Roadmap phases: {len(result.get('roadmap', []))}")
            print("\nTop 5 Skills:")
            for skill in result.get('skills', [])[:5]:
                print(f"  - {skill['name']}: {skill['confidence']:.2f}")
            print("\nRoadmap:")
            for phase in result.get('roadmap', []):
                print(f"  {phase['phase']}: {len(phase['skills'])} skills")
            return True
        else:
            print(f"Error: {response.text}")
            return False

# Test Skills API
def test_skills_api():
    print("Testing Skills API...")
    skills = requests.get(f"{BASE_URL}/skills").json()
    print("Skills:", skills)
    new_skill = {"name": "Machine Learning", "importance": 5}
    response = requests.post(f"{BASE_URL}/skills", json=new_skill)
    print("Added Skill:", response.json())

# Test Gap Analysis API
def test_gap_analysis_api():
    print("\nTesting Gap Analysis API...")
    gaps = requests.get(f"{BASE_URL}/gap-analysis").json()
    print("Skill Gaps:", gaps)

# Test Roadmap API
def test_roadmap_api():
    print("\nTesting Roadmap API...")
    roadmap = requests.get(f"{BASE_URL}/roadmap").json()
    print("Roadmap:", roadmap)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_api.py <resume_file.pdf|.docx> <target_role>")
        print("Example: python test_api.py resume.pdf 'data scientist'")
        sys.exit(1)
    file_path = sys.argv[1]
    target_role = sys.argv[2]
    print("Testing FastAPI Resume Analysis API\n")
    print("=" * 50)
    if not test_root():
        print("Server is not running. Start it with: uvicorn app.main:app --reload")
        sys.exit(1)
    test_resume_analyze(file_path, target_role)
    test_skills_api()
    test_gap_analysis_api()
    test_roadmap_api()
