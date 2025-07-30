from flask import Flask, render_template
import game

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/pokedex')
def pokedex():
    return render_template("pokedex.html", pokemon=get_pokedex())

if __name__ == "__main__":
    app.run(debug=False)
