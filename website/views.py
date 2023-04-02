from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import User, Note
from . import db
from .cipher import VigenereCipher

import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/about')
def about_me():
    return redirect("https://github.com/IronForce-Auscent")

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/account')
@login_required
def account():
    return render_template('account.html')

@views.route('/cipher')
def cipher():
    return render_template('cipher.html')

@views.route('/cipher/<string:cipher_mode>', methods=['POST'])
def switch_cipher(cipher_mode):
    vigenere_cipher = VigenereCipher()
    if cipher_mode == "encrypt":
        plaintext = request.form.get('plaintext')
        encryption_key = request.form.get('encryption-key') or vigenere_cipher.generate_key(plaintext)
        print(plaintext)
        print(encryption_key)
        ciphertext = vigenere_cipher.encrypt(encryption_key, plaintext)
        return render_template('cipher.html', plaintext=plaintext, encryptioncl_key=encryption_key, ciphertext=ciphertext)
    elif cipher_mode == "decrypt":
        ciphertext = request.form.get('ciphertext')
        decryption_key = request.form.get('decryption-key')
        if decryption_key == None or decryption_key == "":
            flash('A decryption key must be entered', category='error')
            return render_template('cipher.html', plaintext="", decryption_key="", ciphertext="")
        plaintext = vigenere_cipher.decrypt(decryption_key, ciphertext)
        return render_template('cipher.html', plaintext=plaintext, decryption_key=decryption_key, ciphertext=ciphertext)
    else:
        return render_template('cipher.html')