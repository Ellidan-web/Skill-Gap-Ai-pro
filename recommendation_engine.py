from typing import List, Dict, Tuple, Optional
import math

# Import models and ML engine
from models import Job, Recommendation
from ml_engine import MLEngine


class RecommendationEngine:
    """Recommendation engine for job suggestions."""
    
    def __init__(self):
        self.ml_engine = MLEngine()
    
    def generate_recommendations(self, resume_text: str, skills: List[str], jobs: List[Job]) -> List[Dict]:
        """Generate job recommendations based on resume."""
        # Load job data into ML engine
        self.ml_engine.load_job_data(jobs)
        
        # Get matching jobs
        matches = self.ml_engine.find_matching_jobs(resume_text, skills)
        
        recommendations = []
        for job, confidence in matches:
            # Calculate match percentage
            job_skills = job.get_skills_list()
            match_data = self.ml_engine.calculate_match_percentage(skills, job_skills)
            
            # Get skill recommendations
            missing_skills = match_data.get('missing_skills', [])
            skill_recommendations = self.ml_engine.get_skill_recommendations(missing_skills)
            
            # Calculate market demand (simplified)
            demand = self._calculate_market_demand(job.title)
            
            # Calculate salary estimate
            salary_estimate = self._estimate_salary(job.salary)
            
            recommendations.append({
                'job_title': job.title,
                'category': job.category,
                'match_percentage': match_data['match_percentage'],
                'confidence': min(100, confidence * 1.2),
                'salary': salary_estimate,
                'market_demand': demand,
                'matched_skills': match_data['matched_skills'][:5],
                'missing_skills': missing_skills[:5],
                'required_skills': job_skills[:10],
                'difficulty': job.difficulty,
                'recommendation_reason': self._generate_recommendation_reason(
                    match_data['match_percentage'],
                    demand,
                    len(missing_skills)
                )
            })
        
        return recommendations[:5]  # Return top 5
    
    def _calculate_market_demand(self, job_title: str) -> str:
        """Calculate market demand for a job title."""
        high_demand = [
            'machine learning', 'data scientist', 'devops', 'cloud',
            'full stack', 'blockchain', 'kubernetes', 'docker'
        ]
        
        medium_demand = [
            'backend', 'frontend', 'python', 'java', 'javascript',
            'mobile', 'react', 'angular'
        ]
        
        job_lower = job_title.lower()
        
        for keyword in high_demand:
            if keyword in job_lower:
                return 'High'
        
        for keyword in medium_demand:
            if keyword in job_lower:
                return 'Medium'
        
        return 'Low'
    
    def _estimate_salary(self, salary_str: str) -> str:
        """Estimate salary range."""
        if not salary_str:
            return "$80,000 - $120,000"
        
        # If it's already a salary string, return it
        if '$' in salary_str or any(c.isdigit() for c in salary_str):
            return salary_str
        
        # Default salary ranges by difficulty
        salary_ranges = {
            'Advanced': '$120,000 - $160,000',
            'Intermediate': '$90,000 - $130,000',
            'Beginner': '$70,000 - $100,000'
        }
        
        for difficulty, salary in salary_ranges.items():
            if difficulty.lower() in salary_str.lower():
                return salary
        
        return "$80,000 - $120,000"
    
    def _generate_recommendation_reason(self, match_percentage: float, demand: str, missing_count: int) -> str:
        """Generate recommendation reason."""
        if match_percentage >= 80:
            return "Excellent match! Your skills align perfectly with this role."
        elif match_percentage >= 60:
            reason = "Good match. You have most required skills."
            if missing_count > 0:
                reason += f" Focus on developing {missing_count} missing skill(s)."
            return reason
        elif match_percentage >= 40:
            reason = "Potential match with some skill gaps."
            if demand == 'High':
                reason += " High market demand makes this role worth pursuing."
            return reason
        else:
            return "Significant skill gaps identified. Consider developing key skills or exploring other roles."
    
    def compare_careers(self, job1: Job, job2: Job) -> Dict:
        """Compare two career paths."""
        skills1 = set(job1.get_skills_list())
        skills2 = set(job2.get_skills_list())
        
        # Find overlapping skills
        overlapping = skills1.intersection(skills2)
        
        # Find skills unique to each
        unique_to_1 = skills1 - skills2
        unique_to_2 = skills2 - skills1
        
        # Calculate similarity percentage
        total_skills = len(skills1.union(skills2))
        similarity = len(overlapping) / max(1, total_skills) * 100 if total_skills > 0 else 0
        
        # Compare salaries
        salary1 = self._parse_salary(job1.salary)
        salary2 = self._parse_salary(job2.salary)
        
        return {
            'job1': {
                'title': job1.title,
                'category': job1.category,
                'salary': job1.salary,
                'difficulty': job1.difficulty
            },
            'job2': {
                'title': job2.title,
                'category': job2.category,
                'salary': job2.salary,
                'difficulty': job2.difficulty
            },
            'similarity_percentage': round(similarity, 2),
            'overlapping_skills': sorted(list(overlapping))[:10],
            'unique_to_job1': sorted(list(unique_to_1))[:10],
            'unique_to_job2': sorted(list(unique_to_2))[:10],
            'salary_comparison': {
                'job1_range': job1.salary,
                'job2_range': job2.salary
            }
        }
    
    def _parse_salary(self, salary_str: str) -> Optional[int]:
        """Parse salary string to get average number."""
        if not salary_str:
            return None
        
        # Extract numbers from salary string
        import re
        numbers = re.findall(r'\d+', salary_str)
        if numbers:
            # Take average of numbers
            avg = sum(int(n) for n in numbers) / len(numbers)
            return int(avg)
        return None