import connection
import os

ANSWER_PATH = os.getenv('ANSWER_PATH') if 'ANSWER_PATH' in os.environ else 'answer.csv'
QUESTIONS_PATH = os.getenv('QUESTIONS_PATH') if 'QUESTIONS_PATH' in os.environ else 'question.csv'

DATA_HEADER_ANSWER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
DATA_HEADER_QUESTIONS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message','image']


def write_data(new_data,action):
    if action == "answers":
        connection.add_in_csv(ANSWER_PATH, new_data, DATA_HEADER_ANSWER)
    elif action == "questions":
        connection.add_in_csv(QUESTIONS_PATH, new_data, DATA_HEADER_QUESTIONS)
    else:
        print("esti prost ai gresit comanda de fisier in write data")    # de sters la final


def read_data(file, id=None):
    if file == "answers":
        question_answers = []
        for answer in connection.get_data(ANSWER_PATH):
            if answer['question_id']== id:
                question_answers.append(answer)
        return question_answers
    elif file == "questions":
        return connection.get_data(QUESTIONS_PATH, id)
    else:
        print("esti prost ai gresit comanda de fisier")    # de sters la final


def update_question(question_id, update_dict):
    connection.update_in_csv(question_id, update_dict, QUESTIONS_PATH, DATA_HEADER_QUESTIONS)
    return "Done"


def update_answer(answer_id,update_dict):
    connection.update_in_csv(answer_id, update_dict, ANSWER_PATH, DATA_HEADER_ANSWER)
    return "Done"

def read_answer(id=None):
    return connection.get_data(ANSWER_PATH, id)

def delete(delete_id):
    connection.delete_in_csv(delete_id, ANSWER_PATH, DATA_HEADER_ANSWER)
    connection.delete_in_csv(delete_id, QUESTIONS_PATH, DATA_HEADER_QUESTIONS)
    return "Done"

def generate_id(filename):
    max_add = 0
    if filename == "questions":
        filename = QUESTIONS_PATH
    elif filename == "answers":
        filename = ANSWER_PATH
    else:
        print("esti prost ai gresit comanda de fisier")    # de sters la final
    for row in connection.get_data(filename):
        if int(row['id']) > max_add:
            max_add = int(row['id'])
    return max_add + 1







