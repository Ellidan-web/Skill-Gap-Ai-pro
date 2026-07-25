import csv
import os
from datetime import datetime
from models import Job, CareerTip, SkillTag, Roadmap

def seed_database():
    """Seed database with initial data."""
    from database import db
    
    # Check if data already exists
    if Job.query.first():
        print("Database already seeded. Skipping...")
        return
    
    print("Seeding database...")
    
    # Seed jobs
    seed_jobs()
    
    # Seed career tips
    seed_career_tips()
    
    # Seed skill tags
    seed_skill_tags()
    
    # Seed roadmaps
    seed_roadmaps()
    
    db.session.commit()
    print("Database seeded successfully!")

def seed_jobs():
    """Seed jobs from CSV."""
    from database import db
    from models import Job
    
    csv_path = os.path.join('dataset', 'jobs.csv')
    
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Skipping job seeding.")
        return
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            job = Job(
                title=row['title'],
                category=row['category'],
                description=row['description'],
                required_skills=row['required_skills'],
                salary=row['salary'],
                difficulty=row['difficulty']
            )
            db.session.add(job)
    
    db.session.commit()
    print(f"Seeded jobs from {csv_path}")

def seed_career_tips():
    """Seed career tips."""
    from database import db
    from models import CareerTip
    
    tips = [
        {
            'title': 'Learn Flask Before Docker',
            'tip': 'Master Flask fundamentals first. Build REST APIs, handle authentication, and deploy simple apps before diving into containerization.',
            'priority': 1,
            'category': 'Backend Development'
        },
        {
            'title': 'Practice SQL JOINs',
            'tip': 'Master INNER JOIN, LEFT JOIN, RIGHT JOIN, and FULL OUTER JOIN. Practice complex queries with multiple tables and subqueries.',
            'priority': 2,
            'category': 'Database'
        },
        {
            'title': 'Master REST APIs',
            'tip': 'Understand HTTP methods, status codes, authentication, rate limiting, and API documentation. Build multiple REST APIs with different frameworks.',
            'priority': 1,
            'category': 'API Development'
        },
        {
            'title': 'Deploy Projects',
            'tip': 'Deploy every project you build. Learn cloud platforms like AWS, Azure, or GCP. Master CI/CD pipelines and containerization.',
            'priority': 1,
            'category': 'DevOps'
        },
        {
            'title': 'Build Portfolio Projects',
            'tip': 'Build at least 3-5 complete projects. Focus on real-world problems. Include documentation, tests, and deployment.',
            'priority': 1,
            'category': 'Career Development'
        },
        {
            'title': 'Improve GitHub Profile',
            'tip': 'Maintain a clean GitHub profile. Write meaningful commit messages. Add README files to projects. Contribute to open source.',
            'priority': 2,
            'category': 'Career Development'
        },
        {
            'title': 'Master Version Control',
            'tip': 'Learn Git branching strategies. Practice merging, rebasing, and resolving conflicts. Use GitHub flow or GitFlow.',
            'priority': 2,
            'category': 'DevOps'
        },
        {
            'title': 'Learn Testing',
            'tip': 'Write unit tests, integration tests, and end-to-end tests. Use pytest, JUnit, or similar frameworks. Aim for high test coverage.',
            'priority': 3,
            'category': 'Quality Assurance'
        },
        {
            'title': 'Master Design Patterns',
            'tip': 'Learn common design patterns: Singleton, Factory, Observer, Strategy, Decorator. Understand when and how to use them.',
            'priority': 3,
            'category': 'Software Design'
        },
        {
            'title': 'Understand System Design',
            'tip': 'Learn system design principles: scalability, reliability, availability. Practice designing systems for real-world scenarios.',
            'priority': 2,
            'category': 'System Design'
        },
        {
            'title': 'Learn CI/CD',
            'tip': 'Set up CI/CD pipelines for your projects. Use Jenkins, GitHub Actions, or GitLab CI. Automate testing and deployment.',
            'priority': 2,
            'category': 'DevOps'
        },
        {
            'title': 'Master API Security',
            'tip': 'Learn API security best practices: JWT, OAuth2, rate limiting, CORS, input validation, and secure headers.',
            'priority': 3,
            'category': 'Security'
        }
    ]
    
    for tip_data in tips:
        tip = CareerTip(**tip_data)
        db.session.add(tip)
    
    db.session.commit()
    print(f"Seeded {len(tips)} career tips")

def seed_skill_tags():
    """Seed skill tags."""
    from database import db
    from models import SkillTag
    
    csv_path = os.path.join('dataset', 'skills.csv')
    
    if not os.path.exists(csv_path):
        print(f"Warning: {csv_path} not found. Skipping skill tag seeding.")
        return
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            skill_tag = SkillTag(
                skill=row['skill'].strip().lower(),
                category=row['category'],
                proficiency=row.get('proficiency', 'Intermediate')
            )
            db.session.add(skill_tag)
    
    db.session.commit()
    print(f"Seeded skill tags from {csv_path}")

