import os

from bson import ObjectId
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   session, url_for)
from werkzeug.utils import secure_filename

from conection_db import connection
from models.character_model import (create_character, delete_character,
                                    get_characters_by_user, update_character)
from models.class_model import create_default_classes, get_class_by_id
from models.race_model import create_default_races, get_race_by_id
from models.session_model import (add_character_to_session, create_session,
                                  get_all_sessions, get_session_by_id)

app = Flask(__name__)
app.secret_key = os.urandom(24)
db = connection()
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    characters = list(get_characters_by_user(db, session['userId']))
    return render_template('home.html', characters=characters)

@app.route('/login', methods=['GET', 'POST'])
def login():
    collection = connection(table_name='users')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = collection.find_one({'username': username, 'password': password})
        if user:
            session['logged_in'] = True
            session['userId'] = user['userId']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Credenciais inválidas')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    collection = connection(table_name='users')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if collection.find_one({'username': username}):
            return render_template('register.html', error='Usuário já existe')
        else:
            new_user = {
                'username': username,
                'password': password,
            }
            result = collection.insert_one(new_user)
            user_id = str(result.inserted_id)
            
            # Update the document to include userId
            collection.update_one({'_id': result.inserted_id}, {'$set': {'userId': user_id}})

            session['userId'] = user_id
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('userId', None)
    return redirect(url_for('login'))

@app.route('/create_character', methods=['GET', 'POST'])
def create_character_route():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['name']
        class_id = request.form['class_id']
        race_id = request.form['race_id']
        origem = request.form['origem']
        
        # Atributos
        forca = int(request.form['forca'])
        destreza = int(request.form['destreza'])
        constituicao = int(request.form['constituicao'])
        inteligencia = int(request.form['inteligencia'])
        sabedoria = int(request.form['sabedoria'])
        carisma = int(request.form['carisma'])

        # Novos atributos
        reflexo = int(request.form['reflexo'])
        fortitude = int(request.form['fortitude'])
        vontade = int(request.form['vontade'])

        # Perícias
        pericias_selecionadas = request.form.getlist('pericias')

        # Processa o upload da imagem
        if 'img_url' in request.files:
            file = request.files['img_url']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                img_url = file_path

                create_character(db, session['userId'], name, class_id, race_id, img_url, forca, destreza, constituicao, inteligencia, sabedoria, carisma, origem, reflexo, fortitude, vontade, pericias_selecionadas)
                return redirect(url_for('home'))

    classes = db['classes.classes'].find()
    races = db['races.races'].find()
    return render_template('create_character.html', classes=classes, races=races)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/edit_character/<character_id>', methods=['GET', 'POST'])
