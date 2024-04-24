# import pandas as pd
# from flask import Flask, request, jsonify
# import spacy

# app = Flask(__name__)

# # Step 1: Import sales data into a pandas DataFrame
# sales_data = pd.read_csv("sales_data_sample.csv")

# # Load English language model for spaCy
# nlp = spacy.load("en_core_web_sm")

# @app.route('/ask', methods=['POST'])
# def ask_question():
#     # Receive the question from the request
#     question = request.json['question']
    
#     # Process the question and find the answer
#     answer = process_question(question)
    
#     # Return the answer as JSON
#     return jsonify({'answer': answer})

# def process_question(question):
#     # Tokenize the question and perform Named Entity Recognition (NER)
#     doc = nlp(question)
    
#     # Extract entities
#     entities = {ent.text.lower(): ent.label_ for ent in doc.ents}
    
#     # Case: What is my top earning sale item?
#     if 'top earning sale item' in question.lower():
#         top_item = sales_data.loc[sales_data['SALES'].idxmax()]
#         return f"The top earning sale item is {top_item['PRODUCTCODE']} with total sales of ${top_item['SALES']}"
    
#     # Case: Which city has my best sales?
#     elif 'city' in entities.values() and 'best sales' in question.lower():
#         city_sales = sales_data.groupby('CITY')['SALES'].sum()
#         best_city = city_sales.idxmax()
#         return f"The city with the best sales is {best_city}"
    
#     # Case: Sales Performance Analysis
#     elif 'top 5 products' in question.lower() and 'last quarter of 2003' in question.lower():
#         top_products = sales_data[(sales_data['YEAR_ID'] == 2003) & 
#                                   (sales_data['QTR_ID'] == 4) &
#                                   (sales_data['STATUS'] == 'Shipped') &
#                                   (sales_data['QUANTITYORDERED'] >= 40)].nlargest(5, 'SALES')
#         return top_products[['PRODUCTCODE', 'SALES']].to_dict(orient='records')
    
#     # Case: Customer Segmentation Query
#     elif 'customers' in question.lower() and '2003' in question.lower():
#         high_value_customers = sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                           (sales_data['SALES'] > 5000) &
#                                           (sales_data['COUNTRY'].isin(['USA', 'France']))].groupby('CUSTOMERNAME').filter(lambda x: len(x) > 3)
#         return high_value_customers['CUSTOMERNAME'].unique().tolist()
    
#     # Case: Product Demand Fluctuation
#     elif 'product' in entities.values() and 'month' in entities.values() and '2003' in question.lower():
#         # Extract product name
#         product_name = [ent.text for ent in doc.ents if ent.label_ == 'PRODUCT'][0]
#         # Filter sales data for the specific product
#         product_sales_2003 = sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                         (sales_data['PRODUCTLINE'].str.lower() == product_name.lower()) &
#                                         (sales_data['SALES'] > 100000) &
#                                         (sales_data['PRICEEACH'] > 80)]
#         # Find the month with the highest average order quantity
#         avg_quantity_by_month = product_sales_2003.groupby('MONTH_ID')['QUANTITYORDERED'].mean()
#         highest_avg_month = avg_quantity_by_month.idxmax()
#         return f"The month in 2003 with the highest average order quantity for {product_name} is {highest_avg_month}"
    
#     # Case: Regional Sales Comparison
#     elif 'compare' in question.lower() and '2003' in question.lower():
#         states = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
#         if len(states) == 2:
#             state1, state2 = states
#             avg_order_value_state1 = sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                                 (sales_data['STATE'] == state1.upper()) &
#                                                 (sales_data['STATUS'] == 'Shipped') &
#                                                 (sales_data['QUANTITYORDERED'] >= 20)]['SALES'].mean()
#             avg_order_value_state2 = sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                                 (sales_data['STATE'] == state2.upper()) &
#                                                 (sales_data['STATUS'] == 'Shipped') &
#                                                 (sales_data['QUANTITYORDERED'] >= 20)]['SALES'].mean()
#             if avg_order_value_state1 > avg_order_value_state2:
#                 return f"The average order value is higher in {state1} compared to {state2} in 2003."
#             elif avg_order_value_state1 < avg_order_value_state2:
#                 return f"The average order value is higher in {state2} compared to {state1} in 2003."
#             else:
#                 return f"The average order value is the same in {state1} and {state2} in 2003."
#         else:
#             return "Please provide exactly two states to compare."
    
