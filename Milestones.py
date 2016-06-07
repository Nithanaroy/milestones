from flask import render_template
from flask import Flask
from flask import request
from flask import jsonify

from DataSource import MySQL

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('add_milestone.html')


@app.route('/milestone', methods=['POST'])
def add_milestone():
    try:
        req = request.json
        data = {"name": req.get('milestone', None),
                "type": req.get("type", None),
                "date": req.get("date", None),
                "time": req.get("time", None),
                "tags": req.get("tags", None),
                "link": req.get("link", None),
                "description": req.get("description", None)}
        insert_sql = MySQL.insert("milestones", data.keys())
        MySQL.execute(insert_sql, data)
        return jsonify({"message": "1 milestone saved forever!", "data": []})
    except:
        return jsonify({"message": "Couldn't save this. Try again!"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
