'''
********  cursor().execute().fetchall returns list of dictionary  ********
'''


import flask
from flask import Flask, render_template, redirect, url_for, request, g, session
import codecs
import os
from pydub import AudioSegment
from pathlib import Path
import sqlite3

# import sys
# import signal

NOT_RECORDED = 'not-recorded'
DELETED = 'deleted'
RECORDED = 'recorded'

id = 'id'
sentence = 'sentence'
status = 'status'
table_name = 'sentence_table'

db_file = 'database.db'

cur_dir = os.path.abspath(os.curdir)
wav_dir = os.path.join(cur_dir, 'wav')
Path(wav_dir).mkdir(exist_ok=True)




def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_file)
        db.row_factory = make_dicts
    return db

def get_id_and_text():
    if session.get('id') == None:
        cur = get_db().cursor()
        row = cur.execute('select * from sentence_table where id=(select max(id) from sentence_table where status = ?);', ('not-recorded', )).fetchone()
        session['id'] = row['id']
        session['sentence'] = row['sentence']

        cur.close()

    return (session['id'], session['sentence'])

app = Flask(__name__)
app.secret_key = 'thisissecret'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return redirect(url_for('record'))

@app.route('/record', methods=['GET', 'POST'])
def record():
    # global idx, meta, cur_dir, wav_dir, file_name, NOT_RECORDED, DELETED, RECORDED
    if request.method == 'POST':
        if request.form.get('delete'):
            # request for deleting the sentence.

            # check-point
            sentence_id, _ = get_id_and_text()
            db = get_db()
            db.cursor().execute('update sentence_table set status = ? where id = ?;', ('deleted', sentence_id))
            
            session['id'] = None
            db.commit()

        else:

            sentence_id, _ = get_id_and_text()

            db = get_db()
            db.cursor().execute('update sentence_table set sentence = ?, status = ? where id = ?;', 
                        (request.form['sentence_text'], 'recorded', sentence_id))
            
            db.commit()

            # request for saving the file.

            f = request.files['recorded_audio']
            filename = f'{sentence_id}.webm'
            f.save(filename)

            AudioSegment.from_file(filename).export(os.path.join(wav_dir, f'{sentence_id}.wav'), format='wav')

            os.remove(filename) # remove the webm file


            session['id'] = None


        resp = flask.Response()
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp

    sentence_id, sentence_text = get_id_and_text()
    return render_template('record.html', sentence=sentence_text, _id=sentence_id)



@app.route('/search')
def search():
    return None




if __name__=='__main__':
    app.run(debug=True)