#     # Case: Order Fulfillment Efficiency
#     elif 'order fulfillment efficiency' in question.lower() and '2003' in question.lower():
#         countries = sales_data[sales_data['YEAR_ID'] == 2003]['COUNTRY'].value_counts()
#         countries_over_50_orders = countries[countries > 50].index.tolist()
#         max_shipped_orders = 0
#         most_efficient_country = ""
#         for country in countries_over_50_orders:
#             total_orders = len(sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                           (sales_data['COUNTRY'] == country)])
#             shipped_orders = len(sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                             (sales_data['COUNTRY'] == country) &
#                                             (sales_data['STATUS'] == 'Shipped') &
#                                             ((pd.to_datetime(sales_data['ORDERDATE']) - pd.to_datetime(sales_data['ORDERDATE']).shift()).dt.days <= 30)])
#             fulfillment_rate = shipped_orders / total_orders
#             if fulfillment_rate > max_shipped_orders:
#                 max_shipped_orders = fulfillment_rate
#                 most_efficient_country = country
#         return f"The country with the highest proportion of orders shipped within 30 days in the first half of 2003 is {most_efficient_country}."
    
#     # Case: Sales Trend Analysis
#     elif 'sales trend analysis' in question.lower() and '2003' in question.lower():
#         product_line = [ent.text for ent in doc.ents if ent.label_ == 'PRODUCT'][0]
#         month_sales = sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                  (sales_data['PRODUCTLINE'].str.lower() == product_line.lower())].groupby('MONTH_ID')['SALES'].sum()
#         previous_month_sales = month_sales.shift(1)
#         percent_change = (month_sales - previous_month_sales) / previous_month_sales * 100
#         if percent_change.max() > 25:
#             return f"There was a month in 2003 where sales for {product_line} increased by more than 25% compared to the previous month."
#         else:
#             return f"There was no month in 2003 where sales for {product_line} increased by more than 25% compared to the previous month."
    
#     else:
#         return "I'm sorry, I couldn't understand the question."

# if __name__ == '__main__':
#     app.run(debug=True)

import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Step 1: Import sales data into a pandas DataFrame
sales_data = pd.read_csv("sales_data_sample.csv")

@app.route('/ask', methods=['POST'])
def ask_question():
    # Receive the question from the request
    question = request.json['question']
    
    # Process the question and find the answer
    answer = process_question(question)
    
    # Return the answer as JSON
    return jsonify({'answer': answer})

def process_question(question):
    # Case: What is my top earning sale item?
    if 'top earning sale item' in question.lower():
        top_item = calculate_top_earning_sale_item()
        return f"The top earning sale item is {top_item}"
    
    # Case: Which city has my best sales?
    elif 'city' in question.lower() and 'best sales' in question.lower():
        best_city = find_city_with_best_sales()
        return f"The city with the best sales is {best_city}"
    
    # Case: Sales Performance Analysis
    elif 'top 5 products' in question.lower() and 'last quarter of 2003' in question.lower():
        top_products = find_top_products_last_quarter_2003()
        return top_products
    
    # Case: Customer Segmentation Query
    elif 'customers' in question.lower() and '2003' in question.lower():
        high_value_customers = identify_high_value_customers()
        return high_value_customers
    
    # Case: Product Demand Fluctuation
    elif 'product' in question.lower() and 'month' in question.lower() and '2003' in question.lower():
        highest_avg_month = find_month_with_highest_avg_order_quantity()
        return f"The month in 2003 with the highest average order quantity is {highest_avg_month}"
    
    # Case: Regional Sales Comparison
    elif 'compare' in question.lower() and '2003' in question.lower():
        comparison_result = compare_regional_sales()
        return comparison_result
    
    # Case: Order Fulfillment Efficiency
    elif 'order fulfillment efficiency' in question.lower() and '2003' in question.lower():
        most_efficient_country = find_most_efficient_country()
        return f"The country with the highest proportion of orders shipped within 30 days is {most_efficient_country}"
    
    # Case: Sales Trend Analysis
    elif 'sales trend analysis' in question.lower() and '2003' in question.lower():
        trend_analysis_result = perform_sales_trend_analysis()
        return trend_analysis_result
    
    else:
        return "I'm sorry, I couldn't understand the question."

