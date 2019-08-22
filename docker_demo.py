from flask import Flask, render_template, request, redirect, url_for
from flask import copy_current_request_context
from flask_sqlalchemy import SQLAlchemy
from threading import Thread
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/testdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #Remove warning
db = SQLAlchemy(app)
class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    ts = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    num1 = db.Column(db.String(32), nullable=False)
    num2 = db.Column(db.String(32), nullable=False)
    ip = db.Column(db.String(16), nullable=False)
    browser_string = db.Column(db.String(256), nullable=False)
    results = db.Column(db.String(64), nullable=False)

@app.route('/main')
def hello() -> '302':
    return redirect(url_for('entry_page'))

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Welcome to Demo page!')

@app.route('/sum', methods=['POST'])
def do_sum() -> 'html':
    @copy_current_request_context
    def log_request(req: 'flask_request', res: str) -> None:
        log = Log(num1=req.form['num1'],
                  num2=req.form['num2'],
                  ip=req.remote_addr,
                  browser_string=req.user_agent.browser,
                  results=res)
        db.session.add(log)
        db.session.commit()
    num1 = request.form['num1']
    num2 = request.form['num2']
    result = str(int(num1) + int(num2))
    try:
        t = Thread(target=log_request, args=(request, result))
        t.start()
    except Exception as err:
        print('Something is wrong. Error:', err)
    return render_template('results.html',
                           the_title='Here is the sum result',
                           the_num1=num1,
                           the_num2=num2,
                           the_results=result)

@app.route('/viewlog')
def view_log() -> 'html':
    content = []
    for log in Log.query.all():
        content.append([log.num1, log.num2,
                        log.ip, log.browser_string,
                        log.results])
    row_titles = ('Num1', 'Num2', 'Remote Address', 'User Agent', 'Result')
    return render_template('viewlog.html',
                           the_title='view log',
                           the_row_titles=row_titles,
                           the_data=content)

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
