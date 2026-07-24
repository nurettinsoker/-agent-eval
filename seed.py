import sys
sys.path.insert(0, 'dashboard/src')
from server.db import db

# Seed a test project
project = db.project.create({
    "name": "Default Project",
    "description": "Default project for evaluations",
    "organizationId": "default-org"
})
print(f"Created project: {project.id} - {project.name}")