def calculate_top_earning_sale_item():
    # Calculate total sales for each product
    product_sales = sales_data.groupby('PRODUCTCODE')['SALES'].sum()
    # Find the product with the highest total sales
    top_item = product_sales.idxmax()
    return top_item

def find_city_with_best_sales():
    # Calculate total sales for each city
    city_sales = sales_data.groupby('CITY')['SALES'].sum()
    # Find the city with the highest total sales
    best_city = city_sales.idxmax()
    return best_city

def find_top_products_last_quarter_2003():
    # Filter data for the last quarter of 2003, shipped orders, and minimum order quantity of 40 units
    filtered_data = sales_data[(sales_data['YEAR_ID'] == 2003) & 
                               (sales_data['QTR_ID'] == 4) &
                               (sales_data['STATUS'] == 'Shipped') &
                               (sales_data['QUANTITYORDERED'] >= 40)]
    # Find the top 5 products with the highest total sales
    top_products = filtered_data.groupby('PRODUCTCODE')['SALES'].sum().nlargest(5)
    return top_products.to_dict()

def identify_high_value_customers():
    # Filter data for customers who placed more than 3 orders above $5000 each in 2003, from USA or France
    high_value_customers = sales_data[(sales_data['YEAR_ID'] == 2003) &
                                      (sales_data['SALES'] > 5000) &
                                      (sales_data['COUNTRY'].isin(['USA', 'France']))].groupby('CUSTOMERNAME').filter(lambda x: len(x) > 3)
    return high_value_customers['CUSTOMERNAME'].unique().tolist()

def find_month_with_highest_avg_order_quantity():
    # Placeholder logic for finding the month with the highest average order quantity
    highest_avg_month = "January"  # Replace with actual logic
    return highest_avg_month

def compare_regional_sales():
    # Calculate average order value for each state in 2003
    state_avg_order_value = sales_data[(sales_data['YEAR_ID'] == 2003) &
                                       (sales_data['STATUS'] == 'Shipped') &
                                       (sales_data['QUANTITYORDERED'] >= 20)].groupby('STATE')['SALES'].mean()
    # Compare the average order value between two specific states (e.g., CA and NY)
    state1_avg_order_value = state_avg_order_value.get('CA', 0)  # Default to 0 if state not found
    state2_avg_order_value = state_avg_order_value.get('NY', 0)  # Default to 0 if state not found
    if state1_avg_order_value > state2_avg_order_value:
        return f"The average order value is higher in CA compared to NY in 2003."
    elif state1_avg_order_value < state2_avg_order_value:
        return f"The average order value is higher in NY compared to CA in 2003."
    else:
        return f"The average order value is the same in CA and NY in 2003."

def find_most_efficient_country():
    # Calculate the proportion of orders shipped within 30 days for each country in the first half of 2003
    shipped_within_30_days = sales_data[(sales_data['YEAR_ID'] == 2003) &
                                        (sales_data['STATUS'] == 'Shipped') &
                                        ((pd.to_datetime(sales_data['ORDERDATE']) - pd.to_datetime(sales_data['ORDERDATE']).shift()).dt.days <= 30)]
    country_order_count = shipped_within_30_days.groupby('COUNTRY').size()
    total_order_count = sales_data[sales_data['YEAR_ID'] == 2003].groupby('COUNTRY')['ORDERNUMBER'].nunique()  # Count unique order numbers
    countries_over_50_orders = total_order_count[total_order_count > 50].index.tolist()
    fulfillment_rate = (country_order_count / total_order_count).fillna(0)
    most_efficient_country = fulfillment_rate.loc[countries_over_50_orders].idxmax()
    return most_efficient_country

def perform_sales_trend_analysis():
    # Calculate moving average of sales data
    sales_data['SALES_MA'] = sales_data['SALES'].rolling(window=12).mean()
    # Detect anomalies based on deviation from moving average
    anomaly_mask = (sales_data['SALES'] > 1.5 * sales_data['SALES_MA']) | (sales_data['SALES'] < 0.5 * sales_data['SALES_MA'])
    anomalies = sales_data[anomaly_mask]
    if not anomalies.empty:
        return f"Anomalies detected in sales data: {anomalies[['ORDERNUMBER', 'ORDERDATE', 'PRODUCTCODE', 'SALES']]}"
    else:
        return "No anomalies detected in sales data."

if __name__ == '__main__':
    app.run(debug=True)