from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
from urllib.error import HTTPError
from urllib.error import URLError
import re

# Armazena apenas os numeros da variavel valor
def trata_valor(valor):
    if valor == 0:
        valor == 0
    else:
        valor = re.sub('[^0-9]', '', valor)
    return valor

# Salva os dados encontrados em um arquivo txt
def salvar(listFilmes):
    arquivo_txt = open('arq_filmes.txt', 'w')
    arquivo_txt.write(listFilmes)
    #for linha in listFilmes:
     #   arquivo_txt.write(linha)
    arquivo_txt.close()

def valida_site(url, listFilmes, contador):
    ssl._create_default_https_context = ssl._create_unverified_context
    try:
        # abre a URL
        html = urlopen(url)
    # Verifica se a pagina não retorna um erro de HTTP
    except HTTPError as e:
        # Retorna Vazio caso encontre um erro HTTP
        return None
    # Verifica se a pagina está fora do ar ou se a URL está incorreta
    except URLError as e:
        # Retorna Vazio caso encontre um erro na URL
        return None
    try:
        var=[]
        # Transforma a pagina em um objeto BeautifulSoup
        bs = BeautifulSoup(html.read(), 'html.parser')
        # Encontra a class 'lister-item mode-advanced' e retorna o conteúdo HTML contido nesta página
        lista_filmes = bs.find_all('div', {'class': 'lister-item mode-advanced'})
        # Percorre todos o filmes disponiveis na lista da pagina
        for filme in lista_filmes:
            try:
                # Encontra a classe com o ano do filme e retorna o valor do mesmo
                ano = trata_valor(filme.find_all('span', {'class': 'lister-item-year text-muted unbold'})[0].get_text())
            except:
                # Caso não exista o ano atribui o valor 0 para a variavel
                ano = 0
            try:
                # Encontra a classe com o ibdb do filme e retorna o valor do mesmo
                ibdb = trata_valor(filme.find_all('div', {'class': 'inline-block ratings-imdb-rating'})[0].get_text())
            except:
                # Caso não exista o ibdb atribui o valor 0 para a variavel
                ibdb = 0
            #Formata o valor do campo
            num_ibdb = float(ibdb)/10
            try:
                # Encontra a classe com o metascore do filme e retorna o valor do mesmo
                metascore = trata_valor(filme.find_all('div', {'class': 'inline-block ratings-metascore'})[0].get_text())
            except:
                # Caso não exista o metascore atribui o valor 0 para a variavel
                metascore = 0
            try:
                # Encontra a classe com o numero de votos do filme
                tmp = filme.find('p', {'class': 'sort-num_votes-visible'})
                # Encontra o span que possui o numero de votos e retorna o valor do mesmo
                votos = trata_valor(tmp.find_all('span')[1].get_text())
            except:
                # Caso não exista o metascore atribui o valor 0 para a variavel
                votos = 0
            # Atraves do select, entra na estrutura do HTML para encontrar o nome do filme
            titulo = filme.select('div#main > div > div > div > div > div > h3 > a')[0].text
            # Cria e formata uma variavel com todos os dados coletados do HTML
            #var = ('{:<5}{:<10}{:<10}{:<100}{:<15}{:<10}').format(str(contador), str(num_ibdb), str(metascore), str(titulo), str(votos), str(ano)[:4])
            var = [str(contador), str(num_ibdb), str(metascore), str(titulo), str(votos), str(ano)[:4]]
            # Salva a variavel na lista
            listFilmes.append(var)
            # Adiciona mais um item no contador da lista
            contador += 1
        # Retorna o valor do contador
        return contador
    except:
        #Caso a aplicacao tenha algum retorno vazio a mesma para
        return None

# Cria um cabecario para os itens da lista
#listFilmes = ['{:<5}{:<10}{:<10}{:<100}{:<15}{:<10}'.format('#', 'imbd', 'metascore', 'filme', 'votos', 'ano')]
titulo = ['#', 'imbd', 'metascore', 'filme', 'votos', 'ano']
listFilmes = []
listFilmes.append(titulo)
# Inicia o contador em 0
contador = 0
# Percorre as paginas de 50 em 50 filmes até chegar em 2000 filmes.
#for pagina in range(1,2001,50):
for pagina in range(1, 150, 50):
    # URL da pagina
    url = ("https://www.imdb.com/search/title/?release_date=2020-01-01,2022-12-31&sort=num_votes,desc&start={}&ref_=adv_nxt").format(str(pagina))
    # Chama def para encontrar as informacoes desejadas
    contador = valida_site(url, listFilmes, contador)

# Chama def para salvar o arquivo txt
salvar(listFilmes)