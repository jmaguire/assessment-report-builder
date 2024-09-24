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
    question_columns = [
        col for col in pivot_df.columns if col not in metadata_columns]

    # Sort question columns using natural sorting
    sorted_question_columns = natsorted(
        question_columns, key=lambda col: str(col))

    # Reorder DataFrame with metadata columns first, followed by sorted question columns
    pivot_df = pivot_df[metadata_columns + sorted_question_columns]

    return pivot_df


def transform_export(
    df: pd.DataFrame,
    assessment_metadata: List[str],
    question_number_column: str = 'questionNumber',
    question_text_column: str = 'questionText',
    question_new_column: str = 'question',
    pivot_column: str = 'question',
    pivot_value: str = 'answer'
) -> pd.DataFrame:
    """
    Transforms the exported DataFrame into the new report format.

    Args:
        df (pd.DataFrame): The input DataFrame containing the export data.
        assessment_metadata (List[str]): List of metadata fields to include.
        question_number_column (str, optional): Column name for question number. Defaults to 'questionNumber'.
        question_text_column (str, optional): Column name for question text. Defaults to 'questionText'.
        question_new_column (str, optional): New column name for combined question. Defaults to 'question'.
        pivot_column (str, optional): The column to pivot on. Defaults to 'question'.
        pivot_value (str, optional): The value column to aggregate. Defaults to 'answer'.

    Returns:
        pd.DataFrame: The transformed DataFrame ready for reporting.
    """
    df[question_new_column] = df[question_number_column].astype(
        str) + ": " + df[question_text_column]
    pivot_df = get_pivoted_data(
        df, assessment_metadata, pivot_column, pivot_value)
    return pivot_df


def main(
    input_csv_path: str,
    output_csv_path: str,
    assessment_metadata: List[str],
    question_number_column: str = 'questionNumber',
    question_text_column: str = 'questionText',
    question_new_column: str = 'question',
    pivot_column: str = 'question',
    pivot_value: str = 'answer',
    encoding: str = 'utf-8'
) -> None:
    """
    Processes the data export and generates a transformed report.

    Args:
        input_csv_path (str): Path to the input CSV file.
        output_csv_path (str): Path where the output CSV will be saved.
        assessment_metadata (List[str]): List of metadata fields to include.
        question_number_column (str, optional): Column name for question number. Defaults to 'questionNumber'.
        question_text_column (str, optional): Column name for question text. Defaults to 'questionText'.
        question_new_column (str, optional): New column name for combined question. Defaults to 'question'.
        pivot_column (str, optional): The column to pivot on. Defaults to 'question'.
        pivot_value (str, optional): The value column to aggregate. Defaults to 'answer'.
        encoding (str, optional): Encoding for the output CSV. Defaults to 'utf-8'.
    """
    # Read input data
    df = pd.read_csv(input_csv_path)

    # Transform data
    transformed_df = transform_export(
        df,
        assessment_metadata,
        question_number_column,
        question_text_column,
        question_new_column,
        pivot_column,
        pivot_value
    )

    # Output the transformed data
    transformed_df.to_csv(output_csv_path, encoding=encoding, index=False)


if __name__ == "__main__":
    main(
        input_csv_path='bulk_export.csv',
        output_csv_path='questions_as_columns.csv',
        assessment_metadata=['partner', 'product',
                             'recipient', 'period', 'industry', 'grade'],
    )
