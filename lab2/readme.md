Это зашифрует все файлы из original_files и сохранит их в encrypted_files.
python main.py encrypt original_files encrypted_files


Введите информацию о пользователе, и система сгенерирует лицензионный ключ.
python main.py generate_license


Замените <license_key> на ваш лицензионный ключ, а <filename> — на имя файла из encrypted_files, который вы хотите просмотреть.
python viewer.py <license_key> <filename>
