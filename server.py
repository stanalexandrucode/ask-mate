from calendar import calendar

from flask import Flask, request, redirect, render_template
import data_manager
from datetime import date, time, datetime

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def all_questions():
    questions = data_manager.read_data('questions')
    ordered_direction = "desc"
    ordered_by = "submission_time"
    args = request.args
    for elem in questions:
        elem["submission_time"] = datetime.fromtimestamp(int(elem["submission_time"]))
    if "ordered_direction" in args and "ordered_by" in args:
        ordered_direction = args.get('ordered_direction')
        ordered_by = args.get('ordered_by')
    if ordered_direction == "desc":
        try:
            questions = sorted(questions, key=lambda k: int(k[ordered_by]), reverse=True)
        except:
            questions = sorted(questions, key=lambda k: k[ordered_by], reverse=True)
    elif ordered_direction == "asc":
        try:
            questions = sorted(questions, key=lambda k: int(k[ordered_by]))
        except:
            questions = sorted(questions, key=lambda k: k[ordered_by])
    return render_template("all_questions.html", questions=questions, ordered_direction=ordered_direction,
                           ordered_by=ordered_by)


@app.route('/question/<question_id>')
def question(question_id):
    file_data = data_manager.read_data('questions', int(question_id))
    file_data["view_number"] = str(int(file_data["view_number"]) + 1)
    data_manager.update_question(question_id, file_data)
    file_data["submission_time"] = datetime.fromtimestamp(int(file_data["submission_time"]))
    answers = data_manager.read_data("answers", question_id)
    for answer in answers:
        answer["submission_time"] = datetime.fromtimestamp(int(answer["submission_time"]))
    return render_template('question.html', id=question_id, data=file_data, answers=answers)

@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    data_manager.delete(question_id)
    return redirect("/list")

@app.route('/question/<question_id>/new_answer', methods=["GET", "POST"])
def post_new_answer(question_id):
    new_id = data_manager.generate_id("answers")
    now = datetime.now()
    x = datetime.timestamp(now)
    if request.method == 'POST':
        new_answer = {
            "id": new_id,
            "submission_time": int(x),  # de modificat timestamp
            "vote_number": str(0),
            "question_id": question_id,
            "message": request.form.get("message"),
            "image": request.form.get('image')}
        data_manager.write_data(new_answer, "answers")
        return redirect('/question/'+str(question_id))
    return render_template('new_answer.html', id=question_id)


@app.route("/question/<question_id>/vote_up")
def Q_vote_up(question_id):
    file_data = data_manager.read_data('questions', question_id)
    file_data["vote_number"] = str(int(file_data["vote_number"]) + 1)
    data_manager.update_question(question_id, file_data)
    return redirect('/list')


@app.route("/question/<question_id>/vote_down")
def Q_vote_down(question_id):
    file_data = data_manager.read_data('questions', question_id)
    file_data["vote_number"] = str(int(file_data["vote_number"]) - 1)
    data_manager.update_question(question_id, file_data)
    return redirect('/list')


@app.route("/answer/<answer_id>/vote_up")
def A_vote_up(answer_id):
    file_data = data_manager.read_answer(answer_id)
    file_data["vote_number"] = str(int(file_data["vote_number"]) + 1)
    data_manager.update_answer(answer_id, file_data)
    question_id = file_data["question_id"]
    question_data = data_manager.read_data('questions', str(question_id))
    question_data["view_number"] = str(int(question_data["view_number"]) - 1)
    data_manager.update_question(question_id, question_data)
    return redirect('/question/' + str(question_id))


@app.route("/answer/<answer_id>/vote_down")
def A_down_up(answer_id):
    file_data = data_manager.read_answer(answer_id)
    file_data["vote_number"] = str(int(file_data["vote_number"]) - 1)
    data_manager.update_answer(answer_id, file_data)
    question_id = file_data["question_id"]
    question_data = data_manager.read_data('questions', str(question_id))
    question_data["view_number"] = str(int(question_data["view_number"]) - 1)
    data_manager.update_question(question_id, question_data)
    return redirect('/question/' + str(question_id))


@app.route('/add_question', methods=["GET", "POST"])
def add_question():
    new_id = data_manager.generate_id('questions')
    now = datetime.now()
    x= datetime.timestamp(now)

    if request.method == 'POST':
        question = {
            "id": new_id,
            "submission_time": int(x),  # de modificat timestamp
            "view_number": 0,
            "vote_number": 0,
            "title": request.form.get('title'),
            "message": request.form.get("message"),
            "image": request.form.get("image")
        }
        data_manager.write_data(question, 'questions')
        return redirect("/list")
    return render_template("add_question.html")


@app.route('/question/<question_id>/edit', methods=["GET", "POST"])
def update(question_id):
    file_data = data_manager.read_data("questions", question_id)

    if request.method == 'POST':
        question = {
            "id": question_id,
            "submission_time": file_data["submission_time"],
            "view_number": file_data['view_number'],
            "vote_number": file_data['vote_number'],
            "title": request.form.get('title'),
            "message": request.form.get("message"),
            "image": request.form.get("image")
        }
        data_manager.update_question(question_id, question)
        return redirect('/list')
    return render_template('edit.html', id=question_id, data=file_data)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
