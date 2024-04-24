from flask import Flask, request, jsonify
import pandas as pd
import logging

# Load the dataset
sales_data = pd.read_csv('gender_sales_data.csv')

# Convert ORDERNUMBER to string and strip whitespace
sales_data['ORDERNUMBER'] = sales_data['ORDERNUMBER'].astype(str).str.strip()

# Initialize Flask app
app = Flask(__name__)

# Define API endpoint
@app.route('/api/get_gender', methods=['GET'])
def get_gender():
    # Get the order_number from the request parameters
    order_number = request.args.get('order_number')
    
    # Check if order_number exists in the dataset
    if order_number in sales_data['ORDERNUMBER'].values:
        # Retrieve customer's gender based on order number
        customer_gender = sales_data.loc[sales_data['ORDERNUMBER'] == order_number, 'GENDER'].iloc[0]
        
        # Log debug information
        app.logger.info(f"Order number {order_number} found. Gender: {customer_gender}")
        
        return jsonify({'order_number': order_number, 'gender': customer_gender})
    else:
        # Log debug information
        app.logger.info(f"Order number {order_number} not found.")
        
        return jsonify({'order_number': order_number, 'gender': 'unknown'})

# Run the Flask app
if __name__ == '__main__':
    # Enable debug logging
    app.logger.setLevel(logging.DEBUG)
    
    # Run the app
    app.run(debug=True)
