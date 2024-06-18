import json
import asyncio
import aiohttp
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

# Load generated data from data2.json
with open('data2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Initialize the GQL client
transport = AIOHTTPTransport(url='http://localhost:8000/gql/')
client = Client(transport=transport, fetch_schema_from_transport=True)

# Define the mutation for inserting survey answers
mutation = gql('''
    mutation InsertSurveyAnswer($answer: SurveyAnswerInput!) {
        surveyAnswerInsert(answer: $answer) {
            id
            msg
            entity {
                id
                value
                answered
                expired
                user_id
                question_id
            }
        }
    }
''') 
mutation = gql("""
        mutation InsertSurveyAnswer($answer: SurveyAnswerInput!) {
            insert_survey_answer(answer: $answer) {
                id
                message
            }
        }
        """)

async def import_data():
    async with client as session:
        for answer in data['surveyanswers']:
            variables = {
                "answer": {
                    "value": answer["value"],
                    "answered": answer["answered"],
                    "expired": answer["expired"],
                    "user_id": answer["user_id"],
                    "question_id": answer["question_id"]
                }
            }
            response = await session.execute(mutation, variable_values=variables)
            print(response)

# Run the import_data function
asyncio.run(import_data())