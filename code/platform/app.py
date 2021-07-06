'''
Author: Lee Chun Hao
GitHub: https://github.com/0x4F776C
LinkedIn: https://sg.linkedin.com/in/lee-chun-hao
'''

from flask import *
from flask_mysqldb import *
from MySQLdb import *
import os

app = Flask(__name__)
app.secret_key = "flash message"    # Required for flash message to work

app.config["MYSQL_HOST"] = "localhost"  # Location/Address of MySQL server
app.config["MYSQL_USER"] = "wss"    # MySQL username
app.config["MYSQL_PASSWORD"] = "P@ssw0rd1"  # MySQL user password
app.config["MYSQL_DB"] = "MP"   # The database name

mysql = MySQL(app)

@app.route("/")
def index():
	cur = mysql.connection.cursor()
	cur.execute("SELECT COUNT(id) FROM MP.tblBlueFlags")
	total_score = cur.fetchone()
	cur.close()
	cur = mysql.connection.cursor()
	cur.execute("SELECT sum(solved) FROM MP.tblBlueFlags")
	current_score = cur.fetchone()
	cur.close()
	return render_template("index.html", total_score=total_score[0], current_score=current_score[0])

@app.route("/flags")
def flags():
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM tblBlueFlags")
	data = cur.fetchall()
	cur.close()
	return render_template("flags.html", flags=data)

@app.route("/insert", methods=["POST"])
def insert():
	if request.method == "POST":
		flag = request.form["flag"]
		escape_string_flag = escape_string(flag)
		clean_flag = escape_string_flag.decode("utf-8")
		cur = mysql.connection.cursor()
		cur.execute("SELECT flag from tblBlueFlags WHERE flag='flag{%s}'" % clean_flag)
		row_count = cur.rowcount
		cur.close()
		if row_count == 0:
			flash("Flag added successfully")
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO tblBlueFlags (flag) VALUES ('flag{%s}')" % clean_flag)
			mysql.connection.commit()
			return redirect(url_for("flags"))
		else:
			flash("Flag already exist")
			return redirect(url_for("flags"))

@app.route("/delete/<string:id_data>", methods=["POST", "GET"])
def delete(id_data):
	input_id = id_data
	escape_string_id = escape_string(input_id)
	clean_id = escape_string_id.decode("utf-8")
	cur = mysql.connection.cursor()
	cur.execute("SELECT id from tblBlueFlags WHERE id=%s" % clean_id)
	row_count = cur.rowcount
	cur.close()
	if row_count != 0:
		flash("Flag deleted successfully")
		input_id = id_data
		escape_string_id = escape_string(input_id)
		clean_id = escape_string_id.decode("utf-8")
		cur = mysql.connection.cursor()
		cur.execute("DELETE FROM tblBlueFlags WHERE id=%s" % clean_id)
		mysql.connection.commit()
		return redirect(url_for("flags"))
	else:
		flash("Invalid id")
		return redirect(url_for("flags"))

@app.route("/check", methods=["POST"])
def check():
	if request.method == "POST":
		flag = request.form["flag"]
		escape_string_flag = escape_string(flag)
		clean_flag = escape_string_flag.decode("utf-8")
		cur = mysql.connection.cursor()
		cur.execute("SELECT flag from tblBlueFlags WHERE flag='flag{%s}'" % clean_flag)
		row_count = cur.rowcount
		cur.close()
		if row_count == 0:
			flash("Flag does not exist")
			return redirect(url_for("index"))
		else:
			cur = mysql.connection.cursor()
			cur.execute("SELECT solved from tblBlueFlags WHERE flag='flag{%s}'" % clean_flag)
			solved_value = cur.fetchone()
			cur.close()
			if solved_value[0] is None:
				flash("Flag submitted")
				cur = mysql.connection.cursor()
				cur.execute("UPDATE tblBlueFlags SET solved=1 WHERE flag='flag{%s}'" % clean_flag)
				mysql.connection.commit()
				return redirect(url_for("index"))
			elif solved_value[0] == 1:
				flash("Flag has already been submitted")
				return redirect(url_for("index"))
			else:
				flash("Unknown error encountered. Contact lecturer")
				return redirect(url_for("index"))

@app.route("/donate")
def donate():
	return redirect("https://www.blockchain.com/btc/address/37jdCj8dePgU5iy5zp3RtSCFo5XndaxKXe")    # Just a simple donation redirection

@app.route("/generate")
def generate():
	command = "sudo /home/wss/Desktop/MP/script/generator.sh"   # Modify the directory where generator.sh resides
	os.system(command)
	flash("Generated new flags")
	return redirect(url_for("index"))

@app.route("/drop")
def drop():
	cur = mysql.connection.cursor()
	cur.execute("TRUNCATE TABLE tblBlueFlags")
	cur.close()
	flash("Deleted all flags")
	return redirect(url_for("index"))

if __name__ == "__main__":
	app.run(host="0.0.0.0",port=8888,debug=True)    # Feel free to change the binding address and port number
