
# Tạo danh sách trống để lưu kết quả
j= []

# Duyệt trong khoảng từ 2000 đến 3200 (lấy cả 3200 nên dùng 3201)
for i in range(2000, 3201):
# Chia hết cho 7 (i % 7 == 0) và không chia hết cho 5 (i % 5 != 0)
    if (i % 7 == 0) and (i % 5 != 0):
        j.append(str(i))

# In kết quả nối với nhau bằng dấu phẩy
print(','.join(j))
