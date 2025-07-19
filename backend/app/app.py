import os
from flask import Flask
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

# MongoDB setup
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['sidequest']
app.config['db'] = db

# Register blueprints
from .routes.user_routes import user_bp
from .routes.search_routes import search_bp
app.register_blueprint(user_bp)
app.register_blueprint(search_bp)

@app.route("/")
def home():
    return "Hello from Sidequest backend!"

if __name__ == "__main__":
    app.run(debug=True)

