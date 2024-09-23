import pandas as pd
from typing import Dict, List, Tuple

def get_meta_data_fields(
  df: pd.DataFrame, 
  metadata_columns: List[str], 
  pivot_column: str
) -> Dict[str, Dict]:
    """
    Extracts assessment metadata indexed by assessment ID.

    Args:
        df (pd.DataFrame): The input DataFrame containing assessment data.
        metadata_columns (List[str]): List of metadata column names.
        pivot_column (str): The column name to pivot on (used as the index).

    Returns:
        Dict[int, Dict[str, any]]: A dictionary mapping each assessment ID to its metadata.
    """
    if pivot_column not in metadata_columns:
        metadata_columns = [pivot_column] + metadata_columns
    return df[metadata_columns].drop_duplicates().set_index(pivot_column).to_dict('index')

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
    return pivot_df

def get_new_columns(
    pivot_df: pd.DataFrame, 
    metadata: Dict[int, Dict[str, any]], 
    assessment_metadata: List[str], 
    pivot_value: str
) -> List[Tuple]:
    """
    Constructs new MultiIndex columns based on metadata.

    Args:
        pivot_df (pd.DataFrame): The pivoted DataFrame.
        metadata (Dict[int, Dict[str, any]]): Metadata indexed by assessment ID.
        assessment_metadata (List[str]): List of metadata fields.
        pivot_value (str): The name of the value column.

    Returns:
        List[Tuple]: A list of tuples representing the new MultiIndex columns.
    """
    new_columns = []
    metadata_count = len(metadata)
    for col in pivot_df.columns:
        if col in metadata.keys(): 
            assessment_id = int(col)
            metadata_for_col = metadata.get(assessment_id, {})
            metadata_as_list = [metadata_for_col[key] for key in assessment_metadata]
            metadata_as_list.append(pivot_value)
            new_columns.append((metadata_as_list))
        else:
            new_columns.append( ('',) * metadata_count + (col,))
    return new_columns

def transform_export(
    df: pd.DataFrame,
    assessment_metadata: List[str],
    pivot_index: List[str],
    pivot_column: str,
    pivot_value: str
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
    pivot_df = get_pivoted_data(df, pivot_index, pivot_column, pivot_value)
    metadata = get_meta_data_fields(df, assessment_metadata, pivot_column)
    new_columns = get_new_columns(pivot_df, metadata, assessment_metadata, pivot_value)
    pivot_df.columns = pd.MultiIndex.from_tuples(new_columns)
    return pivot_df

def main(
    input_csv_path: str,
    output_csv_path: str,
    assessment_metadata: List[str],
    pivot_index: List[str],
    pivot_column: str,
    pivot_value: str
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
        pivot_index,
        pivot_column,
        pivot_value
    )
    
    # Output the transformed data
    transformed_df.to_csv(output_csv_path, encoding='utf-8', index=False)

if __name__ == "__main__":
    main(
        input_csv_path='sample_export.csv',
        output_csv_path='sample_result.csv',
        assessment_metadata=['partner', 'product', 'recipient', 'period', 'industry', 'grade'],
        pivot_index=['questionNumber', 'questionText'],
        pivot_column='assessmentId',
        pivot_value='answer'
    )