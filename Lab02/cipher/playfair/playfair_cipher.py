class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        """
        Tạo ma trận Playfair 5x5 từ khóa (Key).
        Tự động chuyển J thành I, viết hoa và loại bỏ ký tự trùng.
        """
        key = key.replace("J", "I").upper()
        
        matrix_letters = []
        seen = set()

        # 1. Đưa các ký tự duy nhất trong key vào mảng phẳng
        for letter in key:
            if letter not in seen and letter.isalpha():
                seen.add(letter)
                matrix_letters.append(letter)

        # 2. Bảng chữ cái chuẩn 25 ký tự (đã gộp J vào I)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        
        # 3. Điền các ký tự còn lại của bảng chữ cái vào mảng nếu chưa xuất hiện
        for letter in alphabet:
            if letter not in seen:
                seen.add(letter)
                matrix_letters.append(letter)

        # 4. Cắt mảng phẳng 25 ký tự thành ma trận 2 chiều 5x5
        playfair_matrix = [matrix_letters[i:i + 5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        """
        Tìm tọa độ (dòng, cột) của một ký tự trong ma trận 5x5.
        """
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def playfair_encrypt(self, plain_text, matrix):
        """
        Mã hóa văn bản gốc bằng ma trận Playfair.
        Có xử lý tách cặp trùng nhau (ví dụ: LL -> LX) giống cấu trúc bài của Giảng viên.
        """
        # Chuẩn hóa chuỗi đầu vào: viết hoa, chuyển J thành I, xóa khoảng trắng
        plain_text = plain_text.replace("J", "I").upper().replace(" ", "")
        
        # --- THUẬT TOÁN CHÈN KÝ TỰ ĐỆM BIẾN ĐỔI CHUỖI ---
        prepared_text = ""
        i = 0
        while i < len(plain_text):
            prepared_text += plain_text[i]
            
            # Nếu ký tự tiếp theo giống ký tự hiện tại trong cùng một cặp, chèn 'X' vào giữa
            if i + 1 < len(plain_text):
                if plain_text[i] == plain_text[i + 1]:
                    prepared_text += "X"
                    i += 1
                else:
                    prepared_text += plain_text[i + 1]
                    i += 2
            else:
                i += 1

        # Nếu độ dài chuỗi sau xử lý bị lẻ, chèn thêm 'X' vào cuối cùng để làm tròn cặp
        if len(prepared_text) % 2 != 0:
            prepared_text += "X"
        # ------------------------------------------------

        encrypted_text = ""
        # Tiến hành chia cặp 2 ký tự và áp dụng quy tắc hình học trên ma trận
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i + 2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                # Cùng hàng -> Dịch sang phải (vòng tròn % 5)
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                # Cùng cột -> Dịch xuống dưới (vòng tròn % 5)
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                # Khác hàng, khác cột -> Đổi góc hình chữ nhật (đổi cột cho nhau)
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        """
        Giải mã chuỗi mật mã và tự động lọc bỏ các ký tự đệm 'X' thừa,
        trả về chuỗi văn bản sạch ban đầu.
        """
        cipher_text = cipher_text.upper().replace(" ", "")
        decrypted_text = ""

        # 1. Giải mã hình học ngược trên ma trận 5x5
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i + 2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                # Cùng hàng -> Dịch sang trái
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                # Cùng cột -> Dịch lên trên
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                # Khác hàng, khác cột -> Đổi góc hình chữ nhật
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        # 2. --- THUẬT TOÁN KHỬ KÝ TỰ ĐỆM 'X' XẤU XÍ ---
        plain_text_clean = ""
        j = 0
        while j < len(decrypted_text):
            # Nếu phát hiện chữ X nằm kẹp giữa 2 ký tự giống nhau (Ví dụ: L X L), khôi phục lại thành L L
            if j + 2 < len(decrypted_text) and decrypted_text[j] == decrypted_text[j+2] and decrypted_text[j+1] == 'X':
                plain_text_clean += decrypted_text[j] + decrypted_text[j+2]
                j += 3  # Bỏ qua chữ X đệm
            else:
                plain_text_clean += decrypted_text[j]
                j += 1

        # Xóa chữ 'X' vô nghĩa ở cuối chuỗi nếu có (đệm làm tròn chuỗi lẻ lúc mã hóa)
        if plain_text_clean.endswith('X'):
            plain_text_clean = plain_text_clean[:-1]
        # ----------------------------------------

        return plain_text_clean