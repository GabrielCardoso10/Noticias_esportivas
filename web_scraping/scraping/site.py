import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import webbrowser
from urllib.parse import urljoin
import re

class NoticiasSite:
    def __init__(self):
        self.sites = {
            'lance': {
                'url': "https://www.lance.com.br/",
                'cabecalho': {'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36 Edg/129.0.0.0"},
                'funcao_scrape': self._obter_noticias_lance
            },
            'ge': {
                'url': "https://ge.globo.com/",
                'cabecalho': {'user-agent': "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)"},
                'funcao_scrape': self._obter_noticias_ge
            },
            'gazeta': {
                'url': "https://www.gazetaesportiva.com/noticias/",
                'cabecalho': {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"},
                'funcao_scrape': self._obter_noticias_gazeta
            },
            'jovem pan': {
                'url': "https://jovempan.com.br/esportes",
                'cabecalho': {'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"},
                'funcao_scrape': self._obter_noticias_jovem_pan
            }
        }
        self.noticias = {}
        self.console = Console()

    def atualizar_noticias(self, nome_site):
        """Atualiza as notícias de um site escolhido."""
        nome_site = nome_site.lower()
        if nome_site in self.sites:
            site = self.sites[nome_site]
            site['funcao_scrape'](site['url'], site['cabecalho'])
        else:
            print(f"Site {nome_site} não encontrado.")

    def _obter_noticias_lance(self, url, cabecalho):
        self._obter_noticias(url, cabecalho, remover_count=4)

    def _obter_noticias_ge(self, url, cabecalho):
        self._obter_noticias(url, cabecalho, remover_count=4)

    def _obter_noticias_gazeta(self, url, cabecalho):
        self._obter_noticias(url, cabecalho, remover_count=5)
        
    def _obter_noticias_jovem_pan(self, url, cabecalho):
        self._obter_noticias(url, cabecalho, remover_count=20)

    def _obter_noticias(self, url, cabecalho, remover_count):
        try:
            pagina = requests.get(url, headers=cabecalho)
            pagina.raise_for_status()  # Levanta um erro se a resposta for um erro HTTP

            sopa = BeautifulSoup(pagina.text, 'html.parser')
            noticias_encontradas = sopa.find_all('a', href=True)

            dicionario_noticias = {}
            for noticia in noticias_encontradas:
                titulo = noticia.get_text(strip=True)
                link = urljoin(url, noticia['href'])  # Converte links relativos em absolutos

                # Remover horários do título
                titulo = self._remover_horarios(titulo)

                # Verifica se o título e o link são relevantes
                if titulo and link and self._is_noticia_relevante(titulo):
                    dicionario_noticias[titulo] = link

            # Remove as últimas notícias conforme o site
            self._remover_ultimas_noticias(dicionario_noticias, remover_count)

            self.noticias = dicionario_noticias
            self.exibir_noticias()
        except requests.RequestException as e:
            print(f"Erro ao acessar o site: {e}")

    def _remover_horarios(self, titulo):
        # Remove padrões de horários do título
        return re.sub(r'\b\d{1,2}:\d{2} ?[APap][mM]?\b|\b\d{1,2} ?[APap][mM]?\b|\b\d{1,2}(?:h|hs)\d{2}\b', '', titulo).strip()

    def _remover_ultimas_noticias(self, dicionario_noticias, remover_count):
        # Remove as últimas notícias
        for _ in range(remover_count):
            if dicionario_noticias:  # Verifica se ainda há notícias
                dicionario_noticias.popitem()  # Remove a última notícia

    def _is_noticia_relevante(self, titulo):
        # Lista de palavras ou frases a serem excluídas
        palavras_excluir = ['ao vivo', 'resultados', 'agenda', 'calendário', 'promoção']  # Exemplo de palavras a excluir
        return not any(palavra in titulo.lower() for palavra in palavras_excluir)

    def exibir_noticias(self):
        """Exibe as notícias em uma tabela e permite que o usuário clique para abrir."""
        while True: 
            tabela = Table(title="Notícias")

            tabela.add_column("Número", justify="center")
            tabela.add_column("Título", justify="left")

            for idx, (titulo, link) in enumerate(self.noticias.items(), start=1):
                tabela.add_row(str(idx), titulo)

            self.console.print(tabela)

            escolha = input("Digite o número da notícia que deseja abrir (ou '0' para voltar ao menu): ")
            if escolha == '0':
                return 
            else:
                try:
                    indice = int(escolha) - 1
                    if 0 <= indice < len(self.noticias):
                        url = list(self.noticias.values())[indice]
                        webbrowser.open(url)
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Entrada inválida.")

# Menu para o usuário
def menu():
    site = NoticiasSite()

    while True:
        print("\nMenu:")
        print("1. Escolher site e ver notícias")
        print("2. Sair")

        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            nome_site = input("Digite o nome do site (lance, ge, gazeta, jovem pan): ")
            site.atualizar_noticias(nome_site)
        
        elif escolha == '2':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

menu()
