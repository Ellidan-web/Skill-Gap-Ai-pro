from sqlalchemy import create_engine
import os

# Get absolute path
project_path = os.path.abspath('.')
db_path = os.path.join(project_path, 'skillgap.db')
db_url = f'sqlite:///{db_path.replace(os.sep, "/")}'

print(f"Database URL: {db_url}")

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")
