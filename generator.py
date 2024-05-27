import json
import uuid

# Load data from the file data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

new_answers = {"survey_closed_answers": [], "survey_open_answers": []}
# Generate answers for each question in the survey
for question in data['surveyquestions']:
    question_id = question["id"]
    question_type = next((qt for qt in data['surveyquestiontypes'] if qt["id"] == question["survey_question_type_id"]), None)
    
    assert question_type is not None

    if question_type["id"] == "949d74a2-63b1-4478-82f1-e025d8bc6c8b":
        for user in data['users']:
            new_answer = {
                "id": str(uuid.uuid4()),  # Generate a new unique ID for each answer
                "value": "",
                "answered": False,
                "expired": False,
                "user_id": user["id"],
                "question_id": question_id
            }
            new_answers['survey_open_answers'].append(new_answer)
            continue
    
    # Create a new answer for each user
    for user in data['users']:
        new_answer = {
            "id": str(uuid.uuid4()),  # Generate a new unique ID for each answer
            "value_id": "",
            "answered": False,
            "expired": False,
            "user_id": user["id"],
            "question_id": question_id
        }
        new_answers['survey_closed_answers'].append(new_answer)

# Save the new data to the file data2.json
with open('answers.json', 'w', encoding='utf-8') as f:
    json.dump(new_answers, f, ensure_ascii=False, indent=4)