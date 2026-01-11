from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Episode, Guest, Appearance
from config import Config
import sys

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Setup database
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    """Home route with API information"""
    return {
        'message': 'Welcome to Late Show API',
        'endpoints': {
            'GET /episodes': 'List all episodes',
            'GET /episodes/<id>': 'Get episode details',
            'DELETE /episodes/<id>': 'Delete an episode',
            'GET /guests': 'List all guests',
            'POST /appearances': 'Create a new appearance'
        }
    }, 200

@app.route('/episodes', methods=['GET'])
def get_episodes():
    """Get all episodes (without appearances to keep response light)"""
    try:
        episodes = Episode.query.order_by(Episode.number).all()
        
        episodes_data = []
        for episode in episodes:
            episodes_data.append({
                'id': episode.id,
                'date': episode.date,
                'number': episode.number
            })
        
        return jsonify(episodes_data), 200
    
    except Exception as e:
        app.logger.error(f"Error fetching episodes: {str(e)}")
        return jsonify({'error': 'Failed to fetch episodes'}), 500

@app.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    """Get a specific episode by ID with its appearances"""
    try:
        episode = Episode.query.get(episode_id)
        
        if not episode:
            return jsonify({'error': 'Episode not found'}), 404
        
        # Build response manually
        episode_dict = {
            'id': episode.id,
            'date': episode.date,
            'number': episode.number,
            'appearances': []
        }
        
        # Add appearances
        for appearance in Appearance.query.filter_by(episode_id=episode_id).all():
            guest = Guest.query.get(appearance.guest_id)
            if guest:
                episode_dict['appearances'].append({
                    'id': appearance.id,
                    'rating': appearance.rating,
                    'episode_id': appearance.episode_id,
                    'guest_id': appearance.guest_id,
                    'guest': {
                        'id': guest.id,
                        'name': guest.name,
                        'occupation': guest.occupation
                    }
                })
        
        return jsonify(episode_dict), 200
    
    except Exception as e:
        app.logger.error(f"Error fetching episode {episode_id}: {str(e)}")
        return jsonify({'error': 'Failed to fetch episode'}), 500

@app.route('/episodes/<int:episode_id>', methods=['DELETE'])
def delete_episode(episode_id):
    """Delete an episode by ID"""
    try:
        episode = Episode.query.get(episode_id)
        
        if not episode:
            return jsonify({'error': 'Episode not found'}), 404
        
        db.session.delete(episode)
        db.session.commit()
        
        return '', 204  # No content on successful delete
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting episode {episode_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete episode'}), 500

@app.route('/guests', methods=['GET'])
def get_guests():
    """Get all guests"""
    try:
        guests = Guest.query.order_by(Guest.name).all()
        
        guests_data = []
        for guest in guests:
            guests_data.append({
                'id': guest.id,
                'name': guest.name,
                'occupation': guest.occupation
            })
        
        return jsonify(guests_data), 200
    
    except Exception as e:
        app.logger.error(f"Error fetching guests: {str(e)}")
        return jsonify({'error': 'Failed to fetch guests'}), 500

@app.route('/appearances', methods=['GET'])
def get_appearances():
    """Get all appearances"""
    try:
        appearances = Appearance.query.all()
        
        appearances_data = []
        for appearance in appearances:
            episode = Episode.query.get(appearance.episode_id)
            guest = Guest.query.get(appearance.guest_id)
            
            if episode and guest:
                appearances_data.append({
                    'id': appearance.id,
                    'rating': appearance.rating,
                    'episode_id': appearance.episode_id,
                    'guest_id': appearance.guest_id,
                    'episode': {
                        'id': episode.id,
                        'date': episode.date,
                        'number': episode.number
                    },
                    'guest': {
                        'id': guest.id,
                        'name': guest.name,
                        'occupation': guest.occupation
                    }
                })
        
        return jsonify(appearances_data), 200
    
    except Exception as e:
        app.logger.error(f"Error fetching appearances: {str(e)}")
        return jsonify({'error': 'Failed to fetch appearances'}), 500

@app.route('/appearances', methods=['POST'])
def create_appearance():
    """Create a new appearance (link guest to episode with rating)"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'errors': ['No data provided']}), 400
        
        # Check for required fields
        required_fields = ['rating', 'episode_id', 'guest_id']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'errors': [f'Missing fields: {", ".join(missing_fields)}']}), 400
        
        # Validate rating
        rating = data['rating']
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'errors': ['Rating must be an integer between 1 and 5']}), 400
        
        # Check if episode and guest exist
        episode = Episode.query.get(data['episode_id'])
        guest = Guest.query.get(data['guest_id'])
        
        if not episode:
            return jsonify({'errors': ['Episode not found']}), 404
        
        if not guest:
            return jsonify({'errors': ['Guest not found']}), 404
        
        # Create new appearance
        new_appearance = Appearance(
            rating=data['rating'],
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        
        db.session.add(new_appearance)
        db.session.commit()
        
        # Build response manually
        response_data = {
            'id': new_appearance.id,
            'rating': new_appearance.rating,
            'guest_id': new_appearance.guest_id,
            'episode_id': new_appearance.episode_id,
            'episode': {
                'id': episode.id,
                'date': episode.date,
                'number': episode.number
            },
            'guest': {
                'id': guest.id,
                'name': guest.name,
                'occupation': guest.occupation
            }
        }
        
        return jsonify(response_data), 201
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating appearance: {str(e)}")
        return jsonify({'errors': ['validation errors']}), 400

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server
    print("🚀 Starting Late Show API...")
    print("📡 Server running at http://localhost:5555")
    print("Press Ctrl+C to stop")
    app.run(host='0.0.0.0', port=5555, debug=True)