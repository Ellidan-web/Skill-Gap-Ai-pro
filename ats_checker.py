import re
from typing import List, Dict, Set, Tuple

class ATSChecker:
    """Calculate ATS resume score based on various criteria."""
    
    def __init__(self):
        self.keyword_weights = {
            'python': 10,
            'sql': 10,
            'git': 8,
            'docker': 8,
            'aws': 8,
            'javascript': 7,
            'java': 7,
            'rest api': 7,
            'linux': 6,
            'agile': 6,
            'scrum': 5,
            'jenkins': 5,
            'kubernetes': 5,
            'azure': 4,
            'gcp': 4,
            'ci/cd': 4,
            'html': 3,
            'css': 3,
            'react': 3,
            'angular': 3,
            'vue': 3,
            'django': 3,
            'flask': 3,
            'mongodb': 3,
            'postgresql': 3,
            'mysql': 3,
            'redis': 2,
            'nginx': 2,
            'jira': 2,
            'confluence': 2,
            'github': 2,
            'gitlab': 2,
            'selenium': 2,
            'pytest': 2,
            'unittest': 2,
            'postman': 2,
            'swagger': 2,
            'graphql': 2,
            'microservices': 2,
            'docker compose': 2,
            'jenkins pipeline': 2
        }
    
    def calculate_ats_score(self, resume_text: str, skills: List[str]) -> Dict:
        """
        Calculate ATS resume score.
        
        Returns:
            Dict containing:
            - score: Total ATS score (0-100)
            - breakdown: Detailed breakdown of scores by category
            - recommendations: List of recommendations for improvement
            - missing_keywords: Keywords missing from the resume
        """
        text_lower = resume_text.lower()
        skills_lower = [s.lower() for s in skills]
        
        # Score components
        scores = {
            'keyword_match': self._score_keyword_match(text_lower),
            'skill_relevance': self._score_skill_relevance(skills_lower),
            'formatting': self._score_formatting(resume_text),
            'content_quality': self._score_content_quality(resume_text),
            'experience': self._score_experience(resume_text),
            'education': self._score_education(resume_text),
            'projects': self._score_projects(resume_text),
            'certifications': self._score_certifications(resume_text)
        }
        
        # Calculate total score
        total_score = sum(scores.values())
        total_score = min(100, total_score)
        
        # Get missing keywords
        missing_keywords = self._get_missing_keywords(text_lower)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(scores, missing_keywords, skills)
        
        return {
            'score': total_score,
            'breakdown': scores,
            'recommendations': recommendations,
            'missing_keywords': missing_keywords[:10]
        }
    
    def _score_keyword_match(self, text: str) -> float:
        """Score keyword matches in resume."""
        matched_keywords = 0
        total_weight = 0
        
        for keyword, weight in self.keyword_weights.items():
            total_weight += weight
            if keyword in text:
                matched_keywords += weight
        
        if total_weight > 0:
            match_ratio = matched_keywords / total_weight
            score = min(35, match_ratio * 35)
            return max(10, score) if matched_keywords > 0 else 0
        return 0
    
    def _score_skill_relevance(self, skills: List[str]) -> float:
        """Score skill relevance and diversity."""
        if not skills:
            return 0
        
        relevant_skills = 0
        for skill in skills:
            for keyword in self.keyword_weights.keys():
                if keyword in skill:
                    relevant_skills += 1
                    break
        
        skill_diversity = len(set(skills))
        score = min(20, (relevant_skills / max(1, len(skills))) * 15 + min(5, skill_diversity / 5))
        return score
    
    def _score_formatting(self, text: str) -> float:
        """Score resume formatting and structure."""
        score = 0
        
        sections = ['experience', 'education', 'skills', 'projects', 'certifications']
        found_sections = 0
        for section in sections:
            if section in text.lower():
                found_sections += 1
        
        score += min(10, found_sections * 2)
        
        if '•' in text or '*' in text or '-' in text:
            score += 3
        
        if re.search(r'\d{4}\s*[-–]\s*\d{4}', text):
            score += 2
        
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
            score += 2
        if re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', text):
            score += 2
        
        return min(20, score)
    
    def _score_content_quality(self, text: str) -> float:
        """Score content quality and depth."""
        score = 0
        words = text.split()
        word_count = len(words)
        
        if 200 <= word_count <= 1000:
            score += 8
        elif 100 <= word_count < 200:
            score += 4
        elif word_count > 1000:
            score += 6
        else:
            score += 2
        
        action_verbs = [
            'developed', 'created', 'built', 'designed', 'implemented',
            'managed', 'led', 'coordinated', 'improved', 'optimized',
            'analyzed', 'evaluated', 'researched', 'tested', 'deployed'
        ]
        
        found_verbs = 0
        for verb in action_verbs:
            if verb in text.lower():
                found_verbs += 1
        
        score += min(12, found_verbs * 1.5)
        
        if re.search(r'\d+\s*%', text) or re.search(r'\d+\s*(million|thousand|hundred)', text.lower()):
            score += 5
        
        return min(25, score)
    
    def _score_experience(self, text: str) -> float:
        """Score work experience section."""
        score = 0
        
        if 'experience' in text.lower():
            score += 8
            
            years_pattern = r'(\d+)\s*(?:\+|\s*-\s*\d+)?\s*years?\s+(?:of\s+)?experience'
            matches = re.findall(years_pattern, text.lower())
            if matches:
                years = int(matches[0])
                if years >= 5:
                    score += 5
                elif years >= 3:
                    score += 3
                else:
                    score += 2
            
            if 'responsibilities' in text.lower():
                score += 3
            if 'achievements' in text.lower():
                score += 4
        
        return min(20, score)
    
    def _score_education(self, text: str) -> float:
        """Score education section."""
        score = 0
        
        education_keywords = ['bachelor', 'master', 'phd', 'mba', 'bs', 'ms', 'degree']
        found_education = 0
        
        for keyword in education_keywords:
            if keyword in text.lower():
                found_education += 1
        
        if found_education >= 2:
            score += 12
        elif found_education == 1:
            score += 8
        else:
            score += 4
        
        if re.search(r'gpa\s*[:]?\s*\d\.\d+', text.lower()):
            score += 3
        
        return min(15, score)
    
    def _score_projects(self, text: str) -> float:
        """Score projects section."""
        score = 0
        
        if 'projects' in text.lower():
            score += 8
            
            if 'github' in text.lower() or 'git' in text.lower():
                score += 4
            
            if 'deployed' in text.lower() or 'deployment' in text.lower():
                score += 3
            
            if 'built' in text.lower() or 'developed' in text.lower():
                score += 3
        
        return min(15, score)
    
    def _score_certifications(self, text: str) -> float:
        """Score certifications section."""
        score = 0
        
        cert_keywords = [
            'certified', 'certification', 'aws', 'azure', 'google',
            'scrum master', 'pmp', 'ccna', 'ccnp', 'comptia',
            'microsoft certified', 'oracle certified', 'cisco'
        ]
        
        found_certs = 0
        for keyword in cert_keywords:
            if keyword in text.lower():
                found_certs += 1
        
        if found_certs >= 3:
            score += 10
        elif found_certs >= 1:
            score += 6
        
        return min(12, score)
    
    def _get_missing_keywords(self, text: str) -> List[str]:
        """Get keywords missing from the resume."""
        missing = []
        for keyword in self.keyword_weights.keys():
            if keyword not in text:
                missing.append(keyword)
        return sorted(missing, key=lambda x: self.keyword_weights[x], reverse=True)
    
    def _generate_recommendations(self, scores: Dict, missing_keywords: List[str], skills: List[str] = None) -> List[str]:
        """Generate strict ATS score analysis with detailed breakdown."""
        recommendations = []
        
        # ================================================================
        # ATS SCORE BREAKDOWN
        # ================================================================
        keyword_match = scores.get('keyword_match', 0)
        skill_relevance = scores.get('skill_relevance', 0)
        formatting = scores.get('formatting', 0)
        content_quality = scores.get('content_quality', 0)
        experience = scores.get('experience', 0)
        education = scores.get('education', 0)
        projects = scores.get('projects', 0)
        certifications = scores.get('certifications', 0)
        
        total_ats = sum(scores.values())
        total_ats = min(100, total_ats)
        
        # ================================================================
        # ATS SCORE ASSESSMENT - STRICT
        # ================================================================
        recommendations.append("=" * 60)
        recommendations.append("ATS SCORE ANALYSIS")
        recommendations.append("=" * 60)
        recommendations.append("")
        
        if total_ats < 40:
            recommendations.append(f"CRITICAL: Your ATS score is {int(total_ats)}/100")
            recommendations.append("   Your resume will likely be REJECTED by Applicant Tracking Systems.")
            recommendations.append("   Immediate action is required to improve your resume.")
        elif total_ats < 60:
            recommendations.append(f"WARNING: Your ATS score is {int(total_ats)}/100")
            recommendations.append("   Your resume may be filtered out by Applicant Tracking Systems.")
            recommendations.append("   Significant improvements are needed.")
        elif total_ats < 75:
            recommendations.append(f"MODERATE: Your ATS score is {int(total_ats)}/100")
            recommendations.append("   Your resume is acceptable but needs improvement.")
            recommendations.append("   Focus on the areas below to increase your score.")
        elif total_ats < 90:
            recommendations.append(f"GOOD: Your ATS score is {int(total_ats)}/100")
            recommendations.append("   Your resume is well-optimized for most ATS systems.")
            recommendations.append("   Minor improvements can make it excellent.")
        else:
            recommendations.append(f"EXCELLENT: Your ATS score is {int(total_ats)}/100")
            recommendations.append("   Your resume is highly optimized for ATS systems.")
            recommendations.append("   Keep maintaining this quality.")
        
        recommendations.append("")
        
        # ================================================================
        # ATS SCORE BREAKDOWN TABLE
        # ================================================================
        recommendations.append("ATS SCORE BREAKDOWN:")
        
        keyword_status = "OK" if keyword_match >= 25 else "POOR" if keyword_match < 15 else "FAIR"
        skill_status = "OK" if skill_relevance >= 15 else "POOR" if skill_relevance < 10 else "FAIR"
        format_status = "OK" if formatting >= 15 else "POOR" if formatting < 10 else "FAIR"
        content_status = "OK" if content_quality >= 18 else "POOR" if content_quality < 12 else "FAIR"
        exp_status = "OK" if experience >= 15 else "POOR" if experience < 10 else "FAIR"
        edu_status = "OK" if education >= 11 else "POOR" if education < 7 else "FAIR"
        proj_status = "OK" if projects >= 11 else "POOR" if projects < 7 else "FAIR"
        cert_status = "OK" if certifications >= 9 else "POOR" if certifications < 5 else "FAIR"
        
        recommendations.append(f"   * Keyword Match:        {int(keyword_match)}/35  [{keyword_status}]")
        recommendations.append(f"   * Skill Relevance:      {int(skill_relevance)}/20  [{skill_status}]")
        recommendations.append(f"   * Formatting:           {int(formatting)}/20  [{format_status}]")
        recommendations.append(f"   * Content Quality:      {int(content_quality)}/25  [{content_status}]")
        recommendations.append(f"   * Experience:           {int(experience)}/20  [{exp_status}]")
        recommendations.append(f"   * Education:            {int(education)}/15  [{edu_status}]")
        recommendations.append(f"   * Projects:             {int(projects)}/15  [{proj_status}]")
        recommendations.append(f"   * Certifications:       {int(certifications)}/12  [{cert_status}]")
        recommendations.append("")
        
        # ================================================================
        # CRITICAL ISSUES - MUST FIX
        # ================================================================
        critical_issues = []
        
        if keyword_match < 15:
            critical_issues.append(f"   * Keyword Match ({int(keyword_match)}/35): Add more technical keywords to your resume")
        if skill_relevance < 10:
            critical_issues.append(f"   * Skill Relevance ({int(skill_relevance)}/20): Your skills don't match the job requirements")
        if formatting < 10:
            critical_issues.append(f"   * Formatting ({int(formatting)}/20): Resume structure needs improvement")
        if content_quality < 12:
            critical_issues.append(f"   * Content Quality ({int(content_quality)}/25): Add more achievements and details")
        if experience < 10:
            critical_issues.append(f"   * Experience ({int(experience)}/20): Expand work experience section")
        if projects < 7:
            critical_issues.append(f"   * Projects ({int(projects)}/15): Add a projects section")
        
        if critical_issues:
            recommendations.append("CRITICAL ISSUES TO FIX IMMEDIATELY:")
            for issue in critical_issues:
                recommendations.append(issue)
            recommendations.append("")
        
        # ================================================================
        # MISSING SKILLS ANALYSIS
        # ================================================================
        if missing_keywords and len(missing_keywords) > 0:
            top_missing = missing_keywords[:10]
            
            recommendations.append("SKILLS GAP ANALYSIS:")
            recommendations.append(f"   You are missing {len(missing_keywords)} key skills for this role.")
            recommendations.append(f"   Missing skills: {', '.join(top_missing)}")
            recommendations.append("")
            
            recommendations.append("SPECIFIC STEPS TO FILL SKILLS GAPS:")
            
            for skill in top_missing:
                if skill in ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust']:
                    recommendations.append(f"   - {skill.title()}:")
                    recommendations.append(f"     * Complete a course on Codecademy/Udemy/Coursera")
                    recommendations.append(f"     * Build a mini-project using {skill.title()}")
                elif skill in ['sql', 'postgresql', 'mysql', 'mongodb']:
                    recommendations.append(f"   - {skill.upper()}:")
                    recommendations.append(f"     * Practice daily on LeetCode or HackerRank")
                    recommendations.append(f"     * Learn to write complex queries and joins")
                elif skill in ['docker', 'kubernetes', 'aws', 'azure', 'gcp']:
                    recommendations.append(f"   - {skill.upper()}:")
                    recommendations.append(f"     * Use free tier services for hands-on practice")
                    recommendations.append(f"     * Deploy a sample application")
                elif skill in ['git', 'github']:
                    recommendations.append(f"   - {skill.title()}:")
                    recommendations.append(f"     * Learn version control basics")
                    recommendations.append(f"     * Contribute to open source projects")
                elif skill in ['react', 'angular', 'vue', 'django', 'flask', 'spring']:
                    recommendations.append(f"   - {skill.title()}:")
                    recommendations.append(f"     * Build a portfolio project using this framework")
                    recommendations.append(f"     * Follow official tutorials and documentation")
                elif skill in ['rest api', 'graphql', 'microservices']:
                    recommendations.append(f"   - {skill.title()}:")
                    recommendations.append(f"     * Build a small API service")
                    recommendations.append(f"     * Document it using Swagger/OpenAPI")
                elif skill in ['agile', 'scrum', 'tdd']:
                    recommendations.append(f"   - {skill.title()}:")
                    recommendations.append(f"     * Learn the methodology and practice with a team")
                    recommendations.append(f"     * Get certified in Scrum or Agile")
                else:
                    recommendations.append(f"   - {skill.title()}:")
                    recommendations.append(f"     * Learn through tutorials and hands-on practice")
                    recommendations.append(f"     * Find resources online and build a project")
            
            recommendations.append("")
            
            # ================================================================
            # LEARNING PRIORITY
            # ================================================================
            recommendations.append("LEARNING PRIORITY PLAN:")
            
            backend_skills = ['python', 'java', 'c++', 'go', 'rust', 'sql', 'postgresql', 'mysql', 'mongodb']
            frontend_skills = ['javascript', 'html', 'css', 'react', 'angular', 'vue', 'typescript']
            devops_skills = ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'git', 'github', 'ci/cd', 'jenkins', 'linux']
            
            missing_backend = [s for s in top_missing if s in backend_skills]
            missing_frontend = [s for s in top_missing if s in frontend_skills]
            missing_devops = [s for s in top_missing if s in devops_skills]
            
            priority_num = 1
            if missing_backend:
                recommendations.append(f"   {priority_num}. Backend Skills: {', '.join(missing_backend[:3])}")
                priority_num += 1
            if missing_frontend:
                recommendations.append(f"   {priority_num}. Frontend Skills: {', '.join(missing_frontend[:3])}")
                priority_num += 1
            if missing_devops:
                recommendations.append(f"   {priority_num}. DevOps Skills: {', '.join(missing_devops[:3])}")
                priority_num += 1
            
            recommendations.append("")
        
        # ================================================================
        # SKILL COUNT
        # ================================================================
        if skills:
            skill_count = len(skills)
            if skill_count < 5:
                recommendations.append(f"SKILL COUNT: {skill_count} skills found (TARGET: 15+)")
                recommendations.append("   Your resume has very few skills.")
                recommendations.append("   Add more technical skills immediately.")
            elif skill_count < 10:
                recommendations.append(f"SKILL COUNT: {skill_count} skills found (TARGET: 15+)")
                recommendations.append("   Your resume needs more skills.")
                recommendations.append("   Add 5-10 more technical skills.")
            elif skill_count < 15:
                recommendations.append(f"SKILL COUNT: {skill_count} skills found (TARGET: 15+)")
                recommendations.append("   Good skill count, but can still improve.")
                recommendations.append("   Add 2-5 more skills to reach 15.")
            else:
                recommendations.append(f"SKILL COUNT: {skill_count} skills found (TARGET: 15+)")
                recommendations.append("   Excellent skill count!")
            recommendations.append("")
        
        # ================================================================
        # CATEGORY-SPECIFIC RECOMMENDATIONS
        # ================================================================
        if skills:
            has_backend = any(s.lower() in ['python', 'java', 'node.js', 'django', 'flask', 'spring', 'c++', 'c#', 'go', 'rust'] for s in skills)
            has_frontend = any(s.lower() in ['html', 'css', 'javascript', 'react', 'angular', 'vue', 'typescript'] for s in skills)
            has_database = any(s.lower() in ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle'] for s in skills)
            has_devops = any(s.lower() in ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'jenkins', 'git', 'linux'] for s in skills)
            has_testing = any(s.lower() in ['pytest', 'unittest', 'selenium', 'junit', 'testng'] for s in skills)
            
            missing_categories = []
            if not has_backend:
                missing_categories.append("Backend Development")
            if not has_frontend:
                missing_categories.append("Frontend Development")
            if not has_database:
                missing_categories.append("Database")
            if not has_devops:
                missing_categories.append("DevOps")
            if not has_testing:
                missing_categories.append("Testing")
            
            if missing_categories:
                recommendations.append("MISSING SKILL CATEGORIES:")
                for cat in missing_categories:
                    recommendations.append(f"   - {cat}")
                recommendations.append("")
        
        # ================================================================
        # RESUME IMPROVEMENT TIPS - STRICT
        # ================================================================
        recommendations.append("RESUME IMPROVEMENT CHECKLIST:")
        
        if formatting < 15:
            recommendations.append("   [ ] Use clear section headers (Experience, Education, Skills, Projects)")
            recommendations.append("   [ ] Use bullet points for better readability")
            recommendations.append("   [ ] Include contact information (email, phone, LinkedIn)")
            recommendations.append("   [ ] Use consistent formatting throughout")
        
        if content_quality < 18:
            recommendations.append("   [ ] Add quantifiable metrics (e.g., 'Improved performance by 30%')")
            recommendations.append("   [ ] Use strong action verbs: developed, built, designed, implemented")
            recommendations.append("   [ ] Include specific results and outcomes")
        
        if experience < 15:
            recommendations.append("   [ ] Expand work experience section with specific responsibilities")
            recommendations.append("   [ ] Include years of experience clearly")
            recommendations.append("   [ ] Highlight achievements in each role")
        
        if projects < 11:
            recommendations.append("   [ ] Add a projects section with deployed applications")
            recommendations.append("   [ ] Include GitHub links to your projects")
            recommendations.append("   [ ] Describe technologies used in each project")
        
        if certifications < 9:
            recommendations.append("   [ ] Include relevant certifications (AWS, Azure, Google, Scrum Master)")
            recommendations.append("   [ ] Add completion dates for certifications")
        
        if education < 11:
            recommendations.append("   [ ] Include relevant coursework")
            recommendations.append("   [ ] Add GPA if 3.5 or higher")
        
        recommendations.append("")
        
        # ================================================================
        # FINAL SUMMARY
        # ================================================================
        recommendations.append("=" * 60)
        recommendations.append("FINAL SUMMARY")
        recommendations.append("=" * 60)
        
        if total_ats < 40:
            recommendations.append("   Your resume needs MAJOR improvements.")
            recommendations.append("   Focus on ALL recommendations above.")
        elif total_ats < 60:
            recommendations.append("   Your resume needs SIGNIFICANT improvements.")
            recommendations.append("   Focus on critical issues first.")
        elif total_ats < 75:
            recommendations.append("   Your resume needs MODERATE improvements.")
            recommendations.append("   Focus on missing skills and keyword optimization.")
        elif total_ats < 90:
            recommendations.append("   Your resume needs MINOR improvements.")
            recommendations.append("   Fine-tune the areas with low scores.")
        else:
            recommendations.append("   Your resume is EXCELLENT!")
            recommendations.append("   Maintain this quality for all applications.")
        
        recommendations.append("")
        recommendations.append("TARGET: Aim for 85+ ATS score for best results.")
        
        return recommendations[:30]  # Limit to 30 recommendations