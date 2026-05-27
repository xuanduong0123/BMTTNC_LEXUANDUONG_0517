from flask import Flask, render_template, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.playfair import PlayFairCipher
from cipher.railfence import RailFenceCipher     
from cipher.transposition import TranspositionCipher 
from cipher.rsa import RSACipher 

app = Flask(__name__)
# 1. ROUTER TRANG CHỦ (HOME PAGE)
@app.route("/")
def home():
    return render_template('index.html')

# 2. ROUTER CHO CAESAR CIPHER
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    return render_template('caesar.html', plain_text=text, key=key, encrypted_text=encrypted_text)

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    return render_template('caesar.html', cipher_text=text, key=key, decrypted_text=decrypted_text)

# 3. ROUTER CHO PLAYFAIR CIPHER
@app.route("/playfair")
def playfair_page():
    return render_template('playfair.html')

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_web_encrypt():
    plain_text = request.form['inputPlainText']
    key = request.form['inputKeyPlain']
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    encrypted_text = cipher.playfair_encrypt(plain_text, matrix)
    return render_template('playfair.html', plain_text=plain_text, key=key, matrix=matrix, encrypted_text=encrypted_text)

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_web_decrypt():
    cipher_text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    decrypted_text = cipher.playfair_decrypt(cipher_text, matrix)
    return render_template('playfair.html', cipher_text=cipher_text, key=key, matrix=matrix, decrypted_text=decrypted_text)

# 4. ROUTER CHO RAIL FENCE CIPHER
@app.route("/railfence")
def railfence_page():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain']) 
    cipher = RailFenceCipher()
    encrypted_text = cipher.encrypt_text(text, key) 
    return render_template('railfence.html', plain_text=text, key=key, encrypted_text=encrypted_text)

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    cipher = RailFenceCipher()
    decrypted_text = cipher.decrypt_text(text, key) 
    return render_template('railfence.html', cipher_text=text, key=key, decrypted_text=decrypted_text)

# 5. ROUTER CHO TRANSPOSITION CIPHER
@app.route("/transposition")
def transposition_page():
    return render_template('transposition.html')

@app.route("/transposition/encrypt", methods=['POST'])
def transposition_encrypt():
    text = request.form['inputPlainText']
    key = request.form['inputKeyPlain'] 
    cipher = TranspositionCipher()
    encrypted_text = cipher.encrypt_text(text, key) 
    return render_template('transposition.html', plain_text=text, key=key, encrypted_text=encrypted_text)

@app.route("/transposition/decrypt", methods=['POST'])
def transposition_decrypt():
    text = request.form['inputCipherText']
    key = request.form['inputKeyCipher']
    cipher = TranspositionCipher()
    decrypted_text = cipher.decrypt_text(text, key) 
    return render_template('transposition.html', cipher_text=text, key=key, decrypted_text=decrypted_text)

# 6. ROUTER CHO RSA CIPHER (MỚI THÊM)
@app.route("/rsa")
def rsa_page():
    return render_template('rsa.html')

@app.route("/rsa/encrypt", methods=['POST'])
def rsa_web_encrypt():
    plain_text = request.form['inputPlainText']
    e = int(request.form['inputE'])
    n = int(request.form['inputN'])
    cipher = RSACipher()
    encrypted_text = cipher.encrypt(plain_text, e, n) 
    return render_template('rsa.html', plain_text=plain_text, e=e, n=n, encrypted_text=encrypted_text)

@app.route("/rsa/decrypt", methods=['POST'])
def rsa_web_decrypt():
    cipher_text = request.form['inputCipherText']
    d = int(request.form['inputD'])
    n = int(request.form['inputN'])
    cipher = RSACipher()
    decrypted_text = cipher.decrypt(cipher_text, d, n)
    return render_template('rsa.html', cipher_text=cipher_text, d=d, n=n, decrypted_text=decrypted_text)

# MAIN FUNCTION KHỞI CHẠY SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)