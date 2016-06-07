from flask import render_template
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('add_milestone.html')


@app.route('/milestone', methods=['POST'])
def add_milestone():
    return 'Hello World'


if __name__ == '__main__':
    app.run()
