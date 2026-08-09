import os
import sys

# Include vendor packages inside workspace if available
vendor_dir = os.path.join(os.path.dirname(__file__), 'vendor')
if os.path.exists(vendor_dir):
    sys.path.insert(0, vendor_dir)

from flask import Flask, render_template, jsonify, request
from data import EVENT_INFO, CATEGORIES, SCHEDULE, get_all_talks, get_all_speakers, get_talk_by_id, filter_talks


app = Flask(__name__)

@app.route('/')
def index():
    """Render main 1-day conference homepage with schedule, speakers, and event details."""
    talks = get_all_talks()
    speakers = get_all_speakers()
    return render_template(
        'index.html',
        event=EVENT_INFO,
        categories=CATEGORIES,
        schedule=SCHEDULE,
        talks=talks,
        speakers=speakers
    )

@app.route('/api/talks', methods=['GET'])
def api_get_talks():
    """REST API endpoint for filtering talks by category, speaker, or keyword search."""
    q = request.args.get('q', '').strip()
    category = request.args.get('category', 'all').strip()
    speaker = request.args.get('speaker', 'all').strip()

    filtered = filter_talks(query=q, category=category, speaker_name=speaker)
    return jsonify({
        "count": len(filtered),
        "query": q,
        "category": category,
        "speaker": speaker,
        "talks": filtered
    })

@app.route('/api/talk/<int:talk_id>', methods=['GET'])
def api_get_talk_detail(talk_id):
    """REST API endpoint to fetch detailed information for a specific talk."""
    talk = get_talk_by_id(talk_id)
    if not talk:
        return jsonify({"error": "Talk not found", "talk_id": talk_id}), 404
    return jsonify(talk)

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "Google Cloud Tech Conference 2026",
        "talks_count": len(get_all_talks()),
        "speakers_count": len(get_all_speakers())
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
