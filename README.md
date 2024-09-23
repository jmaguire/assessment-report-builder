# assessment-report-builder
Takes tabular data for assessment question and answers and outputs a format with questions as columns

Data input and export format
------
Sample input format

| assessmentId | partner | product| questionNumber | questionTex | answerText |
| ------------- |-------------| -----| -----| -----| -----| 
| 34  | Partner 1 | Product 1 | A.1 | Lorem ipsum dolor sit amet | Yes |
| 34  | Partner 1 | Product 1 | A.2 | Excepteur sint occaecat cupidatat | Yes |
| 37  | Partner 1 | Product 2 | A.1 | Lorem ipsum dolor sit amet | No |
| 37  | Partner 2 | Product 2 | A.2 | Excepteur sint occaecat cupidatat | Yes |

Sample export format (questions as columns)

| Partner Name | A.1 Lorem ipsum dolor sit amet | A.2 Excepteur sint occaecat cupidatat |
| ------------- |-------------| -----|
| Partner 1  | Product 1 |  Yes | Yes |
| Partner 1  | Product 2 | No| Yes |

Sample export format (assessment comparison

|  |  |Partner 1 | Partner 2|
| ------------- |-------------| -----| ---|
|  |  |Product 1|Product 2|
| questionNumber | questionText | answer | answer |
|  A.1 | Lorem ipsum dolor sit amet | Yes | No |
|  A.2 | Excepteur sint occaecat cupidatat | Yes | Yes |


Usage
------
I've designed these to eventually plug into an API so go to the file and adjust the main function

Requirements
------
- python3
- pandas
- natsort
- file must include headers shown in the sample input format
