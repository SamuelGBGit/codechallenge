import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///late_show.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from models import db, Episode, Guest, Appearance

db.init_app(app)

def seed_database():
    """Seed the database with sample data"""
    
    print("🌱 Seeding database...")
    
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create episodes
        episodes_data = [
            {"date": "1/11/99", "number": 1},
            {"date": "1/12/99", "number": 2},
            {"date": "1/13/99", "number": 3},
            {"date": "1/14/99", "number": 4},
            {"date": "1/15/99", "number": 5}
        ]
        
        episodes = []
        for ep_data in episodes_data:
            episode = Episode(**ep_data)
            episodes.append(episode)
        
        db.session.add_all(episodes)
        
        # Create guests
        guests_data = [
            {"name": "Michael J. Fox", "occupation": "actor"},
            {"name": "Sandra Bernhard", "occupation": "Comedian"},
            {"name": "Tracey Ullman", "occupation": "television actress"},
            {"name": "Robin Williams", "occupation": "comedian"},
            {"name": "Whoopi Goldberg", "occupation": "actress"}
        ]
        
        guests = []
        for guest_data in guests_data:
            guest = Guest(**guest_data)
            guests.append(guest)
        
        db.session.add_all(guests)
        db.session.commit()
        
        # Create appearances
        appearances_data = [
            {"rating": 4, "episode_id": 1, "guest_id": 1},
            {"rating": 5, "episode_id": 2, "guest_id": 2},
            {"rating": 3, "episode_id": 2, "guest_id": 3},
            {"rating": 5, "episode_id": 3, "guest_id": 1},
            {"rating": 2, "episode_id": 4, "guest_id": 4},
            {"rating": 4, "episode_id": 5, "guest_id": 5},
            {"rating": 5, "episode_id": 1, "guest_id": 4},
            {"rating": 3, "episode_id": 3, "guest_id": 5}
        ]
        
        appearances = []
        for app_data in appearances_data:
            appearance = Appearance(**app_data)
            appearances.append(appearance)
        
        db.session.add_all(appearances)
        db.session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"   Created: {len(episodes)} episodes")
        print(f"   Created: {len(guests)} guests")
        print(f"   Created: {len(appearances)} appearances")

if __name__ == '__main__':
    seed_database()