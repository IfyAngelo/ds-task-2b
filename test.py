# import pandas as pd
# from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Step 1: Import sales data into a pandas DataFrame
# sales_data = pd.read_csv("sales_data_sample.csv")

# @app.route('/ask', methods=['POST'])
# def ask_question():
#     # Receive the question from the request
#     question = request.json['question']
    
#     # Process the question and find the answer
#     answer = process_question(question)
    
#     # Return the answer as JSON
#     return jsonify({'answer': answer})

# def process_question(question):
#     # Case: What is my top earning sale item?
#     if 'top earning sale item' in question.lower():
#         top_item = calculate_top_earning_sale_item()
#         return f"The top earning sale item is {top_item}"
    
#     # Case: Which city has my best sales?
#     elif 'city' in question.lower() and 'best sales' in question.lower():
#         best_city = find_city_with_best_sales()
#         return f"The city with the best sales is {best_city}"
    
#     # Case: Sales Performance Analysis
#     elif 'top 5 products' in question.lower() and 'last quarter of 2003' in question.lower():
#         top_products = find_top_products_last_quarter_2003()
#         return top_products
    
#     # Case: Customer Segmentation Query
#     elif 'customers' in question.lower() and '2003' in question.lower():
#         high_value_customers = identify_high_value_customers()
#         return high_value_customers
    
#     # Case: Product Demand Fluctuation
#     elif 'product' in question.lower() and 'month' in question.lower() and '2003' in question.lower():
#         highest_avg_month = find_month_with_highest_avg_order_quantity()
#         return f"The month in 2003 with the highest average order quantity is {highest_avg_month}"
    
#     # Case: Regional Sales Comparison
#     elif 'compare' in question.lower() and '2003' in question.lower():
#         comparison_result = compare_regional_sales()
#         return comparison_result
    
#     # Case: Order Fulfillment Efficiency
#     elif 'order fulfillment efficiency' in question.lower() and '2003' in question.lower():
#         most_efficient_country = find_most_efficient_country()
#         return f"The country with the highest proportion of orders shipped within 30 days is {most_efficient_country}"
    
#     # Case: Sales Trend Analysis
#     elif 'sales trend analysis' in question.lower() and '2003' in question.lower():
#         trend_analysis_result = perform_sales_trend_analysis()
#         return trend_analysis_result
    
#     else:
#         return "I'm sorry, I couldn't understand the question."

# def calculate_top_earning_sale_item():
#     # Calculate total sales for each product
#     product_sales = sales_data.groupby('PRODUCTCODE')['SALES'].sum()
#     # Find the product with the highest total sales
#     top_item = product_sales.idxmax()
#     return top_item

# def find_city_with_best_sales():
#     # Calculate total sales for each city
#     city_sales = sales_data.groupby('CITY')['SALES'].sum()
#     # Find the city with the highest total sales
#     best_city = city_sales.idxmax()
#     return best_city

# def find_top_products_last_quarter_2003():
#     # Filter data for the last quarter of 2003, shipped orders, and minimum order quantity of 40 units
#     filtered_data = sales_data[(sales_data['YEAR_ID'] == 2003) & 
#                                (sales_data['QTR_ID'] == 4) &
#                                (sales_data['STATUS'] == 'Shipped') &
#                                (sales_data['QUANTITYORDERED'] >= 40)]
#     # Find the top 5 products with the highest total sales
#     top_products = filtered_data.groupby('PRODUCTCODE')['SALES'].sum().nlargest(5)
#     return top_products.to_dict()

# def identify_high_value_customers():
#     # Filter data for customers who placed more than 3 orders above $5000 each in 2003, from USA or France
#     high_value_customers = sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                       (sales_data['SALES'] > 5000) &
#                                       (sales_data['COUNTRY'].isin(['USA', 'France']))].groupby('CUSTOMERNAME').filter(lambda x: len(x) > 3)
#     return high_value_customers['CUSTOMERNAME'].unique().tolist()

# def find_month_with_highest_avg_order_quantity():
#     # Placeholder logic for finding the month with the highest average order quantity
#     highest_avg_month = "January"  # Replace with actual logic
#     return highest_avg_month

# def compare_regional_sales():
#     # Calculate average order value for each state in 2003
#     state_avg_order_value = sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                        (sales_data['STATUS'] == 'Shipped') &
#                                        (sales_data['QUANTITYORDERED'] >= 20)].groupby('STATE')['SALES'].mean()
#     # Compare the average order value between two specific states (e.g., CA and NY)
#     state1_avg_order_value = state_avg_order_value.get('CA', 0)  # Default to 0 if state not found
#     state2_avg_order_value = state_avg_order_value.get('NY', 0)  # Default to 0 if state not found
#     if state1_avg_order_value > state2_avg_order_value:
#         return f"The average order value is higher in CA compared to NY in 2003."
#     elif state1_avg_order_value < state2_avg_order_value:
#         return f"The average order value is higher in NY compared to CA in 2003."
#     else:
#         return f"The average order value is the same in CA and NY in 2003."

