from flask import Flask

app = Flask(__name__)

@app.route('/')
def Hello_algolia():
    return '<h1>Hello Algolia Test</h1>'

@app.route('/toto')
def Hello_toto():
    return '<h1>Hello Algolia Super Toto</h1>'


if __name__ == "__main__":
    app.run(debug=True)