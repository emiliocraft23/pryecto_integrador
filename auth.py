import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

def get_fernet() -> Fernet:
    key = os.getenv("AES_SECRET_KEY")
    if not key:
        raise ValueError("AES_SECRET_KEY no está configurado en las variables de entorno.")
    return Fernet(key.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """
    Encripta la contraseña usando AES (Fernet).
    Mantenemos el nombre de la función por compatibilidad con el resto del código.
    """
    f = get_fernet()
    encrypted_password = f.encrypt(password.encode('utf-8'))
    return encrypted_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Desencripta la contraseña almacenada y la compara con la ingresada.
    Mantenemos el nombre de la función por compatibilidad con el resto del código.
    """
    f = get_fernet()
    try:
        decrypted_password = f.decrypt(hashed_password.encode('utf-8')).decode('utf-8')
        return plain_password == decrypted_password
    except Exception:
    
        return False
