import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

##Dataset Import
df = pd.read_csv("C:/Users/smita/Desktop/Internships24/CodeClause/Proj1_Customer_Segmentation/Datasets/Mall_Customers.csv")
df.head()
df.describe()

##Plotting
columns = ['Age', 'Annual Income (k$)', 'Spending Score (1-100)']
for i in columns:
    plt.figure()
    sns.displot(df[i])

columns = ('Age', 'Annual Income (k$)', 'Spending Score (1-100)')
for i in columns :
    plt.figure()
    sns.boxplot(data=df, x='Gender', y=df[i])

df['Gender'].value_counts(normalize=True)
sns.scatterplot(data=df, x='Annual Income (k$)', y='Spending Score (1-100)')

##Elbow Method
k_range = range(1,11)
inertia = []
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df[['Annual Income (k$)', 'Spending Score (1-100)']])
    inertia.append(kmeans.inertia_)
plt.figure(figsize=(8, 6))
plt.plot(k_range, inertia, 'bo-')
plt.xlabel('Number of clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method for Optimal k')
plt.show()

##Clustering and Scaling
features = df[['Spending Score (1-100)', 'Annual Income (k$)']]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[['Spending Score (1-100)', 'Annual Income (k$)']])

kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(features)

df['Cluster'] = kmeans.labels_

plt.scatter(df['Spending Score (1-100)'], df['Annual Income (k$)'], c=df['Cluster'], cmap='viridis')
plt.ylabel('Spending Score (1-100)')
plt.xlabel('Annual Income (k$)')
plt.title('Customer Segmentation')
plt.show()