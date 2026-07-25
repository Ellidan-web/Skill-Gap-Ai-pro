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
        'pool_recycle':3600,
        'pool_pre_ping': True,
    }

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
REPORT_FOLDER = os.getenv('REPORT_FOLDER','reports')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH',16*1024*1024))

TFIDF_MAX_FEATURES = 5000
SIMILARITY_THRESHOLD = 0.3

ATS_KEYWORDS = ['python', 'sql', 'git', 'docker', 'aws', 'javascript', 'java', 'rest api', 'linux']

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