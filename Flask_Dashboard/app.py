from flask import Flask, render_template, jsonify, request
import pandas as pd
import plotly
import plotly.express as px
import json

app = Flask(__name__)

# Load segmentation data
def load_segmentation_data():
    df = pd.read_csv('segmentation_results.csv')
    return df

# Dashboard route
@app.route('/')
def dashboard():
    df = load_segmentation_data()

    # Initial charts for the entire dataset
    segment_pie = px.pie(df, names='Segment', title='Customer Segment Distribution')
    pie_json = json.dumps(segment_pie, cls=plotly.utils.PlotlyJSONEncoder)

    feature_bar = px.bar(df, x='CustomerID', y=['Feature1', 'Feature2'], title='Customer Features')
    bar_json = json.dumps(feature_bar, cls=plotly.utils.PlotlyJSONEncoder)

    segments = df['Segment'].unique().tolist()
    return render_template('dashboard.html', pie_chart=pie_json, bar_chart=bar_json, segments=segments)

# API for updating charts based on segment filter
@app.route('/filter', methods=['POST'])
def filter_data():
    segment = request.form.get('segment')
    df = load_segmentation_data()

    if segment != 'All':
        df = df[df['Segment'] == int(segment)]

    # Update the charts for the selected segment
    segment_pie = px.pie(df, names='Segment', title='Segment Distribution')
    pie_json = json.dumps(segment_pie, cls=plotly.utils.PlotlyJSONEncoder)

    feature_bar = px.bar(df, x='CustomerID', y=['Feature1', 'Feature2'], title='Customer Features')
    bar_json = json.dumps(feature_bar, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({'pie_chart': pie_json, 'bar_chart': bar_json})

@app.route('/')
def dashboard():
    df = load_segmentation_data()

    # KPIs
    total_customers = len(df)
    avg_feature1 = df['Feature1'].mean()
    avg_feature2 = df['Feature2'].mean()

    # Generate charts
    segment_pie = px.pie(df, names='Segment', title='Customer Segment Distribution')
    pie_json = json.dumps(segment_pie, cls=plotly.utils.PlotlyJSONEncoder)

    feature_bar = px.bar(df, x='CustomerID', y=['Feature1', 'Feature2'], title='Customer Features')
    bar_json = json.dumps(feature_bar, cls=plotly.utils.PlotlyJSONEncoder)

    segments = df['Segment'].unique().tolist()
    return render_template('dashboard.html', pie_chart=pie_json, bar_chart=bar_json, 
                           segments=segments, total_customers=total_customers,
                           avg_feature1=avg_feature1, avg_feature2=avg_feature2)
