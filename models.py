from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

# Naming convention for constraints
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

class Episode(db.Model):
    """Episode model representing a TV show episode"""
    
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # Relationships
    appearances = db.relationship(
        'Appearance', 
        back_populates='episode',
        cascade='all, delete-orphan',
        lazy=True
    )
    
    def __repr__(self):
        return f'<Episode #{self.number} ({self.date})>'

class Guest(db.Model):
    """Guest model representing a show guest"""
    
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100))
    
    # Relationships
    appearances = db.relationship(
        'Appearance',
        back_populates='guest',
        cascade='all, delete-orphan',
        lazy=True
    )
    
    def __repr__(self):
        return f'<Guest {self.name}>'

class Appearance(db.Model):
    """Appearance model linking episodes and guests with a rating"""
    
    __tablename__ = 'appearances'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(
        db.Integer, 
        db.ForeignKey('episodes.id', ondelete='CASCADE'),
        nullable=False
    )
    guest_id = db.Column(
        db.Integer, 
        db.ForeignKey('guests.id', ondelete='CASCADE'),
        nullable=False
    )
    
    # Relationships
    episode = db.relationship('Episode', back_populates='appearances')
    guest = db.relationship('Guest', back_populates='appearances')
    
    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate that rating is between 1 and 5"""
        if not isinstance(rating, int):
            raise ValueError('Rating must be an integer')
        
        if rating < 1 or rating > 5:
            raise ValueError('Rating must be between 1 and 5')
        
        return rating
    
    def __repr__(self):
        return f'<Appearance: Guest {self.guest_id} on Episode {self.episode_id}>'