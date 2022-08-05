from unicodedata import name
from flask import Flask
from flask import request
from flask_cors import CORS
from waitress import serve
from datetime import date, datetime
import json

#API setup
api = Flask(__name__)
CORS(api)

#Data's
version = "1.0.0"
ipTable = []

@api.route('/get_version/', methods=['GET', 'POST'])
def get_version():
    return version, 200

@api.route('/get_table/', methods=['GET', 'POST'])
def get_table():
    return json.dumps(ipTable), 200

@api.route('/clear_table/', methods=['GET', 'POST'])
def clear_table():
    ipTable.clear()
    return "", 200

@api.route('/add_row', methods=['GET', 'POST'])
def add_table():
    name = request.args.get('name')
    ip = request.args.get('ip')
    date = str(datetime.now().time().strftime("%H:%M:%S"))
    if len(ipTable) > 0:
        for index, i in enumerate(ipTable):
            if str(i).find("'" + name + "'") > -1:
                ipTable[index] = {"name":name, "ip":ip, "date":date}
                return "", 500
    if len(ipTable) < 25:
        ipTable.append({"name":name, "ip":ip, "date":date})
        return "", 200
    else:
        return "to many users", 200

#Run API
if __name__ == '__main__':
    api.debug = True
    api.run(threaded=True)
    #serve(api, host="127.0.0.1", port=5000)