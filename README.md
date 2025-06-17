# Text Translator MVP

Aplicação simples que traduz texto automaticamente quando você digita `:tl` após o texto.

## Como funciona

1. Escreva qualquer texto em um campo de entrada
2. Digite `:tl` no final do texto
3. O texto será automaticamente traduzido para inglês no mesmo campo, e o gatilho `:tl` será apagado.

## Requisitos

- Python 3.8+
- Conexão com internet
- API key do OpenRouter

## Instalação

1. Clone ou baixe este projeto
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
python main.py
```

4. Na primeira execução, você será solicitado a inserir sua API key do OpenRouter

## Configuração da API Key

1. Visite [OpenRouter](https://openrouter.ai/) e crie uma conta
2. Gere uma API key
3. Execute o programa e use o botão "Configurar API Key" na interface
4. A configuração é salva automaticamente no arquivo `translator_config.json`

## Uso

1. Execute `python main.py`
2. Uma janela abrirá, mostrando o status e o histórico
3. Em qualquer aplicação, escreva um texto e digite `:tl` no final
4. O texto será traduzido automaticamente

## Limitações do MVP

- Traduz apenas para inglês
- Usa modelo fixo (GPT-3.5-turbo)
- Interface mínima
- Funciona apenas no Windows

## Estrutura do Projeto

```
text-translator/
├── main.py                    # Aplicação principal
├── translator.py              # Lógica de tradução
├── config.py                 # Configurações
├── requirements.txt          # Dependências
├── translator_config.json   # Configurações salvas (criado automaticamente)
└── README.md                # Este arquivo
```

## Solução de Problemas

- **Erro de API key**: Verifique se a chave está correta e tem créditos
- **Gatilho não funciona**: Veja se o programa está rodando e sem erros.
- **Tradução não cola**: Aguarde alguns segundos entre traduções. O sistema pode estar lento.
