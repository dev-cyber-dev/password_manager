from cryptography.fernet import Fernet

# сгенерировать ключ
key = Fernet.generate_key()

# вывод ключа
print(key)
