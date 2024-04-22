import json
import random
import uuid

# Load data from the file data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Select necessary parts of the data for the new file
new_data = {}
for key in ['surveyquestiontypes', 'surveys', 'surveytypes', 'surveyquestions', 'surveyanswers', 'surveyquestionvalues']:
    new_data[key] = data[key]

# Generate answers for each question in the survey
for question in new_data['surveyquestions']:
    question_id = question["id"]
    question_type = next((qt for qt in new_data['surveyquestiontypes'] if qt["id"] == question["type_id"]), None)
    if question_type:
        if question_type["name"] in ["Yes/No", "True/False"]:
            new_value = random.choice(["yes", "no"])
        elif question_type["name"] in ["Multiple Choice"]:
            options = [option["name"] for option in new_data['surveyquestionvalues'] if option["question_id"] == question_id]
            if options:
                new_value = random.choice(options)
            else:
                new_value = None
        else:
            new_value = str(uuid.uuid4())[:8]
        # Create a new answer for each user
        for user in data['users']:
            new_answer = {
                "id": str(uuid.uuid4()),  # Generate a new unique ID for each answer
                "value": new_value,
                "answered": True,
                "expired": False,
                "user_id": user["id"],
                "question_id": question_id
            }
            new_data['surveyanswers'].append(new_answer)

# Save the new data to the file data2.json
with open('data2.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)