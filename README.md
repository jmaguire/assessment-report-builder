# assessment-report-builder
Takes tabular data for assessment question and answers and outputs a format with questions as columns

Data input and export format
------
Sample input format

| Assessment Id | Assessment Name | Partner Name | Question Number | Question Text | Answer Text |
| ------------- |-------------| -----| -----| -----| -----| 
| 34  | Risk Audit | Partner 1 | A.1 | Lorem ipsum dolor sit amet | Yes |
| 34  | Risk Audit | Partner 1 | A.2 | Excepteur sint occaecat cupidatat | Yes |
| 37  | Risk Audit | Partner 2 | A.1 | Lorem ipsum dolor sit amet | No |
| 37  | Risk Audit | Partner 2 | A.2 | Excepteur sint occaecat cupidatat | Yes |

Sample export format

| Assessment Name | Partner Name | A.1 Lorem ipsum dolor sit amet | A.2 Excepteur sint occaecat cupidatat |
| ------------- |-------------| -----| -----|
| Risk Audit | Partner 1 |  Yes | Yes |
| Risk Audit | Partner 2 | No| Yes |

Usage
------
From the location of the python file call: `python3 rotate_question_data.py -f sample_export.csv`
Outputs `converted.csv` in the same location

Requirements
------
- python3
- file must include headers shown in the sample input format
