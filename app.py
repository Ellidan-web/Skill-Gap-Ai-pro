from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
import tempfile
from datetime import datetime
from database import db, init_db, get_db_manager
from config import config
from models import (
    Job, Resume, ResumeSkill, AnalysisHistory, Favorite,
    Roadmap, CareerTip, Recommendation, SkillTag
)
from resume_parser import ResumeParser, validate_file
from ml_engine import MLEngine
from ats_checker import ATSChecker
from recommendation_engine import RecommendationEngine
from analytics import AnalyticsEngine
from roadmap import RoadmapGenerator
from report_generator import ReportGenerator
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['development'])
CORS(app)

# Initialize database
init_db(app)

# Initialize engines
ml_engine = MLEngine()
ats_checker = ATSChecker()
recommendation_engine = RecommendationEngine()
analytics_engine = AnalyticsEngine()  # Make sure this exists
roadmap_generator = RoadmapGenerator()
report_generator = ReportGenerator()
resume_parser = ResumeParser()

# Ensure upload and report directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['REPORT_FOLDER'], exist_ok=True)

# ============================================================================
# Helper Functions
# ============================================================================

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file):
    """Save uploaded file and return file path."""
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)
    return filepath

# ============================================================================
# Frontend Routes
# ============================================================================

@app.route('/')
def index():
    """Serve main application page."""
    return render_template('index.html')

# ============================================================================
# REST API Routes
# ============================================================================

# Job Routes
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs."""
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = Job.query
    
    if category:
        query = query.filter(Job.category == category)
    
    if search:
        query = query.filter(Job.title.contains(search) | Job.description.contains(search))
    
    jobs = query.all()
    return jsonify([job.to_dict() for job in jobs])

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get job by ID."""
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job.to_dict())

# Resume Routes
@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and parse resume."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Read file data
        file_data = file.read()
        
        # Validate file
        is_valid, message = validate_file(file_data, file.filename)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Parse resume
        parsed_data = resume_parser.parse_resume(file_data, file.filename)
        
        # Save to database
        resume = Resume(
            filename=file.filename,
            resume_text=parsed_data['text'],
            candidate_name=parsed_data['candidate_name'],
            email=parsed_data['email'],
            phone=parsed_data['phone'],
            education=parsed_data['education'],
            experience=parsed_data['experience']
        )
        db.session.add(resume)
        db.session.flush()
        
        # Save skills
        for skill in parsed_data['skills']:
            # Determine skill category
            category = 'General'
            for cat, skills in resume_parser.skill_patterns.items():
                if skill.lower() in skills:
                    category = cat.replace('_', ' ').title()
                    break
            
            resume_skill = ResumeSkill(
                resume_id=resume.id,
                skill=skill,
                category=category
            )
            db.session.add(resume_skill)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'resume_id': resume.id,
            'data': parsed_data
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/resume/<int:resume_id>', methods=['GET'])
def get_resume(resume_id):
    """Get resume by ID."""
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    return jsonify(resume.to_dict())

@app.route('/api/resume-score/<int:resume_id>', methods=['GET'])
def get_resume_score(resume_id):
    """Get ATS score for resume."""
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    skills = resume.get_skills_list()
    ats_result = ats_checker.calculate_ats_score(resume.resume_text, skills)
    
    return jsonify({
        'resume_id': resume_id,
        'ats_score': ats_result['score'],
        'breakdown': ats_result['breakdown'],
        'recommendations': ats_result['recommendations'],
        'missing_keywords': ats_result['missing_keywords']
    })

