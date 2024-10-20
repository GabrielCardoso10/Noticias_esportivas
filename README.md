# 📰 **Noticias esportivas**

> Scripts em Python para **raspagem de notícias de sites esportivos**

---

## 📜 **Descrição**

Este repositório contém scripts em Python desenvolvidos para coletar e exibir as principais manchetes de sites esportivos populares como **Lance, GE (Globo Esporte), Gazeta Esportiva, e Jovem Pan**. O objetivo é facilitar a consulta de notícias esportivas diretamente no terminal e permitir a abertura das notícias no navegador.

---

## 🛠️ **Tecnologias Utilizadas**

- **Linguagem**: Python
- **Bibliotecas**:
  - `requests`: Para fazer requisições HTTP
  - `BeautifulSoup`: Para parsear o HTML
  - `Rich`: Para exibição de tabelas no terminal
  - `Webbrowser`: Para abrir links no navegador
  
---

## 🚀 **Como Usar**

#### obs: tenha o python 3.9 ou acima instalado
### 1. Clone o repositório

```bash
git clone https://github.com/gabrielcardoso10/noticias_esportivas.git
cd noticias_esportivas
```

### 2. Crie um ambiente virtual
2.1. Windows

```bash
python -m venv venv
venv\Scripts\activate
```

2.2. MacOS ou linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as bibliotecas
```bash
pip install requests
pip install beautifulsoup4
pip install rich
```

### 4. Execute o programa
```bash
python site.py
```


