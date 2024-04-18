import json
import random
import uuid

# Načtení dat ze souboru data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Selekce potřebných částí dat pro nový soubor
new_data = {}
for key in ['surveyquestiontypes', 'surveys', 'surveytypes', 'surveyquestions', 'surveyanswers', 'surveyquestionvalues']:
    new_data[key] = data[key]

# Generování odpovědí pro každou možnost v anketních otázkách
for value in new_data['surveyquestionvalues']:
    for user in data['users']:
        if "value" not in value or value["value"] is None:
            # Získání otázky pro aktuální hodnotu
            question_id = value["question_id"]
            question = next((q for q in new_data['surveyquestions'] if q["id"] == question_id), None)
            if question:
                # Typ otázky
                question_type = next((qt for qt in new_data['surveyquestiontypes'] if qt["id"] == question["type_id"]), None)
                if question_type:
                    # Generování odpovědi na základě typu otázky
                    if question_type["name"] in ["Yes/No", "True/False"]:
                        new_value = random.choice(["yes", "no"])
                    elif question_type["name"] in ["Multiple Choice"]:
                        # Pokud je otázka typu Multiple Choice a má možnosti, vybereme náhodnou možnost
                        options = value.get("options", [])
                        if options:
                            new_value = random.choice(options)
                        else:
                            new_value = None  # Pokud nejsou možnosti k dispozici, použijeme None
                    else:
                        # Generování náhodné odpovědi pro jiné typy otázek
                        new_value = str(uuid.uuid4())[:8]  # Náhodný řetězec
                    # Vytvoření nové odpovědi
                    new_answer = {
                        "id": str(uuid.uuid1()),  # Přidání unikátního identifikátoru
                        "value": new_value,
                        "answered": True,
                        "expired": False,
                        "user_id": user["id"],
                        "question_id": question_id
                    }
                    # Přidání nové odpovědi do dat
                    new_data['surveyanswers'].append(new_answer)
        else:
            # Pokud je hodnota k dispozici, přidáme ji jako odpověď
            new_answer = {
                "id": str(uuid.uuid1()),  # Přidání unikátního identifikátoru
                "value": value["value"],
                "answered": True,
                "expired": False,
                "user_id": user["id"],
                "question_id": value["question_id"]
            }
            # Přidání nové odpovědi do dat
            new_data['surveyanswers'].append(new_answer)

# Uložení nových dat do souboru data2.json
with open('data2.json', 'w', encoding='utf-8') as f:
    json.dump(new_data, f, ensure_ascii=False, indent=4)