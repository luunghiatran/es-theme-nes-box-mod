import os
import shutil

# Copy file from child folder to child folder
source_root = r"D:\r36h\themes\RVGM-BT-Theme-master"
target_root = r"D:\r36h\themes\nes-box-nghia1"
filename = "photo.png"

for folder in os.listdir(source_root):
    source_sub = os.path.join(source_root, folder)
    target_sub = os.path.join(target_root, folder)

    # chỉ xử lý nếu là thư mục
    if os.path.isdir(source_sub):
        source_file = os.path.join(source_sub, filename)

        # kiểm tra photo.png có tồn tại ở source và thư mục target có tồn tại hay không
        if os.path.exists(source_file) and os.path.isdir(target_sub):
            try:
                shutil.copy2(source_file, target_sub)
                print(f"Đã copy {source_file} → {target_sub}")
            except Exception as e:
                print(f"Lỗi copy {source_file}: {e}")

print("Hoàn thành!")
