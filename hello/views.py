from django.http import HttpResponse
import psycopg2
import redis
import pika
import traceback, sys
import tarantool

def wellcome(request):
    return HttpResponse("<h1>Wellcome my Python app!</h1>")
def index(request):
    conn = psycopg2.connect(dbname="postrges", user="postrges", password="123456", host="master", port="5432")
    with conn:
        with conn.cursor() as cursor:
            print("Подключение установлено")
            #cursor = connection.cursor()
            # Выполнение SQL-запроса для вставки данных в таблицу
            insert_query = """ INSERT INTO people (name, age) VALUES ('Aaaa',55)"""
            cursor.execute(insert_query)
            conn.commit()
                 
    print(cursor.closed)    # True - курсор закрыт
    # cursor.close()  # нет смысла - объект cursor уже закрыт
    conn.close()    # объект conn не закрыт, надо закрывать
    return HttpResponse("<h1>БД подключена</h1>")

def login(request,name,password):
    conn = psycopg2.connect(dbname="postrges", user="postrges", password="123456", host="master", port="5432")

    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE name='"+str(name)+"' AND password ='" + str(password) + "'"
    cursor.execute(query)
    
    rows = cursor.fetchall()

    if rows != []:
        result = "Ваш идентификатор =" + str(rows[0][0])
    else:
        result = "Нет такого пользователя"

    cursor.close()
    conn.close()

    return HttpResponse(result)       
   
def getuser(request,id):
    #conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="db", port="5432")
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="dbslave", port="5432")
    
    cursor = conn.cursor()

    query = "SELECT name FROM users WHERE id='"+str(id) + "'"
    cursor.execute(query)
    
    rows = cursor.fetchall()

    if rows != []:
        result = "Ваше имя =" + str(rows[0][0])
    else:
        result = "Нет такого пользователя"

    cursor.close()
    conn.close()

    return HttpResponse(result)   
 
def register(request,name,surname,old,sex,hobby,sity,password):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456", host="master", port="5432")

        cursor = conn.cursor()

        query = "INSERT INTO public.users(name, surname, age, sex, interests, city, password) VALUES ('"+ name +"', 'users', 33, 'man', 'Hob1', 'Sity1', 'Pass1');"

        cursor.execute(query)
        conn.commit()  
    
        cursor.close()
        conn.close()

        return HttpResponse('Пользователь зарегистрирован')      
def search(request,firstName,secondName):
    print ("==============================старт=========================")
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="dbslave", port="5432")

    cursor = conn.cursor()
    # firstName LIKE ? and secondName LIKE ?). Сортировать вывод по id анкеты.
    query = "SELECT name, surname FROM users WHERE (name LIKE '"+ firstName + "%') AND (surname LIKE '" + secondName + "%') ORDER BY id"
    # (title LIKE '%Cook%') AND (title LIKE '%Recipe%')

    cursor.execute(query)
    
    rows = cursor.fetchall()

    print(rows)

    if rows != []:
        result = "Ваше имя =" + str(rows[0][0]) + " Фамилия =" + str(rows[0][1])
    else:
        result = "Нет такого пользователя"

    cursor.close()
    conn.close()

    return HttpResponse(rows)

def refresh(request):
    myredis = myCash()
    myredis.removeAllKeys
    myredis.validation('posts','100')
    return HttpResponse('ok')

class myCash:
    def setincash(key , value):
        r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
        r.mset({key: value})
        return True;
    def getincach(key):
        r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
        return r.get(key);
    def validation(self, table, countrecords):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="dbslave", port="5432")
    
        cursor = conn.cursor()

        query = "SELECT * FROM "+ table +" ORDER BY id DESC LIMIT " + countrecords
        
        cursor.execute(query)
    
        rows = cursor.fetchall()

        r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
        
        for row in rows:
            r.mset({row[0]: row[2]})

        cursor.close()
        conn.close()
        return True
    
    def removeAllKeys():
        r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
        rows = r.keys("*")
        for i in rows:        
            r.delete(i)
        return True    

