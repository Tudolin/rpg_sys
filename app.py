from gevent import monkey

monkey.patch_all()
import logging
import os
import sys
from io import BytesIO

from bson import ObjectId
from flask import (Flask, flash, jsonify, redirect, render_template, request,
                   send_file, session, url_for)
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from redis import Redis
from reportlab.lib import colors, enums
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename

from conection_db import connection
from flask_session import Session
from models.character_model import (create_character, delete_character,
                                    get_characters_by_user, update_character)
from models.class_model import create_default_classes, get_class_by_id
from models.race_model import create_default_races, get_race_by_id
from models.session_model import (add_character_to_session, create_session,
                                  get_all_sessions, get_session_by_id,
                                  remove_character_from_session)

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY') or 'a212d3b5e27f9cd2dfb8a9d18587ae51b2f88af9e1e95112'
app.config['SESSION_PROTECTION'] = 'strong'
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379, db=0, password=None)
app.config['SESSION_TYPE'] = 'filesystem' #for local host debug
Session(app)

CORS(app)
sys.path.insert(0, '/home/angellnadalin/rpg_sys')
db = connection()
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app, cors_allowed_origins="https://familyrpg.servebeer.com")
MEDIA_FOLDER = 'static/media/'
app.config['MEDIA_FOLDER'] = MEDIA_FOLDER
MUSIC_FOLDER = 'static/music/'
app.config['MUSIC_FOLDER'] = MUSIC_FOLDER

@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    characters = list(get_characters_by_user(db, session['userId']))
    return render_template('home.html', characters=characters)

