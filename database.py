from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
import sqlite3

db = SQLAlchemy()

def init_db(app):
    """Initialize database with Flask app."""
    db.init_app(app)
    
    with app.app_context():
        # Ensure the instance directory exists for SQLite
        if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            # Handle relative paths
            if not os.path.isabs(db_path):
                db_path = os.path.join(app.root_path, db_path)
            # Create directory if it doesn't exist
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            print(f"Database will be created at: {db_path}")
        
        try:
            db.create_all()
            print("Database tables created successfully!")
        except Exception as e:
            print(f"Error creating database tables: {e}")
            raise
        
        # Import and run seeder
        try:
            from seed import seed_database
            seed_database()
        except Exception as e:
            print(f"Error seeding database: {e}")

def get_db_session():
    """Get database session."""
    return db.session

def get_engine(app):
    """Get database engine."""
    return db.engine

class DatabaseManager:
    """Database manager for handling connections and sessions."""
    
    def __init__(self, app=None):
        self.app = app
        self.engine = None
        self.session_factory = None
        self.Session = None
        
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app."""
        self.app = app
        self.engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            """Close session on app context teardown."""
            self.Session.remove()
    
    def get_session(self):
        """Get a database session."""
        return self.Session()
    
    def close_session(self, session):
        """Close a database session."""
        session.close()
    
    def execute_query(self, query, params=None):
        """Execute a raw SQL query."""
        session = self.get_session()
        try:
            result = session.execute(query, params or {})
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.close_session(session)
    
    def bulk_insert(self, model_class, data_list):
        """Bulk insert data."""
        session = self.get_session()
        try:
            session.bulk_insert_mappings(model_class, data_list)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.close_session(session)

# Singleton instance
db_manager = None

def init_db_manager(app):
    """Initialize database manager singleton."""
    global db_manager
    db_manager = DatabaseManager(app)
    return db_manager

def get_db_manager():
    """Get database manager instance."""
    return db_manager