def getposts(request):
    r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
    rows = r.keys("*")

    sss = []
    for i in rows:
        sss.append(r.get(i))
        sss.append("<br><br>")

    return HttpResponse(sss)   

def post_read(request,id):
    # подключение к БД
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="db", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "SELECT * FROM posts WHERE id_user ='" + str(id) + "'"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()  

    cursor.close()
    conn.close()

    return HttpResponse(rows)

def post_readtarantool(request):
    # Устанавливаем соединение с сервером Tarantool
    connection = tarantool.connect("tarantooldb", 3301)
    #tarantool.connect("localhost", 3301, user=username, password=password)
    
    tester = connection.space('posts')
    result = tester.select()
    return HttpResponse(result)

# Функция по созданию постов
def post_create(request,userid,text):
    # подключение к БД
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="db", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "INSERT INTO posts (id, id_user, text) VALUES (1, '" + str(userid) + "','" + text + "')"
    #query = "SELECT * FROM posts LIMIT 10"
    #query = "SELECT SESSION_USER, CURRENT_USER"
    #query = "SELECT table_catalog, table_schema, table_name, privilege_type FROM information_schema.table_privileges WHERE grantee = 'postgres' and table_name = 'posts'"
    cursor.execute(query)
    #rows = cursor.fetchall()
    conn.commit()  

    result = "Пост создан"

    cursor.close()
    conn.close()

    return HttpResponse(result)
# Функция по отправке сообщения
def dialog_send(request,user,text):
    # подключение к БД
    conn = psycopg2.connect(dbname="postrges", user="postrges", password="pass", host="master", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "INSERT INTO messages (id_user, text) VALUES ('"+str(user) + "','"+ text + "')"
    #INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', DEFAULT);
    cursor.execute(query)
    conn.commit()  
    
    result = "Сообщение отправлено"

    cursor.close()
    conn.close()

    return HttpResponse(result)

def post_send(request):
    # подключение к БД
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="dbslave", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "SELECT text FROM posts where ID=1"
    cursor.execute(query)
    
    rows = cursor.fetchall()

    mess = str(rows[0][0])

    # Устанавливаем соединение с сервером RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))#("amqp://guest:guest@rabbitmq:5672/vhost"))
    channel = connection.channel()
    
    # Объявляем очередь, в которую будем отправлять сообщения
    channel.queue_declare(queue='hello')
    
    # Отправляем сообщение в очередь
    channel.basic_publish(exchange='', routing_key='hello', body=mess)    
    connection.close()

    cursor.close()
    conn.close()

    return HttpResponse(mess)

def post_readmq(request):
    # Устанавливаем соединение с сервером RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))
    channel = connection.channel()
 
    # Объявляем очередь, из которой будем получать сообщения
    channel.queue_declare(queue='hello')
 
    # Функция обработки полученного сообщения
    def callback(channel, method, properties, body):
        print(f"Received: '{body}'")
 
    # Подписываемся на очередь и указываем функцию обработки сообщений
    channel.basic_consume('hello', callback)
    channel.start_consuming()
    channel.close()
    connection.close()

def messages_read(request):
    # Устанавливаем соединение с сервером Tarantool
    connection = tarantool.connect("tarantooldb", 3301)
    #tarantool.connect("localhost", 3301, user=username, password=password)
    
    tester = connection.space('tester')
    return HttpResponse(tester.select(1))

def post_copy(request):
    # подключение к БД
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="db", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "SELECT * FROM posts"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()  


    # Устанавливаем соединение с сервером Tarantool
    connection = tarantool.connect("tarantooldb", 3301)
    #tarantool.connect("localhost", 3301, user=username, password=password)
    posts = connection.space('posts')
    j=1
    for i in rows:
        posts.insert((j,i[1],str(i[2])))
        j=j+1

    cursor.close()
    conn.close()
    
    return HttpResponse('Посты скопированы в Тарантул')