from typing import List, Dict, Any
from models import Roadmap

class RoadmapGenerator:
    """Generate learning roadmaps based on skill gaps."""
    
    def __init__(self):
        # Predefined learning topics by skill area
        self.learning_topics = {
            'python': [
                'Python Fundamentals - Variables, loops, functions, classes',
                'Data Structures - Lists, dictionaries, sets, tuples',
                'OOP in Python - Inheritance, polymorphism, encapsulation',
                'File I/O and Exception Handling',
                'Python Standard Library - os, sys, datetime, json',
                'Python Testing - unittest, pytest, mocking'
            ],
            'sql': [
                'SQL Fundamentals - SELECT, INSERT, UPDATE, DELETE',
                'JOIN Operations - INNER, LEFT, RIGHT, FULL OUTER JOIN',
                'Subqueries and CTEs',
                'Window Functions - RANK, DENSE_RANK, ROW_NUMBER',
                'Query Optimization - Indexes, EXPLAIN plans',
                'Database Design - Normalization, ER diagrams'
            ],
            'docker': [
                'Docker Fundamentals - Images, containers, Dockerfile',
                'Docker Compose - Multi-container applications',
                'Container Networking and Volumes',
                'Docker Registry - Image tagging and pushing',
                'Docker Swarm - Container orchestration',
                'Docker Security Best Practices'
            ],
            'kubernetes': [
                'Kubernetes Fundamentals - Pods, Services, Deployments',
                'Cluster Architecture - Master, Worker nodes',
                'Configuration - ConfigMaps, Secrets',
                'Storage - Volumes, PersistentVolumeClaims',
                'Networking - Ingress, Service types',
                'Helm Charts - Package management'
            ],
            'react': [
                'React Fundamentals - JSX, Components, Props, State',
                'React Hooks - useState, useEffect, useContext',
                'React Router - Navigation and routing',
                'State Management - Redux, Context API',
                'API Integration - useEffect with fetch/axios',
                'React Performance - Memoization, Code splitting'
            ],
            'django': [
                'Django Fundamentals - Models, Views, Templates',
                'Django ORM - QuerySets, relationships',
                'Django Forms - Form handling and validation',
                'Django Authentication - Users, permissions',
                'Django REST Framework - API development',
                'Django Deployment - Production setup'
            ],
            'flask': [
                'Flask Fundamentals - Routes, templates, request handling',
                'Flask SQLAlchemy - ORM integration',
                'Flask Authentication - Sessions, JWT',
                'Flask REST API - Blueprint, validation',
                'Flask Testing - Unit tests, integration tests',
                'Flask Deployment - Gunicorn, Nginx setup'
            ],
            'aws': [
                'AWS Fundamentals - EC2, S3, VPC',
                'AWS Compute - Lambda, ECS, EKS',
                'AWS Storage - RDS, DynamoDB, S3',
                'AWS Networking - Route53, CloudFront, API Gateway',
                'AWS Security - IAM, KMS, Secrets Manager',
                'AWS DevOps - CloudFormation, CodePipeline'
            ],
            'git': [
                'Git Fundamentals - init, add, commit, push',
                'Git Branching - Branch creation, merging',
                'Git Collaboration - Remote, pull requests',
                'Git Advanced - Rebase, cherry-pick, reset',
                'Git Hooks - Pre-commit, pre-push hooks',
                'Git Workflow - GitFlow, GitHub Flow'
            ],
            'jenkins': [
                'Jenkins Fundamentals - Installation, plugins',
                'Jenkins Pipeline - Declarative vs Scripted',
                'Jenkins Integration - Git, Docker, Kubernetes',
                'Jenkins Security - Authentication, authorization',
                'Jenkins Administration - Backup, scaling',
                'Jenkins Best Practices - Pipeline as code'
            ]
        }
        
        # Skill difficulty mapping for week assignment
        self.skill_difficulty = {
            'python': 'easy',
            'javascript': 'easy',
            'sql': 'easy',
            'git': 'easy',
            'html': 'easy',
            'css': 'easy',
            'docker': 'medium',
            'kubernetes': 'hard',
            'react': 'medium',
            'angular': 'medium',
            'vue': 'medium',
            'django': 'medium',
            'flask': 'easy',
            'aws': 'medium',
            'azure': 'medium',
            'gcp': 'medium',
            'linux': 'easy',
            'jenkins': 'medium',
            'ansible': 'medium',
            'terraform': 'hard'
        }
    
    def generate_roadmap(self, job_title: str, missing_skills: List[str], gap_percentage: float) -> Dict:
        """Generate a personalized learning roadmap."""
        roadmap = {
            'job_title': job_title,
            'gap_percentage': gap_percentage,
            'weeks': [],
            'estimated_total_weeks': 0,
            'skill_gaps': missing_skills[:10]
        }
        
        if not missing_skills:
            roadmap['message'] = 'Great job! You have all the required skills for this role.'
            roadmap['estimated_total_weeks'] = 0
            return roadmap
        
        # Organize skills by difficulty
        easy_skills = []
        medium_skills = []
        hard_skills = []
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            difficulty = self.skill_difficulty.get(skill_lower, 'medium')
            if difficulty == 'easy':
                easy_skills.append(skill)
            elif difficulty == 'hard':
                hard_skills.append(skill)
            else:
                medium_skills.append(skill)
        
        # Create weekly plan
        current_week = 1
        
        # Week 1-2: Easy skills
        if easy_skills:
            week_plan = {
                'week': f'Week {current_week}',
                'focus': 'Fundamentals',
                'topics': [],
                'description': 'Start with foundational skills'
            }
            for skill in easy_skills[:3]:
                topics = self.learning_topics.get(skill_lower, [f'Learn {skill} fundamentals'])
                for topic in topics[:2]:
                    week_plan['topics'].append({
                        'skill': skill,
                        'topic': topic,
                        'priority': 'High' if current_week == 1 else 'Medium'
                    })
            roadmap['weeks'].append(week_plan)
            current_week += 1
        
        # Week 2-4: Medium skills
        if medium_skills:
            week_plan = {
                'week': f'Week {current_week}',
                'focus': 'Core Skills Development',
                'topics': [],
                'description': 'Build core competencies'
            }
            for skill in medium_skills[:3]:
                skill_lower = skill.lower()
                topics = self.learning_topics.get(skill_lower, [
                    f'Learn {skill} fundamentals',
                    f'Practice {skill} with projects',
                    f'Master {skill} best practices'
                ])
                for topic in topics[:2]:
                    week_plan['topics'].append({
                        'skill': skill,
                        'topic': topic,
                        'priority': 'High'
                    })
            roadmap['weeks'].append(week_plan)
            current_week += 1
        
        # Month 2: Advanced/Hard skills
        if hard_skills:
            month_plan = {
                'week': f'Month 2',
                'focus': 'Advanced Skills',
                'topics': [],
                'description': 'Master advanced concepts'
            }
            for skill in hard_skills[:3]:
                skill_lower = skill.lower()
                topics = self.learning_topics.get(skill_lower, [
                    f'Learn advanced {skill} concepts',
                    f'Project with {skill}',
                    f'{skill} certification preparation'
                ])
                for topic in topics[:2]:
                    month_plan['topics'].append({
                        'skill': skill,
                        'topic': topic,
                        'priority': 'High'
                    })
            roadmap['weeks'].append(month_plan)
            current_week += 4
        
        # Add practice weeks
        if len(roadmap['weeks']) > 0:
            practice_week = {
                'week': f'Month 3',
                'focus': 'Integration & Projects',
                'topics': [
                    {
                        'skill': 'Project Development',
                        'topic': 'Build a complete project using learned skills',
                        'priority': 'High'
                    },
                    {
                        'skill': 'Portfolio Building',
                        'topic': 'Add projects to GitHub portfolio',
                        'priority': 'High'
                    },
                    {
                        'skill': 'Interview Preparation',
                        'topic': 'Practice technical interviews and coding challenges',
                        'priority': 'Medium'
                    }
                ],
                'description': 'Apply all learned skills in real projects'
            }
            roadmap['weeks'].append(practice_week)
        
        # Calculate estimated total weeks
        roadmap['estimated_total_weeks'] = len(roadmap['weeks']) * 2
        
        return roadmap