# Analysis Routes
@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """Analyze resume against job requirements."""
    data = request.json
    resume_id = data.get('resume_id')
    desired_job = data.get('desired_job')
    
    if not resume_id or not desired_job:
        return jsonify({'error': 'Resume ID and desired job are required'}), 400
    
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    # Get job
    job = Job.query.filter(Job.title == desired_job).first()
    if not job:
        return jsonify({'error': f'Job "{desired_job}" not found'}), 404
    
    # Load job data into ML engine
    all_jobs = Job.query.all()
    ml_engine.load_job_data(all_jobs)
    
    # Calculate match
    skills = resume.get_skills_list()
    job_skills = job.get_skills_list()
    
    match_data = ml_engine.calculate_match_percentage(skills, job_skills)
    
    # Calculate similarity
    similarity = ml_engine.calculate_similarity(resume.resume_text, job.description or '')
    
    # Calculate ATS score
    ats_result = ats_checker.calculate_ats_score(resume.resume_text, skills)
    
    # Save analysis history
    history = AnalysisHistory(
        resume_id=resume_id,
        desired_job=desired_job,
        current_skills=','.join(skills),
        match_score=match_data['match_percentage'],
        ats_score=ats_result['score'],
        missing_skills=','.join(match_data['missing_skills']),
        recommended_skills=','.join(match_data['matched_skills']),
        confidence_score=min(100, (match_data['match_percentage'] * 0.7 + similarity * 30)),
        similarity_score=similarity * 100
    )
    db.session.add(history)
    db.session.commit()
    
    return jsonify({
        'analysis_id': history.id,
        'match_percentage': match_data['match_percentage'],
        'gap_percentage': match_data['gap_percentage'],
        'matched_skills': match_data['matched_skills'],
        'missing_skills': match_data['missing_skills'],
        'extra_skills': match_data['extra_skills'],
        'ats_score': ats_result['score'],
        'ats_breakdown': ats_result['breakdown'],
        'ats_recommendations': ats_result['recommendations'],
        'similarity_score': round(history.similarity_score, 2),
        'confidence_score': round(history.confidence_score, 2)
    })

# Recommendation Routes
@app.route('/api/job-ranking', methods=['POST'])
def rank_jobs():
    """Get job recommendations."""
    data = request.json
    resume_id = data.get('resume_id')
    
    if not resume_id:
        return jsonify({'error': 'Resume ID required'}), 400
    
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    jobs = Job.query.all()
    skills = resume.get_skills_list()
    
    recommendations = recommendation_engine.generate_recommendations(
        resume.resume_text, skills, jobs
    )
    
    # Save recommendations
    for rec in recommendations:
        job = Job.query.filter(Job.title == rec['job_title']).first()
        if job:
            recommendation = Recommendation(
                resume_id=resume_id,
                job_id=job.id,
                match_percentage=rec['match_percentage'],
                confidence=rec['confidence'],
                salary=rec['salary'],
                similarity_score=rec['confidence'] / 100
            )
            db.session.add(recommendation)
    
    db.session.commit()
    
    return jsonify(recommendations)

@app.route('/api/recommendations/<int:resume_id>', methods=['GET'])
def get_recommendations(resume_id):
    """Get saved recommendations."""
    recommendations = Recommendation.query.filter_by(resume_id=resume_id).all()
    return jsonify([rec.to_dict() for rec in recommendations])

# Skill Gap Routes
@app.route('/api/skill-gap/<int:resume_id>', methods=['GET'])
def get_skill_gap(resume_id):
    """Get skill gap analysis."""
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    job_title = request.args.get('job')
    if not job_title:
        return jsonify({'error': 'Job title required'}), 400
    
    job = Job.query.filter(Job.title == job_title).first()
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    skills = resume.get_skills_list()
    job_skills = job.get_skills_list()
    
    match_data = ml_engine.calculate_match_percentage(skills, job_skills)
    
    # Get recommendations for missing skills
    skill_recommendations = ml_engine.get_skill_recommendations(
        match_data['missing_skills']
    )
    
    return jsonify({
        'matched_skills': match_data['matched_skills'],
        'missing_skills': match_data['missing_skills'],
        'extra_skills': match_data['extra_skills'],
        'required_skills': job_skills[:20],
        'gap_percentage': match_data['gap_percentage'],
        'match_percentage': match_data['match_percentage'],
        'skill_recommendations': skill_recommendations
    })

