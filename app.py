import os
from flask import Flask 
from flask import redirect, request, render_template, send_from_directory
app = Flask(__name__)

ANSWERS_DIR = "answers"

@app.route("/", methods=['GET', 'POST'])
def welcome():
    match request.method:
        case "POST":
            input_title = request.form["title"] + ".txt"
            f = open(f"./{ANSWERS_DIR}/{input_title}","w")
            f.write(request.form["answer"])
            f.close()
            return render_template("accept.html", link_to_text=f"{ANSWERS_DIR}/{input_title}")
        case _:
            return render_template("form.html")

@app.route("/delete")
def delete_answer():
    title_to_delete = request.args.get("delete_id")
    try:
        os.remove(f"./{ANSWERS_DIR}/{title_to_delete}")
    except:
        pass
    return redirect(ANSWERS_DIR)

@app.route(f"/{ANSWERS_DIR}/")
def show_answers_list():
    answers = (os.listdir(ANSWERS_DIR))
    return render_template("list.html", answers=answers, delete_link="/delete?delete_id=")

@app.route(f"/{ANSWERS_DIR}/<name>")
def show_answer(name):
    return send_from_directory("answers", name)

if __name__ == "__main__":
    app.run(debug=True)