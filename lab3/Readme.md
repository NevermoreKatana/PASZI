## Шифрование файла без указания пароля (генерация пароля):

```bash
python main.py --encrypt --input test.txt --output secret.enc
```

## Шифрование файла с указанем пароля :

```bash
python main.py --encrypt --input test.txt --output secret.enc --password MyP@ssw0rd!
```

## Дешифрование файла с указанным паролем

```bash
python main.py --decrypt --input secret.enc --output secret_decrypted.txt --password "MyP@ssw0rd!"
```

## Вывод Help:
```bash
python main.py -h
```