from datetime import datetime
from typing import Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from flask import current_app

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(50), default='user', nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password: str) -> None:
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def generate_access_token(self) -> str:
        """Generate JWT access token."""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'role': self.role,
            'exp': datetime.utcnow() + current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)
        }
        return jwt.encode(payload, current_app.config.get('JWT_SECRET_KEY'), algorithm='HS256')
    
    def generate_refresh_token(self) -> str:
        """Generate JWT refresh token."""
        payload = {
            'user_id': self.id,
            'type': 'refresh',
            'exp': datetime.utcnow() + current_app.config.get('JWT_REFRESH_TOKEN_EXPIRES', 86400)
        }
        return jwt.encode(payload, current_app.config.get('JWT_SECRET_KEY'), algorithm='HS256')
    
    @staticmethod
    def decode_token(token: str) -> dict:
        """Decode JWT token."""
        return jwt.decode(token, current_app.config.get('JWT_SECRET_KEY'), algorithms=['HS256'])
    
    def to_dict(self) -> dict:
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'