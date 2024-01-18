from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
@app.route('/index')
def index():
    name = 'Sina'
    users = ['Regina', 'Helena', 'Saeideh']
    return render_template(template_name_or_list='index.html', title='FLASK', members=users)


@app.route('/product/<name>')
def get_product(name):
    return "The product is " + str(name)


@app.route('/fosexam/<grade>')
def get_grade(grade=100):
    return "The grade of your Fos exam is " + str(grade)


@app.route('/create/<last_name>/<first_name>')
def create(first_name, last_name):
    return 'Hello ' + first_name + " " + last_name


if __name__ == "__main__":
    app.run(debug=True)












    import sqlite3
    from sqlite3 import Error

    db_filename = r"C:\Users\Sina Najafi\PycharmProjects\pythonProject1\db\pythonsqlite.db"


    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()


    # 1
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn


    # 2
    def create_table(conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)


    # 3
    def sql_table():
        sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
            id integer PRIMARY KEY,
            firstname text NOT NULL,
            lastname text NOT NULL);
        """


    sql_create_task_table = """ CREATE TABLE IF NOT EXISTS task (
            id integer PRIMARY KEY,
            name text,
            start_date text NOT NULL,
            end_date text NOT NULL,
            priority integer,
            user_id integer NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user (id));
            """

    # 4
    conn = create_connection(db_filename)

    # 5
    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_task_table)
    else:
        print("Error! NO db connection")


    # 6
    def create_user(conn, user):
        sql = """INSERT INTO user(firstname, lastname)
            VALUES(?,?);"""
        c = conn.cursor()
        c.execute(sql, user)
        conn.commit()
        return c.lastrowid


    # 7
    def create_task(conn, task):
        sql = """INSERT INTO task(name,start_date,end_date,priority,user_id)
                 VALUES(?,?,?,?,?);"""
        c = conn.cursor()
        c.execute(sql, task)
        conn.commit()
        return c.lastrowid


    # 8
    def insert_content():
        conn = create_connection(db_filename)
        with conn:
            user = ('Mia', 'Meier')
            user_id = create_user(conn, user)

            # tasks
            task_1 = ("learn python", '2023-11-23', '2024-01-30', 1, user_id)
            task_2 = ("learn Bavarian", '2023-11-23', '2024-01-30', 2, user_id)
            create_task(conn, task_1)
            create_task(conn, task_2)

    # 9
    # sql_table()















    from flask import Flask, render_template, request

    app = Flask(__name__)


    @app.route('/')
    def student():
        return render_template('student.html')


    @app.route('/result', methods=['POST', 'GET'])
    def result():
        if request.method == 'POST':
            result = request.form
            return render_template("result.html", result=result)


    @app.route('/forecast', methods=['GET'])
    def get_forecast():
        data = {}
        data['q'] = request.args.get('city')
        data['appid'] = 'cc8da5f40662bdeab5bd1a83038567'

        print('Data:', data)
        url_values = urllib.parse.urlencode(data)
        print(url_values)
        url = 'http://api.openweathermap.org/data/2.5/forecast'
        full_url = url = '?' + url_values
        print('Full url:', full_url)
        data = urllin.request.urlopen(full_url)

        resp = Response(data)
        print(resp.status_code)
        return render_template('weather.html', title='Weather App',
                               data=json.loads(data.read().decode('utf8')))


    if __name__ == '__main__':
        app.run(port=5001, debug=True)

















import csv
import os

from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['ALLOWED_EXTENSIONS'] = {'csv'}
app.config['UPLOAD_FOLDER'] = 'uploads'

def save_to_csv(data,filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fielnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)

    if file:
        data = []
        csv_reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        for row in csv_reader:
            print(row)
            data.append(row)
            save_to_csv(data, os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_data.csv'))

    return 'File upload successfully'




if __name__ == '__main__':
    app.run(port=5001, debug=True)















