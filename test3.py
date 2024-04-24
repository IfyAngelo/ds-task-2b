from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from scipy.stats import zscore

# Load the dataset
sales_data = pd.read_csv('gender_sales_data.csv', parse_dates=['ORDERDATE'])

# Initialize Flask app
app = Flask(__name__)

# Placeholder function to analyze trends in sales data
def analyze_trends(data):
    # Calculate average sales for the specified month
    average_sales_current_month = data['SALES'].mean()
    
    # Calculate average sales for the previous month
    previous_month = data['ORDERDATE'].iloc[0].month - 1
    average_sales_previous_month = sales_data[sales_data['ORDERDATE'].dt.month == previous_month]['SALES'].mean()
    
    if average_sales_current_month > average_sales_previous_month:
        return "Identified an increasing trend in sales."
    else:
        return "No significant trend identified in sales."

# Placeholder function to detect anomalies in sales data
def detect_anomalies(data):
    # Calculate z-score for each day's sales amount
    data['SALES_ZSCORE'] = zscore(data['SALES'])
    
    # Define threshold for anomaly detection (e.g., z-score > 2)
    anomaly_threshold = 2
    
    # Identify days with z-score above the threshold as anomalies
    anomalies = data[data['SALES_ZSCORE'] > anomaly_threshold]
    
    if len(anomalies) > 0:
        return f"Detected {len(anomalies)} anomalies in sales data."
    else:
        return "No anomalies detected in sales data."

# Update the Flask API endpoint to use these functions
@app.route('/api/recommendation', methods=['GET'])
def generate_recommendation():
    # Get the month from the request parameters
    month = request.args.get('month')
    
    # Filter sales data for the specified month
    sales_in_month = sales_data[sales_data['ORDERDATE'].dt.month == int(month)]
    
    if len(sales_in_month) == 0:
        return jsonify({'error': 'No data available for the specified month'})
    
    # Perform trend analysis
    trend_recommendation = analyze_trends(sales_in_month)
    
    # Perform anomaly detection
    anomaly_recommendation = detect_anomalies(sales_in_month)
    
    # Generate final recommendation
    recommendation = {
        'month': month,
        'trend_recommendation': trend_recommendation,
        'anomaly_recommendation': anomaly_recommendation
    }
    
    return jsonify(recommendation)

if __name__ == '__main__':
    app.run(debug=True)
