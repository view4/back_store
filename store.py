from bottle import route, run, template, static_file, get, post, delete, request,response
from sys import argv
import json
import pymysql
argv[0]="5000"
connection=pymysql.connect(host="localhost",
                        user="root",
                        password="root",
                        db="store",
                        charset="utf8",
                        cursorclass=pymysql.cursors.DictCursor)
#Add one value to the database manually and practice retreiving it.
@get("/admin")
def admin_portal():
	return template("pages/admin.html")

@get("/")
def index():
    return template("./index.html")

@post("/categories")
def categories():
    all_cats=[]
    with connection.cursor() as cursor:
        sql="SELECT * FROM categories"
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)
        for element in result:
            val_to_add={"id":element['cat_id'],"name":element["cat_name"]}
            all_cats.append(val_to_add)
            print(all_cats)
    output={"status":"success",
            "msg":"",
            "categories":all_cats,
            "code":200
            }
    return json.dumps(output)

@get("/category/<id>")
def category(id):
    with connection.cursor() as cursor:
        sqlDeleteRows   = "Delete from categories where cat_id='{}'".format(id)
        cursor.execute(sqlDeleteRows)
        connection.commit()

        sqlremaining="select * from categories"
        cursor.execute(sqlremaining)
        result=cursor.fetchall()
        print(result)



    output={"status":"success",
            "msg":"",
            "code":201
            }
    return json.dumps(output)

@post("/category")
def category():
    new_cat=request.forms.get("name")
    print(type(new_cat))
    with connection.cursor() as cursor:
        sql="INSERT INTO categories (cat_name) VALUES ('{0}')".format(new_cat)
        print(sql)
        cursor.execute(sql)
        connection.commit()
        sql="SELECT * FROM categories"
        cursor.execute(sql)
        result=cursor.fetchall()

    output={"Status": "success",
            "MSG":"",
            "cat_id":4,
            "code":201
            }
    return json.dumps(output)

    #get value from page.
    #Add this value to the database.
    # return as a json

@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')


@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')


@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')


run(host='localhost', port=argv[0])
