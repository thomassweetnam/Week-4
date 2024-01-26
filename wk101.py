import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2_contingency

def non_white_pct_bxplt(data_file):
    data = pd.read_csv(data_file)
    # Group data by 'Local Areas' and 'Wider Ethnic Group'
    grp = data.groupby(['Local Areas', 'Wider Ethnic Group'])['Count'].sum().unstack(fill_value=0)

    grp['Total'] = grp.sum(axis=1)

    grp['NW Count'] = grp['Total'] - grp.get('White', 0)

    # Calculate the percentage of non-white individuals per local area
    grp['NW Percentage'] = (grp['NW Count'] / grp['Total']) * 100

    nw_pct = grp['NW Percentage'].reset_index()

    stats = nw_pct['NW Percentage'].describe()
    stats_dict = stats.to_dict()

    min_val = stats_dict['min']
    max_val = stats_dict['max']
    q1 = stats_dict['25%']
    median_val = stats_dict['50%']
    q3 = stats_dict['75%']

    # Create the boxplot
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

    dac_pct = nw_pct[nw_pct['Local Areas'] == 'Dacorum']['NW Percentage'].values[0]
    plt.text(1.1, dac_pct, f'Dacorum: {dac_pct:.2f}%', color='red')

    # Show the boxplot with annotations
    plt.show()

    # Return the summary statistics
    return stats_dict


def ethnic_pct_chart(data_file, area):
    df = pd.read_csv(data_file)

    df_filt = df[df["Wider Ethnic Group"] != "White"]

    # Filter data for specified "Local Area"
    df_area = df_filt[df_filt["Local Areas"] == area]

    # Calculate total counts for entire dataset and specified "Local Area"
    total_count = df_filt["Count"].sum()
    area_count = df_area["Count"].sum()

    df_filt_pct = df_filt.copy()
    df_filt_pct["Pct Share Total"] = (df_filt["Count"] / total_count) * 100

    df_area_pct = df_area.copy()
    df_area_pct["Pct Share Area"] = (df_area["Count"] / area_count) * 100

    pct_total = df_filt_pct.groupby("Wider Ethnic Group")["Pct Share Total"].sum()
    pct_area = df_area_pct.groupby("Wider Ethnic Group")["Pct Share Area"].sum()

    # Array of indices for x-axis positions
    indices = np.arange(len(pct_total.index))

    bar_w = 0.4
    plt.figure(figsize=(12, 6))

    # Plot percentage share for entire dataset
    bars1 = plt.bar(indices - bar_w/2, pct_total, width=bar_w, label="All Areas", color="skyblue")

    bars2 = plt.bar(indices + bar_w/2, pct_area, width=bar_w, label=area, color="orange")

    # Set x-axis labels
    plt.xticks(indices, pct_total.index, rotation=45, ha="right")

    plt.title(f"Ethnic Group Pct Share (Excl. White) - {area}")
    plt.xlabel("Ethnic Group")
    plt.ylabel("Pct Share")

    plt.legend()

    # Function to add values on top of bars
    def add_values(bars):
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height:.2f}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3), textcoords='offset points', ha='center', va='bottom')

    add_values(bars1)
    add_values(bars2)

    # Show plot
    plt.tight_layout()
    plt.show()


def ethnic_diff_chart(data_file, area):
    df = pd.read_csv(data_file)

    # Filter data for all areas
    data_all = df[(df['Ethnic Group ID'] >= 88) & (df['Ethnic Group ID'] <= 144)]

    # Group by Ethnic Group and sum counts across all areas
    grouped_all = data_all.groupby('Ethnic Group')['Count'].sum().reset_index()

    total_all = grouped_all['Count'].sum()

    grouped_all['Pct Share All'] = (grouped_all['Count'] / total_all) * 100

    # Filter data for specified area
    data_area = df[(df['Local Areas'] == area) & (df['Ethnic Group ID'] >= 88) & (df['Ethnic Group ID'] <= 144)]

    grouped_area = data_area.groupby('Ethnic Group')['Count'].sum().reset_index()

    total_area = grouped_area['Count'].sum()

    # Percentage share for each ethnic group in area
    grouped_area['Pct Share Area'] = (grouped_area['Count'] / total_area) * 100

    compare_df = pd.merge(grouped_all, grouped_area, on='Ethnic Group', how='outer')

    # Percentage share difference
    compare_df['Pct Share Diff'] = compare_df['Pct Share Area'] - compare_df['Pct Share All']

    sorted_df = compare_df.sort_values(by='Pct Share Diff', ascending=False)
    sorted_df['Ethnic Group'] = sorted_df['Ethnic Group'].str.replace('Mixed or Multiple ethnic groups: ', '')

    # Top and bottom 5 differences
    top_5_diff = sorted_df.head(5)
    bottom_5_diff = sorted_df.tail(5)

    # Create figure with subplots
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot top 5 differences
    ax_top.bar(top_5_diff['Ethnic Group'], top_5_diff['Pct Share Diff'], color='blue')
    ax_top.set_title(f'Top 5 Percentage Differences for Mixed Ethic Group: {area} vs All Areas')
    ax_top.set_ylabel('Pct Share Diff')
    ax_top.tick_params(axis='x', rotation=45)

    # Plot bottom 5 differences
    ax_bot.bar(bottom_5_diff['Ethnic Group'], bottom_5_diff['Pct Share Diff'], color='red')
    ax_bot.set_title(f'Bottom 5 Percentage Differences for Mixed Ethic Group: {area} vs All Areas')
    ax_bot.set_ylabel('Pct Share Diff')
    ax_bot.tick_params(axis='x', rotation=45)

    # Adjust spacing
    plt.tight_layout()

    # Show plot
    plt.show()



def chi_square_test(data_file, local_area):
    df = pd.read_csv(data_file)

    # Filter the data for the specified "Local Area"
    local_df = df[df['Local Areas'] == local_area]

    national_wider_counts = df.groupby('Wider Ethnic Group')['Count'].sum()

    # Aggregate the counts for each wider ethnic group for the specified "Local Area"
    local_wider_counts = local_df.groupby('Wider Ethnic Group')['Count'].sum()

    # Create DataFrames for the national and specified "Local Area" wider totals
    national_wider_averages = national_wider_counts.reset_index()
    local_wider_averages = local_wider_counts.reset_index()

    # Merge the specified "Local Area" data with the national wider averages
    merged_wider_data = local_wider_averages.merge(national_wider_averages, on='Wider Ethnic Group', suffixes=('_local', '_national'))

    total_local_population = merged_wider_data['Count_local'].sum()
    total_national_population = merged_wider_data['Count_national'].sum()

    merged_wider_data['Expected'] = merged_wider_data['Count_national'] / total_national_population * total_local_population

    # Prepare the observed and expected counts for the Chi-Square Test
    observed_wider = merged_wider_data['Count_local'].values
    expected_wider = merged_wider_data['Expected'].values

    chi2_wider, p_value_wider, dof_wider, _ = chi2_contingency(np.array([observed_wider, expected_wider]))

    return chi2_wider, p_value_wider, dof_wider
