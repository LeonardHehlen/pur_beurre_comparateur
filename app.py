from flask import Flask, render_template, url_for, redirect, request
import requests

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def main():
    return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True)