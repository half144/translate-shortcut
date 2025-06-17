# MVP - Text Translator

## Visão Geral

MVP simples: aplicação que traduz o conteúdo de um input quando o usuário aperta um atalho de teclado.

**Fluxo básico:**

1. Usuário escreve texto em qualquer input do sistema
2. Aperta `Ctrl+Shift+T`
3. Texto é automaticamente traduzido para inglês no próprio campo

## Stack Tecnológica (Mínima)

- **Python 3.8+** - Linguagem principal
- **pynput** - Captura de hotkeys globais
- **pyperclip** - Manipulação do clipboard
- **requests** - Chamadas HTTP para OpenRouter
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **tkinter** - Interface básica de configuração (nativo do Python)

## Estrutura do Projeto

```
text-translator/
├── main.py                 # Arquivo principal
├── translator.py           # Lógica de tradução
├── config.py              # Configurações
├── .env                   # API key do OpenRouter
├── requirements.txt       # Dependências
└── README.md             # Instruções de uso
```

## Funcionalidades MVP

1. **Hotkey Global** - `Ctrl+Shift+T` para traduzir
2. **Captura de Texto** - Seleciona automaticamente todo o texto do input ativo
3. **Tradução** - Via OpenRouter API (modelo padrão)
4. **Substituição** - Cola o texto traduzido no lugar do original
5. **Configuração Básica** - Interface simples para definir API key

## Implementação Core

### 1. Fluxo de Tradução

```python
def translate_text():
    # 1. Selecionar todo o texto (Ctrl+A)
    # 2. Copiar (Ctrl+C)
    # 3. Traduzir via API
    # 4. Colar texto traduzido (Ctrl+V)
```

### 2. Integração OpenRouter

```python
def call_openrouter(text):
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": f"Translate to English: {text}"}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                           headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
```

### 3. Configuração Mínima

- Arquivo `.env` com `OPENROUTER_API_KEY=sua_chave`
- Interface tkinter básica para inserir/alterar a chave

## Cronograma MVP (2-3 dias)

### Dia 1: Core Functionality

- [x] Setup do projeto Python
- [x] Implementar captura de hotkey
- [x] Integração básica com OpenRouter
- [x] Fluxo de copiar/colar

### Dia 2: Refinamento

- [x] Tratamento de erros
- [x] Interface de configuração
- [x] Testes básicos
- [x] Packaging

### Dia 3: Polimento

- [x] Instalador/executável
- [x] Documentação
- [x] Validação final

## Limitações do MVP

- Apenas traduz para inglês
- Um modelo LLM fixo
- Sem histórico de traduções
- Sem customização de atalhos
- Interface mínima

## Próximos Passos (Pós-MVP)

1. Suporte a múltiplos idiomas
2. Seleção de modelos LLM
3. Histórico de traduções
4. Interface mais robusta
5. Atalhos customizáveis

## Requisitos de Sistema

- Windows 10+ (foco inicial)
- Python 3.8+ instalado
- Conexão com internet
- API key do OpenRouter

## Instalação e Uso

```bash
# 1. Clonar/baixar o projeto
# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar API key
echo "OPENROUTER_API_KEY=sua_chave" > .env

# 4. Executar
python main.py

# 5. Usar: escrever texto + Ctrl+Shift+T
```

Este MVP foca no essencial: traduzir texto rapidamente sem complexidade desnecessária.
