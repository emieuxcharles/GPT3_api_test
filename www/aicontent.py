import openai
import config
openai.api_key = config.OPENAI_API_KEY
start_chat_log = '''Human: Hello, who are you?
                    AI: I am doing great. How can I help you today?
                    '''

def openAIQuery(query):
    response = openai.Completion.create(
        engine="davinci-instruct-beta-v3",
        prompt=query,
        temperature=0.8,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    if 'choices' in response:
        if len(response['choices']) > 0:
            answer = response['choices'][0]['text']
        else:
            answer = 'Opps sorry, you beat the AI this time'
    else:
        answer = 'Opps sorry, you beat the AI this time'

    return answer


def ask(question, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    prompt = f'{chat_log}Human: {question}\nAI:'
    response = openai.Completion.create(
        prompt=prompt, engine="davinci", stop=['\nHuman'], temperature=0.9,
        top_p=1, frequency_penalty=0, presence_penalty=0.6, best_of=1,
        max_tokens=150)
    answer = response.choices[0].text.strip()
    return answer


def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = start_chat_log
    return f'{chat_log}Human: {question}\nAI: {answer}\n'