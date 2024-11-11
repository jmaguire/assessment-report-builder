# assessment-report-builder
Takes tabular data for assessment question and answers and outputs a format with questions as columns

Data input and export format
------
Sample input format

| assessmentId | partner | product| country | questionNumber | questionText | answerText |
| ------------- |-------------| -----|-----| -----| -----| -----| 
| 34  | Partner 1 | Product 1 | United States | A.1 | Lorem ipsum dolor sit amet | Yes |
| 34  | Partner 1 | Product 1 | United States | A.2 | Excepteur sint occaecat cupidatat | Yes |
| 37  | Partner 2 | Product 2 | France | A.1 | Lorem ipsum dolor sit amet | No |
| 37  | Partner 2 | Product 2 | France | A.2 | Excepteur sint occaecat cupidatat | Yes |
| 37  | Partner 3 | Product 3 | Germany | A.1 | Lorem ipsum dolor sit amet | N/A |
| 37  | Partner 3 | Product 3 | Germany | A.2 | Excepteur sint occaecat cupidatat | N/A |

Sample export format (questions as columns)

| Partner Name | A.1 Lorem ipsum dolor sit amet | A.2 Excepteur sint occaecat cupidatat |
| ------------- |-------------| -----|
| Partner 1  | Product 1 |  Yes | Yes |
| Partner 2  | Product 2 | No | Yes |
| Partner 3  | Product 3 | N/A| N/A |

Sample export format (assessment comparison

|  |  |Partner 1 | Partner 2| Partner 3 |
| ------------- |-------------| -----| ---| ---|
|  |  |Product 1|Product 2| Product 3|
|  |  |United States|France| Germany|
| questionNumber | questionText | answer | answer | answer | 
|  A.1 | Lorem ipsum dolor sit amet | Yes | No | N/A | 
|  A.2 | Excepteur sint occaecat cupidatat | Yes | Yes | N/A |


Usage
------
I've designed these to eventually plug into an API so go to the file and adjust the main function

Requirements
------
- python3
- pandas
- natsort
- file must include headers shown in the sample input format
