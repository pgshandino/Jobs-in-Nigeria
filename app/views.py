from flask import Flask
from flask import jsonify, request
import json
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("data/Cleaned Jobs NG.csv")

@app.route('/')
def index():
    """Render the index page
    """
    return jsonify(
        message="Welcome to Jobs in Nigeria API",
        data={},
        error=None
    )

@app.route('/api/v1/jobs', methods=['GET'])
def get_jobs():
    """Return a list of jobs in Nigeria
    """
    # Get pagination parameters from query string
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    # Calculate start and end index
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    # Slice the DataFrame
    paginated_df = df.iloc[start_idx:end_idx]

    # Convert to JSON
    data_json = paginated_df.to_json(orient='index')

    return jsonify(
        message="Successfully fetched jobs",
        data=json.loads(data_json),
        error=None
    )
    