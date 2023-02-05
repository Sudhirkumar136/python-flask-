from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__, template_folder="template")
app.secret_key = "sudhirkumar"

DB_HOST = "localhost"
DB_NAME = "sudhirkumar"
DB_USER = "postgres"
DB_PASS = "1234"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route("/")
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM student"
    cur.execute(s)
    list_users = cur.fetchall()
    list_users.sort(key = lambda x: x[0])
    return render_template("index.html", data = list_users)






@app.route("/submit", methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        result = request.form
        name = result["name"]
        branch = result["branch"]
        college = result["college"]

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 
        cur.execute("Insert into student (name, branch, college) values (%s, %s, %s) ", (name,branch,college))
        conn.commit()
        return redirect("url_for('index')")






@app.route("/change", methods=['GET', 'POST'])
def change():
    return render_template("change.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM student"
    cur.execute(s)
    list_users = cur.fetchall()
    list_users.sort(key = lambda x: x[0])

    if request.method == "POST":
        print('sudhir')
        result = request.form
        name = result["name"]
        branch = result["branch"]
        college = result["college"]
        search_list = []

        if(college!=""):
            for x in list_users:
                if(college == x[3]):
                    print(x)
                    search_list.append(x)

        elif(name!=""):
            for x in list_users:
                if(name == x[1]):
                    print(x)
                    search_list.append(x)

        elif(branch!=""):
            for x in list_users:
                if(branch == x[2]):
                    print(x)
                    search_list.append(x)
        
        return render_template("index.html", s_data=search_list, data=list_users)
    else:
        return render_template('search.html')








@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        result = request.form
        id = result["id"]
        name = result["name"]
        branch = result["branch"]
        college = result["college"]
         
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE student
            SET name = %s,
                branch = %s,
                college = %s
            WHERE id = %s
            """, (name, branch, college, id))
        conn.commit()
        return redirect(url_for('index'))
    else:
        return render_template('change.html')
if __name__ == '__main__':
    app.run(debug=False)