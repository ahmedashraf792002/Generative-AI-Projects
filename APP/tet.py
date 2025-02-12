import os

# الحصول على المجلد الحالي
current_directory = os.path.dirname(os.path.abspath(__file__))

# الحصول على اسم الملف الحالي
file_name = os.path.basename(__file__)

print(f"📂 Current Directory: {current_directory}")
print(f"📄 File Name: {file_name}")
