import unittest
import pandas as pd
from io import StringIO
from typing import Dict, List, Tuple

from assessment_comparison_report import (
    get_meta_data_fields,
    get_pivoted_data,
    get_new_columns,
    transform_export
)

class TestTransformExport(unittest.TestCase):
    def setUp(self):
        # Sample input data as a CSV string
        self.input_csv = StringIO("""
assessmentId,partner,product,country,questionNumber,questionText,answer
34,Partner 1,Product 1,United States,A.1,Lorem ipsum dolor sit amet,Yes
34,Partner 1,Product 1,United States,A.2,Excepteur sint occaecat cupidatat,Yes
37,Partner 2,Product 2,France,A.1,Lorem ipsum dolor sit amet,No
37,Partner 2,Product 2,France,A.2,Excepteur sint occaecat cupidatat,Yes
38,Partner 3,Product 3,Germany,A.1,Lorem ipsum dolor sit amet,N/A
38,Partner 3,Product 3,Germany,A.2,Excepteur sint occaecat cupidatat,N/A
""")
        # Read the sample data into a DataFrame
        self.df = pd.read_csv(self.input_csv,keep_default_na=False)
        
        # Define transformation parameters
        self.assessment_metadata = ['partner', 'product', 'country']
        self.pivot_index = ['questionNumber', 'questionText']
        self.pivot_column = 'assessmentId'
        self.pivot_value = 'answer'
    
    def test_get_meta_data_fields(self):
        expected_metadata = {
            34: {'partner': 'Partner 1', 'product': 'Product 1', 'country': 'United States'},
            37: {'partner': 'Partner 2', 'product': 'Product 2', 'country': 'France'},
            # Note: Partner 3 with assessmentId 37 is already included under 37
        }
        # Adjust the sample data to have unique assessmentIds per partner
        # In the sample, assessmentId 37 is used by both Partner 2 and Partner 3
        # To correct this, assume assessmentId uniquely identifies a single partner
        # For this test, let's modify the input data to have unique assessmentIds
        df_unique = pd.DataFrame({
            'assessmentId': [34, 34, 37, 37, 38, 38],
            'partner': ['Partner 1', 'Partner 1', 'Partner 2', 'Partner 2', 'Partner 3', 'Partner 3'],
            'product': ['Product 1', 'Product 1', 'Product 2', 'Product 2', 'Product 3', 'Product 3'],
            'country': ['United States', 'United States', 'France', 'France', 'Germany', 'Germany'],
            'questionNumber': ['A.1', 'A.2', 'A.1', 'A.2', 'A.1', 'A.2'],
            'questionText': [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat', 
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat',
                'Lorem ipsum dolor sit amet',
                'Excepteur sint occaecat cupidatat'
            ],
            'answer': ['Yes', 'Yes', 'No', 'Yes', 'N/A', 'N/A']
        })
        expected_metadata_unique = {
            34: {'partner': 'Partner 1', 'product': 'Product 1', 'country': 'United States'},
            37: {'partner': 'Partner 2', 'product': 'Product 2', 'country': 'France'},
            38: {'partner': 'Partner 3', 'product': 'Product 3', 'country': 'Germany'}
        }
        metadata = get_meta_data_fields(df_unique, self.assessment_metadata, self.pivot_column)
        self.assertEqual(metadata, expected_metadata_unique)
    
    def test_get_pivoted_data(self):
        pivoted = get_pivoted_data(
            self.df,
            self.pivot_index,
            self.pivot_column,
            self.pivot_value
        )
        # Expected pivoted DataFrame structure
        expected_data = {
            'questionNumber': ['A.1', 'A.2'],
            'questionText': [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat'
            ],
            34: ['Yes', 'Yes'],
            37: ['No', 'Yes'],
            38: ['N/A', 'N/A'],
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df = expected_df.rename_axis('assessmentId')
        self.assertTrue(pivoted.equals(expected_df))
    
    def test_get_new_columns(self):
        # Using a unique assessmentId DataFrame
        df_unique = pd.DataFrame({
            'assessmentId': [34, 34, 37, 37, 38, 38],
            'partner': ['Partner 1', 'Partner 1', 'Partner 2', 'Partner 2', 'Partner 3', 'Partner 3'],
            'product': ['Product 1', 'Product 1', 'Product 2', 'Product 2', 'Product 3', 'Product 3'],
            'country': ['United States', 'United States', 'France', 'France', 'Germany', 'Germany'],
            'questionNumber': ['A.1', 'A.2', 'A.1', 'A.2', 'A.1', 'A.2'],
            'questionText': [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat', 
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat',
                'Lorem ipsum dolor sit amet',
                'Excepteur sint occaecat cupidatat'
            ],
            'answer': ['Yes', 'Yes', 'No', 'Yes', 'N/A', 'N/A']
        })
        pivot_df = get_pivoted_data(
            df_unique,
            self.pivot_index,
            self.pivot_column,
            self.pivot_value
        )
        metadata = get_meta_data_fields(df_unique, self.assessment_metadata, self.pivot_column)
        expected_columns = [
            ('', '', 'questionNumber'),
            ('', '', 'questionText'),
            ('Partner 1', 'Product 1', 'United States', 'answer', '34'),
            ('Partner 2', 'Product 2', 'France', 'answer', '37'),
            ('Partner 3', 'Product 3', 'Germany', 'answer', '38'),
        ]
        # The expected_columns should be tuples with metadata fields and the assessmentId
        # But according to the get_new_columns function, it appends pivot_value
        # So each assessment column tuple should be (partner, product, country, 'answer')
        expected_new_columns = [
            ('', '', '', 'questionNumber'),
            ('', '', '', 'questionText'),
            ('Partner 1', 'Product 1', 'United States', 'answer'),
            ('Partner 2', 'Product 2', 'France', 'answer'),
            ('Partner 3', 'Product 3', 'Germany', 'answer'),
        ]
        new_columns = get_new_columns(pivot_df, metadata, self.assessment_metadata, 'answer')
        self.assertEqual(new_columns, expected_new_columns)
    
    def test_transform_export(self):
        # Adjust the sample data to have unique assessmentIds for accurate testing
        df_unique = pd.DataFrame({
            'assessmentId': [34, 34, 37, 37, 38, 38],
            'partner': ['Partner 1', 'Partner 1', 'Partner 2', 'Partner 2', 'Partner 3', 'Partner 3'],
            'product': ['Product 1', 'Product 1', 'Product 2', 'Product 2', 'Product 3', 'Product 3'],
            'country': ['United States', 'United States', 'France', 'France', 'Germany', 'Germany'],
            'questionNumber': ['A.1', 'A.2', 'A.1', 'A.2', 'A.1', 'A.2'],
            'questionText': [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat', 
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat',
                'Lorem ipsum dolor sit amet',
                'Excepteur sint occaecat cupidatat'
            ],
            'answer': ['Yes', 'Yes', 'No', 'Yes', 'N/A', 'N/A']
        })
        transformed_df = transform_export(
            df_unique,
            self.assessment_metadata,
            self.pivot_index,
            self.pivot_column,
            'answer'
        )
        
        # Define expected MultiIndex columns
        tuples = [
            ('', '', '', 'questionNumber'),
            ('', '', '', 'questionText'),
            ('Partner 1', 'Product 1', 'United States', 'answer'),
            ('Partner 2', 'Product 2', 'France', 'answer'),
            ('Partner 3', 'Product 3', 'Germany', 'answer'),
        ]
        expected_columns = pd.MultiIndex.from_tuples(tuples)
        
        # Define expected data
        expected_data = {
            ('', '', '', 'questionNumber'): ['A.1', 'A.2'],
            ('', '', '', 'questionText'): [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat'
            ],
            ('Partner 1', 'Product 1', 'United States', 'answer'): ['Yes', 'Yes'],
            ('Partner 2', 'Product 2', 'France', 'answer'): ['No', 'Yes'],
            ('Partner 3', 'Product 3', 'Germany', 'answer'): ['N/A', 'N/A']
        }
        expected_df = pd.DataFrame(expected_data)
        
        # Assign MultiIndex to expected_df columns
        expected_df.columns = expected_columns
        
        # Compare the transformed DataFrame with the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df, expected_df)
    
    def test_handle_missing_metadata(self):
        # Create a DataFrame with a missing metadata column (e.g., 'country' is missing for assessmentId 38)
        df_missing = pd.DataFrame({
            'assessmentId': [34, 34, 37, 37, 38, 38],
            'partner': ['Partner 1', 'Partner 1', 'Partner 2', 'Partner 2', 'Partner 3', 'Partner 3'],
            'product': ['Product 1', 'Product 1', 'Product 2', 'Product 2', 'Product 3', 'Product 3'],
            'country': ['United States', 'United States', 'France', 'France', None, None],
            'questionNumber': ['A.1', 'A.2', 'A.1', 'A.2', 'A.1', 'A.2'],
            'questionText': [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat', 
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat',
                'Lorem ipsum dolor sit amet',
                'Excepteur sint occaecat cupidatat'
            ],
            'answer': ['Yes', 'Yes', 'No', 'Yes', 'N/A', 'N/A']
        })
        transformed_df = transform_export(
            df_missing,
            self.assessment_metadata,
            self.pivot_index,
            self.pivot_column,
            self.pivot_value
        )
        
        # Define expected MultiIndex columns with empty strings for missing metadata
        tuples = [
            ('', '', '', 'questionNumber'),
            ('', '', '', 'questionText'),
            ('Partner 1', 'Product 1', 'United States', 'answer'),
            ('Partner 2', 'Product 2', 'France', 'answer'),
            ('Partner 3', 'Product 3', '', 'answer'),  # Missing 'country'
        ]
        expected_columns = pd.MultiIndex.from_tuples(tuples)
        
        # Define expected data
        expected_data = {
            ('', '', '', 'questionNumber'): ['A.1', 'A.2'],
            ('', '', '', 'questionText'): [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat'
            ],
            ('Partner 1', 'Product 1', 'United States', 'answer'): ['Yes', 'Yes'],
            ('Partner 2', 'Product 2', 'France', 'answer'): ['No', 'Yes'],
            ('Partner 3', 'Product 3', '', 'answer'): ['N/A', 'N/A']
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df.columns = expected_columns
        
        # Compare the transformed DataFrame with the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df, expected_df)
    
    
    def test_transform_export_with_additional_metadata(self):
        # Test transformation with additional metadata fields
        # Extend the metadata_columns to include 'recipient', 'period', 'industry', 'grade'
        # For simplicity, add these columns to the DataFrame
        df_extended = pd.DataFrame({
            'assessmentId': [34, 34, 37, 37, 38, 38],
            'partner': ['Partner 1', 'Partner 1', 'Partner 2', 'Partner 2', 'Partner 3', 'Partner 3'],
            'product': ['Product 1', 'Product 1', 'Product 2', 'Product 2', 'Product 3', 'Product 3'],
            'country': ['United States', 'United States', 'France', 'France', 'Germany', 'Germany'],
            'recipient': ['Recipient A', 'Recipient A', 'Recipient B', 'Recipient B', 'Recipient C', 'Recipient C'],
            'period': ['Q1', 'Q1', 'Q2', 'Q2', 'Q3', 'Q3'],
            'industry': ['Industry X', 'Industry X', 'Industry Y', 'Industry Y', 'Industry Z', 'Industry Z'],
            'grade': ['A', 'A', 'B', 'B', 'C', 'C'],
            'questionNumber': ['A.1', 'A.2', 'A.1', 'A.2', 'A.1', 'A.2'],
            'questionText': [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat', 
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat',
                'Lorem ipsum dolor sit amet',
                'Excepteur sint occaecat cupidatat'
            ],
            'answerText': ['Yes', 'Yes', 'No', 'Yes', 'N/A', 'N/A']
        })
        assessment_metadata_extended = ['partner', 'product', 'recipient', 'period', 'industry', 'grade']
        
        transformed_df = transform_export(
            df_extended,
            assessment_metadata_extended,
            self.pivot_index,
            self.pivot_column,
            'answerText'
        )
        
        # Define expected MultiIndex columns with extended metadata
        tuples = [
            ('', '', '', '', '', '', 'questionNumber'),
            ('', '', '', '', '', '', 'questionText'),
            ('Partner 1', 'Product 1', 'Recipient A', 'Q1', 'Industry X', 'A', 'answerText'),
            ('Partner 2', 'Product 2', 'Recipient B', 'Q2', 'Industry Y', 'B', 'answerText'),
            ('Partner 3', 'Product 3', 'Recipient C', 'Q3', 'Industry Z', 'C', 'answerText'),
        ]
        expected_columns = pd.MultiIndex.from_tuples(tuples)
        
        # Define expected data
        expected_data = {
            ('', '', '', '', '', '', 'questionNumber'): ['A.1', 'A.2'],
            ('', '', '', '', '', '', 'questionText'): [
                'Lorem ipsum dolor sit amet', 
                'Excepteur sint occaecat cupidatat'
            ],
            ('Partner 1', 'Product 1', 'Recipient A', 'Q1', 'Industry X', 'A', 'answerText'): ['Yes', 'Yes'],
            ('Partner 2', 'Product 2', 'Recipient B', 'Q2', 'Industry Y', 'B', 'answerText'): ['No', 'Yes'],
            ('Partner 3', 'Product 3', 'Recipient C', 'Q3', 'Industry Z', 'C', 'answerText'): ['N/A', 'N/A']
        }
        expected_df = pd.DataFrame(expected_data)
        expected_df.columns = expected_columns
        
        # Compare the transformed DataFrame with the expected DataFrame
        pd.testing.assert_frame_equal(transformed_df, expected_df)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
