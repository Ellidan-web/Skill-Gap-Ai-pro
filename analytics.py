import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta
from models import AnalysisHistory

class AnalyticsEngine:
    def __init__(self):
        self.df = None
    
    def load_data(self, histories, jobs=None):
        if not histories:
            self.df = pd.DataFrame()
            return
        
        data = []
        for history in histories:
            data.append({
                'id': history.id,
                'resume_id': history.resume_id,
                'desired_job': history.desired_job or 'N/A',
                'match_score': history.match_score or 0,
                'ats_score': history.ats_score or 0,
                'confidence_score': history.confidence_score or 0,
                'similarity_score': history.similarity_score or 0,
                'created_at': history.created_at
            })
        self.df = pd.DataFrame(data)
    
    def get_dashboard_stats(self):
        if self.df is None or self.df.empty:
            return {
                'total_analyses': 0,
                'avg_match_score': 0,
                'highest_score': 0,
                'lowest_score': 0,
                'avg_ats_score': 0,
                'resume_upload_count': 0,
                'most_selected_job': 'N/A'
            }
        
        total = len(self.df)
        avg_match = round(self.df['match_score'].mean(), 2) if not self.df['match_score'].isna().all() else 0
        highest = round(self.df['match_score'].max(), 2) if not self.df['match_score'].isna().all() else 0
        lowest = round(self.df['match_score'].min(), 2) if not self.df['match_score'].isna().all() else 0
        avg_ats = round(self.df['ats_score'].mean(), 2) if not self.df['ats_score'].isna().all() else 0
        
        most_selected = 'N/A'
        if not self.df.empty:
            mode_series = self.df['desired_job'].mode()
            if len(mode_series) > 0:
                most_selected = mode_series.iloc[0]
        
        return {
            'total_analyses': total,
            'avg_match_score': avg_match,
            'highest_score': highest,
            'lowest_score': lowest,
            'avg_ats_score': avg_ats,
            'resume_upload_count': self.df['resume_id'].nunique() if not self.df.empty else 0,
            'most_selected_job': most_selected
        }
    
    def get_match_history(self, limit=30):
        if self.df is None or self.df.empty:
            return []
        sorted_df = self.df.sort_values('created_at', ascending=True).tail(limit)
        result = []
        for _, row in sorted_df.iterrows():
            result.append({
                'date': row['created_at'].isoformat(),
                'match_score': row['match_score'],
                'ats_score': row['ats_score']
            })
        return result
    
    def get_resume_score_trend(self) -> List[Dict]:
        """Get resume score trend over time."""
        if self.df is None or self.df.empty:
            return []
        
        try:
            # Group by date
            self.df['date'] = pd.to_datetime(self.df['created_at']).dt.date
            daily_scores = self.df.groupby('date').agg({
                'match_score': 'mean',
                'ats_score': 'mean'
            }).reset_index()
            
            return [
                {
                    'date': row['date'].isoformat(),
                    'avg_match_score': round(row['match_score'], 2),
                    'avg_ats_score': round(row['ats_score'], 2)
                }
                for _, row in daily_scores.iterrows()
            ]
        except Exception as e:
            print(f"Error getting resume trend: {e}")
            return []
    
    def get_job_popularity(self):
        if self.df is None or self.df.empty:
            return []
        counts = self.df['desired_job'].value_counts().head(10)
        result = []
        for job, count in counts.items():
            result.append({'job': job, 'count': int(count)})
        return result
    
    def get_skill_distribution(self, histories: List[AnalysisHistory]) -> List[Dict]:
        """Get skill distribution from analysis histories."""
        if not histories:
            return []
        
        try:
            skill_counter = {}
            for history in histories:
                # Get skills from current_skills string
                skills_str = getattr(history, 'current_skills', '')
                if skills_str:
                    skills = [s.strip() for s in skills_str.split(',') if s.strip()]
                    for skill in skills:
                        skill_counter[skill] = skill_counter.get(skill, 0) + 1
            
            # Sort by count
            sorted_skills = sorted(skill_counter.items(), key=lambda x: x[1], reverse=True)
            
            return [
                {
                    'skill': skill,
                    'count': count
                }
                for skill, count in sorted_skills[:15]
            ]
        except Exception as e:
            print(f"Error getting skill distribution: {e}")
            return []
    
    def get_missing_skills_analysis(self, histories: List[AnalysisHistory]) -> List[Dict]:
        """Get most common missing skills."""
        if not histories:
            return []
        
        try:
            missing_counter = {}
            for history in histories:
                # Get missing skills from missing_skills string
                missing_str = getattr(history, 'missing_skills', '')
                if missing_str:
                    missing = [s.strip() for s in missing_str.split(',') if s.strip()]
                    for skill in missing:
                        missing_counter[skill] = missing_counter.get(skill, 0) + 1
            
            # Sort by count
            sorted_missing = sorted(missing_counter.items(), key=lambda x: x[1], reverse=True)
            
            return [
                {
                    'skill': skill,
                    'count': count
                }
                for skill, count in sorted_missing[:10]
            ]
        except Exception as e:
            print(f"Error getting missing skills: {e}")
            return []
    
    def get_ats_score_distribution(self, histories):
        if not histories:
            return []
        
        try:
            ranges = {
                'Excellent (80-100)': 0,
                'Good (60-79)': 0,
                'Fair (40-59)': 0,
                'Poor (0-39)': 0
            }
            
            for history in histories:
                score = history.ats_score or 0
                if score >= 80:
                    ranges['Excellent (80-100)'] += 1
                elif score >= 60:
                    ranges['Good (60-79)'] += 1
                elif score >= 40:
                    ranges['Fair (40-59)'] += 1
                else:
                    ranges['Poor (0-39)'] += 1
            
            result = []
            for range_name, count in ranges.items():
                if count > 0:
                    result.append({
                        'range': range_name,
                        'count': count
                    })
            return result
        except Exception as e:
            print(f"Error getting ATS distribution: {e}")
            return []
    
    def get_recent_analyses(self, histories, limit=10):
        if not histories:
            return []
        sorted_h = sorted(histories, key=lambda x: x.created_at, reverse=True)[:limit]
        result = []
        for h in sorted_h:
            result.append({
                'id': h.id,
                'desired_job': h.desired_job,
                'match_score': h.match_score,
                'ats_score': h.ats_score,
                'created_at': h.created_at.isoformat() if h.created_at else None
            })
        return result
    
    def get_trending_skills(self, histories, days=30):
        return []