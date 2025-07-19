from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from routes.db.user_routes import users_bp
from routes.db.event_routes import events_bp
from routes.db.itinerary_routes import itins_bp

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Use MongoDB Atlas URI from .env
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise ValueError("MONGO_URI not found in .env")

# Connect to MongoDB Atlas
client = MongoClient(mongo_uri)
db = client["mydatabase"]  # same name as in your connection string (optional)
app.config["DB"] = db  # pass DB into app context (can be used in blueprints)

# Register the blueprint
app.register_blueprint(users_bp, url_prefix="/api")
app.register_blueprint(events_bp, url_prefix="/api")
app.register_blueprint(itins_bp, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
