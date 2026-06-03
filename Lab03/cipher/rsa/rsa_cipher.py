import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic  # Dùng uic để nạp trực tiếp file .ui không qua file .py trung gian

# =============================================================
# BƯỚC 1: CÔ LẬP HỆ THỐNG TRÁNH TRÙNG MODULE RSA CỦA BẠN
if sys.path[0] == '' or 'Lab03' in sys.path[0]:
    sys.path.pop(0)

import rsa  # Thư viện rsa chuẩn hệ thống

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, 'keys')
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, 'publicKey.pem')
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, 'privateKey.pem')

# Đường dẫn tuyệt đối động trỏ thẳng tới file rsa.ui gốc
UI_PATH = os.path.join(BASE_DIR, '..', '..', 'ui', 'rsa.ui')

if not os.path.exists(KEYS_DIR):
    os.makedirs(KEYS_DIR)


# =============================================================
# BƯỚC 2: KHỐI THUẬT TOÁN RSA NGẦM
class RSACipher:
    def __init__(self):
        pass

    def generate_keys(self):
        (public_key, private_key) = rsa.newkeys(1024)
        with open(PUBLIC_KEY_PATH, 'wb') as p:
            p.write(public_key.save_pkcs1('PEM'))
        with open(PRIVATE_KEY_PATH, 'wb') as p:
            p.write(private_key.save_pkcs1('PEM'))

    def load_keys(self):
        with open(PUBLIC_KEY_PATH, 'rb') as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())
        with open(PRIVATE_KEY_PATH, 'rb') as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())
        return private_key, public_key

    def encrypt(self, message, key):
        return rsa.encrypt(message.encode('ascii'), key)

    def decrypt(self, ciphertext, key):
        try:
            return rsa.decrypt(ciphertext, key).decode('ascii')
        except:
            return False

    def sign(self, message, key):
        return rsa.sign(message.encode('ascii'), key, 'SHA-1')

    def verify(self, message, signature, key):
        try:
            return rsa.verify(message.encode('ascii'), signature, key) == 'SHA-1'
        except:
            return False


# =============================================================
# BƯỚC 3: KHỐI LIÊN KẾT ĐIỀU KHIỂN GIAO DIỆN (UI)
class RSA_App(QMainWindow):
    def __init__(self):
        super().__init__()
        # Nạp trực tiếp file cấu trúc thiết kế rsa.ui vào thẳng class ứng dụng
        uic.loadUi(UI_PATH, self)
        
        # URL kết nối API Flask của bạn
        self.api_url = "http://127.0.0.1:5000/api/rsa"
        
        # KẾT NỐI SỰ KIỆN: Do dùng loadUi nên gọi trực tiếp qua self (không cần qua self.ui)
        self.btn_generate_key.clicked.connect(self.generate_keys)
        self.btn_encrypt.clicked.connect(self.encrypt_text)
        self.btn_decrypt.clicked.connect(self.decrypt_text)
        self.btn_sign.clicked.connect(self.sign_text)
        self.btn_verify.clicked.connect(self.verify_signature)

    def generate_keys(self):
        try:
            response = requests.post(f"{self.api_url}/generate_keys")
            if response.status_code == 200:
                self.txt_info.setPlainText("Tạo cặp khóa mới thành công!")
            else:
                self.txt_info.setPlainText(f"Lỗi Server: {response.status_code}")
        except Exception as e:
            self.txt_info.setPlainText(f"Lỗi kết nối API: {str(e)}")

    def encrypt_text(self):
        try:
            msg = self.txt_plain_text.toPlainText()
            payload = {"message": msg, "key_type": "public"}
            response = requests.post(f"{self.api_url}/encrypt", json=payload)
            if response.status_code == 200:
                result = response.json()
                self.txt_cipher_text.setPlainText(result.get("encrypted_message", ""))
        except Exception as e:
            self.txt_info.setPlainText(str(e))

    def decrypt_text(self):
        try:
            ciphertext = self.txt_cipher_text.toPlainText()
            payload = {"ciphertext": ciphertext, "key_type": "private"}
            response = requests.post(f"{self.api_url}/decrypt", json=payload)
            if response.status_code == 200:
                result = response.json()
                self.txt_plain_text.setPlainText(result.get("decrypted_message", ""))
        except Exception as e:
            self.txt_info.setPlainText(str(e))

    def sign_text(self):
        try:
            msg = self.txt_plain_text.toPlainText()
            payload = {"message": msg}
            response = requests.post(f"{self.api_url}/sign", json=payload)
            if response.status_code == 200:
                result = response.json()
                self.txt_sign.setPlainText(result.get("signature", ""))
        except Exception as e:
            self.txt_info.setPlainText(str(e))

    def verify_signature(self):
        try:
            msg = self.txt_plain_text.toPlainText()
            signature = self.txt_sign.toPlainText()
            payload = {"message": msg, "signature": signature}
            response = requests.post(f"{self.api_url}/verify", json=payload)
            if response.status_code == 200:
                result = response.json()
                status = "Kết quả kiểm tra: Chữ ký HỢP LỆ! ✔" if result.get("is_verified") else "Kết quả kiểm tra: Chữ ký KHÔNG hợp lệ! ❌"
                self.txt_info.setPlainText(status)
        except Exception as e:
            self.txt_info.setPlainText(str(e))


# =============================================================
# BƯỚC 4: KHỞI CHẠY GIAO DIỆN
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSA_App()
    window.show()
    sys.exit(app.exec_())