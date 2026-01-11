import os

class Config:
    """Application configuration settings"""
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///late_show.db'  
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JSON settings for pretty printing
    JSON_SORT_KEYS = False  # Keep original order
    JSONIFY_PRETTYPRINT_REGULAR = True