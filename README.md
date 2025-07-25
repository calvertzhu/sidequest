# **Sidequest**
Solo travel made social — AI-powered itineraries and new friends, city by city.

**Sidequest** is an AI-powered travel planning app that generates personalized itineraries based on your interests, travel dates, and destination. It also matches you with other travelers on similar journeys, helping you connect, explore, and adventure together.

## Features

- AI-generated travel itineraries based on preferences and schedule
- Traveler matching via profile similarity and overlapping trips
- Real-time activity suggestions from Eventbrite, Google Places, and more
- User authentication and saved trip profiles


## Tech Stack

- **Frontend:** React, Tailwind CSS, Vite
- **Backend:** Flask (Python)
- **AI:** Google Gemini API, LangChain
- **Auth:** Auth0
- **Database:** MongoDB (via MongoDB Atlas)
- **APIs:** Google Places, Eventbrite, Ticketmaster


## Getting Started

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
python3 -m app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```


## API Endpoints

### POST /activities/search

Returns curated activities based on user input.

#### Payload:

```json
{
  "user_email": "user@example.com",
  "location": "Toronto",
  "start_date": "2025-08-01",
  "end_date": "2025-08-05",
  "categories": ["food", "music", "sightseeing"],
  "budget": "medium",
  "trip_name": "Toronto Trip"
}
```

### POST /match

Matches users based on shared preferences and trip overlap.

## Project Status

Originally built at **Hack The 6ix 2025**, Sidequest is now being developed into a full web app. Tthe team is actively working on deployment and feature refinement.


## Roadmap

- Core MVP deployment with basic itinerary + matching
- Add user dashboard and saved trips
- Expand matching logic using embeddings and clustering
- Improve UI/UX and error handling
- Aggregate more travel/event APIs


## Contact

For contributions or inquiries, contact: `calvert.zhu@mail.utoronto.ca`
