# main.py

import sys
from cli import parse_arguments, get_password
from crypto_utils import encrypt_file, decrypt_file


def main():
    args = parse_arguments()

    password = get_password(args.password)

    try:
        if args.encrypt:
            encrypt_file(args.input, args.output, password)
            print(f"Файл успешно зашифрован и сохранен как {args.output}")
        elif args.decrypt:
            decrypt_file(args.input, args.output, password)
            print(f"Файл успешно дешифрован и сохранен как {args.output}")
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
