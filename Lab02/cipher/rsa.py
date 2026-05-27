class RSACipher:
    def __init__(self):
        pass

    def encrypt(self, plain_text, e, n):
        """Mã hóa bản rõ thành chuỗi các số cách nhau bởi dấu cách"""
        try:
            # Nếu người dùng nhập số nguyên
            if plain_text.isdigit():
                m = int(plain_text)
                c = pow(m, e, n)
                return str(c)
            # Nếu người dùng nhập chuỗi văn bản
            else:
                cipher_ints = [str(pow(ord(char), e, n)) for char in plain_text]
                return " ".join(cipher_ints)
        except Exception as ex:
            return f"Lỗi mã hóa: {str(ex)}"

    def decrypt(self, cipher_text, d, n):
        """Giải mã chuỗi số thành bản rõ tương ứng"""
        try:
            cipher_text = cipher_text.strip()
            # Nếu bản mã là một số nguyên duy nhất
            if " " not in cipher_text and cipher_text.isdigit():
                c = int(cipher_text)
                m = pow(c, d, n)
                return str(m)
            # Nếu bản mã là chuỗi các số cách nhau bởi dấu cách
            else:
                cipher_ints = [int(x) for x in cipher_text.split() if x.isdigit()]
                plain_chars = [chr(pow(c, d, n)) for c in cipher_ints]
                return "".join(plain_chars)
        except Exception as ex:
            return f"Lỗi giải mã: {str(ex)}"