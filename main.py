from flask import jsonify,Flask,request, render_template
import json
import sqlite3
from datetime import datetime
app = Flask(__name__)

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

    #to sie wjebie przy zapisywaniu obliczen
    feedback = json.dumps([13.0, 9.158356952756275, 6.848577267441179, 5.688847368181831, 5.3242431258034255, 5.501176120907685,
                 6.034404179965026, 6.79012186655758, 7.672681427294654, 8.614604080104233, 9.56918360593638,
                 10.504864898750888, 11.401158680051136, 12.24548092198102, 13.030965719820589, 13.754687747851214,
                 14.416480987405443, 15.017984532396248, 15.562037781205916, 16.05217375197864, 16.492295040158105,
                 16.886437947239376, 17.238612534664032, 17.552697801535444, 17.83237001464451, 18.08106885159793,
                 18.301980229030008, 18.49801861339885, 18.671849324576506, 18.825880506591403, 18.962287863754856,
                 19.08303038811924, 19.189861088800892, 19.28434891569606, 19.36789529029278, 19.441747061802232,
                 19.507015741263434, 19.564687037909188, 19.615637032505457, 19.6606430868025, 19.700393999682348,
                 19.73549946481067, 19.7665000563815, 19.793873379128797, 19.81804270845294, 19.83938141435088,
                 19.858220524929372, 19.874852132066813, 19.889534131304643])
    setpoint = json.dumps([20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20])
    time = json.dumps([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49])
    conn = sqlite3.connect('baza.db')
    c = conn.cursor()
    c.execute("INSERT INTO wykres VALUES (?,?,?,?)",(feedback,setpoint,time,datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
    conn.commit()
    #koniec zapisywania
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