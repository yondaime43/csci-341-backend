from flask import request
import json

import psycopg2


def get_db_connection():
    conn = psycopg2.connect(database="postgres",
                            host="db.ufvlhahwppcrmhowkztw.supabase.co",
                            user="postgres",
                            password="qMJDFVli1kuNwcIx",
                            port="5432")

    return conn

# data = cursor.fetchone()
# print("Connection established to: ", data)
def query_db(query, args=()):
    cur = get_db_connection().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return r


def doctors():
    getDoctors = '''
        SELECT 
            *, u1.degree
        FROM
            public."Users" t1
        INNER JOIN public."Doctor" u1 ON (t1.email = u1.email)
    
    '''

    query = query_db(getDoctors)
    doctors = json.dumps(query)

    if request.method == 'POST':
        data = request.json
        for i in query:
            if request.json["email"] == i["email"]:
                return "Exists", 500

        addUser = f'''
            insert into public."Users" (email, name, surname, salary, phone, cname) values ('{data["email"]}', '{data["name"]}', '{data["surname"]}', {data["salary"]}, '{data["phone"]}', '{data["cname"]}');
        '''

        addDoctor = f'''
            insert into public."Doctor" (email, degree) values ('{data["email"]}', '{data["degree"]}');
        '''

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(addUser)
        conn.commit()
        cur.connection.close()

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(addDoctor)
        conn.commit()
        cur.connection.close()
        
        return "Added"
    else:
        return doctors


def doctor(email):
    if request.method == 'PUT':
        data = request.json

        resultStr = ""
        resultDoctorStr = ""

        for k, v in data.items():
            if v != "":
                if k != "degree":
                    if k == "salary":
                        resultStr += f"{k}={v}, "
                    else:
                        resultStr += f"{k}='{v}', "

                if k == "degree" or k == "email":
                    resultDoctorStr += f"{k}='{v}', "
        resultStr = resultStr[:-2]
        resultDoctorStr = resultDoctorStr[:-2]

        updateUser = f'''
            UPDATE public."Users"
            SET {resultStr}
            WHERE email='{email}'
        '''


        updateDoctor= f'''
            UPDATE public."Doctor"
            SET {resultDoctorStr}
            WHERE email='{email}'
        '''

        print(updateDoctor)

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(updateUser)
        conn.commit()
        cur.connection.close()

        if resultDoctorStr:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(updateDoctor)
            conn.commit()
            cur.connection.close()

        return "Updated"
    else:
        deleteDoctor = f'''
            DELETE FROM public."Specialize" WHERE email='{email}';
            DELETE FROM public."Doctor" WHERE email='{email}';
            DELETE FROM public."Users" WHERE email='{email}';
        '''
    
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(deleteDoctor)
        conn.commit()
        cur.connection.close()

        return "deleted"
        
