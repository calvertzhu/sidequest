from flask import Blueprint, request, jsonify, current_app
from .langchain_match import generate_langchain_match_analysis, get_match_summary, MatchAnalysis
from bson import ObjectId

match_bp = Blueprint('match', __name__)

@match_bp.route('/match', methods=['POST'])
def match_users():
    """Match two user profiles and return compatibility analysis using LangChain."""
    data = request.get_json()
    db = current_app.config["DB"]

    # Accept user1_id and user2_id
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')
    if not user1_id or not user2_id:
        return jsonify({'error': 'Missing user1_id or user2_id'}), 400

    # Fetch user profiles from DB
    user1 = db.users.find_one({"_id": ObjectId(user1_id)})
    user2 = db.users.find_one({"_id": ObjectId(user2_id)})
    if not user1 or not user2:
        return jsonify({'error': 'User not found'}), 404

    # Build prompt profiles, using IDs as names
    user1_profile = {
        'name': str(user1_id),
        'interests': user1.get('interests', []),
        'location': user1.get('location', ''),
        'travel_dates': user1.get('travel_dates', '')
    }
    user2_profile = {
        'name': str(user2_id),
        'interests': user2.get('interests', []),
        'location': user2.get('location', ''),
        'travel_dates': user2.get('travel_dates', '')
    }

    # Validate required fields
    required_fields = ['name', 'interests', 'location', 'travel_dates']
    for user in [user1_profile, user2_profile]:
        if not all(field in user and user[field] for field in required_fields):
            return jsonify({'error': 'User profiles must include name, interests, location, and travel_dates'}), 400

    try:
        # Generate match analysis using LangChain
        match_analysis = generate_langchain_match_analysis(user1_profile, user2_profile)
        # Get summary for quick reference
        summary = get_match_summary(match_analysis, user1_id, user2_id)
        # Convert Pydantic model to dict for JSON response
        analysis_dict = match_analysis.model_dump()
        return jsonify({
            'success': True,
            'match_analysis': analysis_dict,
            'summary': summary
        }), 200
    except Exception as e:
        return jsonify({
            'error': f'Match analysis failed: {str(e)}'
        }), 500

@match_bp.route('/match/summary', methods=['POST'])
def get_match_summary_only():
    """Get just the match summary without full analysis."""
    data = request.get_json()
    
    if not data or 'user1' not in data or 'user2' not in data:
        return jsonify({'error': 'Missing user1 or user2 data'}), 400
    
    user1 = data['user1']
    user2 = data['user2']
    
    try:
        # Generate full analysis first
        match_analysis = generate_langchain_match_analysis(user1, user2)
        
        # Return only the summary
        summary = get_match_summary(match_analysis)
        
        return jsonify({
            'success': True,
            'summary': summary
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Match analysis failed: {str(e)}'
        }), 500

@match_bp.route('/match/health', methods=['GET'])
def match_health():
    """Health check endpoint for the matching service."""
    return jsonify({
        'status': 'healthy',
        'service': 'travel_compatibility_matcher',
        'version': '2.0.0',
        'features': [
            'langchain_integration',
            'structured_outputs',
            'fallback_algorithm',
            'pydantic_validation'
        ]
    }), 200 