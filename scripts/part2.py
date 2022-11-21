from sqlalchemy.engine import create_engine, URL
from sqlalchemy.sql import text
import pandas as pd 

engine = create_engine("postgresql+psycopg2://postgres:Almaz071@localhost:5432/CSCI_341_Assignment_2")

url = URL.create(  drivername='postgresql+psycopg2',
                        database="CSCI_341_Assignment_2",
                        host="127.0.0.1",
                        username="postgres",
                        password="Almaz071",
                        port="5432")

engine = create_engine(url)

def query_df(query_str):
    return pd.read_sql_query(query_str, engine)

def query_float(query_str):
    with engine.connect() as con:
        result = con.execute(text(query_str))
        return float(result.fetchone()[0])

print("query for 1 ----------------\n")

# query for 1
print(query_df("""
    select 
        t1.disease_code,
        t1.description
    from 
        public."Disease" t1
    where 
        t1.pathogen = 'bacteria'
"""))

print(' query for 11 ----------------\n')

# query for 11
print(query_df("""
    select 
        t2.description,
        sum(t3.total_patients - t3.total_deaths) as total
    from 
        public."Disease" t1
    left join public."DiseaseType" t2 on (t1.id = t2.id)
    left join public."Record" t3 on (t1.disease_code = t3.disease_code)
    group by
        t2.description
"""))

print('query for 10 ----------------\n')

# query for 10
print(query_df("""
    select 
        t1.cname,
        sum(t2.total_patients) as total_patients
    from 
        public."Country" t1
    left join public."Record" t2 on (t1.cname = t2.cname)
    group by
        t1.cname
    order by
        2 desc
    limit  5
"""))

print('query for 9 ----------------\n')

# query for 9
print(query_df("""
    select 
        t1.email,
        t3.name,
        t1.department
    from 
        public."PublicServant" t1
    left join public."Record" t2 on (t1.email = t2.email)
    left join public."Users" t3 on (t1.email = t3.email)
    where t2.total_patients between 100000 and 999999
"""))

print('query for 4 ----------------\n')

# query for 4
print(query_df("""
    select 
        t1.cname,
        avg(t2.salary) as avg_salary
    from 
        public."Country" t1
    left join public."Users" t2 on (t1.cname = t2.cname)
    left join public."Doctor" t3 on (t2.email = t3.email)
    where lower(t3.degree) = 'virology'
    group by
        t1.cname
"""))

print('query for 3 ----------------\n')

# query for 3
print(query_df("""
    select 
        t1.name,
        t1.surname,
        t2.degree
    from 
        public."Users" t1
    left join public."Doctor" t2 on (t1.email = t2.email)
    left join public."Specialize" t3 on (t1.email = t2.email)
    left join public."DiseaseType" t4 on (t3.id = t4.id)
    group by
        t1.name,
        t1.surname,
        t2.degree
    having count(t4.id) >= 2
""")) 

print('query for 2 ----------------\n')

# query for 2
print(query_df("""
    select 
        t1.name,
        t1.surname,
        t2.degree
    from 
        public."Users" t1
    left join public."Doctor" t2 on (t1.email = t2.email)
    left join public."Specialize" t3 on (t1.email = t2.email)
    left join public."DiseaseType" t4 on (t3.id = t4.id)
    where 
        lower(t4.description) <> 'infectious diseases'
""")) 









