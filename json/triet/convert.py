# Input and output file paths
input_txt = r"C:\Users\Admin\Documents\html and shit\thcs\json\triet\triet.txt"  # Input text file
output_txt = r"C:\Users\Admin\Documents\html and shit\thcs\json\triet\formatted_triet.txt"  # Output text file

import re

def convert_txt_to_formatted_txt(input_txt, output_txt):
    with open(input_txt, "r", encoding="utf-8") as file:
        content = file.read()

    # Split the content into raw questions based on "Câu [number]:"
    raw_questions = re.split(r"Câu\s+\d+:\s+", content)
    raw_questions = [q.strip() for q in raw_questions if q.strip()]  # Remove empty entries

    formatted_questions = []

    for i, raw_question in enumerate(raw_questions, start=1):
        # Extract the question text (before the first choice "A.")
        question_match = re.search(r"^(.*?)(?=\nA\.)", raw_question, re.DOTALL)
        question_text = question_match.group(1).strip().replace("\n", " ") if question_match else None

        # Extract the choices (e.g., "A.", "B.", etc.)
        choices = re.findall(r"([A-D]\..+?)(?=\n[A-D]\.|$)", raw_question, re.DOTALL)
        choices = [choice.strip().replace("\n", " ") for choice in choices]

        # Extract the correct answers (e.g., "Đáp án: A, B", "Đáp án: C và D")
        answer_match = re.search(r"Đáp án:\s*(.*)", raw_question)
        if answer_match:
            answer_text = answer_match.group(1).strip()
            # Extract individual letters (e.g., A, B, C) as answers
            answers = re.findall(r"[A-D]", answer_text)
            correct_answers = [ord(ans) - ord("A") for ans in answers]
        else:
            correct_answers = []

        # Skip invalid entries
        if question_text and choices and correct_answers:
            formatted_question = {
                "question": question_text,
                "choices": choices,
                "answer": correct_answers
            }
            formatted_questions.append(formatted_question)

    # Write the formatted questions to the output file
    with open(output_txt, "w", encoding="utf-8") as file:
        for question in formatted_questions:
            file.write(f"Question: {question['question']}\n")
            for choice in question['choices']:
                file.write(f"{choice}\n")
            file.write(f"Answer: {', '.join(map(str, question['answer']))}\n\n")

    print(f"Conversion complete. Formatted text saved to {output_txt}")

# Execute the conversion
convert_txt_to_formatted_txt(input_txt, output_txt)
