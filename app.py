from flask import Flask, render_template, request
import requests

GROQ_API_KEY = "API KEY"  # Replace with your Groq API key
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Flask setup
app = Flask(__name__)

def get_groq_full_response(task_description):
    """
    This function sends the task description to Groq API and receives a response.
    Groq will process the task and provide a complete response (like a review, summary, or advice).
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Act as a highly skilled assistant. For the task described below, provide a complete response with detailed and thoughtful analysis, 
    advice, or completion of the task at hand.
    Task: {task_description}
    """
    
    payload = {
        "model": "llama3-8b-8192",  
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500, 
        "temperature": 0.7,  
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        tasks = request.form['tasks'].splitlines()

        # Process each task and get the response from Groq API
        task_responses = {}
        for task in tasks:
            task_responses[task] = get_groq_full_response(task.strip())

        return render_template('index.html', task_responses=task_responses)

    return render_template('index.html', task_responses=None)


if __name__ == '__main__':
    app.run(debug=True)
