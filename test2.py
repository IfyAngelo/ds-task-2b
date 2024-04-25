from flask import Flask, request, jsonify
import pandas as pd
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules

# Load the dataset
data = pd.read_csv("C:/Users/Michael.A_Sydani/Desktop/test_folder2/ds_task_2/orders.csv.csv")
data.dropna(inplace=True)

# Clean the dataset and perform clustering
item_data = data.drop(['order_dow', 'order_hour_of_day', 'days_since_prior_order'], axis=1)
kmeans = KMeans(n_clusters=2)
kmeans.fit(item_data)
data['cluster'] = kmeans.labels_

# Find frequent itemsets using Apriori algorithm
transaction_data = item_data.applymap(lambda x: 1 if x > 0 else 0)
frequent_itemsets = apriori(transaction_data, min_support=0.05, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)

# Create a Flask application
app = Flask(__name__)

# Define a route to predict gender based on order ID
@app.route('/predict_gender', methods=['POST'])
def predict_gender():
    # Get order ID from the request
    order_id = int(request.json['order_id'])

    # Find the cluster label associated with the given order ID
    try:
        cluster_label = data[data['order_id'] == order_id]['cluster'].values[0]
    except IndexError:
        return jsonify({'error': 'Order ID not found'}), 404

    # Determine the gender based on the cluster label
    predicted_gender = "Male" if cluster_label == 0 else "Female"
    
    return jsonify({'order_id': order_id, 'predicted_gender': predicted_gender})

if __name__ == '__main__':
    app.run(debug=True)