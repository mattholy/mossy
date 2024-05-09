# -*- encoding: utf-8 -*-
'''
encryption.py
----
make your data safe


@Time    :   2024/05/09 10:19:38
@Author  :   Mattholy
@Version :   1.0
@Contact :   smile.used@hotmail.com
@License :   MIT License
'''

from utils.logger import logger, log_error_to_db
from sqlalchemy.types import TypeDecorator, String
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode, urlsafe_b64decode
import os

ENC_PREFIX = "ENC:"


class EncryptedType(TypeDecorator):
    impl = String

    def __init__(self, key=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key = key or self.get_encryption_key()

    @staticmethod
    def get_encryption_key():
        return os.getenv('ENCRYPTION_KEY')

    def encrypt_value(self, plaintext):
        if not self.key:
            return plaintext
        iv = os.urandom(12)
        cipher = Cipher(algorithms.AES(self.key),
                        modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ct = encryptor.update(plaintext.encode()) + encryptor.finalize()
        encrypted = urlsafe_b64encode(iv + encryptor.tag + ct).decode('utf-8')
        return f"{ENC_PREFIX}{encrypted}"

    def decrypt_value(self, ciphertext):
        if not ciphertext.startswith(ENC_PREFIX):
            return ciphertext
        ciphertext = ciphertext[len(ENC_PREFIX):]
        if not self.key:
            return 'ERROR: DECRYPTION KEY NOT FOUND'
        try:
            decoded_data = urlsafe_b64decode(ciphertext)
            iv = decoded_data[:12]
            tag = decoded_data[12:28]
            ct = decoded_data[28:]
            cipher = Cipher(algorithms.AES(self.key), modes.GCM(
                iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            return decryptor.update(ct) + decryptor.finalize()
        except Exception as e:
            return 'ERROR: DECRYPTION FAILED'

    def process_bind_param(self, value, dialect):
        if value is not None:
            return self.encrypt_value(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return self.decrypt_value(value).decode('utf-8')
        return value
