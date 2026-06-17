import sys
import os

# Thêm cấu hình tránh lỗi hiển thị của Qt
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = "./platforms"

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from rsa_ui import Ui_MainWindow  # Đã sửa lại đường dẫn import đúng cấp thư mục
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Kết nối các nút bấm với hàm xử lý
        self.ui.btn_generate_key.clicked.connect(self.call_api_gen_keys)
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)
        self.ui.btn_sign.clicked.connect(self.call_api_sign)
        self.ui.btn_verify.clicked.connect(self.call_api_verify)

    def call_api_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(data.get("message", "Đã tạo key thành công!"))
                msg.exec_()
            else:
                print(f"Error while calling API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")  # Đã sửa lỗi bỏ .message

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/encrypt"
        payload = {
            "message": self.ui.txt_plain_text.toPlainText(),
            "key_type": "public"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_cipher_text.setPlainText(data.get("encrypted_message", ""))
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Encrypted Successfully")  # Sửa lỗi chính tả Successfully
                msg.exec_()
            else:
                print(f"Error while calling API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")  # Đã sửa lỗi bỏ .message

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/rsa/decrypt"
        payload = {
            "ciphertext": self.ui.txt_cipher_text.toPlainText(),
            "key_type": "private"
        }    
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_plain_text.setPlainText(data.get("decrypted_message", ""))

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Decrypted Successfully")
                msg.exec_()
            else:
                print(f"Error while calling API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")  # Đã sửa lỗi bỏ .message

    def call_api_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                self.ui.txt_sign.setPlainText(data.get("signature", ""))

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Signed Successfully")
                msg.exec_()
            else:
                print(f"Error while calling API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")  # Đã sửa lỗi bỏ .message

    def call_api_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.txt_info.toPlainText(),
            "signature": self.ui.txt_sign.toPlainText()
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                
                # Kiểm tra khóa 'is_verified' hoặc 'valid' tùy API trả về để tránh lỗi crash
                is_verified = data.get("is_verified") or data.get("valid") or False
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                if is_verified:
                    msg.setText("Verified Successfully")
                else:
                    msg.setText("Verified Failed")  # Đã sửa ngữ pháp từ Fail -> Failed
                msg.exec_()
            else:
                print(f"Error while calling API. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")  # Đã sửa lỗi bỏ .message

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())