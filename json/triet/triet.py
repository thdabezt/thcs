# Input and output file paths
input_txt = r"C:\Users\Admin\Documents\html and shit\thcs\json\triet\triet_copy.txt"  # Input text file
output_json = r"C:\Users\Admin\Documents\html and shit\thcs\json\triet\triets.json"  # Output JSON file

import re
import json

def parse_questions(input_txt):
    with open(input_txt, "r", encoding="utf-8") as file:
        content = file.read()

    # Normalize the text to handle irregularities
    content = content.replace("\n", " ")  # Replace newlines with spaces

    # Find all questions using the pattern "Câu X:" followed by "Câu X+1:" or end of file
    question_blocks = re.split(r"(Câu \d+:)", content)
    questions_data = []

    for i in range(1, len(question_blocks) - 1, 2):
        question_number = question_blocks[i].strip()  # "Câu X:"
        raw_question = question_blocks[i + 1].strip()  # Content of the question

        # Extract choices
        choices = []
        current_index = 0
        for option in ["A. ", "B. ", "C. ", "D. ", "E. "]:
            match = re.search(rf"{re.escape(option)}(.*?)(?=(\s[A-E]\. |\sĐáp án:|$))", raw_question[current_index:], re.DOTALL)
            if match:
                choice_text = match.group(1).strip()
                # Check if this option contains "Cả " and extend until "Đáp án:" or end of the block
                if "Cả " in choice_text:
                    end_match = re.search(r"Đáp án:|$", raw_question[current_index + match.end():], re.DOTALL)
                    if end_match:
                        choice_text += " " + raw_question[current_index + match.end():current_index + match.end() + end_match.start()].strip()
                choices.append(f"{option}{choice_text.strip()}")
                current_index += match.end()

        # Extract the correct answer
        answer_match = re.search(r"Đáp án:\s*([A-E])", raw_question)
        correct_answer = ord(answer_match.group(1)) - ord("A") if answer_match else None

        # Extract the question text (everything before "A. ")
        question_text_match = re.match(r"(.*?)(?=A\. )", raw_question)
        question_text = question_text_match.group(1).strip() if question_text_match else ""

        # Prepend the question number to the question text
        if question_text:
            question_text = f"{question_number} {question_text}"

        # Add to the list if all parts are valid
        if question_text and choices and correct_answer is not None:
            questions_data.append({
                "question": question_text,
                "choices": choices,
                "answer": correct_answer
            })

    return questions_data

def save_as_json(questions_data, output_json):
    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(questions_data, json_file, ensure_ascii=False, indent=4)

# Process the text file and save the JSON
def process_text_to_json(input_txt, output_json):
    questions = parse_questions(input_txt)
    save_as_json(questions, output_json)
    print(f"Questions extracted and saved to {output_json}")

process_text_to_json(input_txt, output_json)
