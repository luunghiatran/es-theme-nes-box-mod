import os
import shutil

# Copy theme.xml from 3do folder to all other folders in the same root
# Thư mục gốc
root = r"D:\r36h\themes\nes-box-nghia1"

# File theme gốc cần copy
source_file = os.path.join(root, "3do", "theme.xml")

if not os.path.exists(source_file):
    print("Không tìm thấy file nguồn:", source_file)
    exit()

# Duyệt tất cả thư mục con trong root
for folder in os.listdir(root):
    target_dir = os.path.join(root, folder)

    # bỏ qua thư mục 3do để không copy vào chính nó
    if folder.lower() == "3do":
        continue

    if os.path.isdir(target_dir):
        target_file = os.path.join(target_dir, "theme.xml")

        # Chỉ copy nếu thư mục đó đã có sẵn theme.xml
        if os.path.exists(target_file):
            try:
                shutil.copy2(source_file, target_file)
                print(f"Đã copy vào: {target_file}")
            except Exception as e:
                print(f"Lỗi khi copy vào {target_file}: {e}")

print("Hoàn thành!")
