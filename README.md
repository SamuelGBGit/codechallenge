# Late Show API

A Flask REST API for managing Late Show episodes, celebrity guests, and their appearances.

## Installation

1. Install dependencies:
```bash
cd ~/assignment/codechallenge
pip install -r requirements.txt
```

2. Create and seed the database:
```bash
python seed.py
```

3. Run the API server:
```bash
python app.py
```

The server will run at `http://localhost:5555`

## API Endpoints

### GET /episodes
Returns a list of all episodes.

Response:
```json
[
  {
    "id": 1,
    "date": "1/11/99",
    "number": 1
  }
]
```

### GET /episodes/:id
Returns a specific episode with all guest appearances.

Response:
```json
{
  "id": 1,
  "date": "1/11/99",
  "number": 1,
  "appearances": [
    {
      "id": 1,
      "rating": 4,
      "episode_id": 1,
      "guest_id": 1,
      "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
      }
    }
  ]
}
```

If episode not found, returns 404:
```json
{
  "error": "Episode not found"
}
```

### DELETE /episodes/:id
Deletes an episode and all associated appearances.

Returns 204 No Content on success.

### GET /guests
Returns a list of all guests.

Response:
```json
[
  {
    "id": 1,
    "name": "Michael J. Fox",
    "occupation": "actor"
  }
]
```

### POST /appearances
Creates a new appearance linking a guest to an episode.

Request body:
```json
{
  "rating": 5,
  "episode_id": 2,
  "guest_id": 3
}
```

Response (201 Created):
```json
{
  "id": 162,
  "rating": 5,
  "guest_id": 3,
  "episode_id": 2,
  "episode": {
    "date": "1/12/99",
    "id": 2,
    "number": 2
  },
  "guest": {
    "id": 3,
    "name": "Tracey Ullman",
    "occupation": "television actress"
  }
}
```

Validation errors return 400:
```json
{
  "errors": ["validation errors"]
}
```

## Database Models

### Episode
- id (Primary Key)
- date (String)
- number (Integer)

### Guest
- id (Primary Key)
- name (String)
- occupation (String)

### Appearance
- id (Primary Key)
- rating (Integer, 1-5)
- episode_id (Foreign Key)
- guest_id (Foreign Key)

Validations:
- Rating must be between 1 and 5

Relationships:
- Episode has many Guests through Appearances
- Guest has many Episodes through Appearances
- Deleting an Episode cascades to delete its Appearances

## Database

The project uses SQLite. After running `python seed.py`, the database contains:
- 5 episodes
- 5 celebrity guests
- 8 appearance records

## Project Structure

```
app.py           - Flask API endpoints
models.py        - SQLAlchemy models
config.py        - Database configuration
seed.py          - Database seeding script
requirements.txt - Python dependencies
README.md        - This file
```

## Troubleshooting

If the database gets corrupted, reset it:
```bash
rm late_show.db
python seed.py
```

If port 5555 is in use, edit the last line in app.py to use a different port:
```python
app.run(host='0.0.0.0', port=5556, debug=True)
```

If you get import errors, reinstall dependencies:
```bash
pip install -r requirements.txt
```
