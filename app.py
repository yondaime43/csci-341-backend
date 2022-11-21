from flask import Flask
from flask_cors import CORS

import routes.doctors
import routes.publicServants
import routes.record
import routes.diseases

app = Flask(__name__)
CORS(app)

app.add_url_rule('/doctors/<email>',  'doctor', routes.doctors.doctor, methods=['PUT', 'DELETE'])
app.add_url_rule('/doctors',  'doctors', routes.doctors.doctors, methods=['GET', 'POST'])

app.add_url_rule('/public-servants/<email>',  'public-servant', routes.publicServants.publicServant, methods=['PUT', 'DELETE'])
app.add_url_rule('/public-servants',  'public-servants', routes.publicServants.publicServants, methods=['GET', 'POST'])

app.add_url_rule('/records/<email>',  'record', routes.record.record, methods=['PUT', 'DELETE'])
app.add_url_rule('/records',  'records', routes.record.records, methods=['GET', 'POST'])

app.add_url_rule('/diseases/<disease_code>',  'disease', routes.diseases.disease, methods=['PUT', 'DELETE'])
app.add_url_rule('/diseases',  'diseases', routes.diseases.diseases, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run()