# def find_most_efficient_country():
#     # Calculate the proportion of orders shipped within 30 days for each country in the first half of 2003
#     shipped_within_30_days = sales_data[(sales_data['YEAR_ID'] == 2003) &
#                                         (sales_data['STATUS'] == 'Shipped') &
#                                         ((pd.to_datetime(sales_data['ORDERDATE']) - pd.to_datetime(sales_data['ORDERDATE']).shift()).dt.days <= 30)]
#     country_order_count = shipped_within_30_days.groupby('COUNTRY').size()
#     total_order_count = sales_data[sales_data['YEAR_ID'] == 2003].groupby('COUNTRY')['ORDERNUMBER'].nunique()  # Count unique order numbers
#     countries_over_50_orders = total_order_count[total_order_count > 50].index.tolist()
#     fulfillment_rate = (country_order_count / total_order_count).fillna(0)
#     most_efficient_country = fulfillment_rate.loc[countries_over_50_orders].idxmax()
#     return most_efficient_country

# def perform_sales_trend_analysis():
#     # Calculate moving average of sales data
#     sales_data['SALES_MA'] = sales_data['SALES'].rolling(window=12).mean()
#     # Detect anomalies based on deviation from moving average
#     anomaly_mask = (sales_data['SALES'] > 1.5 * sales_data['SALES_MA']) | (sales_data['SALES'] < 0.5 * sales_data['SALES_MA'])
#     anomalies = sales_data[anomaly_mask]
#     if not anomalies.empty:
#         return f"Anomalies detected in sales data: {anomalies[['ORDERNUMBER', 'ORDERDATE', 'PRODUCTCODE', 'SALES']]}"
#     else:
#         return "No anomalies detected in sales data."

# if __name__ == '__main__':
#     app.run(debug=True)

import os
import openai
import pandas as pd
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

# Setting up the API key for OpenAI
os.environ['OPENAI_API_KEY'] = "api"
openai.api_key = os.environ['OPENAI_API_KEY']

# Initialize Pinecone and OpenAI
pc = Pinecone(api_key="pinecone_api", environment="")
index = pc.Index("index-name", host="index-host")

# Loading the Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to add data to the Pinecone vector database
def add_data_from_csv(file_path, batch_size=1000):
    df = pd.read_csv(file_path)
    
    # Chunk the DataFrame into batches
    chunks = [df[i:i + batch_size] for i in range(0, len(df), batch_size)]
    
    for chunk in chunks:
        # Concatenate values from all columns into a single text string
        text_data = chunk.apply(lambda row: ' '.join(row.astype(str)), axis=1).tolist()
        
        # Encode the concatenated text data
        embeddings = model.encode(text_data).tolist()
        
        # Prepare data for upsert
        data = [(str(i), embedding) for i, embedding in enumerate(embeddings)]
        
        # Add data to Pinecone index
        index.upsert(vectors=data)


# This function is responsible for matching the input string with already existing data on the vector database.
def find_match(query, k):
    query_em = model.encode(query).tolist()
    print("Query embedding:", query_em)
    result = index.query(vector=query_em, top_k=k)
    if result is None:
        print("Error: No result returned from Pinecone index.")
        return []
    else:
        print("Matching context IDs:", result.ids)
        return result.ids

# Function to generate an answer using GPT-3
def generate_answer(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Specify the correct GPT-3 model here
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response.choices[0].message["content"].strip()

# Function to handle user queries
def user_query(query):
    # Find the best matching context based on the query
    best_context_ids = find_match(query, k=1)

    if not best_context_ids:  # If best_context_ids is empty or None
        return "Sorry, I couldn't find a suitable answer to your query."

    # Get corresponding text from CSV
    df = pd.read_csv("csv")
    
    # Check if the index is within the bounds of the DataFrame
    if 0 <= int(best_context_ids[0]) < len(df):
        best_context = df.loc[int(best_context_ids[0])]['text']
    else:
        return "Sorry, I couldn't find a suitable answer to your query."

    # Create a prompt using the best context and the query
    prompt = f"Context: {best_context}\n\nQuestion: {query}\n\nAnswer:"

    # Generate an answer using GPT-3
    answer = generate_answer(prompt)

    return answer


# Test the process
csv_file_path = "csv"
add_data_from_csv(csv_file_path)
print("CSV file loaded and processed successfully.")

# Now, we can use user_query function to get answers for queries.
# Let's define a sample query and get an answer.
query = "Which city has best sales?"
answer = user_query(query)
print("Answer:", answer)
