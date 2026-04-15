import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("This would be the path to a csv if I had one")
df.head()
df.info()
df.describe()
# Check missing values
print(df.isnull().sum())

# Drop rows missing critical fields
df = df.dropna(subset=['Category', 'Rating', 'Installs', 'Price'])

# Fill Rating (if needed)
df['Rating'].fillna(df['Rating'].median(), inplace=True)
#Clean Data
df['Installs'] = df['Installs'].str.replace(',', '')
df['Installs'] = df['Installs'].str.replace('+', '')
df['Installs'] = df['Installs'].astype(int)
#Price
df['Price'] = df['Price'].str.replace('$', '')
df['Price'] = df['Price'].astype(float)
#Remove Duplicates
df = df.drop_duplicates()
#Data Visualization
print(df['Category'].unique())
print(df['Content Rating'].unique())

# Remove extreme ratings
df = df[(df['Rating'] >= 1) & (df['Rating'] <= 5)]

# Remove extreme installs (optional)
df = df[df['Installs'] < df['Installs'].quantile(0.99)]

# Remove extreme price outliers
df = df[df['Price'] < df['Price'].quantile(0.99)]

Analisis
category_rating = df.groupby('Category')['Rating'].mean().sort_values(ascending=False)

plt.figure()
category_rating.head(10).plot(kind='bar')
plt.title("Top Categories by Average Rating")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
plt.show()

category_installs = df.groupby('Category')['Installs'].sum().sort_values(ascending=False)
#Categories with most instals
plt.figure()
category_installs.head(10).plot(kind='bar')
plt.title("Top Categories by Total Installs")
plt.ylabel("Installs")
plt.xticks(rotation=45)
plt.show()

#Pricing Vs. Ratings
plt.figure()
plt.scatter(df['Price'], df['Rating'])
plt.title("Price vs Rating")
plt.xlabel("Price")
plt.ylabel("Rating")
plt.show()

#Free vs, paid
df['Type'] = df['Type'].fillna('Free')

type_analysis = df.groupby('Type')[['Rating', 'Installs']].mean()

print(type_analysis)