import pandas as pd
import matplotlib.pyplot as plt

# create a dictionary of clubs and their countries
clubs = {'Ajax': 'Netherlands',
         'Atalanta': 'Italy',
         'Atlético': 'Spain',
         'Barcelona': 'Spain',
         'Bayern': 'Germany',
         'Benfica': 'Portugal',
         'Beşiktaş': 'Turkey',
         'Chelsea': 'England',
         'Club Brugge': 'Belgium',
         'Dortmund': 'Germany',
         'Dynamo Kyiv': 'Ukraine',
         'Inter': 'Italy',
         'Juventus': 'Italy',
         'LOSC': 'France',
         'Leipzig': 'Germany',
         'Liverpool': 'England',
         'Malmö FF': 'Sweden',
         'Man. City': 'England',
         'Man. United': 'England',
         'Milan': 'Italy',
         'Paris': 'France',
         'Porto': 'Portugal',
         'Real Madrid': 'Spain',
         'Salzburg': 'Austria',
         'Sevilla': 'Spain',
         'Shakhtar Donetsk': 'Ukraine',
         'Sheriff Tiraspol': 'Moldova',
         'Sporting CP': 'Portugal',
         'Villarreal': 'Spain',
         'VfL Wolfsburg': 'Germany',
         'BSC Young Boys': 'Switzerland',
         'Zenit': 'Russia'}

df = pd.read_csv('/Users/anshulhallur/Documents/ISTA 131 Spring 23/Final /attacking.csv')

# drop the first column
df = df.drop(df.columns[0], axis=1)

# add a new "Country" column based on the dictionary
df['Country'] = df['club'].map(clubs)
df.dropna(subset=['Country'], inplace=True) # drop rows with missing values


# group the DataFrame by club and count the number of assists
assists = df.groupby('club')['assists'].count().reset_index()

# rename the column to "Assists"
assists = assists.rename(columns={'assists': 'Assists'})

# add a new "Country" column to the "assists" df based on the dictionary
assists['Country'] = assists['club'].map(clubs)


# set colors for each country
colors = {'England': '#1f77b4',
          'Spain': '#ff7f0e',
          'Italy': '#2ca02c',
          'Germany': '#d62728',
          'France': '#9467bd',
          'Portugal': '#8c564b',
          'Netherlands': '#e377c2',
          'Belgium': '#7f7f7f',
          'Ukraine': '#bcbd22',
          'Turkey': '#17becf',
          'Austria': '#9c2e2e',
          'Sweden': '#f0ad4e',
          'Moldova': '#4dd4b4',  # Changed color for Moldova
          'Switzerland': '#d9534f',
          'Russia': '#4089a8'}

# group the assists DataFrame by Country and sum the number of assists
assists_by_country = assists.groupby('Country')['Assists'].sum().reset_index()

# Sort the assists_by_country DataFrame by the number of assists, in descending order
assists_by_country_sorted = assists_by_country.sort_values('Assists', ascending=False)

# Select the top 5 countries
top_5_countries = assists_by_country_sorted.head(5)

# Set up the plot and plot the pie chart
fig, ax = plt.subplots(figsize=(10, 10))
# Create the pie chart
ax.pie(
    x=top_5_countries['Assists'], # Data to plot
    labels=top_5_countries['Country'], # Set Label
    colors=top_5_countries['Country'].map(colors), # Set colors
    autopct='%1.1f%%', # Format for the percentage values
    startangle=90 # Angle at which to start
)

# Customize the plot
ax.set_title('Number of Assists by Country (Top 5)', fontsize=20)
ax.axis('equal')  # ensures that the pie chart is circular

# Add a legend to the plot
handles = []
for country in top_5_countries['Country']:
    if country in colors:
        handle = plt.Rectangle((0, 0), 1, 1, color=colors[country], ec='k')
        handles.append(handle)
labels = []
for country in top_5_countries['Country']:
    if country in colors:
        labels.append(country)
ax.legend(handles, labels, loc='upper right', fontsize=10)

# Set the font size of labels and percentages
for text in ax.texts:
    text.set_fontsize(12)

plt.show()


from scipy.stats import f_oneway

assists_list = []
for country in assists_by_country['Country']:
    country_assists = assists.loc[assists['Country'] == country, 'Assists'].values
    assists_list.append(country_assists)

f_statistic, p_value = f_oneway(*assists_list)
print("F statistic:", f_statistic)
print("P-value:", p_value)

"""
F statistic: 1.9894828330071475
P-value: 0.10249178302007035

"""
