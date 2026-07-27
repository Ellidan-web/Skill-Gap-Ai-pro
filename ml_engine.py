import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple, Optional
import re
from models import Job

class MLEngine:
    """Machine Learning engine for resume analysis and job matching."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            lowercase=True,
            analyzer='word',
            token_pattern=r'[a-zA-Z]+'
        )
        self.job_vectors = None
        self.job_titles = []
        self.job_data = []
    
    def load_job_data(self, jobs: List[Job]) -> None:
        """Load job data for matching."""
        if not jobs:
            return
        
        # Prepare job descriptions
        descriptions = []
        self.job_titles = []
        self.job_data = []
        
        for job in jobs:
            # Combine title, category, description, and skills for better matching
            text_parts = [
                job.title,
                job.category,
                job.description or '',
                job.required_skills or ''
            ]
            text = ' '.join(text_parts)
            descriptions.append(text.lower())
            self.job_titles.append(job.title)
            self.job_data.append(job)
        
        # Create TF-IDF vectors
        if descriptions:
            self.job_vectors = self.vectorizer.fit_transform(descriptions)
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract technical skills from text using regex patterns."""
        skills = set()
        
        # Common programming languages and technologies
        tech_keywords = [
            # Programming Languages
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
            'kotlin', 'golang', 'rust', 'typescript', 'scala', 'perl', 'r', 'matlab',
            'dart', 'elixir', 'clojure', 'haskell', 'lua', 'objective-c',
            
            # Frameworks
            'django', 'flask', 'fastapi', 'spring', 'spring boot', 'node.js',
            'express', 'react', 'vue', 'angular', 'laravel', 'symfony', 'rails',
            'asp.net', 'react native', 'flutter', 'tensorflow', 'pytorch',
            'scikit-learn', 'keras', 'jquery', 'bootstrap', 'sass', 'less',
            
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'firebase', 'cassandra', 'dynamodb', 'oracle', 'mariadb', 'sqlite',
            'neo4j', 'graphql', 'prisma', 'sequelize',
            
            # DevOps
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux', 'git',
            'jenkins', 'ansible', 'terraform', 'prometheus', 'grafana', 'nginx',
            'ci/cd', 'github actions', 'gitlab ci', 'circleci', 'travis ci',
            
            # Data Science
            'pandas', 'numpy', 'scikit-learn', 'opencv', 'nltk', 'spacy',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'data analysis', 'statistics', 'big data', 'hadoop', 'spark',
            
            # Development
            'rest api', 'graphql', 'microservices', 'html', 'css', 'agile',
            'scrum', 'jira', 'confluence', 'nosql', 'api', 'restful',
            'soap', 'json', 'xml', 'http', 'oauth2', 'jwt',
            
            # Additional
            'redis', 'mongodb', 'postgresql', 'mysql', 'sql', 'nosql',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux', 'git',
            'react', 'angular', 'vue', 'django', 'flask', 'fastapi'
        ]
        
        text_lower = text.lower()
        
        # Find exact matches
        for keyword in tech_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                skills.add(keyword)
        
        # Extract skills from skill sections
        skill_patterns = [
            r'(?:skills|technologies|tools|tech stack|expertise)[:]\s*([^\n]+)',
            r'(?:proficient in|experienced with|skilled in)\s+([^\n]+)',
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Split by common separators
                items = re.split(r'[,;|]|\s+and\s+|\s*•\s*|\s+-\s+', match)
                for item in items:
                    item = item.strip()
                    if item and len(item) > 2:
                        skills.add(item)
        
        return sorted(list(skills))
    
    def calculate_similarity(self, resume_text: str, job_text: str) -> float:
        """Calculate cosine similarity between resume and job text."""
        try:
            # Ensure vectorizer is fitted
            if not hasattr(self.vectorizer, 'vocabulary_'):
                # Fit on both texts if not fitted
                combined = [resume_text, job_text]
                self.vectorizer.fit(combined)
            
            # Transform texts
            resume_vec = self.vectorizer.transform([resume_text])
            job_vec = self.vectorizer.transform([job_text])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(resume_vec, job_vec)[0][0]
            return float(similarity)
        except Exception:
            return 0.0
    
    def find_matching_jobs(self, resume_text: str, skills: List[str]) -> List[Tuple[Job, float]]:
        """Find matching jobs for a resume."""
        if not self.job_data or self.job_vectors is None:
            return []
        
        # Prepare resume text
        text_parts = [
            resume_text,
            ' '.join(skills)
        ]
        resume_text_combined = ' '.join(text_parts)
        
        # Vectorize resume
        resume_vector = self.vectorizer.transform([resume_text_combined])
        
        # Calculate similarities
        similarities = cosine_similarity(resume_vector, self.job_vectors)[0]
        
        # Pair jobs with similarities
        job_similarities = []
        for i, job in enumerate(self.job_data):
            if i < len(similarities):
                similarity_score = float(similarities[i])
                job_similarities.append((job, similarity_score))
        
        # Sort by similarity score
        job_similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Add confidence based on skills match
        enhanced_results = []
        for job, similarity in job_similarities[:10]:
            # Calculate skill overlap
            job_skills = job.get_skills_list()
            matched_skills = set(skills).intersection(set(job_skills))
            skill_match_ratio = len(matched_skills) / max(1, len(job_skills))
            
            # Combine similarity and skill match
            confidence = (similarity * 0.6 + skill_match_ratio * 0.4) * 100
            enhanced_results.append((job, min(100, confidence)))
        
        return enhanced_results[:5]  # Return top 5 matches
    
    def calculate_match_percentage(self, resume_skills: List[str], job_skills: List[str]) -> Dict:
        """Calculate match percentage between resume skills and job requirements."""
        from config import SKILL_SYNONYMS
        
        # Clean and normalize resume skills
        resume_skills_lower = []
        for s in resume_skills:
            if s and s.strip():
                cleaned = s.lower().strip()
                cleaned = cleaned.rstrip('.,;:')
                cleaned = cleaned.strip('"\'')
                if cleaned and len(cleaned) > 1:
                    # Check if this skill has a normalized version
                    normalized = cleaned
                    for normalized_skill, variations in SKILL_SYNONYMS.items():
                        if cleaned in variations or cleaned == normalized_skill:
                            normalized = normalized_skill
                            break
                    resume_skills_lower.append(normalized)
        
        # Clean and normalize job skills
        job_skills_lower = []
        for s in job_skills:
            if s and s.strip():
                cleaned = s.lower().strip()
                cleaned = cleaned.strip('"\'')
                if cleaned:
                    # Check if this skill has a normalized version
                    normalized = cleaned
                    for normalized_skill, variations in SKILL_SYNONYMS.items():
                        if cleaned in variations or cleaned == normalized_skill:
                            normalized = normalized_skill
                            break
                    job_skills_lower.append(normalized)
        
        # Debug prints
        print(f"Resume skills (cleaned): {resume_skills_lower}")
        print(f"Job skills (cleaned): {job_skills_lower}")
        print(f"Total job skills: {len(job_skills_lower)}")
        
        # Find matches and gaps
        matched = []
        missing = []
        extra = []
        
        # Check each job skill against resume skills
        for job_skill in job_skills_lower:
            is_matched = False
            job_skill_parts = job_skill.split()
            
            for resume_skill in resume_skills_lower:
                # Check exact match
                if job_skill == resume_skill:
                    matched.append(job_skill)
                    is_matched = True
                    break
                # Check if job skill is contained in resume skill
                elif job_skill in resume_skill:
                    matched.append(job_skill)
                    is_matched = True
                    break
                # Check if resume skill is contained in job skill
                elif resume_skill in job_skill:
                    matched.append(job_skill)
                    is_matched = True
                    break
                # Check if any word matches (for multi-word skills)
                elif any(part in resume_skill for part in job_skill_parts if len(part) > 2):
                    matched.append(job_skill)
                    is_matched = True
                    break
            
            if not is_matched:
                missing.append(job_skill)
        
        # Check for extra skills (skills in resume not in job)
        for resume_skill in resume_skills_lower:
            is_extra = True
            for job_skill in job_skills_lower:
                if resume_skill in job_skill or job_skill in resume_skill:
                    is_extra = False
                    break
                # Check if any word matches
                resume_parts = resume_skill.split()
                job_parts = job_skill.split()
                if any(rp in job_parts for rp in resume_parts if len(rp) > 2):
                    is_extra = False
                    break
            if is_extra:
                extra.append(resume_skill)
        
        # Calculate percentages
        total_required = len(job_skills_lower)
        matched_count = len(matched)
        
        if total_required > 0:
            match_percentage = (matched_count / total_required) * 100
        else:
            match_percentage = 0
        
        gap_percentage = 100 - match_percentage if total_required > 0 else 0
        
        # Debug prints
        print(f"Matched: {matched}")
        print(f"Missing: {missing}")
        print(f"Extra: {extra}")
        print(f"Match %: {match_percentage}")
        print(f"Gap %: {gap_percentage}")
        
        return {
            'match_percentage': round(match_percentage, 2),
            'gap_percentage': round(gap_percentage, 2),
            'matched_skills': matched[:10],
            'missing_skills': missing[:10],
            'extra_skills': extra[:10],
            'total_required': total_required,
            'matched_count': matched_count
        }
    
    def get_skill_recommendations(self, missing_skills: List[str]) -> List[Dict]:
        """Generate recommendations for missing skills."""
        recommendations = []
        
        # Skill difficulty mapping
        difficulty_map = {
            'python': 'beginner',
            'javascript': 'beginner',
            'sql': 'intermediate',
            'docker': 'intermediate',
            'kubernetes': 'advanced',
            'react': 'intermediate',
            'angular': 'intermediate',
            'vue': 'intermediate',
            'django': 'intermediate',
            'flask': 'beginner',
            'aws': 'intermediate',
            'azure': 'intermediate',
            'gcp': 'intermediate',
            'linux': 'beginner',
            'git': 'beginner',
            'jenkins': 'intermediate',
            'ansible': 'intermediate',
            'terraform': 'advanced',
        }
        
        # Learning time estimates (hours)
        time_estimates = {
            'python': 40,
            'javascript': 30,
            'sql': 20,
            'docker': 15,
            'kubernetes': 25,
            'react': 25,
            'angular': 20,
            'vue': 15,
            'django': 20,
            'flask': 10,
            'aws': 20,
            'azure': 20,
            'gcp': 20,
            'linux': 15,
            'git': 10,
            'jenkins': 15,
            'ansible': 15,
            'terraform': 20,
        }
        
        for skill in missing_skills[:8]:
            skill_lower = skill.lower()
            difficulty = difficulty_map.get(skill_lower, 'intermediate')
            estimated_hours = time_estimates.get(skill_lower, 20)
            
            # Generate learning resources
            resources = [
                f"https://www.learn{skill_lower}.com",
                f"https://www.youtube.com/results?search_query={skill_lower}+tutorial"
            ]
            
            recommendations.append({
                'skill': skill,
                'difficulty': difficulty,
                'estimated_hours': estimated_hours,
                'priority': 'High' if difficulty == 'advanced' else ('Medium' if difficulty == 'intermediate' else 'Low'),
                'resources': resources[:2]
            })
        
        return recommendations