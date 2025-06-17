import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog

class Config:
    def __init__(self):
        self.config_file = "translator_config.json"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "openai/gpt-4.1-nano"
        self.languages = {
            "English": "english",
            "Español": "spanish", 
            "Français": "french",
            "Deutsch": "german",
        }
        config_data = self.load_config()
        self.api_key = config_data.get('api_key', '')
        self.target_language = config_data.get('target_language', 'english')
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def load_api_key(self):
        config_data = self.load_config()
        return config_data.get('api_key', '')
    
    def save_config(self, api_key=None, target_language=None):
        try:
            config_data = self.load_config()
            if api_key is not None:
                config_data['api_key'] = api_key
                self.api_key = api_key
            if target_language is not None:
                config_data['target_language'] = target_language
                self.target_language = target_language
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configuração: {str(e)}")
            return False
    
    def save_api_key(self, api_key):
        return self.save_config(api_key=api_key)
    
    def get_api_key(self):
        return self.api_key
    
    def get_target_language(self):
        return self.target_language
    
    def set_target_language(self, language):
        return self.save_config(target_language=language)
    
    def get_available_languages(self):
        return self.languages
    
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
            self.target_language = 'english'
            return True
        except Exception:
            return False 