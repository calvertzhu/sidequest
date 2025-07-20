from flask import Blueprint, request, jsonify
from .langchain_match import generate_langchain_match_analysis, get_match_summary, MatchAnalysis

match_bp = Blueprint('match', __name__)

@match_bp.route('/match', methods=['POST'])
def match_users():
    """Match two user profiles and return compatibility analysis using LangChain."""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'user1' not in data or 'user2' not in data:
        return jsonify({'error': 'Missing user1 or user2 data'}), 400
    
    user1 = data['user1']
    user2 = data['user2']
    
    # Validate user profiles have required fields
    required_fields = ['name', 'interests', 'location', 'travel_dates']
    for user in [user1, user2]:
        if not all(field in user for field in required_fields):
            return jsonify({'error': 'User profiles must include name, interests, location, and travel_dates'}), 400
    
    try:
        # Generate match analysis using LangChain
        match_analysis = generate_langchain_match_analysis(user1, user2)
        
        # Get summary for quick reference
        summary = get_match_summary(match_analysis)
        
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