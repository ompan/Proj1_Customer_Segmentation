from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from plotly.utils import PlotlyJSONEncoder
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)

# Step 1: Load dataset and process it
def load_and_preprocess_data():
    # Replace this with the correct path
    df = pd.read_csv('C:/Users/smita/Desktop/Internships24/CodeClause/Proj1_Customer_Segmentation/Datasets/Customers.csv')

    # Preprocess data (as done in the notebook)
    scaler = MinMaxScaler()
    df[['Age', 'Annual Income ($)', 'Spending Score (1-100)']] = scaler.fit_transform(df[['Age', 'Annual Income ($)', 'Spending Score (1-100)']])

    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=5)
    df['Cluster'] = kmeans.fit_predict(df[['Age', 'Annual Income ($)', 'Spending Score (1-100)']])

    return df

# Step 2: Create dynamic scatter plot for clustering
def create_scatter_plot(df):
    scatter_fig = px.scatter(
        df, x='Annual Income ($)', y='Spending Score (1-100)', color='Cluster',
        title="Customer Segmentation Scatter Plot",
        labels={'Annual Income ($)': 'Annual Income ($)', 'Spending Score (1-100)': 'Spending Score'}
    )
    scatter_json = json.dumps(scatter_fig, cls=PlotlyJSONEncoder)
    return scatter_json

# Step 3: Create dynamic bar chart for customer distribution
def create_bar_chart(df):
    bar_fig = px.bar(
        df, x='Cluster', y='CustomerID', title="Customer Distribution by Cluster",
        labels={'CustomerID': 'Number of Customers', 'Cluster': 'Customer Cluster'},
        barmode='group'
    )
    bar_json = json.dumps(bar_fig, cls=PlotlyJSONEncoder)
    return bar_json

# Dashboard route
@app.route('/')
def dashboard():
    df = load_and_preprocess_data()

    # Generate scatter plot and bar chart
    scatter_plot = create_scatter_plot(df)
    bar_chart = create_bar_chart(df)

    print(scatter_plot)
    print(bar_chart)


    return render_template('dashboard.html', scatter_plot=scatter_plot, bar_chart=bar_chart)

if __name__ == '__main__':
    app.run(debug=True)