# History Routes
@app.route('/api/history', methods=['GET'])
def get_history():
    """Get analysis history."""
    limit = request.args.get('limit', default=50, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    histories = AnalysisHistory.query.order_by(
        AnalysisHistory.created_at.desc()
    ).limit(limit).offset(offset).all()
    
    return jsonify([h.to_dict() for h in histories])

@app.route('/api/history/<int:history_id>', methods=['DELETE'])
def delete_history(history_id):
    """Delete analysis history."""
    history = AnalysisHistory.query.get(history_id)
    if not history:
        return jsonify({'error': 'History not found'}), 404
    
    db.session.delete(history)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics."""
    try:
        from models import AnalysisHistory, Job, Resume
        
        histories = AnalysisHistory.query.all()
        jobs = Job.query.all()
        resumes = Resume.query.all()
        
        # Load data into analytics engine
        analytics_engine.load_data(histories)
        
        # Get stats
        stats = analytics_engine.get_dashboard_stats()
        
        # Convert numpy types to Python types for JSON serialization
        stats['total_analyses'] = int(stats['total_analyses'])
        stats['avg_match_score'] = float(stats['avg_match_score'])
        stats['highest_score'] = float(stats['highest_score'])
        stats['lowest_score'] = float(stats['lowest_score'])
        stats['avg_ats_score'] = float(stats['avg_ats_score'])
        stats['resume_upload_count'] = int(stats['resume_upload_count'])
        stats['total_resumes'] = len(resumes)
        stats['total_jobs'] = len(jobs)
        
        # Get recent analyses
        stats['recent_analyses'] = analytics_engine.get_recent_analyses(histories, 5)
        
        return jsonify(stats)
    except Exception as e:
        print(f"Error in /api/stats: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'total_analyses': 0,
            'avg_match_score': 0,
            'highest_score': 0,
            'lowest_score': 0,
            'avg_ats_score': 0,
            'resume_upload_count': 0,
            'most_selected_job': 'N/A',
            'most_missing_skill': 'N/A',
            'trending_skill': 'N/A',
            'total_resumes': 0,
            'total_jobs': 0,
            'recent_analyses': []
        })

@app.route('/api/trending-skills', methods=['GET'])
def get_trending_skills():
    """Get trending skills."""
    histories = AnalysisHistory.query.all()
    trending = analytics_engine.get_trending_skills(histories)
    return jsonify(trending)


@app.route('/api/charts', methods=['GET'])
def get_chart_data():
    """Get chart data for dashboard."""
    try:
        histories = AnalysisHistory.query.all()
        
        # Initialize analytics engine with data
        analytics_engine.load_data(histories)
        
        # Get chart data with safe defaults
        return jsonify({
            'match_history': analytics_engine.get_match_history() or [],
            'resume_score_trend': analytics_engine.get_resume_score_trend() or [],
            'job_popularity': analytics_engine.get_job_popularity() or [],
            'skill_distribution': analytics_engine.get_skill_distribution(histories) or [],
            'missing_skills': analytics_engine.get_missing_skills_analysis(histories) or [],
            'ats_distribution': analytics_engine.get_ats_score_distribution(histories) or []
        })
    except Exception as e:
        print(f"Error in /api/charts: {e}")
        import traceback
        traceback.print_exc()
        # Return empty data instead of failing
        return jsonify({
            'match_history': [],
            'resume_score_trend': [],
            'job_popularity': [],
            'skill_distribution': [],
            'missing_skills': [],
            'ats_distribution': []
        })
@app.route('/api/roadmap/generate', methods=['POST'])
def generate_roadmap():
    """Generate personalized roadmap based on missing skills."""
    data = request.json
    resume_id = data.get('resume_id')
    job_title = data.get('job_title')
    
    if not resume_id or not job_title:
        return jsonify({'error': 'Resume ID and job title required'}), 400
    
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    job = Job.query.filter(Job.title == job_title).first()
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    skills = resume.get_skills_list()
    job_skills = job.get_skills_list()
    
    match_data = ml_engine.calculate_match_percentage(skills, job_skills)
    
    roadmap = roadmap_generator.generate_roadmap(
        job_title,
        match_data['missing_skills'],
        match_data['gap_percentage']
    )
    
    return jsonify(roadmap)

# ADD THIS NEW ROUTE RIGHT HERE ↓↓↓
@app.route('/api/roadmap/<job_title>', methods=['GET'])
def get_roadmap(job_title):
    """Get learning roadmap for a job."""
    from models import Roadmap
    from flask import jsonify
    
    # Debug print
    print(f"Looking for roadmap: {job_title}")
    
    # Try exact match first
    roadmaps = Roadmap.query.filter_by(job_title=job_title).order_by(
        Roadmap.priority, Roadmap.week
    ).all()
    
    print(f"Found {len(roadmaps)} roadmaps for exact match")
    
    # If no exact match, try case-insensitive
    if not roadmaps:
        roadmaps = Roadmap.query.filter(
            Roadmap.job_title.ilike(job_title)
        ).order_by(
            Roadmap.priority, Roadmap.week
        ).all()
        print(f"Found {len(roadmaps)} roadmaps for case-insensitive match")
    
    if not roadmaps:
        return jsonify({'error': 'Roadmap not found for this job'}), 404
    
    return jsonify([r.to_dict() for r in roadmaps])

# Career Tips Routes
@app.route('/api/career-tips', methods=['GET'])
def get_career_tips():
    """Get career tips."""
    category = request.args.get('category')
    limit = request.args.get('limit', default=10, type=int)
    
    query = CareerTip.query
    if category:
        query = query.filter(CareerTip.category == category)
    
    tips = query.order_by(CareerTip.priority).limit(limit).all()
    return jsonify([t.to_dict() for t in tips])

# Favorites Routes
@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    """Get favorites."""
    favorites = Favorite.query.order_by(Favorite.created_at.desc()).all()
    return jsonify([f.to_dict() for f in favorites])

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    """Add favorite job."""
    data = request.json
    job_title = data.get('job_title')
    job_id = data.get('job_id')
    
    if not job_title:
        return jsonify({'error': 'Job title required'}), 400
    
    # Check if already exists
    existing = Favorite.query.filter_by(job_title=job_title).first()
    if existing:
        return jsonify({'error': 'Already in favorites'}), 400
    
    favorite = Favorite(job_title=job_title, job_id=job_id)
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify(favorite.to_dict()), 201

@app.route('/api/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    """Delete favorite."""
    favorite = Favorite.query.get(favorite_id)
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
    
    db.session.delete(favorite)
    db.session.commit()
    
    return jsonify({'success': True})

# Report Routes
@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    """Generate PDF report."""
    data = request.json
    resume_id = data.get('resume_id')
    job_title = data.get('job_title')
    analysis_id = data.get('analysis_id')
    
    if not resume_id:
        return jsonify({'error': 'Resume ID required'}), 400
    
    resume = Resume.query.get(resume_id)
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404
    
    # Get analysis
    analysis = None
    if analysis_id:
        analysis = AnalysisHistory.query.get(analysis_id)
    elif job_title:
        analysis = AnalysisHistory.query.filter_by(
            resume_id=resume_id,
            desired_job=job_title
        ).order_by(AnalysisHistory.created_at.desc()).first()
    
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    # Get recommendations
    recommendations = Recommendation.query.filter_by(resume_id=resume_id).all()
    
    # Generate report
    report_data = {
        'resume': resume.to_dict(),
        'analysis': analysis.to_dict(),
        'recommendations': [r.to_dict() for r in recommendations[:5]],
        'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Generate PDF
    report_path = report_generator.generate_report(report_data)
    
    return jsonify({
        'report_url': f'/api/download-report/{os.path.basename(report_path)}',
        'report_path': report_path
    })

@app.route('/api/download-report/<filename>', methods=['GET'])
def download_report(filename):
    """Download generated report."""
    report_path = os.path.join(app.config['REPORT_FOLDER'], filename)
    if not os.path.exists(report_path):
        return jsonify({'error': 'Report not found'}), 404
    
    return send_file(report_path, as_attachment=True)

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)