import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg

import matplotlib.pyplot as plt
import pandas as pd

# Read the data from the CSV file
data = pd.read_csv('PPA_results.csv')
    
def boxplot(data):

    # Group the data by configuration
    grouped_data = data.groupby('Configuration')['Cost'].apply(list)

    # Convert the grouped data to a list of lists
    boxplot_data = grouped_data.tolist()

    # Create the boxplot
    plt.boxplot(boxplot_data)

    # Set the x-axis labels
    labels = [label.split(' ')[-1][6:] for label in grouped_data.index]
    plt.xticks(range(1, len(grouped_data) + 1), labels)

    # Set the y-axis label
    plt.ylabel('Cost')

    # Set the title
    plt.title('Boxplot of Costs by Configuration')

    # Show the plot
    plt.savefig('boxplot PPA')

def compare(data):
    # Filter the data for config2 and config8
    filtered_data = data[data['Configuration'].isin(['PPA config2', 'PPA config8'])]

    # Create a boxplot
    labels = filtered_data['Configuration'].unique()
    values = [filtered_data[filtered_data['Configuration'] == label]['Cost'] for label in labels]
    plt.boxplot(values, labels=labels)

    # Set the y-axis label
    plt.ylabel('Cost')

    # Set the title
    plt.title('Comparison of Cost - config2 vs config8')

    # Save the plot as an image
    plt.savefig('compare2_8_boxplot.png')


compare(data)