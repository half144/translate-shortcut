import time
import threading
import pyperclip
from pynput import keyboard
from pynput.keyboard import Key
from translator import Translator
from config import Config
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime

class TextTranslatorApp:
    def __init__(self):
        self.config = Config()
        self.translator = Translator(self.config)
        self.is_processing = False
        self.translation_history = []
        self.key_buffer = []

        self.root = tk.Tk()
        self.root.title("Text Translator & Fixer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.setup_ui()
        self.keyboard_listener = None

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        title_label = ttk.Label(main_frame, text="Text Translator & Fixer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        language_frame = ttk.Frame(main_frame)
        language_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        language_frame.columnconfigure(1, weight=1)

        ttk.Label(language_frame, text="Idioma de destino:").grid(row=0, column=0, sticky=tk.W)
        
        self.language_var = tk.StringVar()
        languages = list(self.config.get_available_languages().keys())
        current_lang = self.config.get_target_language()
        current_lang_display = next((k for k, v in self.config.get_available_languages().items() if v == current_lang), languages[0])
        self.language_var.set(current_lang_display)
        
        self.language_combo = ttk.Combobox(language_frame, textvariable=self.language_var, values=languages, state="readonly", width=15)
        self.language_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        self.language_combo.bind('<<ComboboxSelected>>', self.on_language_change)

        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)

        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(status_frame, text="Carregando...", foreground="orange")
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))

        ttk.Label(status_frame, text="Comandos:").grid(row=1, column=0, sticky=tk.W)
        commands_label = ttk.Label(status_frame, text=":tl (traduzir) | :ft (corrigir texto)", font=("Arial", 10, "bold"))
        commands_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))

        history_label = ttk.Label(main_frame, text="Histórico", font=("Arial", 12, "bold"))
        history_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))

        self.history_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20, width=70)
        self.history_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Button(button_frame, text="Limpar Histórico", command=self.clear_history).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="Configurar API Key", command=self.setup_api_key).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(button_frame, text="Limpar Configuração", command=self.clear_config).pack(side=tk.LEFT, padx=(10, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def add_to_history(self, action_type, original_text, processed_text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        action_label = "Tradução" if action_type == "translate" else "Correção"
        
        self.translation_history.append({
            'timestamp': timestamp,
            'action': action_label,
            'original': original_text,
            'processed': processed_text
        })
        self.update_history_display()

    def update_history_display(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        if not self.translation_history:
            self.history_text.insert(tk.END, "Nenhuma ação realizada ainda.\n\n:tl - Traduzir texto\n:ft - Corrigir texto em inglês")
        else:
            for entry in reversed(self.translation_history[-20:]):
                self.history_text.insert(tk.END, f"[{entry['timestamp']}] {entry['action']}\n", "timestamp")
                self.history_text.insert(tk.END, f"Original: {entry['original']}\n", "original")
                self.history_text.insert(tk.END, f"Resultado: {entry['processed']}\n", "processed")
                self.history_text.insert(tk.END, "-" * 60 + "\n\n")
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)
        
        self.history_text.tag_config('timestamp', font=('Arial', 8, 'italic'), foreground='gray')
        self.history_text.tag_config('original', font=('Arial', 9))
        self.history_text.tag_config('processed', font=('Arial', 9, 'bold'))

    def clear_history(self):
        self.translation_history.clear()
        self.update_history_display()

    def on_language_change(self, event=None):
        selected_display = self.language_var.get()
        languages = self.config.get_available_languages()
        print(f"Language changed to: {selected_display}")
        if selected_display in languages:
            language_code = languages[selected_display]
            print(f"Setting language code: {language_code}")
            self.config.set_target_language(language_code)
            print(f"Current config language: {self.config.get_target_language()}")

    def setup_api_key(self):
        self.config.setup_api_key()
        self.check_configuration()

    def clear_config(self):
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar a configuração da API key?"):
            if self.config.clear_config():
                self.check_configuration()
                languages = list(self.config.get_available_languages().keys())
                current_lang = self.config.get_target_language()
                current_lang_display = next((k for k, v in self.config.get_available_languages().items() if v == current_lang), languages[0])
                self.language_var.set(current_lang_display)
                messagebox.showinfo("Sucesso", "Configuração limpa com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao limpar configuração.")

    def check_configuration(self):
        if self.config.is_configured():
            self.status_label.config(text="Ativo - Aguardando comandos", foreground="green")
            return True
        else:
            self.status_label.config(text="API Key não configurada", foreground="red")
            return False

    def on_press(self, key):
        if self.is_processing:
            return

        if hasattr(key, 'char') and key.char:
            self.key_buffer.append(key.char)
            if len(self.key_buffer) > 3:
                self.key_buffer.pop(0)
            
            buffer_text = ''.join(self.key_buffer)
            
            if buffer_text == ':tl':
                self.key_buffer.clear()
                self.process_text_action('translate')
            elif buffer_text == ':ft':
                self.key_buffer.clear()
                self.process_text_action('fix')
            elif len(buffer_text) == 3 and not (buffer_text.endswith('tl') or buffer_text.endswith('ft')):
                if not buffer_text.startswith(':'):
                    self.key_buffer.clear()
                    
        elif key == Key.backspace:
            if self.key_buffer:
                self.key_buffer.pop()
        elif key in [Key.space, Key.enter, Key.tab, Key.esc, Key.left, Key.right, Key.up, Key.down]:
            self.key_buffer.clear()

    def process_text_action(self, action_type):
        self.is_processing = True
        threading.Thread(target=self._process_text_thread, args=(action_type,), daemon=True).start()

    def _process_text_thread(self, action_type):
        try:
            action_label = "Traduzindo..." if action_type == "translate" else "Corrigindo..."
            self.root.after(0, lambda: self.status_label.config(text=action_label, foreground="orange"))

            keyboard_controller = keyboard.Controller()
            
            for _ in range(3):
                keyboard_controller.press(Key.backspace)
                keyboard_controller.release(Key.backspace)
                time.sleep(0.01)
            
            time.sleep(0.01)

            original_clipboard = pyperclip.paste()
            
            keyboard_controller.press(Key.ctrl)
            keyboard_controller.press('a')
            keyboard_controller.release('a')
            keyboard_controller.release(Key.ctrl)
            time.sleep(0.01)

            keyboard_controller.press(Key.ctrl)
            keyboard_controller.press('c')
            keyboard_controller.release('c')
            keyboard_controller.release(Key.ctrl)
            time.sleep(0.01)

            text_to_process = pyperclip.paste()
            pyperclip.copy(original_clipboard)

            if not text_to_process or text_to_process == original_clipboard:
                raise Exception("Não foi possível copiar o texto para processamento.")

            if action_type == "translate":
                processed_text = self.translator.translate_text(text_to_process)
            else:
                processed_text = self.translator.fix_text(text_to_process)
            
            pyperclip.copy(processed_text)
            time.sleep(0.01)
            
            keyboard_controller.press(Key.ctrl)
            keyboard_controller.press('v')
            keyboard_controller.release('v')
            keyboard_controller.release(Key.ctrl)
            
            self.root.after(0, lambda: self.add_to_history(action_type, text_to_process[:50], processed_text[:50]))
            
        except Exception as e:
            error_msg = f"Erro no processamento: {str(e)}"
            self.root.after(0, lambda: self.show_error(error_msg))
        finally:
            self.root.after(0, lambda: self.status_label.config(text="Ativo - Aguardando comandos", foreground="green"))
            self.is_processing = False

    def show_error(self, message):
        messagebox.showerror("Erro", message)

    def start_keyboard_listener(self):
        try:
            self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
            self.keyboard_listener.start()
        except Exception as e:
            self.show_error(f"Erro ao iniciar o listener de teclado: {str(e)}")

    def stop_keyboard_listener(self):
        if self.keyboard_listener:
            self.keyboard_listener.stop()

    def on_closing(self):
        self.stop_keyboard_listener()
        self.root.destroy()

    def run(self):
        if not self.check_configuration():
            self.config.setup_api_key()
            self.check_configuration()

        if self.config.is_configured():
            self.start_keyboard_listener()
            self.update_history_display()

        self.root.mainloop()

def main():
    app = TextTranslatorApp()
    app.run()

if __name__ == "__main__":
    main() 