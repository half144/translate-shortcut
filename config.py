import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

class Config:
    def __init__(self):
        self.config_file = "translator_config.json"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "openai/gpt-4.1-nano"
        self.api_key = self.load_api_key()
    
    def load_api_key(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    return config_data.get('api_key', '')
        except Exception:
            pass
        return ''
    
    def save_api_key(self, api_key):
        try:
            config_data = {'api_key': api_key}
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f)
            self.api_key = api_key
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configuração: {str(e)}")
            return False
    
    def get_api_key(self):
        return self.api_key
    
    def setup_api_key(self):
        root = tk.Tk()
        root.withdraw()
        
        current_key = "***" + self.api_key[-4:] if self.api_key and len(self.api_key) > 4 else "Nenhuma"
        
        messagebox.showinfo("Configuração", f"Configure sua API key do OpenRouter.\n\nAPI Key atual: {current_key}")
        
        api_key = simpledialog.askstring("API Key", "Digite sua API key do OpenRouter:", show='*')
        
        if api_key and api_key.strip():
            if self.save_api_key(api_key.strip()):
                messagebox.showinfo("Sucesso", "API key configurada e salva com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar API key.")
        else:
            if not self.api_key:
                messagebox.showwarning("Aviso", "API key é obrigatória para o funcionamento do tradutor.")
        
        root.destroy()
    
    def is_configured(self):
        return bool(self.api_key and self.api_key.strip())
    
    def clear_config(self):
        try:
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            self.api_key = ''
            return True
        except Exception:
            return False 