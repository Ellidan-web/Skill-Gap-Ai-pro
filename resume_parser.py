import re
import os
import io
import magic
import pdfplumber
import docx
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class ResumeParser:
    """Parse resume files and extract text and structured information."""
    
    def __init__(self):
        self.skill_patterns = self._compile_skill_patterns()
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.phone_pattern = re.compile(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        self.name_pattern = re.compile(r'^[A-Z][a-z]+\s+[A-Z][a-z]+')
        
    def _compile_skill_patterns(self) -> Dict[str, List[str]]:
        """Compile skill patterns for extraction."""
        # Common technical skills
        programming_languages = [
            'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 
            'kotlin', 'golang', 'rust', 'typescript', 'scala', 'perl', 'r', 'matlab'
        ]
        frameworks = [
            'django', 'flask', 'fastapi', 'spring', 'spring boot', 'node.js', 'express',
            'react', 'vue', 'angular', 'laravel', 'symfony', 'rails', 'asp.net',
            'react native', 'flutter', 'tensorflow', 'pytorch', 'scikit-learn'
        ]
        databases = [
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
            'firebase', 'cassandra', 'dynamodb', 'oracle', 'mariadb'
        ]
        devops = [
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux', 'git', 'jenkins',
            'ansible', 'terraform', 'prometheus', 'grafana', 'nginx', 'ci/cd'
        ]
        data_science = [
            'pandas', 'numpy', 'scikit-learn', 'opencv', 'nltk', 'spacy',
            'machine learning', 'deep learning', 'nlp', 'computer vision'
        ]
        development = [
            'rest api', 'graphql', 'microservices', 'html', 'css', 'agile',
            'scrum', 'jira', 'confluence', 'sql', 'nosql'
        ]
        
        return {
            'programming_languages': programming_languages,
            'frameworks': frameworks,
            'databases': databases,
            'devops': devops,
            'data_science': data_science,
            'development': development
        }
    
    def parse_resume(self, file_data: bytes, filename: str) -> Dict:
        """Parse resume from file data."""
        # Determine file type
        file_extension = filename.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            text = self._parse_pdf(file_data)
        elif file_extension == 'docx':
            text = self._parse_docx(file_data)
        elif file_extension == 'txt':
            text = self._parse_txt(file_data)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        # Extract structured data
        candidate_name = self._extract_name(text)
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        education = self._extract_education(text)
        experience = self._extract_experience(text)
        skills = self._extract_skills(text)
        
        return {
            'text': text,
            'candidate_name': candidate_name,
            'email': email,
            'phone': phone,
            'education': education,
            'experience': experience,
            'skills': skills,
            'filename': filename
        }
    
    def _parse_pdf(self, file_data: bytes) -> str:
        """Parse PDF file and extract text."""
        try:
            with io.BytesIO(file_data) as pdf_file:
                with pdfplumber.open(pdf_file) as pdf:
                    text = ''
                    for page in pdf.pages:
                        page_text = page.extract_text() or ''
                        text += page_text + '\n'
                    return text
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _parse_docx(self, file_data: bytes) -> str:
        """Parse DOCX file and extract text."""
        try:
            with io.BytesIO(file_data) as docx_file:
                doc = docx.Document(docx_file)
                text = ''
                for paragraph in doc.paragraphs:
                    text += paragraph.text + '\n'
                return text
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    def _parse_txt(self, file_data: bytes) -> str:
        """Parse TXT file and extract text."""
        try:
            return file_data.decode('utf-8', errors='ignore')
        except Exception as e:
            raise Exception(f"Error parsing TXT: {str(e)}")
    
    def _extract_name(self, text: str) -> Optional[str]:
        """Extract candidate name from text."""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line) < 50:
                match = self.name_pattern.match(line)
                if match:
                    return match.group()
        return None
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email from text."""
        match = self.email_pattern.search(text)
        return match.group() if match else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text."""
        match = self.phone_pattern.search(text)
        return match.group() if match else None
    
    def _extract_education(self, text: str) -> str:
        """Extract education information."""
        education_keywords = [
            'education', 'academic', 'degree', 'university', 'college',
            'bachelor', 'master', 'phd', 'bsc', 'msc', 'bs', 'ba', 'mba'
        ]
        
        education_lines = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                # Include this line and the next 3 lines
                for j in range(i, min(i + 3, len(lines))):
                    education_lines.append(lines[j].strip())
                education_lines.append('---')
        
        return '\n'.join(education_lines[:50])  # Limit to prevent too much text
    
    def _extract_experience(self, text: str) -> str:
        """Extract work experience."""
        experience_keywords = [
            'experience', 'work', 'employment', 'position', 'role',
            'responsibilities', 'achievements', 'projects'
        ]
        
        experience_lines = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in experience_keywords):
                for j in range(i, min(i + 5, len(lines))):
                    experience_lines.append(lines[j].strip())
                experience_lines.append('---')
        
        return '\n'.join(experience_lines[:100])  # Limit to prevent too much text
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text using keyword matching."""
        from config import SKILL_SYNONYMS
        text_lower = text.lower()
        found_skills = set()
        
        # Build skill mapping: skill_name -> normalized_skill
        skill_to_normalized = {}
        for normalized_skill, variations in SKILL_SYNONYMS.items():
            skill_to_normalized[normalized_skill] = normalized_skill
            for variation in variations:
                skill_to_normalized[variation] = normalized_skill
        
        # Check for skills in text
        for category, skills in self.skill_patterns.items():
            for skill in skills:
                pattern = r'\b' + re.escape(skill) + r'\b'
                if re.search(pattern, text_lower):
                    # Check if this skill has a normalized version
                    normalized = skill_to_normalized.get(skill.lower(), skill)
                    found_skills.add(normalized)
        
        # Check for skill variations from synonyms
        for normalized_skill, variations in SKILL_SYNONYMS.items():
            for variation in variations:
                if re.search(r'\b' + re.escape(variation) + r'\b', text_lower):
                    found_skills.add(normalized_skill)
        
        # Extract additional skills from common patterns
        skill_section_patterns = [
            r'(?:skills|technologies|tools|tech stack)[:]\s*([^\n]+)',
            r'(?:skills|technologies|tools|tech stack)\s+([^\n]+)',
        ]
        
        for pattern in skill_section_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                # Split by common delimiters
                skills = re.split(r'[,;|]|\s+and\s+|\s*•\s*', match)
                for skill in skills:
                    skill = skill.strip()
                    if skill and len(skill) > 2:
                        found_skills.add(skill.lower())
        
        return sorted(list(found_skills))

def validate_file(file_data: bytes, filename: str) -> Tuple[bool, str]:
    """Validate uploaded file."""
    # Check file size
    if len(file_data) > 16 * 1024 * 1024:  # 16MB
        return False, "File size exceeds 16MB limit"
    
    # Check file extension
    allowed_extensions = {'pdf', 'docx', 'txt'}
    file_extension = filename.split('.')[-1].lower()
    
    if file_extension not in allowed_extensions:
        return False, f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
    
    # Check MIME type
    mime = magic.from_buffer(file_data, mime=True)
    allowed_mimes = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'text/plain'
    }
    
    if mime not in allowed_mimes:
        return False, f"Invalid file format: {mime}"
    
    return True, "File validated successfully"