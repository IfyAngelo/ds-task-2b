# ds-task-2b
My submission to the second task in recruitment phase

**README.md**

# Sales Data Analysis API

This repository contains three Python scripts (`test.py`, `test2.py`, and `test3.py`) for building a Flask-based API to analyze sales data. Each script serves a specific purpose, ranging from answering questions about sales data to detecting trends and anomalies.

## `test.py`

The `test.py` script provides an API endpoint `/ask` that allows users to ask questions about sales data, and the script responds with relevant information based on the question. It uses Named Entity Recognition (NER) with spaCy to process questions and extract key entities for analysis.

### Usage

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Run the Flask app by executing `python test.py`.
3. Send POST requests to `http://localhost:5000/ask` with a JSON body containing the question to receive an answer.

## `test2.py`

The `test2.py` script implements an API endpoint `/api/get_gender` to retrieve the gender of a customer based on their order number. It loads sales data from a CSV file and searches for the provided order number, returning the gender associated with that order if found.

### Usage

1. Ensure the sales data CSV file (`gender_sales_data.csv`) is in the same directory as the script.
2. Run the Flask app by executing `python test2.py`.
3. Send GET requests to `http://localhost:5000/api/get_gender?order_number=<order_number>` to retrieve the gender associated with the specified order number.

## `test3.py`

The `test3.py` script analyzes sales data to identify trends and anomalies. It defines an API endpoint `/api/recommendation` that accepts a month parameter and provides recommendations based on the sales data for that month. Trend analysis and anomaly detection are performed to generate recommendations.

### Usage

1. Ensure the sales data CSV file (`gender_sales_data.csv`) is in the same directory as the script.
2. Run the Flask app by executing `python test3.py`.
3. Send GET requests to `http://localhost:5000/api/recommendation?month=<month>` to receive recommendations for the specified month.

## Dependencies

- Flask
- pandas
- spaCy
- numpy
- scipy

These scripts offer various functionalities for analyzing sales data through a user-friendly API interface. Users can interact with the API to gain insights, retrieve specific information, and detect trends or anomalies in the sales dataset.
