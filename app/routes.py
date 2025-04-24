from flask import (
    Flask,
    request as flask_request,
    render_template
)
import requests

BACKEND_URL = "http://127.0.0.1:5000/tasks"

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/about")
def about():
    return render_template("about.html")

@app.get("/tasks")
def task_list():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_data = response.json().get("tasks")
        return render_template("list.html", tasks=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.get("/task/<int:pk>")
def get_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template("detail.html", task=single_task)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )


#New tasks Routes
@app.get("/tasks/new")
def new_form():
    return render_template("new.html")

@app.get("/tasks/new")
def trash_form():
    return render_template("trash.html")


@app.post("/tasks/new")
def create_task():
    task_data = flask_request.form
    response = requests.post(BACKEND_URL, json=task_data)
    if response.status_code == 204:
        return render_template("succes.html", msg="Task created")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )