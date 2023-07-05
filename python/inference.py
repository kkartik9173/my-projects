from flask import Flask, request, jsonify
from joblib import load
import pandas as pd
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Load model
clf = load('clf.joblib')

# Load label encoder
le = load('le.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    df = pd.DataFrame(data)
    
    # Make sure the columns are in the same order as in the training data
    df = df[['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'RSI']]

    # Replace non-numeric values with NaN
    df = df.apply(pd.to_numeric, errors='coerce')

    # Drop the rows where at least one element is missing
    df = df.dropna()

    prediction = clf.predict(df)
    prediction_label = le.inverse_transform(prediction)
    
    return jsonify({'predictions': prediction_label.tolist()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
