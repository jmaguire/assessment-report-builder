import argparse
import csv
import sys

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# Required fields in input csv file
PARTNER = 'Partner Name'
QUESTION = 'Question Text'
QUESTION_NUMBER= 'Question Number'
ANSWER = 'Answer Text'
ASSESSMENT = 'Assessment Name'
ASSESSMENT_ID = 'Assessment ID'

def main():
    # Usage: python3 rotate_question_data.py -f file.csv
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--file',
        help='JSON input file', 
        type=argparse.FileType('r')
    )
    args = parser.parse_args()

    if not args.file:
        parser.print_usage()
        return sys.exit(EXIT_FAILURE)

    report = {} 
    questions = set()
   
    # Iterate over the file and for each assessment id, create a new entry
    # with the questions as the columns
    try:
        with args.file as f:
            for row in csv.DictReader(f):
                assessment_id = row[ASSESSMENT_ID]
                if assessment_id not in report:
                    report[assessment_id] = {
                        PARTNER : row[PARTNER],
                        ASSESSMENT : row[ASSESSMENT],
                    }
                question_text = row[QUESTION_NUMBER] + ': ' + row[QUESTION]
                answer_text = row[ANSWER]
                report[assessment_id][question_text] = answer_text
                questions.add(question_text)
    except KeyError as k:
        print('Required field not found:', k)
        return sys.exit(EXIT_FAILURE)

    # Change the dictionary to a list by extracting each entry for each assessment
    report_list = [report[assessment_id] for assessment_id in report]

    # Sort the questions so the output file is predictable
    sorted_questions = sorted(list(questions), key=lambda item: (int(item.partition(' ')[0])
                               if item[0].isdigit() else float('inf'), item))

    header = [ASSESSMENT, PARTNER] + sorted_questions

    # Write file converted.csv with the data
    with open('converted.csv', 'w') as f:
        writer = csv.DictWriter(f, header)
        writer.writeheader()
        writer.writerows(report_list)
    
    return sys.exit(EXIT_SUCCESS)

if __name__ == '__main__':
    main()