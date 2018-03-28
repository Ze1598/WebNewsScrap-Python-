import requests, json, re

def get_picsV1(tags_):
    '''Obtém os links das imagens do feed de um utilizador, dadas as devidas
    tags para o POST request.
    Esta função converte o resultado do request num objeto de JSON, guarda-o num
    ficheiro .json e lê em seguida esse objeto para o converted para um dicionário
    de Python. Por fim, cria uma lista com o pretendido através das chaves desse 
    dicionário.'''
    #Se for mais do que uma tag, separar cada tag com um sinal de mais (+)
    if len(tags_.split()) > 1:
        tags_ = "+".join(tags_.split())

    #Criar uma clausa de try/except para prevenir exceções no request
    try:
        #O URL para o POST request é este (formatado com as tags de input da função)
        website = f"https://api.flickr.com/services/feeds/photos_public.gne?format=json&tags={tags_}&tagmode=any"
        #Fazer o POST request e obter o texto desse request
        req = requests.post(website).text
        '''É criado/editado primeiro um ficheiro .json para guardar o resultado do request 
        feito e é aberto em seguida de forma a que seja possível converter o objeto JSON
        para um dicionário de Python (assim é possível aceder à informação através dos pares
        key-value)'''
        #Converter o resultado do request para um objeto de JSON e guardá-lo num ficheiro .json
        with open('json_scrape.json', 'w') as f:
            #Não é convertido o texto na totalidade para não criar erros nas conversões
            f.write(req[15:-1])
        #Abrir o ficheiro criado e converter o objeto de JSON num dicionário de Python
        with open('json_scrape.json') as f:
            req_j = json.load(f)
        #Criar uma lista que contém apenas os links das imagens do feed da pessoa por quem se\
        #procurou com o POST request
        return [item['media']['m'] for item in req_j['items']]
    
    #Se tiver havido problemas com o request, não devolver nada
    except:
        return None


def get_picsV2(tags_):
    '''Obtém os links das imagens do feed de um utilizador, dadas as devidas
    tags para o POST request.
    Começa por fazer o request, e em seguida encontra os URLs pretendido usando
    expressões regulares (regex). Armazena estes URLs numa única lista.'''
    #Se for mais do que uma tag, separar cada tag com um sinal de mais (+)
    if len(tags_.split()) > 1:
        tags_ = "+".join(tags_.split())
    
    #Criar uma clausa de try/except para prevenir exceções no request
    try:
        #O URL para o POST request é este (formatado com as tags de input da função)
        website = f"https://api.flickr.com/services/feeds/photos_public.gne?format=json&tags={tags_}&tagmode=any"
        #Fazer o POST request e obter o texto desse request
        req = requests.post(website).text
        #Usando esta expressão regular, encontrar no string de texto do request apenas\
        #os links pretendidos (a parte inicial 'm":" é usada apenas para especificar\
        #o que se procura)
        regex = re.finditer(r'm":"http.+jpg', req)
        #Por último, os URLs são armazenados numa única lista
        #As barras são removidas (substituídas por um string vazio)
        return [req[link.start()+4:link.end()].replace('\\', '') for link in regex]

    #Se tiver havido problemas com o request, não devolver nada 
    except:
        return None

continuar = 's'
counter = 1
#Executa enquanto o utilizador quiser
while continuar == 's':
    #O nome do ficheiro é diferente para cada conjunto de tags procuradas
    nome_ficheiro = 'links_fotos_' + str(counter) + '.txt'

    #Pedir tags para procurar com o POST request
    tags = input('Insira tags para procurar (separadas por espaço): ')
    query_result = get_picsV1(tags)
    # query_result = get_picsV2(tags)

    #Verificar se o request foi feito com sucesso. Se sim, gravar num ficheiro\
    #.txt os links
    if query_result != None:
        
        #Iterar pela lista de links para fazer output de cada link numa linha nova
        for link in query_result:
            print(link)

        #Gravar num ficheiro .txt a lista dos links
        with open(nome_ficheiro, 'w') as f:
            #Criar um único string que contenha os vários links, um em cada linha para\
            #melhor legibilidade
            string = ''
            for link in query_result:
                string += link + '\n'
            f.write(string)
    
    #Em caso de insucesso, apenas imprime uma mensagem
    else:
        print('Houve um problema com o request. Tente de novo.')
    #Linha em branco
    print()

    # for link in query_result2:
        # print(link)

    #Perguntar se o utilizador pretende continuar (inserir um novo conjunto de tags)
    continuar = input('Continuar? [s/n]')
    #Incrementar o contador de forma a que o próximo .txt tenha um nome diferente
    counter += 1

#Quando terminar o while loop, imprimir uma mensagem final
else:
    print('O programa terminou')