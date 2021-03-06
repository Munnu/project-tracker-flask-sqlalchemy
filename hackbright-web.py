from flask import Flask, request, render_template, redirect, url_for

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    project_info = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html", 
                            first=first, 
                            last=last, 
                            github=github, 
                            project_info=project_info)
    return html

@app.route("/student-search")
def get_student_form():
    """ Show form for searching for a student. """

    return render_template("student_search.html")

@app.route("/student-add-form")
def student_add_form():
    """Render form to add student."""
    return render_template("add_student.html")

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student."""

    # first_name = student_data['first_name']
    first = request.form.get("first_name")
    last = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first, last, github)

    return redirect(url_for('get_student', first=first, last=last, github=github))

@app.route("/project")
def get_project_info():
    """Render a page showing information about a project"""

    project_title = request.args.get('title', 'Markov')
    project_info = hackbright.get_project_by_title(project_title)
    projecty = hackbright.get_grades_by_title(project_title)

    html = render_template("project_info.html", 
                            project_info=project_info,
                            projecty=projecty)
    return html

@app.route("/project-search")
def get_project_form():
    """ Show form for searching for a project. """

    return render_template("project_search.html")


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
