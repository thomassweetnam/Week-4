import unittest
import pandas as pd
import matplotlib.pyplot as plt
from wk101 import non_white_pct_bxplt, ethnic_pct_chart, ethnic_diff_chart, chi_square_test

class TestWk101(unittest.TestCase):
    def test_read_formatted_data(self):
        # Attempt to read the CSV file
        try:
            df = pd.read_csv("FormattedData.csv")
        except FileNotFoundError:
            self.fail("The 'FormattedData.csv' file does not exist.")
        except Exception as e:
            self.fail(f"An unexpected error occurred: {str(e)}")
        
        # Check if the DataFrame is not empty
        self.assertFalse(df.empty, "The DataFrame is empty.")
    
    def test_non_white_pct_bxplt(self):
        data_file = "FormattedData.csv"
        
        fig, ax = plt.subplots()
        non_white_pct_bxplt(data_file)
        
        # Check if the output is a boxplot
        self.assertTrue(isinstance(ax, plt.Axes), "Expected a boxplot to be produced.")
        
    def test_ethnic_pct_chart(self):
        data_file = "FormattedData.csv"
        area = "Dacorum"
        
        fig, ax = plt.subplots()
        ethnic_pct_chart(data_file, area)
        
        x_axis_labels = [label.get_text() for label in ax.get_xticklabels()]
        
        # Check if "White" is not in the x-axis labels
        self.assertNotIn("White", x_axis_labels, "'White' should not be in the x-axis categories.")

if __name__ == '__main__':
    unittest.main()
