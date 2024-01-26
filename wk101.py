import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('FormattedData.csv')

# Group data by 'Local Areas' and 'Wider Ethnic Group'
grp = data.groupby(['Local Areas', 'Wider Ethnic Group'])['Count'].sum().unstack(fill_value=0)

# Calculate the total count per local area
grp['Total'] = grp.sum(axis=1)

grp['NW Count'] = grp['Total'] - grp.get('White', 0)

# Calculate the percentage of non-white individuals per local area
grp['NW Percentage'] = (grp['NW Count'] / grp['Total']) * 100

# We only need the 'NW Percentage' column for the final output
nw_pct = grp['NW Percentage'].reset_index()

stats = nw_pct['NW Percentage'].describe()
stats_dict = stats.to_dict()

# Extract the required values
min_val = stats_dict['min']
max_val = stats_dict['max']
q1 = stats_dict['25%']
median_val = stats_dict['50%']
q3 = stats_dict['75%']

# Add these values to the boxplot as text annotations
plt.figure(figsize=(10, 6))
plt.boxplot(nw_pct['NW Percentage'])
plt.title('Boxplot of Non-White Percentage by Local Area')
plt.ylabel('Non-White Percentage')
plt.xticks([1], ['Local Areas'])

# Annotate the summary statistics on the plot
plt.text(1.1, min_val, f'Min: {min_val:.2f}%')
plt.text(1.1, q1, f'Q1: {q1:.2f}%')
plt.text(1.1, median_val, f'Median: {median_val:.2f}%')
plt.text(1.1, q3, f'Q3: {q3:.2f}%')
plt.text(1.1, max_val, f'Max: {max_val:.2f}%')

# Annotate "Dacorum" for its non-white percentage
dac_pct = nw_pct[nw_pct['Local Areas'] == 'Dacorum']['NW Percentage'].values[0]
plt.text(1.1, dac_pct, f'Dacorum: {dac_pct:.2f}%', color='red')

# Show the boxplot with annotations
plt.show()

# Return the summary statistics
stats_dict