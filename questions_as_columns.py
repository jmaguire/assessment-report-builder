from natsort import natsorted
import pandas as pd
from typing import List


def get_pivoted_data(
  df: pd.DataFrame, 
  pivot_index: List[str], 
  pivot_column: str, 
  pivot_value: str
) -> pd.DataFrame:
    """
    Pivots the DataFrame based on specified index, column, and value.

    Args:
        df (pd.DataFrame): The input DataFrame containing assessment data.
        pivot_index (List[str]): List of columns to set as the pivot index.
        pivot_column (str): The column to pivot on.
        pivot_value (str): The value column to aggregate.

    Returns:
        pd.DataFrame: The pivoted DataFrame.
    """
    pivot_df = df.pivot_table(
        index=pivot_index,
        columns=pivot_column,
        values=pivot_value,
        aggfunc='first'
    ).reset_index()
    
    # Extract assessment metadata columns (pivot_index)
    metadata_columns = pivot_index
    
    # Extract question columns (all columns that are not in metadata)
    question_columns = [col for col in pivot_df.columns if col not in metadata_columns]
    
    # Sort question columns using natural sorting
    sorted_question_columns = natsorted(question_columns, key=lambda col: str(col))

    # Reorder DataFrame with metadata columns first, followed by sorted question columns
    pivot_df = pivot_df[metadata_columns + sorted_question_columns]
    
    return pivot_df


def transform_export(
    df: pd.DataFrame,
    assessment_metadata: List[str],
) -> pd.DataFrame:
    """
    Transforms the exported DataFrame into the new report format.

    Args:
        df (pd.DataFrame): The input DataFrame containing the export data.
        assessment_metadata (List[str]): List of metadata fields to include.
        pivot_index (List[str]): List of columns to set as the pivot index.
        pivot_column (str): The column to pivot on.
        pivot_value (str): The value column to aggregate.

    Returns:
        pd.DataFrame: The transformed DataFrame ready for reporting.
    """
    df['question'] = df['questionNumber'] + ": " + df['questionText']
    pivot_df = get_pivoted_data(df, assessment_metadata, 'question', 'answer')
    return pivot_df

def main(
    input_csv_path: str,
    output_csv_path: str,
    assessment_metadata: List[str],
) -> None:
    """
    Main function to execute the data transformation.

    Args:
        input_csv_path (str): Path to the input CSV file.
        output_csv_path (str): Path where the output CSV will be saved.
        assessment_metadata (List[str]): List of metadata fields to include.
        pivot_index (List[str]): List of columns to set as the pivot index.
        pivot_column (str): The column to pivot on.
        pivot_value (str): The value column to aggregate.
    """
    # Read input data
    df = pd.read_csv(input_csv_path)
    
    # Transform data
    transformed_df = transform_export(
        df,
        assessment_metadata,
    )
    
    # Output the transformed data
    transformed_df.to_csv(output_csv_path, encoding='utf-8', index=False)

if __name__ == "__main__":
    main(
        input_csv_path='bulk_export.csv',
        output_csv_path='questions_as_columns.csv',
        assessment_metadata=['partner', 'product', 'recipient', 'period', 'industry', 'grade'],
    )
