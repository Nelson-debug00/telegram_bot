# Guía de Sintaxis: Flask y Jinja2

Esta guía resume la sintaxis más utilizada en el desarrollo web con Python usando Flask para el backend y Jinja2 para las plantillas.

---

## 1. Flask (Sintaxis de Python)

Flask es el framework que maneja las rutas y la lógica del servidor.

### Decoradores de Rutas

Se usan para definir a qué URL responde cada función.

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return "Hola Mundo"

# Ruta con parámetros dinámicos
@app.route('/usuario/<nombre>')
def perfil(nombre):
    return f"Perfil de: {nombre}"
```

### Métodos HTTP

Por defecto, las rutas solo aceptan `GET`. Para formularios, se debe especificar `POST`.

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        return redirect(url_for('dashboard'))
    return render_template('login.html')
```

### Funciones Comunes

- `render_template('archivo.html', variable=valor)`: Envía datos a la plantilla.
- `redirect(url_for('nombre_funcion'))`: Redirecciona a otra ruta.
- `request.form.get('input_name')`: Obtiene datos de un formulario de forma segura.
- `request.args.get('param')`: Obtiene parámetros de la URL (`?param=valor`).

---

## 2. Jinja2 (Sintaxis de Plantillas HTML)

Jinja permite escribir lógica de programación dentro de archivos HTML.

### Delimitadores

- `{{ ... }}`: **Expresiones**. Se usa para imprimir variables o resultados de funciones en el HTML.
- `{% ... %}`: **Sentencias**. Se usa para lógica como bucles `for`, condicionales `if` y herencia.
- `{# ... #}`: **Comentarios**. No se verán en el código fuente del navegador.

### Estructuras de Control

#### Condicionales (if)

```html
{% if usuario %}
<h1>Bienvenido, {{ usuario }}</h1>
{% else %}
<h1>Por favor, inicia sesión</h1>
{% endif %}
```

#### Bucles (for)

```html
<ul>
  {% for item in lista %}
  <li>{{ item }}</li>
  {% endfor %}
</ul>
```

### Herencia de Plantillas

Permite reutilizar una estructura base (como el navbar) en todas las páginas.

**base.html**

```html
<html>
  <body>
    <nav>Mi App</nav>
    {% block content %}{% endblock %}
  </body>
</html>
```

**index.html**

```html
{% extends "base.html" %} {% block content %}
<h1>Inicio</h1>
<p>Contenido de la página de inicio.</p>
{% endblock %}
```

### Filtros Comunes

Se usan con el símbolo pipe `|`.

- `{{ nombre | upper }}`: Convierte a mayúsculas.
- `{{ texto | length }}`: Devuelve la longitud.
- `{{ variable | default('Valor por defecto') }}`: Si la variable no existe.

---

_Guía creada para referencia rápida en proyectos de Flask._