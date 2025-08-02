from flask import Flask, render_template, request, redirect, jsonify
import base64
from game import get_pokedex, get_pc, battle, battle_resolve, get_pokemon_from_name

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", pokemon=get_pokedex(), pc=get_pc())

@app.route('/battle', methods=['POST'])
def fight():
    pokemon_name = request.form.get('pokemon_name')
    if pokemon_name:
        result = battle(pokemon_name)
        if 'msg' in result and result['msg'] == "Error Occurred!":
            return redirect('/?tab=battle')
        else:
            return render_template("battle.html",
                                   red_pokemon=get_pokemon_from_name(pokemon_name),
                                   blue_pokemon=get_pokemon_from_name(result['enemy']))
        
@app.route('/results', methods=['POST'])
def resolve_fight():
    choice = request.form.get('choice')
    red_pokemon = get_pokemon_from_name(request.form.get('red_pokemon'))
    blue_pokemon = get_pokemon_from_name(request.form.get('blue_pokemon'))

    results = battle_resolve(choice=choice, red_pokemon=red_pokemon, blue_pokemon=blue_pokemon)
    enc_results = base64.b64encode(results["msg"].encode()).decode()
    return redirect(f'/?tab=battle&results={enc_results}')

if __name__ == "__main__":
    # listen on all interfaces
    app.run(host='0.0.0.0', debug=False)