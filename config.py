import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/Zzzze/skillgap-aipro/skillgap.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    REPORT_FOLDER = os.getenv('REPORT_FOLDER', 'reports')
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # ML Configuration
    TFIDF_MAX_FEATURES = 5000
    SIMILARITY_THRESHOLD = 0.3
    
    # ATS Configuration
    ATS_KEYWORDS = ['python', 'sql', 'git', 'docker', 'aws', 'javascript', 'java', 'rest api', 'linux']
    
    # Report Configuration
    REPORT_LOGO = None
    
class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_ECHO = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Skill Synonyms for better matching
SKILL_SYNONYMS = {
    # Programming Languages
    'python': ['python3', 'python 3', 'py', 'python programming'],
    'javascript': ['js', 'javascript', 'es6', 'ecmascript'],
    'java': ['java', 'java 8', 'java 11', 'j2ee'],
    'c++': ['cpp', 'c plus plus', 'cxx'],
    'c#': ['csharp', 'c sharp'],
    'ruby': ['ruby', 'ruby on rails'],
    'php': ['php', 'php7', 'php8'],
    'typescript': ['ts', 'typescript', 'type script'],
    
    # Frameworks
    'react': ['reactjs', 'react.js', 'react js', 'react native'],
    'angular': ['angularjs', 'angular.js', 'angular 2+', 'angular 2', 'angular 4', 'angular 8'],
    'vue': ['vuejs', 'vue.js', 'vue js', 'vuetify'],
    'django': ['django', 'django rest', 'django rest framework'],
    'flask': ['flask', 'flask api'],
    'fastapi': ['fast api', 'fastapi'],
    'spring': ['spring boot', 'spring framework', 'spring mvc', 'springcloud'],
    'node.js': ['nodejs', 'node js', 'node'],
    'express': ['expressjs', 'express.js', 'express js'],
    
    # Data Science
    'machine learning': ['ml', 'machine learning', 'ai', 'artificial intelligence'],
    'deep learning': ['dl', 'deep learning', 'neural networks'],
    'nlp': ['natural language processing', 'npl', 'natural language'],
    'computer vision': ['cv', 'vision', 'image processing'],
    'pandas': ['pandas', 'pd', 'python pandas'],
    'numpy': ['numpy', 'np', 'python numpy'],
    'scikit-learn': ['sklearn', 'scikit learn', 'scikit'],
    'tensorflow': ['tf', 'tensor flow', 'tensorflow'],
    'pytorch': ['pt', 'torch', 'pytorch'],
    
    # Databases
    'sql': ['sql', 'structured query language', 'mysql', 'postgresql', 'postgres'],
    'postgresql': ['postgres', 'postgre', 'pg', 'psql'],
    'mysql': ['mysql', 'my sql', 'mariadb'],
    'mongodb': ['mongo', 'mongodb', 'document db'],
    'redis': ['redis', 'redis cache'],
    'elasticsearch': ['elastic', 'es', 'elastic search'],
    'dynamodb': ['dynamo', 'dynamodb', 'aws dynamodb'],
    
    # DevOps
    'docker': ['docker', 'docker container', 'containerization'],
    'kubernetes': ['k8s', 'kubernetes', 'kube'],
    'aws': ['amazon web services', 'aws', 'ec2', 's3', 'lambda'],
    'azure': ['microsoft azure', 'azure', 'azure cloud'],
    'gcp': ['google cloud', 'gcp', 'google cloud platform'],
    'git': ['git', 'github', 'gitlab', 'bitbucket'],
    'linux': ['linux', 'unix', 'bash'],
    'jenkins': ['jenkins', 'jenkins ci', 'ci/cd'],
    
    # General
    'rest api': ['restful api', 'rest', 'restful', 'api', 'restapis'],
    'graphql': ['graphql', 'gql', 'graph ql'],
    'microservices': ['microservices', 'micro service', 'micro-service'],
}