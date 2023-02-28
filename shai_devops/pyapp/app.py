from flask import Flask, request, make_response
import mysql.connector
import socket
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

mydb = mysql.connector.connect(
  user='root', password='rootpass', host='mysql', port="3306", database='db')
print("DB CONNECTED")
mycursor = mydb.cursor(buffered=True)

mycursor.execute("SELECT * FROM counter")
if mycursor.fetchone() is None:
    mycursor.execute("INSERT INTO counter (value) VALUES (0)")
    mydb.commit()
else:
    mycursor.execute("UPDATE counter SET value = 0")
    mydb.commit()

@app.route('/')
def increment_counter():
    mycursor.execute("UPDATE counter SET value = value + 1")
    mydb.commit()
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip_one = request.environ['REMOTE_ADDR'] # ngixn container ip
    else:
        ip_one = request.environ['HTTP_X_FORWARDED_FOR']  # ngixn container ip

    ip_two = request.headers.get('X-Forwarded-For', request.remote_addr) # ngixn container ip

    ip_three = request.remote_addr # ngixn container ip

    ip_four = socket.gethostbyname(socket.gethostname()) # ip of the app container

        # Create cookie for 5 minutes with internal IP

    response = make_response("Internal IP address: {}".format(ip_four))
    timer = datetime.now() + timedelta(minutes=5)
    response.set_cookie('internal_ip', ip_four, max_age=300, expires = timer)
    # Record access log to MySQL table
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO access_log (date_time, client_ip, server_ip) VALUES (%s, %s, %s)"
    val = (now, ip_one, ip_two)
    mycursor.execute(sql, val)
    mydb.commit()
    answer = "First ip: " + ip_one + "\nSecond ip: " + ip_two + "\nThird ip: " + ip_three + "\nFourth ip: " + ip_four
    return answer


# Route for showing global counter
@app.route('/showcount')
def show_counter():
    mycursor.execute("SELECT * FROM counter")
    result = mycursor.fetchone()
    counter = result[0]
    return "Global counter number: {}".format(counter)

if __name__ == '__main__':
    app.run('0.0.0.0')