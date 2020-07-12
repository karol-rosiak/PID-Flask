from flask import jsonify,Flask,request, render_template
import json
import sqlite3
from datetime import datetime
import PID
import Zbiornik
import time
import numpy as np
from scipy.interpolate import BSpline, make_interp_spline #  Switched to BSpline
app = Flask(__name__)

def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class

    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    zbiornik = Zbiornik.ZBIORNIK()
    pid = PID.PID(P, I, D)

    pid.SetPoint = 20
    pid.setSampleTime(0.01)

    END = L
    feedback = zbiornik.poziom

    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        if output > 100:
            output = 100
        zbiornik.open(output)
        feedback = zbiornik.poziom

        time.sleep(0.02)

        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)


    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)

    # feedback_smooth = spline(time_list, feedback_list, time_smooth)
    # Using make_interp_spline to create BSpline
    helper_x3 = make_interp_spline(time_list, feedback_list)
    feedback_smooth = helper_x3(time_smooth)

    #zapisz do bazy wyniki
    print(type(feedback_smooth))
    feedback = json.dumps(feedback_smooth.tolist())
    setpoint = json.dumps(setpoint_list)
    time_to_save = json.dumps( time_list)
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    c.execute("INSERT INTO wykres VALUES (?,?,?,?)",
              (feedback, setpoint, time_to_save, datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    conn.commit()
    conn.close()

def createtable():
    import sqlite3
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    c.execute('''create table if not exists wykres (feedback TEXT, setpoint TEXT, time INTEGER, timeCreated TEXT)''')
    c.execute('''create table if not exists lokalizacja (lat NUMERIC, lang NUMERIC, timeCreated TEXT)''')
    conn.commit()
    conn.close()


@app.route('/')
def main():
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    createtable()
    tab = c.execute('SELECT * FROM lokalizacja ORDER BY rowid DESC LIMIT 1').fetchone()
    conn.close()
    print(tab)
    return render_template('index.html', title='Obliczanie PID', lat=tab[0], lng=tab[1])

@app.route('/updateLocation' ,methods=['POST'])
def updatelocation():
    data = request.json
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    c.execute("INSERT INTO lokalizacja VALUES (?,?,?)",(data['lat'],data['lng'],datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    conn.commit()
    conn.close()
    return jsonify({"status":"ok"})

@app.route('/chartData' ,methods=['POST'])
def summary():
    test_pid(3, 13, 0.01, L=200)
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    tab = c.execute('SELECT * FROM wykres ORDER BY rowid DESC LIMIT 1').fetchone()
    conn.close()

    dict = {}
    #data = request.json
    #print(data['weather'])
    #a,b,labels = test_pid()
    dict['a'] = json.loads(tab[0])
    dict['b'] = json.loads(tab[1])
    dict['title'] = 'test'
    dict['aLabel'] = 'feedback'
    dict['bLabel'] = 'setpoint'
    dict['labels'] = json.loads(tab[2])
    dict['xLabel'] = 'x'
    dict['yLabel'] = 'y'

    return jsonify(dict)

if __name__ == '__main__':
    app.run(port=5000,debug=True)