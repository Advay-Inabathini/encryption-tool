from flask import Flask, render_template, request, send_file, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.fernet import Fernet
import os

app = Flask(__name__)

# Change these to your secret key and salt
SECRET_KEY = b'my_secret_key'
SALT = b'my_salt'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from os import urandom
from cryptography.hazmat.primitives import serialization

# ... (other imports and code)

def encrypt_file_aes(file_content, key):
    iv = urandom(16)  # Generate a random 128-bit (16-byte) initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_file = encryptor.update(file_content) + encryptor.finalize()
    return iv + encrypted_file

def decrypt_file_aes(file_content, key):
    iv = file_content[:16]  # Extract the initialization vector from the first 16 bytes
    encrypted_data = file_content[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_file = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_file

# ... (rest of your code)


# ... (rest of your code)

def generate_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=SALT,
        iterations=100000,
        length=32,  # AES key size
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        password = request.form["password"]
        selected_algorithm = request.form["algorithm"]
        operation = request.form["operation"]

        if selected_algorithm == "AES":
            key = generate_key(password)
        elif selected_algorithm == "RSA":
            # Implement RSA key generation and encryption/decryption here
            pass
        else:
            return jsonify({"error": "Invalid algorithm selected"})

        if operation == "encrypt":
            if selected_algorithm == "AES":
                processed_content = encrypt_file_aes(file.read(), key)
                filename_prefix = "encrypted"
            elif selected_algorithm == "RSA":
                # Implement RSA encryption here
                # You may need to use a different filename_prefix for RSA
                filename_prefix = "rsa_encrypted"
            else:
                return jsonify({"error": "Invalid algorithm selected"})
        elif operation == "decrypt":
            if selected_algorithm == "AES":
                processed_content = decrypt_file_aes(file.read(), key)
                filename_prefix = "decrypted"
            elif selected_algorithm == "RSA":
                # Implement RSA decryption here
                # You may need to use a different filename_prefix for RSA
                filename_prefix = "rsa_decrypted"
            else:
                return jsonify({"error": "Invalid algorithm selected"})
        else:
            return jsonify({"error": "Invalid operation selected"})

        filename = f"{filename_prefix}_file.txt"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        with open(filepath, "wb") as processed_file:
            processed_file.write(processed_content)

        return send_file(filepath, as_attachment=True, download_name=filename)

    return render_template("index.html")

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
