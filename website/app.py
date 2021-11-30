from flask import Flask , render_template
import pymysql
#import mysql.connector

app = Flask(__name__, static_folder='static')

db = pymysql.connect(host='localhost',
                             user='root',
                             password='1234',
                             database='proddis')

# mydb = mysql.connector.connect(
#    host = 'localhost',
#    user = 'root',
#    passwd = '1234',
#    database = 'proddis'
# )

@app.route('/')
def pull():
   mycursor = db.cursor() 
   mycursor.execute('SELECT * FROM proddis.agg_data_final order by comment_mentions DESC')
   data = mycursor.fetchmany(100)
   return render_template('index.html', data = data)


# @app.route("/")
# def pull():
#     return render_template('test.html', posts = posts)

if __name__ == '__main__':
    app.run(debug = True)   