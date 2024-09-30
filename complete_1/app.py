from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sklearn.cluster import KMeans

app = Flask(__name__)

# Load and preprocess the data
df = pd.read_csv("C:/Users/smita/Desktop/Internships24/CodeClause/Proj1_Customer_Segmentation/Datasets/Mall_Customers.csv")
features = df[['Spending Score (1-100)', 'Annual Income (k$)']]
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(features)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot')
def plot():
    # Create the plot
    plt.figure(figsize=(6, 6))
    plt.scatter(df['Spending Score (1-100)'], df['Annual Income (k$)'], c=df['Cluster'], cmap='viridis')
    plt.xlabel('Spending Score (1-100)')
    plt.ylabel('Annual Income (k$)')
    plt.title('Customer Segmentation')

    # Save the plot to a buffer
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    # Encode the plot to base64 string for displaying in HTML
    plot_url = base64.b64encode(buf.getvalue()).decode('utf8')
    return render_template('plot.html', plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
