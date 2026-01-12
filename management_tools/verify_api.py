import requests

# Base URL
BASE_URL = 'http://127.0.0.1:5000/api/questions'

# 1. Test GET all questions
print("--- GET All Questions ---")
response = requests.get(BASE_URL)
if response.status_code == 200:
    questions = response.json()
    print(f"Retrieved {len(questions)} questions.")
    # Print first question as sample
    if questions:
        print("Sample:", questions[0])
else:
    print("Failed to retrieve questions:", response.status_code)

# 2. Test POST (Create) a question
print("\n--- POST Create Question ---")
new_question = {
    'level': 1,
    'text': 'What is the capital of France?',
    'correct_answer': 'Paris',
    'wrong_answers': 'London,Berlin,Madrid', # Note: API expects list, but let's see how our parser handles it.
    # Actually our parser action='append' creates a list if keys are repeated?
    # Or if we send JSON? requests.post(json=...) sends JSON.
    # Let's check how reqparse handles JSON lists.
    # Usually request parser with action='append' looks for repeated keys in form data or json list.
    'info': 'City of Lights'
}
# For 'append' in reqparse with JSON, we should send a list for that key
new_question_json = {
    'level': 1,
    'text': 'What is the capital of France?',
    'correct_answer': 'Paris',
    'wrong_answers': ['London', 'Berlin', 'Madrid'],
    'info': 'City of Lights'
}

response = requests.post(BASE_URL, json=new_question_json)
if response.status_code == 200:
    created_question = response.json()
    print("Created:", created_question)
    created_id = created_question['id']
else:
    print("Failed to create question:", response.status_code, response.text)
    created_id = None

# 3. Test GET single question
if created_id:
    print(f"\n--- GET Question {created_id} ---")
    response = requests.get(f"{BASE_URL}/{created_id}")
    if response.status_code == 200:
        print("Retrieved:", response.json())
    else:
        print("Failed to retrieve question:", response.status_code)

# 4. Test PUT (Update) question
if created_id:
    print(f"\n--- PUT Update Question {created_id} ---")
    update_data = {
        'text': 'What is the capital of France (Updated)?'
    }
    response = requests.put(f"{BASE_URL}/{created_id}", json=update_data)
    if response.status_code == 200:
        print("Updated:", response.json())
    else:
        print("Failed to update question:", response.status_code)

# 5. Test DELETE question
if created_id:
    print(f"\n--- DELETE Question {created_id} ---")
    response = requests.delete(f"{BASE_URL}/{created_id}")
    if response.status_code == 200:
        print("Deleted:", response.json())
    else:
        print("Failed to delete question:", response.status_code)

# 6. Test Search
print("\n--- SEARCH 'HTML' ---")
response = requests.get(f"{BASE_URL}/search/HTML")
if response.status_code == 200:
    results = response.json()
    print(f"Found {len(results)} matches.")
else:
    print("Failed to search:", response.status_code)

# 7. Test Random Question API
print("\n--- Random Question (Level 1) ---")
response = requests.get("http://127.0.0.1:5000/game_random_question?level=1")
if response.status_code == 200:
    print("Random Question:", response.json())
else:
    print("Failed to get random question:", response.status_code)
