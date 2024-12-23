from flask import Flask, jsonify, request
from flask_cors import CORS
from main import main
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/search', methods=['GET'])
def search_places():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Please provide a search query using the 'q' parameter"}), 400
    
    try:
        # Run the scraper
        main(query)
        
        # Read and return the results
        with open('results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
