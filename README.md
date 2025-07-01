# Tienda en Línea - Proyecto Django

Este es un proyecto de tienda en línea desarrollado con Django, diseñado para ofrecer una experiencia de compra fluida y atractiva para los usuarios.

## Características

- Catálogo de productos con categorías
- Carrito de compras interactivo
- Sistema de autenticación de usuarios
- Panel de administración personalizado
- Diseño responsivo con Tailwind CSS
- Integración con base de datos PostgreSQL

## Requisitos del Sistema

- Python 3.10.8 o superior
- PostgreSQL
- pip (gestor de paquetes de Python)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd myproject
   ```

2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows
   source venv/bin/activate  # En Linux/Mac
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configura las variables de entorno:
   Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
   ```
   DEBUG=True
   SECRET_KEY=tu_clave_secreta_aqui
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=postgresql://usuario:contraseña@localhost/nombre_bd
   ```

5. Aplica las migraciones:
   ```bash
   python manage.py migrate
   ```

6. Crea un superusuario (opcional):
   ```bash
   python manage.py createsuperuser
   ```

7. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

## Despliegue en Railway

1. Crea una cuenta en [Railway](https://railway.app/)
2. Conecta tu repositorio de GitHub
3. Configura las variables de entorno en el panel de Railway
4. Railway detectará automáticamente el proyecto Django y lo desplegará

## Estructura del Proyecto

```
myproject/
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
├── .gitignore
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tienda/
    ├── migrations/
    ├── static/
    ├── templates/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    └── views.py
```

## Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| DEBUG | Modo depuración | False |
| SECRET_KEY | Clave secreta de Django | (ninguno) |
| ALLOWED_HOSTS | Hosts permitidos | localhost,127.0.0.1 |
| DATABASE_URL | URL de conexión a la base de datos | (ninguno) |

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
