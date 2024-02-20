from flask import Flask, render_template, request, jsonify
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

import base64
import os

app = Flask(__name__)

# Change these to your secret key and salt
SECRET_KEY = b'my_secret_key'
SALT = b'my_salt'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

private_key = None  # Initialize private key variable
private_key_str = None  # Initialize private key string variable

def encrypt_text_aes(text, key):
    iv = os.urandom(16)  # Generate a random 128-bit (16-byte) initialization vector
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_text = encryptor.update(text.encode()) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_text).decode()

def decrypt_text_aes(encrypted_text, key):
    encrypted_data = base64.b64decode(encrypted_text.encode())
    iv = encrypted_data[:16]  # Extract the initialization vector from the first 16 bytes
    encrypted_data = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(encrypted_data) + decryptor.finalize()
    return decrypted_text.decode()

def aes_generate_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        salt=SALT,
        iterations=100000,
        length=32,  # AES key size
        backend=default_backend()
    )
    key = kdf.derive(password.encode())
    return key

def generate_rsa_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_private_key(private_key):
    # Serialize the private key to a string representation
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()

def encrypt_text_rsa(text, public_key):
    global private_key_str  # Declare private_key_str as global
    ciphertext = public_key.encrypt(
        text.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    private_key_str = serialize_private_key(private_key)
    return base64.b64encode(ciphertext).decode(), private_key_str

def decrypt_text_rsa(encrypted_text, private_key_str):
    try:
        ciphertext = base64.b64decode(encrypted_text.encode())
        private_key = serialization.load_pem_private_key(private_key_str.encode(), password=None, backend=default_backend())
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext.decode()
    except Exception as e:
        print(f"Decryption failed: {str(e)}")
        return f"Decryption failed: {str(e)}"


@app.route("/", methods=["GET", "POST"])
def index():
    global private_key, private_key_str  # Use the global private_key and private_key_str variables
    if request.method == "POST":
        text = request.form["text"]
        password = request.form["password"]
        selected_algorithm = request.form["algorithm"]
        operation = request.form["operation"]

        if selected_algorithm == "AES":
            key = aes_generate_key(password)
        elif selected_algorithm == "RSA":
            private_key, public_key = generate_rsa_key()
        else:
            return jsonify({"error": "Invalid algorithm selected"})

        if operation == "encrypt":
            if selected_algorithm == "AES":
                processed_content = encrypt_text_aes(text, key)
            elif selected_algorithm == "RSA":
                cipher_text, private_key_str = encrypt_text_rsa(text, public_key)
                return jsonify({"cipher_text": cipher_text, "private_key": private_key_str})
            else:
                return jsonify({"error": "Invalid algorithm selected"})
        elif operation == "decrypt":
            if selected_algorithm == "AES":
                processed_content = decrypt_text_aes(text, key)
            elif selected_algorithm == "RSA":
                processed_content = decrypt_text_rsa(text, private_key_str)
            else:
                return jsonify({"error": "Invalid algorithm selected"})
        else:
            return jsonify({"error": "Invalid operation selected"})

        return jsonify({"result": processed_content})

    return render_template("index.html")

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
    