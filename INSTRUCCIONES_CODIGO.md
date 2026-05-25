# API de Autenticación Segura (FastAPI + SQLModel)

Este proyecto es una implementación de gestión de identidades y autenticación que utiliza técnicas avanzadas de seguridad como **Hashing**, **Salting** y **Peppering**. Cumple con el requisito de mantener una base de datos "quemada" en código con un usuario de ejemplo al iniciar.

## Estructura de Archivos

El proyecto está dividido en varios módulos para mantener el código ordenado (Separación de Responsabilidades):

- **`models.py`**: Contiene la definición de la base de datos (modelo `User`) y los esquemas Pydantic.
- **`database.py`**: Archivo de configuración de SQLModel para la conexión a la base de datos local SQLite (`auth_api.db`).
- **`security.py`**: El corazón de la seguridad. Utiliza `bcrypt` para cargar el **Pepper** desde las variables de entorno, generar un **Salt** por usuario, encriptar y verificar contraseñas.
- **`main.py`**: Archivo principal de FastAPI. Contiene el endpoint de inicio de sesión (`POST /login`) y el evento `lifespan` que arranca la base de datos e **inyecta automáticamente al usuario de prueba (`admin` / `admin123`)**.
- **`.env`**: Archivo oculto que almacena el secreto global (`PEPPER_SECRET`).
- **`test_api.py`**: Script de pruebas automáticas para validar que el login funciona y bloquea accesos no autorizados.

---

## Instrucciones para Levantar el Proyecto

### 1. Entorno de Python
El proyecto recomienda Python 3.10, 3.11 o 3.12.
*(Nota: Evita usar Python 3.15 u otras versiones experimentales, ya que algunas librerías de seguridad aún no tienen binarios precompilados y darán error).*

Puedes instalar las dependencias directamente en tu entorno global de Python ejecutando:
```bash
pip install -r requirements.txt
```

*(Si prefieres usar un entorno virtual, asegúrate de crearlo con una versión estable: `python -m venv .venv` y activarlo antes de instalar).*

### 2. Iniciar el Servidor
Para correr la aplicación, usa Uvicorn. Ejecuta el siguiente comando en tu terminal (asegúrate de estar en la carpeta `Partial`):
```bash
python -m uvicorn main:app --reload --port 8080
```
*(Nota: Se utiliza el puerto 8080 para evitar el error común de puerto ocupado `[WinError 10013]`).*

Al iniciarse, verás en la consola un mensaje indicando: *"Usuario de ejemplo 'admin' (clave: 'admin123') creado exitosamente."*

### 3. Probar la API (Documentación Interactiva)
FastAPI genera automáticamente documentación que puedes usar para interactuar con tu API.
Abre tu navegador y entra a:
👉 **[http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)**

Desde allí, podrás:
1. Desplegar el bloque de **`POST /login`**.
2. Hacer clic en *"Try it out"* (Probarlo).
3. Ingresar el usuario `"admin"` y contraseña `"admin123"` en formato JSON y ejecutar (Execute).
4. Ver cómo la respuesta indica "Autenticación exitosa" (HTTP 200). 
5. Si pruebas con una contraseña incorrecta, verás el error de "Credenciales inválidas" (HTTP 401).

### 4. Pruebas Automáticas
Para verificar que todo el sistema de seguridad está funcionando correctamente, puedes ejecutar el script de pruebas en tu terminal:
```bash
python test_api.py
```
Esto simulará peticiones correctas e incorrectas e imprimirá *"All tests passed"* si todo está bien configurado.

### 5. Ver Base de Datos SQLite
Al arrancar el proyecto, se generará automáticamente el archivo `auth_api.db`.
Puedes abrir este archivo usando **DBeaver** o la extensión **SQLite Viewer** en VS Code. Podrás observar en la tabla `user` que el campo `hashed_password` contiene el hash indescifrable del usuario admin en lugar de la contraseña en texto claro.
