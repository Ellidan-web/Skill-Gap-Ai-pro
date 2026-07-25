from database import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Job(db.Model):
    """Job model representing job roles and requirements."""
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    required_skills = Column(Text)  # Comma-separated skills
    salary = Column(String(50))
    difficulty = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommendations = relationship('Recommendation', backref='job', lazy=True)
    favorites = relationship('Favorite', backref='job', lazy=True)
    
    def get_skills_list(self):
        """Get list of required skills."""
        if self.required_skills:
            # Split by comma and clean each skill
            skills = []
            for s in self.required_skills.split(','):
                # Remove leading/trailing whitespace
                cleaned = s.strip()
                # Remove quotes if any
                cleaned = cleaned.strip('"\'')
                # Skip empty strings
                if cleaned and len(cleaned) > 0:
                    skills.append(cleaned)
            return skills
        return []
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'required_skills': self.required_skills,
            'salary': self.salary,
            'difficulty': self.difficulty
        }

class Resume(db.Model):
    """Resume model storing uploaded resume data."""
    __tablename__ = 'resumes'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    resume_text = Column(Text)
    candidate_name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    education = Column(Text)
    experience = Column(Text)
    upload_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    skills = relationship('ResumeSkill', backref='resume', lazy=True, cascade='all, delete-orphan')
    analyses = relationship('AnalysisHistory', backref='resume', lazy=True, cascade='all, delete-orphan')
    recommendations = relationship('Recommendation', backref='resume', lazy=True, cascade='all, delete-orphan')
    
    def get_skills_list(self):
        """Get list of extracted skills."""
        return [skill.skill for skill in self.skills]
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'filename': self.filename,
            'candidate_name': self.candidate_name,
            'email': self.email,
            'phone': self.phone,
            'education': self.education,
            'experience': self.experience,
            'skills': self.get_skills_list(),
            'upload_date': self.upload_date.isoformat() if self.upload_date else None
        }

class ResumeSkill(db.Model):
    """Resume skills model."""
    __tablename__ = 'resume_skills'
    
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    skill = Column(String(255), nullable=False, index=True)
    category = Column(String(100), default='General')
    created_at = Column(DateTime, default=datetime.utcnow)

class AnalysisHistory(db.Model):
    """Analysis history model storing all resume analyses."""
    __tablename__ = 'history'
    
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    desired_job = Column(String(255), nullable=False, index=True)
    current_skills = Column(Text)
    match_score = Column(Float)
    ats_score = Column(Float)
    missing_skills = Column(Text)
    recommended_skills = Column(Text)
    confidence_score = Column(Float)
    similarity_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def get_current_skills_list(self):
        """Get list of current skills."""
        if self.current_skills:
            return [s.strip() for s in self.current_skills.split(',') if s.strip()]
        return []
    
    def get_missing_skills_list(self):
        """Get list of missing skills."""
        if self.missing_skills:
            return [s.strip() for s in self.missing_skills.split(',') if s.strip()]
        return []
    
    def get_recommended_skills_list(self):
        """Get list of recommended skills."""
        if self.recommended_skills:
            return [s.strip() for s in self.recommended_skills.split(',') if s.strip()]
        return []
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'desired_job': self.desired_job,
            'current_skills': self.get_current_skills_list(),
            'match_score': self.match_score,
            'ats_score': self.ats_score,
            'missing_skills': self.get_missing_skills_list(),
            'recommended_skills': self.get_recommended_skills_list(),
            'confidence_score': self.confidence_score,
            'similarity_score': self.similarity_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Favorite(db.Model):
    """Favorite jobs model."""
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True)
    job_title = Column(String(255), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'job_title': self.job_title,
            'job_id': self.job_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Roadmap(db.Model):
    """Learning roadmap model."""
    __tablename__ = 'roadmaps'
    
    id = Column(Integer, primary_key=True)
    job_title = Column(String(255), nullable=False, index=True)
    week = Column(String(50), nullable=False)
    topic = Column(Text, nullable=False)
    description = Column(Text)
    priority = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'job_title': self.job_title,
            'week': self.week,
            'topic': self.topic,
            'description': self.description,
            'priority': self.priority
        }

class CareerTip(db.Model):
    """Career tips model."""
    __tablename__ = 'career_tips'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    tip = Column(Text, nullable=False)
    priority = Column(Integer, default=1)
    category = Column(String(100), default='General')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'tip': self.tip,
            'priority': self.priority,
            'category': self.category
        }

class Recommendation(db.Model):
    """Job recommendations model."""
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True)
    resume_id = Column(Integer, ForeignKey('resumes.id', ondelete='CASCADE'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    match_percentage = Column(Float)
    confidence = Column(Float)
    salary = Column(String(50))
    similarity_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'job_id': self.job_id,
            'job_title': self.job.title if self.job else None,
            'match_percentage': self.match_percentage,
            'confidence': self.confidence,
            'salary': self.salary,
            'similarity_score': self.similarity_score,
            'required_skills': self.job.get_skills_list() if self.job else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SkillTag(db.Model):
    """Skill tags for reference."""
    __tablename__ = 'skill_tags'
    
    id = Column(Integer, primary_key=True)
    skill = Column(String(255), nullable=False, unique=True, index=True)
    category = Column(String(100), nullable=False)
    proficiency = Column(String(50), default='Intermediate')
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'skill': self.skill,
            'category': self.category,
            'proficiency': self.proficiency
        }