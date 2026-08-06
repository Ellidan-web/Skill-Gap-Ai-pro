from typing import Optional, Dict, Any
from datetime import datetime
from src.domain.models.user import User, db
from src.core.exceptions import ValidationError, AuthenticationError, ConflictError
from src.core.logging import get_logger

logger = get_logger(__name__)


class AuthService:
    """Service for authentication operations."""
    
    def register(self, email: str, password: str, full_name: Optional[str] = None) -> Dict[str, Any]:
        """Register a new user."""
        
        # Validate email
        if not email or '@' not in email:
            raise ValidationError('Valid email is required')
        
        # Validate password
        if not password or len(password) < 8:
            raise ValidationError('Password must be at least 8 characters')
        
        # Check if user exists
        existing = User.query.filter_by(email=email.lower()).first()
        if existing:
            raise ConflictError('User with this email already exists')
        
        # Create user
        user = User(
            email=email.lower(),
            full_name=full_name,
            role='user'
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f"User registered: {email}")
        
        return {
            'user': user.to_dict(),
            'access_token': user.generate_access_token(),
            'refresh_token': user.generate_refresh_token()
        }
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return tokens."""
        
        # Find user
        user = User.query.filter_by(email=email.lower()).first()
        if not user:
            raise AuthenticationError('Invalid email or password')
        
        # Verify password
        if not user.verify_password(password):
            raise AuthenticationError('Invalid email or password')
        
        # Check if active
        if not user.is_active:
            raise AuthenticationError('Account is disabled')
        
        logger.info(f"User logged in: {email}")
        
        return {
            'user': user.to_dict(),
            'access_token': user.generate_access_token(),
            'refresh_token': user.generate_refresh_token()
        }
    
    def refresh_token(self, refresh_token: str) -> Dict[str, str]:
        """Refresh access token using refresh token."""
        
        try:
            payload = User.decode_token(refresh_token)
            if payload.get('type') != 'refresh':
                raise AuthenticationError('Invalid token type')
            
            user = User.query.get(payload.get('user_id'))
            if not user or not user.is_active:
                raise AuthenticationError('Invalid or expired token')
            
            return {
                'access_token': user.generate_access_token()
            }
        except Exception as e:
            logger.warning(f"Token refresh failed: {str(e)}")
            raise AuthenticationError('Invalid or expired token')
    
    def logout(self, user_id: int) -> None:
        """Logout user (placeholder for token blacklisting)."""
        # Note: In production, add token to blacklist in Redis
        logger.info(f"User logged out: {user_id}")