@app.route('/delete_session/<session_id>', methods=['POST'])
def delete_session(session_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    session_data = get_session_by_id(db, session_id)
    
    if session_data['created_by'] == ObjectId(session['userId']):
        db.sessions.delete_one({"_id": ObjectId(session_id)})
        flash("Sessão excluída com sucesso.", "success")
    else:
        flash("Você não tem permissão para excluir esta sessão.", "danger")
    
    return redirect(url_for('sessions'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    collection = connection(table_name='users')
    if collection is None:
        app.logger.error("Failed to connect to the users collection.")
        return render_template('login.html', error='Database connection failed.')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        app.logger.info(f"Tentativa de login com usuário: {username}")

        user = collection.find_one({'username': username, 'password': password})
        if user:
            session['logged_in'] = True
            session['userId'] = str(user['_id'])
            session['username'] = user['username']
            app.logger.info("Login bem-sucedido")
            return redirect(url_for('home'))
        else:
            app.logger.warning("Credenciais inválidas")
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
    # Remover o usuário da sessão de jogo, se estiver em uma
    if 'game_session_id' in session:
        session_data = get_session_by_id(db, session['game_session_id'])
        for character_id in session_data.get('characters', []):
            character = db.chars.find_one({"_id": ObjectId(character_id)})
            if character and str(character['user_id']) == session['userId']:
                remove_character_from_session(db, session['game_session_id'], character_id)
        session.pop('game_session_id', None)

    # Finalizar a sessão do usuário
    session.pop('logged_in', None)
    session.pop('userId', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/create_character', methods=['GET', 'POST'])
def create_character_route():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # Carregar dados do MongoDB
    classes = list(db['classes.classes'].find())
    races = list(db['races.races'].find())
    abilities = list(db['abilities.abilities'].find())

    habilidades_disponiveis = {
        'race': [],
        'class': []
    }

    # Populate race abilities
    for race in races:
        habilidades_race = []
        for habilidade in abilities:
            if race['_id'] in [ObjectId(id) for id in habilidade['related_to']['race_ids']]:
                habilidades_race.append({
                    'nome': habilidade['name'],
                    'descricao': habilidade['description'],
                    'custo_mana': habilidade['cost']['mana'],
                    'custo_energia': habilidade['cost']['energy']
                })
        habilidades_disponiveis['race'].append({
            'id': str(race['_id']),
            'habilidades': habilidades_race
        })

    # Populate class abilities
    for classe in classes:
        habilidades_class = []
        for habilidade in abilities:
            if classe['_id'] in [ObjectId(id) for id in habilidade['related_to']['race_ids']]:
                habilidades_class.append({
                    'nome': habilidade['name'],
                    'descricao': habilidade['description'],
                    'custo_mana': habilidade['cost']['mana'],
                    'custo_energia': habilidade['cost']['energy']
                })
        habilidades_disponiveis['class'].append({
            'id': str(classe['_id']),
            'habilidades': habilidades_class
        })

    if request.method == 'POST':
        # Processamento do formulário
        name = request.form['name']
        class_id = request.form.get('class_id')
        race_id = request.form.get('race_id')
        origem = request.form['origem']

        # Atributos
        forca = int(request.form['forca'])
        destreza = int(request.form['destreza'])
        constituicao = int(request.form['constituicao'])
        inteligencia = int(request.form['inteligencia'])
        sabedoria = int(request.form['sabedoria'])
        carisma = int(request.form['carisma'])

        # Get selected skills and abilities
        pericias_selecionadas = request.form.getlist('pericias')
        habilidades_selecionadas = request.form.getlist('habilidades')

        print("Pericias : ", pericias_selecionadas)
        print("Habilidades : ", habilidades_selecionadas)

        if len(habilidades_selecionadas) > 5:
            return "Você pode selecionar no máximo 5 habilidades.", 400

        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        img_url = None
        if 'img_url' in request.files:
            file = request.files['img_url']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                img_url = file_path
            else:
                return "Unsupported image format. Only PNG and JPG are supported.", 400

        if not class_id or not race_id:
            return "Class ID and Race ID are required.", 400

        # Chamar função para criar o personagem
        create_character(
            db, session['userId'], name, class_id, race_id, img_url,
            forca, destreza, constituicao, inteligencia, sabedoria, carisma,
            origem, pericias_selecionadas, habilidades_selecionadas
        )
        return redirect(url_for('home'))

    # Renderizar o template com os dados
    return render_template('create_character.html', classes=classes, races=races, habilidades_disponiveis=habilidades_disponiveis)





def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/edit_character/<character_id>', methods=['GET', 'POST'])
def edit_character_route(character_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    character = db.chars.find_one({"_id": ObjectId(character_id)})

    if request.method == 'POST':
        name = request.form['name']
        class_id = request.form.get('class_id')
        race_id = request.form.get('race_id')

        
        # Atualizando os atributos
        forca = int(request.form['forca'])
        destreza = int(request.form['destreza'])
        constituicao = int(request.form['constituicao'])
        inteligencia = int(request.form['inteligencia'])
        sabedoria = int(request.form['sabedoria'])
        carisma = int(request.form['carisma'])

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

        # Atualizando o personagem no banco de dados
        update_data = {
            "name": name,
            "class_id": ObjectId(class_id),
            "race_id": ObjectId(race_id),
            "forca": forca,
            "destreza": destreza,
            "constituicao": constituicao,
            "inteligencia": inteligencia,
            "sabedoria": sabedoria,
            "carisma": carisma,
            "img_url": img_url
        }

        db.chars.update_one(
            {"_id": ObjectId(character_id)},
            {"$set": update_data}
        )
        return redirect(url_for('home'))

    # Carregando as classes e raças para o formulário de edição
    classes = db['classes.classes'].find()
    races = db['races.races'].find()
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
        session_id = create_session(db, session_name, session['userId'])
        return redirect(url_for('sessions'))

    all_sessions = list(get_all_sessions(db))

    # Adicionando o nome do criador para cada sessão e convertendo ID para string
    for sess in all_sessions:
        user = db.users.find_one({"_id": sess['created_by']})
        sess['creator_name'] = user['username'] if user else "Desconhecido"
        sess['created_by'] = str(sess['created_by'])  # Convertendo o ID do criador para string
        sess['userId'] = session['userId']  # Adicionando o userId atual à sessão para comparação no template

    return render_template('sessions.html', sessions=all_sessions)


@app.route('/join_session/<session_id>', methods=['GET', 'POST'])
def join_session(session_id):
    if not session.get('logged_in'):
        app.logger.info('Usuário não está logado, redirecionando para login.')
        return redirect(url_for('login'))

    app.logger.info('Usuário está logado. ID: %s', session['userId'])

    # Carregue os personagens do usuário atual
    characters = get_characters_by_user(db, session['userId'])

    # Carregar o nome da sessão
    session_data = get_session_by_id(db, session_id)
    session_name = session_data.get('name', 'Sessão Desconhecida') if session_data else 'Sessão Desconhecida'

    if request.method == 'POST':
        character_id = request.form['character_id']

        # Verificar se o personagem já está na sessão
        if character_id in session_data.get('characters', []):
            flash('Este personagem já está na sessão.', 'danger')
            return redirect(url_for('game_lobby'))

        # Lógica para adicionar o personagem à sessão
        add_character_to_session(db, session_id, character_id)
        session['game_session_id'] = session_id  # Certifique-se de que o ID da sessão do jogo é armazenado na sessão
        
        # Emitir evento de entrada de jogador via WebSocket
        character = db.chars.find_one({"_id": ObjectId(character_id)})
        class_info = db['classes.classes'].find_one({"_id": ObjectId(character['class_id'])})
        race_info = db['races.races'].find_one({"_id": ObjectId(character['race_id'])})
        
        character_data = {
            'name': character['name'],
            'class_name': class_info['name'] if class_info else "Classe Desconhecida",
            'race_name': race_info['name'] if race_info else "Raça Desconhecida",
            'hp': character['hp'],
            'img_url': character['img_url']
        }

        socketio.emit('new_player', character_data, room=session_id)

        return redirect(url_for('game_lobby'))

    return render_template('join_session.html', characters=characters, session_name=session_name, session_data=session_data)





@app.route('/game_lobby')
def game_lobby():
    if not session.get('logged_in') or 'game_session_id' not in session:
        return redirect(url_for('login'))

    session_data = get_session_by_id(db, session['game_session_id'])
    character = db.chars.find_one({"user_id": ObjectId(session['userId'])})
    if not character:
        return redirect(url_for('home'))

    if 'current_hp' not in character or character['current_hp'] is None:
        character['current_hp'] = character['hp']
        logging.debug(f"Set default current_hp for character: {character['_id']}")

    # Certifique-se de atualizar `current_hp` corretamente
    db.chars.update_one(
        {"_id": ObjectId(character['_id'])},
        {"$set": {"current_hp": character.get('current_hp', character['hp'])}}
    )

    # Buscando informações de classe e raça
    class_info = db['classes.classes'].find_one({"_id": ObjectId(character['class_id'])})
    race_info = db['races.races'].find_one({"_id": ObjectId(character['race_id'])})

    # Adicionando as informações de classe e raça ao personagem do usuário
    character['class_name'] = class_info['name'] if class_info else "Classe Desconhecida"
    character['race_name'] = race_info['name'] if race_info else "Raça Desconhecida"
    character['habilidades'] = class_info.get('habilidades_classe', {}).copy() if class_info else {}
    character['habilidades'].update(race_info.get('habilidades_inatas', {})) if race_info else {}

    # Formatando habilidades para exibição
    habilidades_formatadas = [f"{nome}: {descricao}" for nome, descricao in character['habilidades'].items()]
    character['habilidades'] = habilidades_formatadas

    # Perícias
    character['pericias'] = character.get('pericias', {})

    # Carregando os personagens dos outros jogadores
    other_characters = []
    for char_id in session_data.get('characters', []):
        if str(char_id) != str(character['_id']):
            char = db.chars.find_one({"_id": ObjectId(char_id)})
            if char:
                char_class = db['classes.classes'].find_one({"_id": ObjectId(char['class_id'])})
                char_race = db['races.races'].find_one({"_id": ObjectId(char['race_id'])})
                
                char['class_name'] = char_class['name'] if char_class else "Classe Desconhecida"
                char['race_name'] = char_race['name'] if char_race else "Raça Desconhecida"
                char['habilidades'] = char_class.get('habilidades_classe', {}).copy() if char_class else {}
                char['habilidades'].update(char_race.get('habilidades_inatas', {})) if char_race else {}
                
                # Formatando habilidades para exibição
                char['habilidades'] = [f"{nome}: {descricao}" for nome, descricao in char['habilidades'].items()]
                char['pericias'] = char.get('pericias', {})
                
                other_characters.append(char)

    # Remova duplicatas do `other_characters`
    other_characters = list({v['_id']:v for v in other_characters}.values())

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
            "habilidades": character['habilidades'],
            "pericias": character['pericias'],
            "img_url": character['img_url'] if 'img_url' in character else '/static/images/default.png'  # Adiciona a imagem
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
            "habilidades": character['habilidades'],
            "pericias": character['pericias'],
            "img_url": character['img_url'] if 'img_url' in character else '/static/images/default.png'  # Adiciona a imagem
        }
        return jsonify(response)
    else:
        return jsonify({"error": "Character not found"}), 404


@app.route('/master_control/<session_id>', methods=['GET', 'POST'])
def master_control(session_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    session_data = get_session_by_id(db, session_id)

    if session_data['created_by'] != ObjectId(session['userId']):
        flash("Apenas o Mestre da sessão pode acessar essa página.", "danger")
        return redirect(url_for('home'))

    characters = []
    for char_id in session_data['characters']:
        character = db.chars.find_one({"_id": ObjectId(char_id)})
        if character:
            characters.append(character)

    if request.method == 'POST':
        char_id = request.form['char_id']
        hp = int(request.form['hp'])
        db.chars.update_one(
            {"_id": ObjectId(char_id)},
            {"$set": {"current_hp": hp}}
        )

        # Emitir atualização de vida via Socket.IO
        character = db.chars.find_one({"_id": ObjectId(char_id)})
        room = session_id
        if room:
            socketio.emit('health_updated', {
                'character_id': str(character['_id']),
                'new_health': character['current_hp'],
                'max_health': character['hp']
            }, room=room)

        flash("Status do personagem atualizado com sucesso!", "success")
        return redirect(url_for('master_control', session_id=session_id))

    return render_template('master_control.html', characters=characters,session_data=session_data, session_name=session_data['name'])


@app.route('/update_character', methods=['POST'])
def update_character():
    data = request.get_json()
    
    char_id = data.get('char_id')
    new_hp = data.get('hp')
    new_status = data.get('status')

    if char_id:
        # Atualiza o personagem no banco de dados
        db.chars.update_one(
            {"_id": ObjectId(char_id)},
            {"$set": {"current_hp": int(new_hp), "status": new_status}}
        )
        
        # Emitir uma mensagem via Socket.IO para atualizar a vida em tempo real
        character = db.chars.find_one({"_id": ObjectId(char_id)})
        room = session.get('game_session_id')
        if room:
            socketio.emit('health_updated', {
                'character_id': str(character['_id']),
                'new_health': character['current_hp'],
                'max_health': character['hp']
            }, room=room)

        return jsonify({"success": True})
    
    return jsonify({"success": False}), 400

@app.route('/remove_player/<char_id>', methods=['POST'])
def remove_player(char_id):
    if not session.get('logged_in'):
        return jsonify({"success": False, "error": "Not logged in"}), 403

    session_id = session.get('game_session_id')
    if not session_id:
        return jsonify({"success": False, "error": "No active session"}), 403

    # Verifique se o usuário é o mestre da sessão
    session_data = get_session_by_id(db, session_id)
    if session_data['created_by'] != ObjectId(session['userId']):
        return jsonify({"success": False, "error": "Not the session master"}), 403

    # Remova o personagem da sessão
    remove_character_from_session(db, session_id, char_id)

    # Envie uma mensagem via WebSocket para desconectar o jogador
    socketio.emit('player_removed', {'character_id': char_id}, room=session_id)

    return jsonify({"success": True})


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm'}

@app.route('/upload_media', methods=['POST'])
def upload_media():
    if 'media' not in request.files:
        return jsonify({'error': 'No media file provided'}), 400

    file = request.files['media']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    display_time = request.form.get('display_time', type=int)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['MEDIA_FOLDER'], filename)
        file.save(file_path)

        # Send the media to all players
        socketio.emit('new_media', {
            'media_url': url_for('static', filename=f'media/{filename}'),
            'display_time': display_time
        }, to='/')  # Broadcast to all connected clients

        return jsonify({'success': True, 'media_url': url_for('static', filename=f'media/{filename}')})
    
    return jsonify({'error': 'File not allowed'}), 400



@app.route('/music_tracks', methods=['GET'])
def get_music_tracks():
    tracks = []
    for filename in os.listdir(app.config['MUSIC_FOLDER']):
        print(filename)
        if filename.lower().endswith(('mp3', 'wav', 'ogg')):
            tracks.append({
                'name': filename.rsplit('.', 1)[0],
                'url': url_for('static', filename=f'music/{filename}')
            })
    return jsonify(tracks)

@app.route('/play_music', methods=['POST'])
def play_music():
    try:
        data = request.get_json()
        track_url = data.get('track_url')
        
        # Logging the track URL for debugging
        print(f"Received request to play track: {track_url}")
        
        if track_url:
            # Further validation can be added here, such as checking if the file exists
            if not os.path.exists(os.path.join(app.static_folder, track_url.replace('/static/', ''))):
                print(f"Track not found: {track_url}")
                return jsonify({'error': 'Track not found'}), 404
            
            # Emit the message to all connected clients without broadcast
            socketio.emit('play_music', {'track_url': track_url}, namespace='/')
            return jsonify({'success': True})
        else:
            print("No track URL provided")
            return jsonify({'error': 'No track URL provided'}), 400
    except Exception as e:
        # Print the error to the console for debugging
        print(f"Error in /play_music: {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/stop_music', methods=['POST'])
def stop_music():
    try:
        # Emit the stop_music event to all connected clients in the default namespace
        socketio.emit('stop_music', namespace='/')
        return jsonify({'success': True})
    except Exception as e:
        # Print the error to the console for debugging
        print(f"Error in /stop_music: {e}")
        return jsonify({'error': str(e)}), 500


@socketio.on('join')
def on_join(data):
    room = session.get('game_session_id')
    if room:
        join_room(room)
        character = db.chars.find_one({"user_id": ObjectId(session['userId'])})
        
        if character:
            class_info = db['classes.classes'].find_one({"_id": ObjectId(character['class_id'])})
            race_info = db['races.races'].find_one({"_id": ObjectId(character['race_id'])})
            
            character_data = {
                '_id': str(character['_id']),
                'name': character['name'],
                'class_name': class_info['name'] if class_info else "Classe Desconhecida",
                'race_name': race_info['name'] if race_info else "Raça Desconhecida",
                'hp': character['hp'],
                'img_url': character['img_url']
            }

            # Verificar se o personagem já está na lista de personagens da sessão
            session_data = get_session_by_id(db, room)
            if str(character['_id']) not in [str(c_id) for c_id in session_data.get('characters', [])]:
                add_character_to_session(db, room, character['_id'])

            # Emite a lista atualizada de todos os personagens para sincronização completa
            emit('session_sync', get_current_session_data(room), room=room)


@socketio.on('disconnect')
def handle_disconnect():
    room = session.get('game_session_id')
    if room:
        # Encontra o personagem associado ao usuário que está desconectando
        character = db.chars.find_one({"user_id": ObjectId(session['userId'])})
        if character:
            # Remove o personagem da sessão
            remove_character_from_session(db, room, character['_id'])

            # Notifique os outros jogadores, incluindo o mestre, que o jogador saiu
            socketio.emit('player_left', {'_id': str(character['_id'])}, room=room)

@socketio.on('connect')
def on_connect():
    room = session.get('game_session_id')
    if room:
        join_room(room)
        character = db.chars.find_one({"user_id": ObjectId(session['userId'])})

        if character:
            # Adiciona o personagem à sessão se ele não estiver nela
            session_data = get_session_by_id(db, room)
            if str(character['_id']) not in [str(c_id) for c_id in session_data.get('characters', [])]:
                add_character_to_session(db, room, character['_id'])

            # Enviar a lista atualizada de todos os jogadores na sessão
            all_characters = session_data.get('characters', [])
            all_character_data = []
            for char_id in all_characters:
                char = db.chars.find_one({"_id": ObjectId(char_id)})
                if char:  # Garante que o personagem foi encontrado
                    char_class_info = db['classes.classes'].find_one({"_id": ObjectId(char['class_id'])})
                    char_race_info = db['races.races'].find_one({"_id": ObjectId(char['race_id'])})
                    all_character_data.append({
                        '_id': str(char['_id']),
                        'name': char['name'],
                        'class_name': char_class_info['name'] if char_class_info else "Classe Desconhecida",
                        'race_name': char_race_info['name'] if char_race_info else "Raça Desconhecida",
                        'hp': char['hp'],
                        'img_url': char['img_url']
                    })

            emit('session_sync', {'characters': all_character_data}, room=room)



@socketio.on('new_media')
def handle_new_media(data):
    session_id = session.get('game_session_id')
    if session_id:
        filename = data.get('filename')
        if filename:
            media_url = url_for('static', filename=f'media/{filename}')
            socketio.emit('new_media', {'media_url': media_url}, room=session_id)

def get_current_session_data(session_id):
    session_data = get_session_by_id(db, session_id)
    app.logger.info(f"Session Data: {session_data}")

    if session_data:
        characters = []
        for char_id in session_data.get('characters', []):
            character = db.chars.find_one({"_id": ObjectId(char_id)})
            if character:
                class_info = db['classes.classes'].find_one({"_id": ObjectId(character['class_id'])})
                race_info = db['races.races'].find_one({"_id": ObjectId(character['race_id'])})
                
                character_info = {
                    '_id': str(character['_id']),
                    'name': character['name'],
                    'class_name': class_info['name'] if class_info else 'Classe Desconhecida',
                    'race_name': race_info['name'] if race_info else 'Raça Desconhecida',
                    'hp': character['hp'],
                    'img_url': character.get('img_url', '/static/images/default.png')
                }
                characters.append(character_info)
                app.logger.info(f"Character info added to session sync: {character_info}")
        
        session_sync_data = {
            'session_id': session_id,
            'characters': characters
        }
        app.logger.info(f"Session sync data: {session_sync_data}")
        return session_sync_data
    return {}



def get_session_id_from_char(character_id):
    session = db.sessions.find_one({"characters": ObjectId(character_id)})
    if session:
        return str(session['_id'])
    return None

@socketio.on('play_music')
def handle_play_music(data):
    session_id = session.get('game_session_id')
    if session_id:
        emit('play_music', {'track_url': data['track_url']}, room=session_id)

@socketio.on('stop_music')
def handle_stop_music():
    session_id = session.get('game_session_id')
    if session_id:
        emit('stop_music', {}, room=session_id)


@socketio.on('player_removed')
def handle_player_removed(data):
    session_id = get_session_id_from_char(data['character_id'])
    if session_id:
        remove_character_from_session(db, session_id, data['character_id'])
        emit('session_sync', get_current_session_data(session_id), room=session_id)

@socketio.on('request_session_sync')
def handle_session_sync(data):
    session_id = data.get('session_id')
    if session_id:
        emit('session_sync', get_current_session_data(session_id), room=session_id)


@socketio.on('update_health')
def handle_update_health(data):
    character_id = data['character_id']
    new_health = data['new_health']
    
    db.chars.update_one(
        {"_id": ObjectId(character_id)},
        {"$set": {"current_hp": new_health}}
    )

    session_id = get_session_id_from_char(character_id)
    if session_id:
        emit('health_updated', {
            'character_id': character_id,
            'new_health': new_health
        }, room=session_id)


pdfmetrics.registerFont(TTFont('MedievalFont', 'static/fonts/Enchanted Land.otf'))


@app.route('/export_pdf/<character_id>')
def export_pdf(character_id):
    # Fetch character data from the database
    character = db.chars.find_one({"_id": ObjectId(character_id)})
    
    if character:
        # Fetch class and race details
        class_info = db['classes.classes'].find_one({"_id": ObjectId(character['class_id'])})
        race_info = db['races.races'].find_one({"_id": ObjectId(character['race_id'])})

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Set parchment-like background color
        p.setFillColorRGB(0.96, 0.87, 0.70)  # Light beige color
        p.rect(0, 0, width, height, stroke=0, fill=1)

        # Set font
        p.setFont("MedievalFont", 16)

        # Add title with medieval font
        p.setFont("MedievalFont", 24)
        p.setFillColor(colors.darkred)
        p.drawCentredString(width / 2.0, height - 50, f"Ficha de Personagem: {character['name']}")

        if character['img_url']:
            image_path = character['img_url']

            image_extension = os.path.splitext(image_path)[1].lower()

            try:
                if image_extension in ['.png', '.jpg', '.jpeg', '.webp']:
                    img_x = width - 220
                    img_y = height - 250
                    img_width = 150
                    img_height = 150
                    p.setStrokeColor(colors.black)
                    p.setLineWidth(2)
                    p.rect(img_x - 10, img_y - 10, img_width + 20, img_height + 20)
                    p.drawImage(ImageReader(image_path), img_x, img_y, width=img_width, height=img_height)
                else:
                    print("Unsupported image format. Only PNG and JPG are supported.")
            except Exception as e:
                print(f"Error loading the image: {e}")

        # Add character details with adjusted spacing
        p.setFont("MedievalFont", 16)
        text_x = 60
        text_y_start = height - 150
        line_height = 20

        # Titles and values in the same line but with different colors
        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start, "Classe:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start, f"{class_info['name'] if class_info else 'Classe Desconhecida'}")

        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - line_height, "Raca:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start - line_height, f"{race_info['name'] if race_info else 'Raca Desconhecida'}")

        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - 2 * line_height, "HP:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start - 2 * line_height, f"{character['hp']}")

        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - 3 * line_height, "Forca:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start - 3 * line_height, f"{character['forca']}")

        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - 4 * line_height, "Destreza:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start - 4 * line_height, f"{character['destreza']}")

        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - 5 * line_height, "Constituição:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start - 5 * line_height, f"{character['constituicao']}")

        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - 6 * line_height, "Inteligência:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start - 6 * line_height, f"{character['inteligencia']}")

        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - 7 * line_height, "Sabedoria:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start - 7 * line_height, f"{character['sabedoria']}")

        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - 8 * line_height, "Carisma:")
        p.setFillColor(colors.black)
        p.drawString(text_x + 100, text_y_start - 8 * line_height, f"{character['carisma']}")

        # Add skills and abilities with headers and adjusted spacing
        p.setFont("MedievalFont", 18)
        p.setFillColor(colors.darkred)
        p.drawString(text_x, text_y_start - 10 * line_height, "Habilidades de Classe:")

        y = text_y_start - 11 * line_height
        p.setFont("MedievalFont", 14)
        if class_info:
            for habilidade, descricao in class_info.get("habilidades_classe", {}).items():
                p.setFillColor(colors.black)
                p.drawString(text_x + 20, y, f"{habilidade}: {descricao}")
                y -= line_height

        p.setFont("MedievalFont", 18)
        p.setFillColor(colors.darkred)
        p.drawString(text_x, y - line_height, "Habilidades Raciais:")

        y -= 2 * line_height
        p.setFont("MedievalFont", 14)
        if race_info:
            for habilidade, descricao in race_info.get("habilidades_inatas", {}).items():
                p.setFillColor(colors.black)
                p.drawString(text_x + 20, y, f"{habilidade}: {descricao}")
                y -= line_height
        
        p.setFont("MedievalFont", 18)
        p.setFillColor(colors.darkred)
        p.drawString(text_x, y - line_height, "Perícias:")

        y -= 2 * line_height
        p.setFont("MedievalFont", 14)
        for pericia, valor in character.get("pericias", {}).items():
            p.setFillColor(colors.black)
            p.drawString(text_x + 20, y, f"{pericia}: +{valor}")
            y -= line_height

        # Add character history (História)
        if "origem" in character:
            p.setFont("MedievalFont", 18)
            p.setFillColor(colors.darkred)
            p.drawString(text_x, y - 2 * line_height, "História do Personagem:")

            y -= 3 * line_height
            p.setFont("MedievalFont", 14)
            history_text = character["origem"]
            text_lines = history_text.split('\n')  # Split history into lines
            for line in text_lines:
                p.setFillColor(colors.black)
                p.drawString(text_x + 20, y, line)
                y -= line_height

        # Finalize PDF
        p.showPage()
        p.save()

        buffer.seek(0)
        
        # Send the PDF as a downloadable file
        return send_file(buffer, as_attachment=True, download_name=f'{character["name"]}_Ficha.pdf', mimetype='application/pdf')
    else:
        return "Character not found", 404

    
if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=8000)
    # pass
