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


# group the df by club and count the number of assists
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
          'Moldova': '#4dd4b4', 
          'Switzerland': '#d9534f',
          'Russia': '#4089a8'}

# Filter out countries with more than 0 assists
countries_with_assists = assists[assists['Assists'] > 0]['Country'].unique()

# Create a new dictionary for countries with more than 0 assists
colors_with_assists = {}
for country, color in colors.items():
    if country in countries_with_assists:
        colors_with_assists[country] = color

# plot a horizontal bar chart of the number of assists by club, colored by country
fig, ax = plt.subplots(figsize=(10, 10))
ax.barh(assists['club'], assists['Assists'], color=assists['Country'].map(colors))
ax.set_title('Number of Assists by Club', fontsize=20)
ax.set_xlabel('Number of Assists', fontsize=14)
ax.set_ylabel('Club', fontsize=14)
ax.tick_params(axis='both', which='major', labelsize=12)

# Add a legend to the plot
handles, labels = [], []
for country, color in colors_with_assists.items():
    handles.append(plt.Rectangle((0, 0), 1, 1, color=color, ec='k'))
    labels.append(country)
ax.legend(handles, labels, loc='upper right', fontsize=11.7)
plt.show()
