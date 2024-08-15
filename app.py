import os

from bson import ObjectId
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from werkzeug.utils import secure_filename

from conection_db import connection
from models.character_model import (create_character, delete_character,
                                    get_characters_by_user, update_character)
from models.class_model import create_default_classes, get_class_by_id
from models.race_model import create_default_races, get_race_by_id

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

        # Processa o upload da imagem
        if 'img_url' in request.files:
            file = request.files['img_url']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                img_url = file_path

                create_character(db, session['userId'], name, class_id, race_id, img_url, forca, destreza, constituicao, inteligencia, sabedoria, carisma, origem)
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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