def seed_roadmaps():
    """Seed learning roadmaps."""
    from database import db
    from models import Roadmap
    
    roadmaps = [
        # Backend Developer Roadmap
        {'job_title': 'Backend Developer', 'week': 'Week 1', 'topic': 'Python Fundamentals - Data types, functions, OOP, and modules', 'priority': 1},
        {'job_title': 'Backend Developer', 'week': 'Week 2', 'topic': 'Flask/Django - Build REST APIs, handle routing, middleware, and authentication', 'priority': 1},
        {'job_title': 'Backend Developer', 'week': 'Week 3', 'topic': 'SQL & Databases - Design schemas, write complex queries, and use ORMs', 'priority': 1},
        {'job_title': 'Backend Developer', 'week': 'Week 4', 'topic': 'REST API Design - Design principles, documentation, and best practices', 'priority': 2},
        {'job_title': 'Backend Developer', 'week': 'Month 2', 'topic': 'Docker & Containerization - Containerize applications and manage containers', 'priority': 2},
        {'job_title': 'Backend Developer', 'week': 'Month 3', 'topic': 'Cloud Deployment - Deploy applications on AWS, Azure, or GCP', 'priority': 3},
        
        # Full Stack Developer Roadmap
        {'job_title': 'Full Stack Developer', 'week': 'Week 1', 'topic': 'JavaScript & ES6+ - Modern JavaScript, async/await, and DOM manipulation', 'priority': 1},
        {'job_title': 'Full Stack Developer', 'week': 'Week 2', 'topic': 'Frontend Framework - Learn React, Vue, or Angular', 'priority': 1},
        {'job_title': 'Full Stack Developer', 'week': 'Week 3', 'topic': 'Backend Development - Learn Node.js, Express, or Django', 'priority': 1},
        {'job_title': 'Full Stack Developer', 'week': 'Week 4', 'topic': 'Database Integration - Connect frontend and backend with databases', 'priority': 2},
        {'job_title': 'Full Stack Developer', 'week': 'Month 2', 'topic': 'API Integration - Build and consume REST APIs, GraphQL', 'priority': 2},
        {'job_title': 'Full Stack Developer', 'week': 'Month 3', 'topic': 'Full Stack Projects - Build and deploy complete full stack applications', 'priority': 3},
        
        # Data Analyst Roadmap
        {'job_title': 'Data Analyst', 'week': 'Week 1', 'topic': 'Python & Pandas - Data manipulation and analysis with pandas', 'priority': 1},
        {'job_title': 'Data Analyst', 'week': 'Week 2', 'topic': 'SQL & Databases - Write complex queries and data extraction', 'priority': 1},
        {'job_title': 'Data Analyst', 'week': 'Week 3', 'topic': 'Data Visualization - Create charts and dashboards with Tableau, Power BI', 'priority': 2},
        {'job_title': 'Data Analyst', 'week': 'Week 4', 'topic': 'Statistical Analysis - Statistics fundamentals and data interpretation', 'priority': 2},
        {'job_title': 'Data Analyst', 'week': 'Month 2', 'topic': 'ETL Pipelines - Build data pipelines and data cleaning processes', 'priority': 3},
        
        # Machine Learning Engineer Roadmap
        {'job_title': 'Machine Learning Engineer', 'week': 'Week 1', 'topic': 'Python & Libraries - NumPy, Pandas, and Scikit-learn fundamentals', 'priority': 1},
        {'job_title': 'Machine Learning Engineer', 'week': 'Week 2', 'topic': 'Machine Learning Algorithms - Supervised and unsupervised learning', 'priority': 1},
        {'job_title': 'Machine Learning Engineer', 'week': 'Week 3', 'topic': 'Deep Learning - Neural networks and deep learning with TensorFlow/PyTorch', 'priority': 2},
        {'job_title': 'Machine Learning Engineer', 'week': 'Week 4', 'topic': 'MLOps - Model deployment, monitoring, and versioning', 'priority': 2},
        {'job_title': 'Machine Learning Engineer', 'week': 'Month 2', 'topic': 'NLP or Computer Vision - Specialize in a subfield', 'priority': 3},
        
        # DevOps Engineer Roadmap
        {'job_title': 'DevOps Engineer', 'week': 'Week 1', 'topic': 'Linux & Bash - Command line, shell scripting, and system administration', 'priority': 1},
        {'job_title': 'DevOps Engineer', 'week': 'Week 2', 'topic': 'Version Control & CI/CD - Git, Jenkins, GitHub Actions', 'priority': 1},
        {'job_title': 'DevOps Engineer', 'week': 'Week 3', 'topic': 'Containerization - Docker and container management', 'priority': 1},
        {'job_title': 'DevOps Engineer', 'week': 'Week 4', 'topic': 'Orchestration - Kubernetes and container orchestration', 'priority': 2},
        {'job_title': 'DevOps Engineer', 'week': 'Month 2', 'topic': 'Infrastructure as Code - Terraform, Ansible, CloudFormation', 'priority': 2},
        {'job_title': 'DevOps Engineer', 'week': 'Month 3', 'topic': 'Monitoring & Observability - Prometheus, Grafana, ELK stack', 'priority': 3}
    ]
    
    for roadmap_data in roadmaps:
        roadmap = Roadmap(**roadmap_data)
        db.session.add(roadmap)
    
    db.session.commit()
    print(f"Seeded {len(roadmaps)} roadmap items")

if __name__ == '__main__':
    seed_database()