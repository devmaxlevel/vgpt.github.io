from flask import Flask, render_template, request, jsonify
import openai
import datetime
import random

app = Flask(__name__)

# Replace 'YOUR_OPENAI_API_KEY' with your actual OpenAI API key
openai.api_key = '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'

user_name = "User"  # Default user name

def generate_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=50,
        temperature=0.7
    )
    return response.choices[0].message['content']

def generate_study_tip():
    study_tips = [
        "Take short breaks between study sessions to stay focused and avoid burnout.",
        "Create a study schedule to manage your time effectively and cover all subjects.",
        "Teach the material to someone else to reinforce your understanding.",
        "Use mnemonic devices to remember complex information.",
        "Stay hydrated and eat nutritious snacks to maintain your energy levels.",
        "Use online resources and educational apps to enhance your learning.",
        "Practice active recall by quizzing yourself on the material.",
        "Get enough sleep to improve your concentration and memory.",
        "Stay organized by keeping your study materials and notes tidy.",
        "Join study groups to collaborate and share insights with classmates.",
    ]
    return random.choice(study_tips)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    global user_name

    user_input = request.form['user_input']
    conversation = [
        {"role": "system", "content": "You are a helpful assistant that provides information about various topics."},
        {"role": "user", "content": user_input}
    ]

    if "who created you" in user_input.lower():
        bot_response = "I was created by KIRA Group."
    elif "hello" in user_input.lower() or "hi" in user_input.lower():
        bot_response = f"Hello, {user_name}!"
    elif "goodbye" in user_input.lower() or "bye" in user_input.lower():
        bot_response = f"Goodbye, {user_name}! Have a great day."
    elif "help" in user_input.lower():
        bot_response = "I'm here to help you. Just type your questions or statements, and I'll do my best to assist you."
    elif "my name is" in user_input.lower():
        user_name = user_input.split("my name is", 1)[1].strip()
        bot_response = f"Nice to meet you, {user_name}!"
    elif "tell me a joke" in user_input.lower():
        bot_response = "Why did the scarecrow win an award? Because he was outstanding in his field!"
    elif "study tip" in user_input.lower():
        bot_response = generate_study_tip()
    elif "calculate" in user_input.lower():
        expression = user_input.split("calculate", 1)[1].strip()
        try:
            result = eval(expression)
            bot_response = f"The result of {expression} is {result}."
        except:
            bot_response = "Sorry, I couldn't perform the calculation."
    elif "time" in user_input.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        bot_response = f"The current time is {current_time}."
    elif "date" in user_input.lower():
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        bot_response = f"Today's date is {current_date}."
    elif "fun fact" in user_input.lower():
        fun_facts = [
            "Honey never spoils.",
            "A group of flamingos is called a 'flamboyance'.",
            "The Eiffel Tower can grow up to 6 inches in summer due to the expansion of the iron in the heat.",
            "Bananas are berries, but strawberries are not.",
            "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
            "The average person will spend six months of their life waiting for red lights to turn green."
        ]
        bot_response = random.choice(fun_facts)
    else:
        bot_response = generate_response(conversation)

    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
