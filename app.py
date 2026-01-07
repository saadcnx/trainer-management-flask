from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  

# MySQL Configuration
app.config['MYSQL_HOST'] = '10.230.150.81'
app.config['MYSQL_USER'] = 'saad2'
app.config['MYSQL_PASSWORD'] = 'oopp#'
app.config['MYSQL_DB'] = 'alnafi'

mysql = MySQL(app)


# Home Page
@app.route("/")
def get_home():
    return "HOME PAGE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"


# Show Form
@app.route("/trainer")
def trainer():
    return render_template("trainer_details.html")


# Handle Form Submission
@app.route("/trainer_create", methods=["POST", "GET"])
def trainer_create():
    if request.method == "POST":
        try:
            fname_data = request.form.get("fname")
            lname_data = request.form.get("lname")
            design_data = request.form.get("design")
            course_data = request.form.get("course")

          
            cdate_data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # SQL Query
            sql = """INSERT INTO trainer_details2
                         (fname, lname, design, course, cdate)
                     VALUES (%s, %s, %s, %s, %s)"""
            val = (fname_data, lname_data, design_data, course_data, cdate_data)

            # Execute query
            cursor = mysql.connection.cursor()
            cursor.execute(sql, val)
            mysql.connection.commit()
            cursor.close()

            # Success message
            flash(f"✅ Success! Trainer {fname_data} {lname_data} added successfully!", "success")
            return redirect(url_for('trainer'))

        except Exception as e:
            flash(f"❌ Error: {str(e)}", "error")
            return redirect(url_for('trainer'))

    # If GET request, show form
    return render_template('trainer_details.html')


# View All Trainers (New Route)
@app.route("/view_trainers")
def view_trainers():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM trainer_details2 ORDER BY id DESC")
    trainers = cursor.fetchall()
    cursor.close()
    return render_template("view_trainers.html", trainers=trainers)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
