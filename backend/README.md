# Sidequest Backend - Gemini-Powered Travel Planning

A Flask backend that uses Gemini AI to generate personalized travel itineraries by combining user data from MongoDB with real-time activity data from external APIs.

## 🎯 Core Features

- **User Management**: MongoDB-based user profiles with interests and dietary restrictions
- **Activity Discovery**: Real-time data from Google Places and Ticketmaster APIs
- **AI-Powered Itineraries**: Gemini AI generates personalized 2-day itineraries
- **Smart Integration**: Combines user preferences with actual available activities

## 🏗️ Architecture

```
User Request → Flask Routes → MongoDB (User Data) + APIs (Activities) → Gemini AI → Personalized Itinerary
```

## 📁 Project Structure

```
backend/
├── run.py                 # Entry point
├── src/
│   └── app.py             # Main Flask application
├── routes/
│   ├── db/
│   │   └── user_routes.py # User management (MongoDB)
│   ├── activity_routes.py # Activity discovery (Google Places + Ticketmaster)
│   ├── itinerary_routes.py # Gemini-powered itinerary generation
│   └── gemini/
│       └── gemini.py      # Gemini AI integration
├── test_activity_integration.py # Integration testing
└── requirements.txt       # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create a `.env` file:
```bash
MONGO_URI=mongodb://localhost:27017/
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_API_KEY=your_google_places_api_key
TICKETMASTER_API_KEY=your_ticketmaster_api_key
```

### 3. Start the Server
```bash
python run.py
```

## 📡 API Endpoints

### User Management
- `POST /api/users` - Create user profile
- `GET /api/get_all_users` - List all users
- `GET /api/users/<id>` - Get user by ID
- `GET /api/users/search?email=<email>` - Find user by email

### Activity Discovery
- `GET /api/activities/search` - Search for activities in a location

### Itinerary Generation (Gemini AI)
- `POST /api/generate-itinerary` - Personalized itinerary using user data
- `POST /api/generate-itinerary/quick` - Quick itinerary without user registration
- `GET /api/itinerary/health` - Health check

## 🧠 Gemini AI Integration

The Gemini AI system:

1. **Fetches User Data** from MongoDB (interests, dietary restrictions, age, etc.)
2. **Discovers Activities** using Google Places and Ticketmaster APIs
3. **Creates Rich Prompts** with user context and available activities
4. **Generates Itineraries** with realistic timing and geographic logic

### Example Gemini Prompt Structure:
```
Traveler Profile:
- Name, Age, Gender, Dietary Restrictions

Trip Information:
- Destination, Date Range, Available Activities

Available Places and Events:
- Formatted list from activity APIs

Instructions:
- Use available activities for realistic itinerary
- Consider dietary restrictions
- Mix activity types
- Group geographically
- Include appropriate timing
```

## 🧪 Testing

Run the integration test:
```bash
python test_activity_integration.py
```

This will:
1. Create a test user in the database
2. Search for activities in San Francisco
3. Generate a personalized itinerary using Gemini
4. Save results to JSON files for inspection

## 📝 Example Usage

### Create a User
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alex Johnson",
    "email": "alex@example.com",
    "birthday": "1995-06-15",
    "gender": "non-binary",
    "interests": ["art", "food", "music"],
    "dietary_restrictions": "vegetarian"
  }'
```

### Generate Personalized Itinerary
```bash
curl -X POST http://localhost:8000/api/generate-itinerary \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_id_from_above",
    "location": "New York",
    "start_date": "2024-06-01",
    "end_date": "2024-06-03",
    "budget": "medium"
  }'
```

## 🔧 Configuration

### Required API Keys
- **Gemini API**: For AI-powered itinerary generation
- **Google Places API**: For restaurant, museum, and attraction data
- **Ticketmaster API**: For live events and entertainment

### MongoDB Setup
- Local MongoDB instance or MongoDB Atlas
- Database: `sidequest`
- Collections: `users`

## 🎨 Response Format

### Itinerary Response
```json
{
  "success": true,
  "user_info": {
    "name": "Alex Johnson",
    "age": 29,
    "interests": ["art", "food", "music"],
    "dietary_restrictions": "vegetarian"
  },
  "trip_info": {
    "location": "New York",
    "start_date": "2024-06-01",
    "end_date": "2024-06-03",
    "budget": "medium"
  },
  "available_activities": 45,
  "itinerary": {
    "day_1": {
      "morning": [...],
      "afternoon": [...],
      "evening": [...]
    },
    "day_2": {
      "morning": [...],
      "afternoon": [...],
      "evening": [...]
    }
  }
}
```

## 🚀 Future Enhancements

- Multi-day itinerary support
- Weather integration
- Transportation recommendations
- Budget tracking
- Social features for group travel
- Real-time availability checking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details 