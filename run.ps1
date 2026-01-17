# Initialize the database
Write-Host "Initializing SkillGenome Database..." -ForegroundColor Cyan
python backend/init_db.py

# Start the backend server
Write-Host "Starting backend server..." -ForegroundColor Green
python backend/app.py

# Run the Python starter (Windows PowerShell)
python src/main.py

# To run Node starter, uncomment:
# node src/index.js
