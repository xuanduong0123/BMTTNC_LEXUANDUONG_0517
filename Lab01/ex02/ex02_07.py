print("Nhập các dòng văn bản (Nhập 'done' để kết thúc):")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line.upper())

print("\nCác dòng đã chuyển thành chữ in hoa:")
for line in lines:
    print(line)