import requests
import sys

def test_root():
    url = "http://localhost:5000/"
    try:
        response = requests.get(url)
        print(f"GET {url}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}\n")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}\n")
        return False

def test_analyze(file_path, target_role, manual_skills=None):
    url = "http://localhost:5000/resume/analyze"
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f, 'application/pdf' if file_path.endswith('.pdf') else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
            data = {'target_role': target_role}
            if manual_skills:
                data['manual_skills'] = manual_skills
            
            print(f"POST {url}")
            print(f"File: {file_path}")
            print(f"Target Role: {target_role}")
            if manual_skills:
                print(f"Manual Skills: {manual_skills}")
            
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
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_simple.py <resume_file.pdf|.docx> <target_role> [manual_skills_json]")
        print("Example: python test_simple.py resume.pdf 'data scientist'")
        print("Example with manual skills: python test_simple.py resume.pdf 'frontend developer' '[{\"name\":\"react\",\"confidence\":0.9}]'")
        sys.exit(1)
    
    file_path = sys.argv[1]
    target_role = sys.argv[2]
    manual_skills = sys.argv[3] if len(sys.argv) > 3 else None
    
    print("Testing Flask Resume Analysis API\n")
    print("=" * 50)
    
    if not test_root():
        print("Server is not running. Start it with: python -m flask run")
        sys.exit(1)
    
    test_analyze(file_path, target_role, manual_skills)
