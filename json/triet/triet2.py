import json
import re

# Function to process the input file and convert to JSON format
def convert_to_json(input_txt, output_json):
    # Read the content of the text file
    with open(input_txt, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Initialize a list to hold the questions
    questions = []
    question = {}
    choices = []
    answer = None
    question_number = None

    for line in lines:
        # Strip extra spaces or newline characters
        line = line.strip()
        
        # Identify the questions
        if line.startswith("Câu"):
            # If there's an existing question, append it to the list first
            if question:
                question["choices"] = choices
                question["answer"] = answer
                questions.append(question)
            
            # Start a new question entry
            question_number = line.split(":")[0].strip()  # Extract question number (e.g., Câu 20)
            question = {"question": line.split(":")[1].strip(), "question_number": question_number}
            choices = []
            answer = None
        
        # Identify the answer choices (A, B, C, D, E)
        elif re.match(r"^[A-E]\.", line):
            choices.append(line.strip())
        
        # Identify the answer (typically after the choices)
        elif line.startswith("Đáp án"):
            # Extract the correct answer
            match = re.search(r"Đáp án: (\w)", line)
            if match:
                answer = ord(match.group(1).upper()) - ord('A')  # Convert A, B, C... to 0, 1, 2...

    # Don't forget to append the last question
    if question:
        question["choices"] = choices
        question["answer"] = answer
        questions.append(question)
    
    # Write the output to a JSON file
    with open(output_json, "w", encoding="utf-8") as json_file:
        json.dump(questions, json_file, ensure_ascii=False, indent=4)

# Specify the file paths
input_txt = r"C:\Users\Admin\Documents\html and shit\thcs\json\triet\triet_copy.txt"  # Update to your actual path
output_json = r"C:\Users\Admin\Documents\html and shit\thcs\json\triet\triet.json"  # Desired JSON output path

# Call the function
convert_to_json(input_txt, output_json)

print("Conversion complete!")
