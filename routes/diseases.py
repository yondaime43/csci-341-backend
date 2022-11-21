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


def diseases():
    getDoctors = '''
        SELECT 
            *
        FROM
            public."Disease" t1
    '''

    query = query_db(getDoctors)
    doctors = json.dumps(query)

    if request.method == 'POST':
        data = request.json

        # try:
        #     getDisease = f'''
        #         SELECT 
        #             *
        #         FROM
        #             public."Disease" t1
        #         WHERE disease_code='{data['disease_code']}'
        #     '''
            

        #     print(query_db(getDisease))
        # except:
        #     return "Does not exists", 500


        addUser = f'''
            insert into public."Disease" (disease_code, pathogen, description, id) values ('{data["disease_code"]}', '{data["pathogen"]}', '{data["description"]}', {data["id"]});
        '''

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(addUser)
        conn.commit()
        cur.connection.close()
        
        return "Added"
    else:
        return doctors


def disease(disease_code):
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
            WHERE email='{disease_code}'
        '''


        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(updateUser)
        conn.commit()
        cur.connection.close()

        return "Updated"
    else:
        deleteDoctor = f'''
            DELETE FROM public."Record" WHERE email='{disease_code}';
        '''
    
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(deleteDoctor)
        conn.commit()
        cur.connection.close()

        return "deleted"
        
