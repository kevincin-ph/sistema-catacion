# ☕ Sistema de Catación de Café

Aplicación de escritorio para registrar, almacenar y analizar cataciones de café
en laboratorios o cooperativas cafeteras. Desarrollada en Python.

Nace de una necesidad real: digitalizar un proceso que normalmente se hace en
cuaderno, agregando cálculo automático de puntajes y análisis comparativo entre lotes.

## ✨ Funcionalidades

- Registro de cataciones con validación de datos (catador, café, origen, puntajes sensoriales)
- Cálculo automático del puntaje total
- Persistencia en Excel (sin necesidad de base de datos externa)
- Historial consultable desde la interfaz
- Gráficas comparativas entre cafés y perfil sensorial individual (radar chart)
- Interfaz gráfica de escritorio (tkinter, incluido con Python)
- Suite de tests automatizados (pytest)

## 🖼️ Capturas

> *(Agrega aquí capturas de tu interfaz una vez la ejecutes)*

## 🛠️ Tecnologías

- Python 3.9+
- tkinter — interfaz gráfica
- openpyxl — persistencia en Excel
- matplotlib — gráficas y reportes visuales
- pytest — testing automatizado

## 📦 Instalación

```bash
git clone https://github.com/kevincin-ph/sistema-catacion.git
cd sistema-catacion-cafe
pip3 install -r requirements.txt
```

## ▶️ Uso

```bash
python3 src/main.py
```

Esto abre la interfaz gráfica donde puedes:
1. Registrar una nueva catación con sus puntajes sensoriales
2. Ver el historial de cataciones guardadas
3. Generar gráficas comparativas de los cafés evaluados

Los datos se guardan automáticamente en `datos/cataciones.xlsx` y las gráficas
en la carpeta `reportes/`.

## 🧪 Tests

```bash
pip3 install pytest
pytest tests/ -v
```

## 📁 Estructura del proyecto

```
sistema_catacion/
├── src/
│   ├── modelo.py       # Lógica de negocio y persistencia
│   ├── graficas.py     # Generación de gráficas
│   ├── interfaz.py     # Interfaz gráfica (tkinter)
│   └── main.py         # Punto de entrada
├── tests/
│   └── test_modelo.py  # Tests automatizados
├── datos/               # Excel generado (no versionado)
├── reportes/             # Gráficas generadas (no versionado)
├── requirements.txt
└── README.md
```

## 🗺️ Roadmap

- [ ] Migrar de Excel a SQLite para mejor escalabilidad
- [ ] Versión web (Flask) para acceso multiusuario
- [ ] Exportar reportes en PDF
- [ ] Autenticación por catador

## 📄 Licencia

MIT — libre para usar, modificar y distribuir.
