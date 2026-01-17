def seed_roles():
    roles = [
        # Computer Science roles
        PredefinedRole(
            sector="Computer Science",
            role_title="Software Engineer",
            experience_level="Entry",
            required_skills=json.dumps([
                {"skill": "Python", "importance": "Critical", "proficiency": "Intermediate"},
                {"skill": "Data Structures", "importance": "Critical", "proficiency": "Intermediate"},
                {"skill": "Algorithms", "importance": "High", "proficiency": "Intermediate"},
                {"skill": "Version Control (Git)", "importance": "High", "proficiency": "Beginner"}
            ])
        ),
        PredefinedRole(
            sector="Computer Science",
            role_title="Data Scientist",
            experience_level="Mid",
            required_skills=json.dumps([
                {"skill": "Python", "importance": "Critical", "proficiency": "Advanced"},
                {"skill": "Machine Learning", "importance": "Critical", "proficiency": "Intermediate"},
                {"skill": "Data Visualization", "importance": "High", "proficiency": "Intermediate"},
                {"skill": "SQL", "importance": "High", "proficiency": "Intermediate"}
            ])
        ),
        # Urban Development roles
        PredefinedRole(
            sector="Urban Development",
            role_title="Urban Planner",
            experience_level="Entry",
            required_skills=json.dumps([
                {"skill": "GIS", "importance": "Critical", "proficiency": "Intermediate"},
                {"skill": "Urban Planning Theory", "importance": "High", "proficiency": "Beginner"},
                {"skill": "Data Analysis", "importance": "High", "proficiency": "Intermediate"},
                {"skill": "Visualization Tools", "importance": "Medium", "proficiency": "Beginner"}
            ])
        ),
        PredefinedRole(
            sector="Urban Development",
            role_title="Smart City Analyst",
            experience_level="Mid",
            required_skills=json.dumps([
                {"skill": "IoT", "importance": "Critical", "proficiency": "Intermediate"},
                {"skill": "Data Analysis", "importance": "Critical", "proficiency": "Intermediate"},
                {"skill": "Urban Infrastructure", "importance": "High", "proficiency": "Intermediate"},
                {"skill": "Python", "importance": "High", "proficiency": "Intermediate"}
            ])
        )
    ]
    db.session.bulk_save_objects(roles)
    db.session.commit()
    print(f"✅ Seeded {len(roles)} predefined roles")