import unittest
import pandas as pd
import matplotlib.pyplot as plt
from wk101 import calculate_summary_statistics, load_and_preprocess_data

class TestWk101Code(unittest.TestCase):
    def setUp(self):
        # Load the dataset and perform necessary preprocessing
        self.data = load_and_preprocess_data('FormattedData.csv')

    def test_data_loading(self):
        # Ensure that the dataset is loaded successfully
        self.assertIsNotNone(self.data)

    def test_grouping_and_calculations(self):
        grp, nw_pct = calculate_summary_statistics(self.data)

        # Ensure that the required columns are present
        self.assertIn('NW Percentage', grp.columns)
        self.assertIn('Total', grp.columns)
        self.assertIn('NW Count', grp.columns)

    def test_summary_statistics(self):
        grp, nw_pct = calculate_summary_statistics(self.data)
        stats_dict = nw_pct['NW Percentage'].describe().to_dict()

        # Ensure that summary statistics are correctly calculated
        self.assertIn('min', stats_dict)
        self.assertIn('max', stats_dict)
        self.assertIn('25%', stats_dict)
        self.assertIn('50%', stats_dict)
        self.assertIn('75%', stats_dict)

if __name__ == '__main__':
    unittest.main()