# Перед использованием

создать папки - `original_files`, `encrypted_files`, `decrypted_files`


## Шифрование всех файлов из original_files в encrypted_files
```bash
python main.py encrypt original_files encrypted_files
```

## Генерация лицензионного ключа
```bash
python main.py generate_license
```

## Просмотр файлв
```bash
python viewer.py <license_key> <filename>
```
