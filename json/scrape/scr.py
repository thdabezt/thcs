import os
from bs4 import BeautifulSoup
import json

# Define the input directory containing .html files
input_dir = r"C:\Users\Admin\Documents\html and shit\thcs\json\scrape\web"
output_dir = os.path.join(input_dir, "json")
os.makedirs(output_dir, exist_ok=True)  # Create /json/ directory if it doesn't exist

BASE_URL = "https://portal.uet.vnu.edu.vn"

# Process each .html file in the input directory
for file_name in os.listdir(input_dir):
    if file_name.endswith(".html"):
        input_html = os.path.join(input_dir, file_name)

        # Parse the HTML content
        with open(input_html, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Extract the quiz title
        quiz_title_element = soup.find("h1", id="quiz_title")
        if not quiz_title_element:
            print(f"Skipping file '{file_name}': No quiz title found.")
            continue

        quiz_title = quiz_title_element.get_text(strip=True)
        output_json = os.path.join(output_dir, f"{quiz_title}.json")

        # Initialize an empty list to store the questions
        data = []

        # Load existing data if the file already exists
        if os.path.exists(output_json):
            with open(output_json, "r", encoding="utf-8") as existing_file:
                try:
                    data = json.load(existing_file)
                except json.JSONDecodeError:
                    data = []

        # Extract existing questions for deduplication
        existing_questions = {item["question"] for item in data}

        # Find all question containers (assumed by class "display_question")
        questions = soup.find_all("div", class_="display_question")

        # Loop through each question and extract the required information
        for question in questions:
            # Initialize a dictionary to store image tags and their links
            links = {}
            tag_counter = 1

            # Extract the question text and replace <img> tags with placeholders
            question_text_element = question.find("div", class_="question_text")
            question_text = question_text_element.get_text(strip=True) if question_text_element else ""

            # Replace <img> in the question
            for img in question_text_element.find_all("img"):
                tag = f"[Image{tag_counter}]"
                img_link = BASE_URL + img["src"]
                links[tag] = img_link
                img.replace_with(tag)  # Replace the <img> with the tag
                tag_counter += 1

            # Skip the question if it already exists in the JSON
            if question_text in existing_questions:
                continue

            # Check for a matrix (table) in the question
            matrix = None
            table = question.find("table")
            if table:
                try:
                    # Parse the table into a 2D list (matrix)
                    rows = table.find_all("tr")
                    matrix = [[cell.get_text(strip=True) for cell in row.find_all(["td", "th"])] for row in rows]
                except Exception as e:
                    print(f"Skipping question due to matrix parsing error: {question_text} ({e})")
                    continue

            # Find all choices and replace <img> tags in choices
            choices = []
            for choice in question.find_all("div", class_="answer_text"):
                choice_text = choice.get_text(strip=True)
                for img in choice.find_all("img"):
                    tag = f"[Image{tag_counter}]"
                    img_link = BASE_URL + img["src"]
                    links[tag] = img_link
                    img.replace_with(tag)  # Replace the <img> with the tag
                    tag_counter += 1
                choices.append(choice_text)

            # Find the correct answer
            correct_choice = question.find("div", class_="correct_answer")
            if not correct_choice:
                print(f"Skipping question with no correct answer: {question_text}")
                continue

            # Extract only the correct answer's text
            correct_text = correct_choice.find("div", class_="answer_text")
            if not correct_text:
                print(f"Skipping question with no valid answer text: {question_text}")
                continue
            correct_text = correct_text.get_text(strip=True)

            # Match it with choices to find the correct index
            try:
                correct_index = choices.index(correct_text)
            except ValueError:
                print(f"Skipping question with unmatched correct answer: {question_text}")
                continue

            # Append to the data list
            question_data = {
                "question": question_text,
                "choices": choices,
                "answer": correct_index,
                "links": links  # Include image links
            }
            if matrix:
                question_data["matrix"] = matrix  # Include matrix if present

            data.append(question_data)

        # Save the extracted data to a JSON file
        with open(output_json, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        print(f"Questions extracted and saved to {output_json}")
