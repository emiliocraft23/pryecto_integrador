import os
import base64
from dotenv import load_dotenv
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

load_dotenv()

def get_aes_key() -> bytes:
    """
    Obtiene la clave AES de las variables de entorno y la decodifica de base64.
    Valida que la clave resultante tenga una longitud apta para AES (16, 24 o 32 bytes).
    """
    key_b64 = os.getenv("AES_SECRET_KEY")
    if not key_b64:
        raise ValueError("AES_SECRET_KEY no está configurado en las variables de entorno.")
    try:
        key_bytes = base64.b64decode(key_b64)
        if len(key_bytes) not in [16, 24, 32]:
            raise ValueError(f"La clave AES debe ser de 16, 24 o 32 bytes (recibido {len(key_bytes)} bytes).")
        return key_bytes
    except Exception as e:
        raise ValueError(f"Error al decodificar la clave AES: {str(e)}")

def get_password_hash(password: str) -> str:
    """
    Encripta la contraseña usando AES-CBC.
    Genera un vector de inicialización (IV) aleatorio de 16 bytes.
    Retorna IV + ciphertext codificados en base64.
    """
    key = get_aes_key()
    # AES utiliza bloques de 16 bytes (128 bits), por lo que el IV debe ser de 16 bytes.
    iv = os.urandom(16)
    
    # Aplicar padding PKCS7 para ajustar el tamaño del bloque a 16 bytes
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(password.encode('utf-8')) + padder.finalize()
    
    # Configurar el cifrador AES-CBC
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Concatenar IV + ciphertext y codificar a Base64 para almacenar como string
    combined = iv + ciphertext
    return base64.b64encode(combined).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Desencripta la contraseña almacenada en AES-CBC y la compara con la ingresada.
    """
    try:
        key = get_aes_key()
        combined = base64.b64decode(hashed_password.encode('utf-8'))
        
        # El IV son los primeros 16 bytes
        if len(combined) < 16:
            return False
        
        iv = combined[:16]
        ciphertext = combined[16:]
        
        # Configurar el descifrador AES-CBC
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Quitar el padding PKCS7
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_password = unpadder.update(padded_data) + unpadder.finalize()
        
        return plain_password == decrypted_password.decode('utf-8')
    except Exception:
        return False

