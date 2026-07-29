# SkillGap AI Pro

## Description
SkillGap AI Pro is a Flask-based web application that helps job seekers evaluate their resumes, identify skill gaps, and improve their chances of landing target roles. The platform combines resume parsing, ATS scoring, job matching, recommendations, and report generation in a simple dashboard.

## Features
- Upload and parse resumes in PDF or DOCX format
- Analyze resume alignment with job descriptions
- Generate ATS compatibility scores and keyword insights
- Recommend missing skills and career growth actions
- Create downloadable reports and career roadmaps
- Track analysis history

## Screenshots

![Home dashboard](static/screenshots/skillgap-dashboard.JPG)
![Home dashboard](static/screenshots/skillgap-dashboard2.JPG)
![Resume analysis view](static/screenshots/skillgap-resumeupload.JPG)
![Report and insights view](static/screenshots/skillgap-skillanalyzer.JPG)
![Career Path](static/screenshots/skillgap-careerpath.JPG)
![Career Path](static/screenshots/skillgap-careerpath2.JPG)
![History](static/screenshots/skillgap-history.JPG)
![Report Generated](static/screenshots/skillgap-report.JPG)
![Report PDF](static/screenshots/skillgap-pdf.JPG)
![Report PDF](static/screenshots/skillgap-pdf2.JPG)


## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![ReportLab](https://img.shields.io/badge/ReportLab-PDF-red?style=for-the-badge)

## What I Learned

Building SkillGap AI Pro strengthened my understanding of:

- Developing full-stack web applications with Flask and SQLAlchemy
- Processing and analyzing resume data using Python
- Implementing TF-IDF and cosine similarity for job matching
- Designing and integrating relational databases
- Generating PDF reports with ReportLab
- Building responsive interfaces with HTML, CSS, and JavaScript
- Writing clean, maintainable, and scalable code

## Installation
1. Clone the repository
2. Create and activate a virtual environment
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application
   ```bash
   python app.py
   ```

## Usage
1. Open the app in your browser at http://localhost:5000
2. Upload your resume
3. Select or enter a target job title
4. Review the match score, ATS score, and skill recommendations
5. Generate and download your report
