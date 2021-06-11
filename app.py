from re import I
from classify_image import classify_image
from flask import Flask, render_template, request, redirect, url_for, request, json, jsonify, current_app as app
from datetime import date
from sense_hat import SenseHat
from time import sleep
from datetime import date
from subprocess import Popen, PIPE
import random
#from random import seed
#from random import randint
import time
import argparse
import contextlib
import select
import sys
import termios
import tty
import numpy as np
from cv2 import imread
from pycoral.utils.dataset import read_label_file
import vision
import requests
import sys
import sqlite3 
import collect_images
import classify_image
import threading

w = (255, 255, 255)
b = (0, 0, 0)

number = [
    b, b, b, b, b, b, b, b,
    b, b, w, w, w, b, b, b,
    b, b, b, b, w, b, b, b,
    b, b, b, b, w, b, b, b,
    b, b, b, b, w, b, b, b,
    b, b, b, b, w, b, b, b,
    b, b, w, w, w, w, w, b,
    b, b, b, b, b, b, b, b]

number2 = [
    b, b, b, b, b, b, b, b,
    b, b, w, w, w, w, b, b,
    b, b, b, b, b, w, b, b,
    b, b, w, w, w, w, b, b,
    b, b, w, b, b, b, b, b,
    b, b, w, b, b, b, b, b,
    b, b, w, w, w, w, b, b,
    b, b, b, b, b, b, b, b]

number3 = [
    b, b, b, b, b, b, b, b,
    b, b, w, w, w, w, b, b,
    b, b, b, b, b, w, b, b,
    b, b, b, b, b, w, b, b,
    b, b, w, w, w, w, b, b,
    b, b, b, b, b, w, b, b,
    b, b, b, b, b, w, b, b,
    b, b, w, w, w, w, b, b]




sense = SenseHat()

classifier = vision.Classifier(vision.CLASSIFICATION_MODEL)
labels = read_label_file(vision.CLASSIFICATION_LABELS)

app = Flask(__name__)

def countdown():
    global t
    t = 15
    while t:
        t -= 1
        time.sleep(1)
        print(t)

@app.route('/')
def info():
    return redirect(url_for('all'))

@app.route('/all', methods=(['GET', 'POST']))
def all():
    if request.method == 'POST':
        #code to store user and date
        user = request.form['user']
        today = str(date.today())
        score = 0
        return redirect(url_for('game', user=user, today=today, score=score))
    else:
        #code to get data from  database
        conn = sqlite3.connect('./static/data/game.db')
        curs = conn.cursor()
        scores = []
        rows = curs.execute("SELECT * FROM game ORDER BY score DESC")
        for row in rows:
            score = ({'id': row[0], 'user': row[1], 'date':row[2], 'score': row[3]})
            scores.append(score)
        return render_template('index.html', scores=scores)

@app.route('/data/<user>/<today>/<score>', methods=(['GET', 'POST']))
def data(user, today, score):
    #database and storing task
    conn = sqlite3.connect('./static/data/game.db')
    curs = conn.cursor()
    curs.execute("INSERT INTO game (user, date, score) VALUES((?),(?),(?))", (user, today, score))
    conn.commit ()
    #closes connection to database
    conn.close()

    return redirect(url_for('all'))

@app.route('/game/<user>/<today>/<score>', methods=(['GET', 'POST']))
def game(user, today, score):
    #objects for games
    objects = ['0', 'mouse', 'controller', 'remote']
    #i = 0
    #sense.show_message('1 = mouse 2 = controller 3 = remote GL')
    while True:    
        value = random.randint(1, 3)
        #print(value)
        w = (255, 255, 255)
        if value == 1:
            sense.set_pixels(number)
        elif value == 2:
            sense.set_pixels(number2)
        elif value == 3:
            sense.set_pixels(number3)
        else:
            print('rand error')

        count_thread = threading.Thread(target=countdown)
        count_thread.start()
        score = int(score)

        for frame in vision.get_frames():

            objectA =  classify_image.classify_image(frame) #detector.get_objects(frame)
            #print(objectA)
            time.sleep(.1)
            #output = classify_image.classify_image(vision.get_frames())
            #if objectA == 'mouse':
            #    return objectA
            #elif objectA == 'controller':
            #    return objectA
            #elif objectA == 'remote':
            #    return objectA
            if t > 0:
                if objectA == objects[value]:
                    score = score + 1
                    break
                elif objectA == 'Background':
                    score = score
                else:
                    print('game over')
                    return redirect(url_for('data', user=user, today=today, score=str(score)))
            else:
                return redirect(url_for('data', user=user, today=today, score=str(score)))

@app.route('/test')
def test():
    return 0
      



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')