def edit_character_route(character_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    character = db.chars.find_one({"_id": ObjectId(character_id)})

    if request.method == 'POST':
        name = request.form['name']
        class_id = request.form['class_id']
        race_id = request.form['race_id']

        # Processa o upload da nova imagem, se for o caso
        if 'img_url' in request.files and request.files['img_url'].filename != '':
            file = request.files['img_url']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                img_url = file_path
            else:
                img_url = character['img_url']
        else:
            img_url = character['img_url']

        update_character(db, character_id, name, class_id, race_id, img_url)
        return redirect(url_for('home'))

    classes = db.classes.find()
    races = db.races.find()
    return render_template('edit_character.html', character=character, classes=classes, races=races)

@app.route('/delete_character/<character_id>')
def delete_character_route(character_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    delete_character(db, character_id)
    return redirect(url_for('home'))

@app.route('/sessions', methods=['GET', 'POST'])
def sessions():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        session_name = request.form['session_name']
        create_session(db, session_name, session['userId'])
        return redirect(url_for('sessions'))

    all_sessions = list(get_all_sessions(db))
    return render_template('sessions.html', sessions=all_sessions)


@app.route('/join_session/<session_id>', methods=['GET', 'POST'])
def join_session(session_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        character_id = request.form['character_id']
        add_character_to_session(db, session_id, character_id)
        
        # Atualiza a sessão Flask para refletir a sessão do jogo
        session['game_session_id'] = session_id
        session['character_id'] = character_id
        
        return redirect(url_for('game_lobby'))

    characters = list(get_characters_by_user(db, session['userId']))
    session_data = get_session_by_id(db, session_id)
    return render_template('join_session.html', session=session_data, characters=characters)

@app.route('/game_lobby')
def game_lobby():
    if not session.get('logged_in') or 'game_session_id' not in session:
        return redirect(url_for('login'))

    session_data = get_session_by_id(db, session['game_session_id'])
    character = db.chars.find_one({"user_id": ObjectId(session['userId'])})

    # Buscando informações de classe e raça
    class_info = db['classes.classes'].find_one({"_id": ObjectId(character['class_id'])})
    race_info = db['races.races'].find_one({"_id": ObjectId(character['race_id'])})

    # Adicionando as informações de classe e raça ao personagem do usuário
    character['class_name'] = class_info['name'] if class_info else "Classe Desconhecida"
    character['race_name'] = race_info['name'] if race_info else "Raça Desconhecida"
    character['class_habilidades'] = class_info['habilidades_classe'] if class_info else []
    character['race_habilidades'] = race_info['habilidades_inatas'] if race_info else []

    # Carregando os personagens dos outros jogadores
    other_characters = []
    for char_id in session_data['characters']:
        if str(char_id) != str(character['_id']):
            char = db.chars.find_one({"_id": ObjectId(char_id)})
            if char:
                char_class = db['classes.classes'].find_one({"_id": ObjectId(char['class_id'])})
                char_race = db['races.races'].find_one({"_id": ObjectId(char['race_id'])})

                char['class_name'] = char_class['name'] if char_class else "Classe Desconhecida"
                char['race_name'] = char_race['name'] if char_race else "Raça Desconhecida"
                char['class_habilidades'] = char_class['habilidades_classe'] if char_class else []
                char['race_habilidades'] = char_race['habilidades_inatas'] if char_race else []
                other_characters.append(char)

    return render_template('game_lobby.html', character=character, other_characters=other_characters, session_name=session_data['name'])


@app.route('/get_player_details/<player_id>', methods=['GET'])
def get_player_details(player_id):
    character = db.chars.find_one({"_id": ObjectId(player_id)})

    if character:
        # Busca informações de classe e raça
        class_info = db['classes.classes'].find_one({"_id": ObjectId(character['class_id'])})
        race_info = db['races.races'].find_one({"_id": ObjectId(character['race_id'])})
        
        response = {
            "name": character['name'],
            "class_name": class_info['name'] if class_info else "Classe Desconhecida",
            "race_name": race_info['name'] if race_info else "Raça Desconhecida",
            "forca": character['forca'],
            "destreza": character['destreza'],
            "constituicao": character['constituicao'],
            "inteligencia": character['inteligencia'],
            "sabedoria": character['sabedoria'],
            "carisma": character['carisma'],
            "class_habilidades": class_info['habilidades_classe'] if class_info else [],
            "race_habilidades": race_info['habilidades_inatas'] if race_info else []
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Character not found"}), 404

@app.route('/get_current_player_details', methods=['GET'])
def get_current_player_details():
    character = db.chars.find_one({"user_id": ObjectId(session['userId'])})

    if character:
        # Busca informações de classe e raça
        class_info = db['classes.classes'].find_one({"_id": ObjectId(character['class_id'])})
        race_info = db['races.races'].find_one({"_id": ObjectId(character['race_id'])})
        
        response = {
            "name": character['name'],
            "class_name": class_info['name'] if class_info else "Classe Desconhecida",
            "race_name": race_info['name'] if race_info else "Raça Desconhecida",
            "forca": character['forca'],
            "destreza": character['destreza'],
            "constituicao": character['constituicao'],
            "inteligencia": character['inteligencia'],
            "sabedoria": character['sabedoria'],
            "carisma": character['carisma'],
            "class_habilidades": class_info['habilidades_classe'] if class_info else [],
            "race_habilidades": race_info['habilidades_inatas'] if race_info else []
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Character not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
