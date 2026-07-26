import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
import json

class ReportGenerator:
    """Generate PDF reports for resume analysis."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()
    
    def _add_custom_styles(self):
        """Add custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'),
            alignment=TA_CENTER,
            spaceAfter=30
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1E293B'),
            spaceAfter=12,
            spaceBefore=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#334155'),
            spaceAfter=6
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSmall',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#64748B'),
            spaceAfter=4
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBullet',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#334155'),
            leftIndent=20,
            spaceAfter=4
        ))
    
    def generate_report(self, data: dict) -> str:
        """Generate a PDF report."""
        # Create filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{timestamp}.pdf"
        filepath = os.path.join('reports', filename)
        
        # Create document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph("SkillGap AI Pro - Resume Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.25 * inch))
        
        # Date
        story.append(Paragraph(f"Generated: {data.get('generated_date', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}", self.styles['CustomSmall']))
        story.append(Spacer(1, 0.25 * inch))
        
        # Resume Summary
        story.append(Paragraph("Resume Summary", self.styles['CustomHeading']))
        resume_data = data.get('resume', {})
        story.append(Paragraph(f"<b>Candidate:</b> {resume_data.get('candidate_name', 'N/A')}", self.styles['CustomBody']))
        story.append(Paragraph(f"<b>Email:</b> {resume_data.get('email', 'N/A')}", self.styles['CustomBody']))
        story.append(Paragraph(f"<b>Phone:</b> {resume_data.get('phone', 'N/A')}", self.styles['CustomBody']))
        
        skills = resume_data.get('skills', [])
        if skills:
            skills_text = ', '.join(skills[:15])
            if len(skills) > 15:
                skills_text += f" and {len(skills) - 15} more"
            story.append(Paragraph(f"<b>Skills Found:</b> {skills_text}", self.styles['CustomBody']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Analysis Results
        analysis = data.get('analysis', {})
        story.append(Paragraph("Analysis Results", self.styles['CustomHeading']))
        
        # Create results table
        results_data = [
            ['Metric', 'Score'],
            ['Match Percentage', f"{analysis.get('match_score', 0):.1f}%"],
            ['ATS Score', f"{analysis.get('ats_score', 0):.1f}"],
            ['Confidence Score', f"{analysis.get('confidence_score', 0):.1f}%"],
            ['Similarity Score', f"{analysis.get('similarity_score', 0):.1f}%"]
        ]
        
        results_table = Table(results_data, colWidths=[3*inch, 2*inch])
        results_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        story.append(results_table)
        story.append(Spacer(1, 0.2 * inch))
        
        # Skill Analysis
        story.append(Paragraph("Skill Analysis", self.styles['CustomHeading']))
        
        missing_skills = analysis.get('missing_skills', [])
        matched_skills = analysis.get('current_skills', [])
        extra_skills = analysis.get('extra_skills', [])
        
        if missing_skills:
            story.append(Paragraph(f"<b>Missing Skills ({len(missing_skills)}):</b>", self.styles['CustomBody']))
            story.append(Paragraph(', '.join(missing_skills[:20]), self.styles['CustomBody']))
        else:
            story.append(Paragraph("<b>Missing Skills:</b> None! Great job!", self.styles['CustomBody']))
        
        story.append(Spacer(1, 0.1 * inch))
        
        if matched_skills:
            story.append(Paragraph(f"<b>Matched Skills ({len(matched_skills)}):</b>", self.styles['CustomBody']))
            matched_text = ', '.join(matched_skills[:20])
            if len(matched_skills) > 20:
                matched_text += f" and {len(matched_skills) - 20} more"
            story.append(Paragraph(matched_text, self.styles['CustomBody']))
        
        if extra_skills and len(extra_skills) > 0:
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph(f"<b>Extra Skills ({len(extra_skills)}):</b>", self.styles['CustomBody']))
            story.append(Paragraph(', '.join(extra_skills[:10]), self.styles['CustomBody']))
        
        story.append(Spacer(1, 0.2 * inch))
        
        # Job Recommendations
        recommendations = data.get('recommendations', [])
        if recommendations:
            story.append(Paragraph("Top Job Recommendations", self.styles['CustomHeading']))
            
            rec_data = [['Job Title', 'Match %', 'Confidence', 'Salary']]
            for rec in recommendations[:5]:
                rec_data.append([
                    rec.get('job_title', 'N/A'),
                    f"{rec.get('match_percentage', 0):.1f}%",
                    f"{rec.get('confidence', 0):.1f}%",
                    rec.get('salary', 'N/A')
                ])
            
            rec_table = Table(rec_data, colWidths=[2.2*inch, 1.2*inch, 1.2*inch, 1.4*inch])
            rec_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            story.append(rec_table)
            story.append(Spacer(1, 0.2 * inch))
        
        # ================================================================
        # RECOMMENDATIONS SECTION - ATS SCORE & MISSING SKILLS FIRST
        # ================================================================
        story.append(Paragraph("Recommendations", self.styles['CustomHeading']))
        
        # Get data
        ats_recommendations = analysis.get('ats_recommendations', [])
        missing_skills = analysis.get('missing_skills', [])
        ats_score = analysis.get('ats_score', 0)
        matched_skills = analysis.get('current_skills', [])
        
        if ats_recommendations and len(ats_recommendations) > 0:
            # Filter recommendations
            ats_related = []
            skill_gap_related = []
            other_recommendations = []
            
            for rec in ats_recommendations:
                rec_lower = rec.lower()
                if 'ats' in rec_lower or 'score' in rec_lower or 'critical' in rec_lower or 'warning' in rec_lower or 'breakdown' in rec_lower:
                    ats_related.append(rec)
                elif 'missing' in rec_lower or 'skill' in rec_lower or 'gap' in rec_lower or 'learn' in rec_lower or 'fill' in rec_lower:
                    skill_gap_related.append(rec)
                else:
                    other_recommendations.append(rec)
            
            # 1. ATS Score Analysis - FIRST
            if ats_related:
                story.append(Paragraph("ATS Score Analysis:", self.styles['CustomBody']))
                story.append(Spacer(1, 0.05 * inch))
                for rec in ats_related[:10]:
                    if rec.strip():
                        story.append(Paragraph(f"• {rec}", self.styles['CustomBullet']))
                story.append(Spacer(1, 0.1 * inch))
            
            # 2. Missing Skills / Skill Gaps - SECOND
            if missing_skills and len(missing_skills) > 0:
                story.append(Paragraph(f"Skill Gaps - Missing {len(missing_skills)} Skills:", self.styles['CustomBody']))
                story.append(Spacer(1, 0.05 * inch))
                story.append(Paragraph(f"Missing skills: {', '.join(missing_skills[:15])}", self.styles['CustomBody']))
                story.append(Spacer(1, 0.05 * inch))
                
                # Show learning recommendations for missing skills
                if skill_gap_related:
                    for rec in skill_gap_related[:10]:
                        if rec.strip():
                            story.append(Paragraph(f"• {rec}", self.styles['CustomBullet']))
                else:
                    # Generate learning recommendations for each missing skill
                    for skill in missing_skills[:8]:
                        story.append(Paragraph(f"• Learn {skill.title()} through online courses and hands-on practice", self.styles['CustomBullet']))
                story.append(Spacer(1, 0.1 * inch))
            
            # 3. Other Recommendations - THIRD
            if other_recommendations:
                story.append(Paragraph("Additional Recommendations:", self.styles['CustomBody']))
                story.append(Spacer(1, 0.05 * inch))
                for rec in other_recommendations[:5]:
                    if rec.strip():
                        story.append(Paragraph(f"• {rec}", self.styles['CustomBullet']))
        
        else:
            # Fallback - Show ATS score and missing skills first
            story.append(Paragraph(f"ATS Score: {ats_score}/100", self.styles['CustomBody']))
            story.append(Spacer(1, 0.05 * inch))
            
            if ats_score < 60:
                story.append(Paragraph("Your ATS score is low. Focus on improving the following areas:", self.styles['CustomBody']))
                story.append(Spacer(1, 0.05 * inch))
            
            if missing_skills and len(missing_skills) > 0:
                story.append(Paragraph(f"Missing Skills ({len(missing_skills)}):", self.styles['CustomBody']))
                story.append(Paragraph(', '.join(missing_skills[:15]), self.styles['CustomBody']))
                story.append(Spacer(1, 0.05 * inch))
                story.append(Paragraph("Recommendations to fill these gaps:", self.styles['CustomBody']))
                
                for skill in missing_skills[:8]:
                    story.append(Paragraph(f"• Learn {skill.title()} through online courses and practice", self.styles['CustomBullet']))
            else:
                story.append(Paragraph("No missing skills found. Great job!", self.styles['CustomBody']))
            
            story.append(Spacer(1, 0.1 * inch))
            story.append(Paragraph("General Resume Tips:", self.styles['CustomBody']))
            general_tips = [
                "Add quantifiable metrics (e.g., 'Improved performance by 30%')",
                "Include specific technologies and tools used in each project",
                "Add links to GitHub, portfolio, or LinkedIn profile",
                "Tailor your resume for each job application",
                "Use strong action verbs: developed, built, designed, implemented"
            ]
            for tip in general_tips:
                story.append(Paragraph(f"• {tip}", self.styles['CustomBullet']))
        
        story.append(Spacer(1, 0.2 * inch))
        
        # Additional Tips Section
        story.append(Paragraph("Quick Tips for Job Applications", self.styles['CustomHeading']))
        quick_tips = [
            "Research the company and role before applying",
            "Customize your resume for each job application",
            "Practice common technical interview questions",
            "Build a portfolio of personal projects",
            "Network with professionals in your target field",
            "Follow up after interviews with thank-you notes"
        ]
        for tip in quick_tips:
            story.append(Paragraph(f"• {tip}", self.styles['CustomBullet']))
        
        story.append(Spacer(1, 0.2 * inch))
        
        # Footer
        story.append(Paragraph("---", self.styles['CustomBody']))
        story.append(Paragraph("Generated by SkillGap AI Pro", self.styles['CustomSmall']))
        story.append(Paragraph("https://skillgap-ai-pro.com", self.styles['CustomSmall']))
        
        # Build PDF
        doc.build(story)
        
        return filepath

    def generate_summary_report(self, resume_data: dict, analysis_data: dict) -> str:
        """Generate a summary report."""
        return self.generate_report({
            'resume': resume_data,
            'analysis': analysis_data,
            'generated_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })