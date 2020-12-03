from flask import Flask, render_template, request, make_response, session, redirect, url_for
import sqlite3
import datetime
from datetime import datetime

app = Flask(__name__)

# Steps with commands for creating table "POSTS":
# 1.source venv/bin/activate
# 2.sqlite3 blog.sqlite
# 3.CREATE TABLE POSTS(Id integer primary key autoincrement, Title text, Description text, Date text);

@app.route('/')
@app.route('/show')
def show():
    """Page for displaying all posts in the blog. It display in the template
    all the info about each posts(position). Info includes
    ID, tittle, description, time, when this post has been edited."""
    connection = sqlite3.connect("blog.sqlite")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM POSTS")
    fields = cursor.fetchall()
    connection.close()
    return render_template('show.html', fields=fields)


@app.route('/add', methods=['GET', 'POST'])
def get_title():
    """Page shows form for entering tittle and description of the new position.
    System add created position into the blog under new exclusive ID.
    After adding new position with id, tittle, description and current time,
    system redirect user to the updated page with all posts in the blog."""
    if request.method == 'GET':
        response = make_response(render_template('add.html'))
    elif request.method == 'POST':
        tittle = request.form['Tittle']
        description = request.form['Description']
        if not tittle:
            return 'Sorry, you should insert tittle'
        if not description:
            return 'Sorry, you should insert description'
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        connection = sqlite3.connect("blog.sqlite")
        cursor = connection.cursor()
        values = (tittle, description, date)
        cursor.execute("""insert into POSTS ( Title,Description,Date)
                   VALUES               (  ?,             ?,             ? )""",
                       values)
        connection.commit()
        connection.close()
        response= redirect("/show")
    return response


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """This page will give user an access to update tittle and description of any existing position in the blog.
    Page shows form for entering existing in the blog ID and forms for updated tittle and description.
    If entered ID has corresponding position in the blog, system update post information and redirect user
    into updated page with all posts in the blog."""
    if request.method == 'GET':
        response = make_response(render_template('edit.html'))
    elif request.method == 'POST':
        tittle = request.form['Tittle']
        description = request.form['Description']
        id = request.form['ID']
        now = datetime.now()
        date = now.strftime("%d/%m/%Y %H:%M:%S")
        connection = sqlite3.connect("blog.sqlite")
        cursor = connection.cursor()
        values = (tittle, description, date, id)
        cursor.execute("""UPDATE POSTS SET Title = ?,Description = ?,Date= ? WHERE id = ?;""",
                       values)
        connection.commit()
        connection.close()
        response= redirect("/show")
    return response

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    """This page will delete post with all the info under the existing ID, that user
    will enter in the form. After deleting post system will redirect user into updated
    page with all posts in the blog."""
    if request.method == 'GET':
        response = make_response(render_template('delete.html'))
    elif request.method == 'POST':
        id = request.form['ID']
        connection = sqlite3.connect("blog.sqlite")
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM POSTS WHERE Id = ?''', (id))
        connection.commit()
        connection.close()
        response= redirect("/show")
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5002)
