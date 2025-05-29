# EthicalKeylogger

## Descripción
`EthicalKeylogger` es una utilidad en Python para fines **educativos** y de **pruebas de ciberseguridad**.  
Registra de forma responsable:

- Pulsaciones de teclado (filtrando auto-repeats y descartando teclas de control).  
- Todo lo copiado al portapapeles (Ctrl+C y menú contextual) **solo** tras iniciar el script.  
- Marca de tiempo en cada entrada.  
- Límite de tamaño de log configurable con parada automática.  
- Mensaje de advertencia legal al arranque.

> **Importante:** Utilízalo únicamente en sistemas y cuentas donde tengas permiso explícito. El autor no se responsabiliza por usos indebidos.

---

## Características principales

- Registro limpio de caracteres imprimibles.  
- Filtrado de auto-repeats para evitar duplicados.  
- Captura de portapapeles desde el inicio.  
- Control de tamaño de log (1 MB por defecto).  
- Estructura modular, fácil de extender (cifrado, rotación, etc.).

---

## Requisitos

- **Python 3.8+**  
- **Dependencias de terceros**:
  ```bash
  pip install keyboard pyperclip
  ```
- **Librerías de la estándar**:
  ```python
  import threading
  import time
  import os
  import sys
  from datetime import datetime
  ```

---

## Instalación

1. **Clona** tu repositorio:
   ```bash
   git clone https://github.com/BrayanZambranoDev/ethical-keylogger.git
   cd ethical-keylogger
   ```
2. (Opcional) **Entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate      # Windows
   ```
3. **Instala** dependencias:
   ```bash
   pip install -r requirements.txt
   ```

---

## Uso

El script principal se llama **`keylogger.py`**. Para ejecutarlo:

```bash
python keylogger.py
```

- Verás la **advertencia legal** en consola.  
- Se creará/actualizará `keystrokes_log.txt` en el mismo directorio.  
- Cada copia al portapapeles tras el inicio se guardará con la etiqueta `CLIPBOARD:`.  
- Para detener la captura, presiona **Ctrl+C**; verás un resumen de la duración.

---

## Configuración

Para cambiar los parámetros, edita las variables al inicio de `keylogger.py`:

```python
LOG_FILE     = "keystrokes_log.txt"
MAX_LOG_SIZE = 1_048_576  # bytes (1 MB)
```

---

## Personalización

- **Filtrado de teclas**: ajusta el set `SKIP_KEYS` en la clase `EthicalKeylogger`.  
- **Intervalo de monitor**: modifica el `time.sleep(1)` dentro de `_monitor_clipboard()`.  
- **Rotación de logs**: reemplaza la escritura manual por `logging.handlers.RotatingFileHandler`.  
- **Cifrado**: integra `cryptography.Fernet` en `_write_log()`.

---

## Contribuciones

¡Bienvenidas!  
1. Abre un **issue** para reportar bugs o sugerir mejoras.  
2. Crea un **fork** y trabaja en una rama descriptiva.  
3. Envía un **pull request** con tus cambios y actualiza este README si es necesario.

---

## Licencia

Este proyecto está licenciado bajo la **MIT License**.  
Consulta el fichero [LICENSE](LICENSE) para más detalles.
