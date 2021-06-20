from flask import Flask, render_template, request
views = Flask(__name__)
views.debug = True

@views.route('/', methods=['GET'])
def dropdown():
    sets = ['STX', 'KHM', 'ZNR', 'M21']
    return render_template('home.html', sets=sets)
