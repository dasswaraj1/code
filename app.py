from unittest import result

from flask import Flask, render_template, request, redirect, url_for 
app = Flask(__name__) 

tasks = [ 
{ 
"id": 1, 
"title": "Learn Flask", 
"description": "Study Flask CRUD", 
"status": "Pending", 
"priority": "High" 
}, 
{
"id": 2, 
"title": "Python Practice", 
"description": "Solve list problems", 
"status": "Completed", 
"priority": "Medium" }
]
def generate_id(): 

    if not tasks: 
        return 1 
    return tasks[-1]["id"] + 1 
def find_task_by_id(task_id): 

    for task in tasks: 
        if task["id"] == task_id: 
            return task 
    return None 

def search_by_title(keyword): 

    result = [] 
    for task in tasks: 
        if keyword.lower() in task["title"].lower(): 
            result.append(task) 
    return result 
 
def search_by_status(status): 
    """ 
    Search task by status 
    """ 
    result = [] 
 
    for task in tasks: 
        if task["status"].lower() == status.lower(): 
            result.append(task) 
 
    return result 
 
 
def search_by_priority(priority): 
    """ 
    Search task by priority 
    """ 
    result = [] 
 
    for task in tasks: 
        if task["priority"].lower() == priority.lower(): 
            result.append(task) 
 
    return result 
 
 
def keyword_search(keyword): 
    """ 
    Search in title + description 
    """ 
    result = [] 
 
    for task in tasks: 
        if ( 
            keyword.lower() in task["title"].lower() 
            or keyword.lower() in task["description"].lower() 
        ): 
            result.append(task) 
 
    return result 

@app.route("/") 
def home(): 
    return render_template("index.html", tasks=tasks) 

@app.route("/add", methods=["GET", "POST"]) 
def add_task(): 
    if request.method == "POST": 
        new_task = { 
            "id": generate_id(), 
            "title": request.form["title"], 
            "description": request.form["description"], 
            "status": request.form["status"], 
            "priority": request.form["priority"] 
} 
        tasks.append(new_task) 
        return redirect(url_for("home")) 
    return render_template("add_task.html") 

@app.route("/edit/<int:task_id>", methods=["GET", "POST"]) 
def edit_task(task_id): 
    task = find_task_by_id(task_id) 
    if not task: 
        return "Task Not Found" 
    if request.method == "POST": 
        task["title"] = request.form["title"] 
        task["description"] = request.form["description"] 
        task["status"] = request.form["status"] 
        task["priority"] = request.form["priority"] 
        return redirect(url_for("home")) 
    return render_template("edit_task.html", task=task) 

@app.route("/delete/<int:task_id>") 
def delete_task(task_id): 
    task = find_task_by_id(task_id) 
    if task: 
        tasks.remove(task) 
    return redirect(url_for("home")) 

@app.route("/search") 
def search_task(): 
    search_type = request.args.get("type") 
    keyword = request.args.get("keyword") 
    result = [] 
    if search_type == "title": 
        result = search_by_title(keyword) 
    elif search_type == "status": 
        result = search_by_status(keyword) 
    elif search_type == "priority": 
        result = search_by_priority(keyword) 
    elif search_type == "keyword": 
        result = keyword_search(keyword) 
    return render_template("index.html", tasks=result) 

if __name__ == "__main__": 
    app.run(debug=True)