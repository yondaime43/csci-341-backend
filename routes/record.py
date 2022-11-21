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


def records():
    getDoctors = '''
        SELECT 
            *
        FROM
            public."Record" t1
    '''

    query = query_db(getDoctors)
    doctors = json.dumps(query)

    if request.method == 'POST':
        data = request.json

        print(data['disease_code'])

        try:
            getDisease = f'''
                SELECT 
                    *
                FROM
                    public."Disease" t1
                WHERE disease_code='{data['disease_code']}'
            '''
            

            print(query_db(getDisease))
        except:
            return "Does not exists", 500


        addUser = f'''
            insert into public."Record" (email, cname, disease_code, total_deaths, total_patients) values ('{data["email"]}', '{data["cname"]}', '{data["disease_code"]}', {data["total_deaths"]}, {data["total_patients"]});
        '''

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(addUser)
        conn.commit()
        cur.connection.close()
        
        return "Added"
    else:
        return doctors


def record(email):
    if request.method == 'PUT':
        data = request.json

        resultStr = ""
        resultDoctorStr = ""

        for k, v in data.items():
            if v != "":
                if k == "total_deaths" or k == "total_patients":
                    resultStr += f"{k}={v}, "
                else:
                    resultStr += f"{k}='{v}', "

                
        resultStr = resultStr[:-2]
        resultDoctorStr = resultDoctorStr[:-2]

        updateUser = f'''
            UPDATE public."Record"
            SET {resultStr}
            WHERE email='{email}'
        '''


        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(updateUser)
        conn.commit()
        cur.connection.close()

        return "Updated"
    else:
        deleteDoctor = f'''
            DELETE FROM public."Record" WHERE email='{email}';
        '''
    
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(deleteDoctor)
        conn.commit()
        cur.connection.close()

        return "deleted"
        
