### Grupo: SO-TI-23
### Aluno 1: Gonçalo Domingues (fc51751)
### Aluno 2: Beatriz Pereira (fc57579)
### Aluno 3: Jorge Ferreira (fc58951)
import os
import sys
from multiprocessing import Process, Array, Lock
lista_ficheiros=[] #lista de ficheiros
l_ficheiro_processo=[] #lista de ficheiros por processo
l_linhas_processo=[] #lista de linhas por processo
criticalZone=Lock() #zona critica: cada processo são apresentados sequencialmente, sem serem intercalados com os resultados dos outros processos
array = Array('i',10) #array de ocorrencias da palavra e linhas encontradas
erro=0

def main(args):
    #print('Programa: pgrepwc_processos.py')
    #print('Argumentos: ', args)
    pass





def trata_processo(ocurrences, lista_linhas, indice, palavra):
    ocurrences = lista_linhas[indice].count(palavra) #número total de ocorrências isoladas da palavra a pesquisar
    array[0] = array[0] + ocurrences
    linha = 0 #número total de linhas que contêm uma ou mais ocorrências da palavra a pesquisar
    if palavra in lista_linhas[indice]:
        linha+=1
        print("Processo: ", os.getpid(),"| Linha:",indice,"-->",lista_linhas[indice])
    array[1] = array[1] + linha




def trata_processo_filho(ficheiro, i, palavra, n_palavras, linha, ocurrences):
    file = open(ficheiro, "r")
    data = file.readlines()
    print("")
    print("Processo filho, PID:", os.getpid())
    print("")
    for line in data: #percorre as linhas do ficheiro
            i+=1
            if palavra in line: #verifica se existe a palavra a pesquisar na linha
                n_palavras = line.count(palavra)
                print("Ficheiro:",ficheiro ,"| Linha:",i, "-->", line)
                linha+=1
                ocurrences = ocurrences + n_palavras #número total de ocorrências isoladas da palavra a pesquisar
    array[0] = array[0] + ocurrences
    array[1] = array[1] + linha






def processa_resto(resto, lista, conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros,palavra,indice,numero_processo,l_processo,fim):
    print_n_processos(numero_paralelizaçao)
    if(resto==0): # exemplo -resto = 0 , paralelizaçao 3 ficheiro com 6 linhas
        for x in range(numero_paralelizaçao): #cria processos conforme numero de paralelizaçao
            fim=fim+l_processo[x]
            newProcess=Process(target=contador,args=(conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros,palavra,indice,numero_processo,l_processo,fim,))
            if(indice<len(lista)-1): #indice = ao indice inicial da lista de ficheiros que cada processo executa
                indice+=l_processo[x]
            newProcess.start()
        newProcess.join()
        print_palavra(conta_palavras, palavra, total_linhas)         
    else: #resto de linhas diferente de 0
        for x in range(numero_paralelizaçao): #cria processos conforme numero de paralelizaçao
            fim = fim+l_processo[x]
            newProcess=Process(target=contador,args=(conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros,palavra,indice,numero_processo,l_processo,fim,))
            indice=fim
            newProcess.start()
        newProcess.join()
        print_palavra(conta_palavras, palavra, total_linhas)





def print_n_processos(x):
    """Imprime no terminal o número de processos utilizados
    Args:
        x (int): número de processos utilizados 
    """
    print("-------------------------------------------------------------------------------------------------------")
    print("---Número de processos utilizados:",x,"---")
    print("-------------------------------------------------------------------------------------------------------")







def print_palavra(conta_palavras, palavra, total_linhas):
    """Imprime no terminal o número total de ocorrências isoladas da palavra, bem como o número total de linhas onde esta foi encontrada.
    Args:
        conta_palavras (int): número de ocorrências isoladas da palavra a pesquisar.
        palavra (str): a palavra a pesquisar no conteúdo do(s) ficheiro(s).
        total_linhas (int): número total de linhas que contêm uma ou mais ocorrências da palavra a pesquisar.
    """
    ocorrencias = array[0] #número total de ocorrências isoladas da palavra a pesquisar.
    linhas = array[1] #número total de linhas que contêm uma ou mais ocorrências da palavra a pesquisar. 
    print("-------------------------------------------------------------------------------------------------------")
    if(conta_palavras):
        print("A palavra '"+palavra+"' ocorre", ocorrencias, "vezes.")
    if(total_linhas):
        print("A palavra '"+palavra+"' é escrita em", linhas,"linhas.")





lista=[]

def funcao(conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros,palavra,indice,numero_ficheiros_processo):
    
     for x in lista_ficheiros: #recebe a lista de ficheiros
            file = open(x, "r")
            lista.append(file)
            
    """após a validação das opções do comando, o processo pai cria os processos filhos definidos pelo nível de paralelização do comando (valor n). 
    Estes processos pesquisam as palavras nos ficheiros, contam as ocorrências das palavras e o número de linhas em que estas foram encontradas nos ficheiros, 
    e escrevem os resultados (linhas encontradas e contagens) na saída (stdout).
    Args:
        conta_palavras (int): número de ocorrências isoladas da palavra a pesquisar.
        total_linhas (int): número total de linhas que contêm uma ou mais ocorrências da palavra a pesquisar.
        paralelizaçao (str): paralelização normal
        numero_paralelizaçao (int): número da paralelização
        paralelizaçao_especial (str): paralelização especial
        lista_ficheiros (lst): lista de ficheiros dados na linha de comandos
        palavra (str):  palavra a pesquisar no conteúdo do(s) ficheiro(s)
        indice (int): indice inicial da lista de ficheiros que cada processo executa
        numero_ficheiros_processo (int): número de ficheiros por processo
    """
    print("-------------------------------------------------------------------------------------------------------")
    print("---Ficheiros: ", lista_ficheiros,"---")
    fim = 0
    try:
        resto = len(lista_ficheiros) % numero_paralelizaçao
    except ZeroDivisionError:
        print("ERRO! O número da paralelização nao pode ser zero, pois não é possível dividir um número por zero!")
    indice = 0
    #---------------------------------------------------------------------------------------------------------------------
    if (paralelizaçao==False): #um processo faz todos os ficheiros, ou seja, cria um processo com varios argumentos (incluindo a lista de ficheiros)
        contador(conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros,palavra,indice,numero_ficheiros_processo,l_ficheiro_processo,fim)
    
    for x in range(numero_paralelizaçao):
        l_ficheiro_processo.append(numero_ficheiros_processo) #preencher lista com numero de ficheiros por processo 
    #---------------------------------------------------------------------------------------------------------------------
    if(paralelizaçao==True and paralelizaçao_especial==False): #um processo por ficheiro - a paralelização do trabalho de pesquisa e contagem é coordenada pelo processo pai
        for i in range(resto): #No caso normal, cada ficheiro é atribuído pelo processo pai a um único processo, não havendo assim divisão do conteúdo de um ficheiro por vários processos
            l_ficheiro_processo[i]=l_ficheiro_processo[i]+1
       
        if(numero_paralelizaçao>=len(lista_ficheiros)): #se o numero de paralelizaçao for superior ao número de ficheiros, o comando (o processo pai) redefine-o automaticamente para o número de ficheiros
            print_n_processos(len(lista_ficheiros)) #cria tantos processos quantos os ficheiros a pesquisar
            for x in range(len(lista_ficheiros)): #cria 1 processo por ficheiro
                newProcess=Process(target=contador,args=(conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros[x],palavra,indice,numero_ficheiros_processo,l_ficheiro_processo,fim,))
                newProcess.start()
            newProcess.join()
            print_palavra(conta_palavras, palavra, total_linhas)
        else: #numero de paralelizaçao menor que len(lista_ficheiros) - os ficheiros sao divididos equitativamente(em termos do número de ficheiros atribuídos a cada processo) pelos processos(numero_paralelizaçao), ou seja, existirem mais ficheiros do que processos, o processo pai decide distribuir o mais equitativo possível os ficheiros   
            processa_resto(resto, lista_ficheiros, conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros,palavra,indice,numero_ficheiros_processo, l_ficheiro_processo,fim)
    #---------------------------------------------------------------------------------------------------------------------      
    if(paralelizaçao_especial==True and len(lista_ficheiros)==1 and numero_paralelizaçao>1): #No caso especial apenas é indicado um ficheiro a pesquisar
        file = open(lista_ficheiros[0],'r')
        lista_linhas = file.readlines() #O processo pai terá de saber quantas linhas tem o ficheiro para poder fazer uma divisão tão equitativa quanto possível.
        resto_linhas = len(lista_linhas) % numero_paralelizaçao   
        numero_linhas_processo = len(lista_linhas) // numero_paralelizaçao
        for x in range(numero_paralelizaçao): 
           l_linhas_processo.append(numero_linhas_processo) #preencher lista com numero de linhas do ficheiro por processo 

        for i in range(resto_linhas): #percorre o resto de linhas para adicionar no indice +1 a seguir o processo
            l_linhas_processo[i]=l_linhas_processo[i]+1
        
        if(numero_paralelizaçao>=len(lista_linhas)): #se numero de paralelizaçao maior ou igual que len(lista_linhas) //exemplo linhas = 5 p = 5
            print_n_processos(len(lista_linhas))
            for x in range(len(lista_linhas)): #cria 1 processo por linhas do ficheiro   
                indice=x   #feita pelo processo pai de forma que o conteúdo do ficheiro indicado seja dividido pelos n processos que estiverem disponíveis.
                newProcess=Process(target=contador,args=(conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_linhas[x],palavra,indice,numero_linhas_processo,l_linhas_processo,fim,))
                newProcess.start()
            newProcess.join()
            print_palavra(conta_palavras, palavra, total_linhas)
        else: #entra quando o numero de paralelizaçao for menor que o numero de linhas, ou seja, se existirem mais linhas do que processos, o processo pai decide inicialmente como distribuir as linhas do ficheiros, tentando ser o mais equitativo possível 
            processa_resto(resto_linhas, lista_linhas, conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros,palavra,indice,numero_linhas_processo,l_linhas_processo, fim)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    




def contador(conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,ficheiro,palavra,indice,numero_ficheiros_processo,l_ficheiro_processo,fim): 
    """processos pesquisam as palavras nos ficheiros, contam as ocorrências das palavras e o número de linhas em que estas foram encontradas nos ficheiros, 
    e escrevem os resultados (linhas encontradas e contagens) na saída (stdout).
    Args:
        conta_palavras (int): número de ocorrências isoladas da palavra a pesquisar.
        total_linhas (int): número total de linhas que contêm uma ou mais ocorrências da palavra a pesquisar.
        paralelizaçao (str): paralelização normal
        numero_paralelizaçao (int): número da paralelização
        paralelizaçao_especial (str): paralelização especial
        ficheiro (str): ficheiro dado na linha de comandos
        palavra (str):  palavra a pesquisar no conteúdo do(s) ficheiro(s)
        indice (int): indice inicial da lista de ficheiros que cada processo executa
        numero_ficheiros_processo (int): número de ficheiros por processo
        l_ficheiro_processo (lst): lista de ficheiros por processo
        fim (int): indice final da lista de ficheiros que cada processo executa
    """
    ocurrences=0 #número total de ocorrências isoladas da palavra a pesquisar
    i=0 
    linha=0 #número total de linhas que contêm uma ou mais ocorrências da palavra a pesquisar
    n_palavras=0 
    if(paralelizaçao==False):
        print("-------------------------------------------------------------------------------------------------------")
        print("Processo pai,  PID:", os.getpid())
        print("")
        for x in ficheiro: #recebe a lista de ficheiros
            file = open(x, "r")
            data = file.readlines()
            for line in data: #percorre as linhas do ficheiro 
                i+=1
                if palavra in line: #verifica na linha a palavra a pesquisar
                    n_palavras = line.count(palavra)
                    print("Ficheiro:",x,"| Linha:",i, "-->", line)
                    linha+=1
                    ocurrences = ocurrences + n_palavras     
        print("-------------------------------------------------------------------------------------------------------")       
        if(total_linhas):
            print("A palavra '"+palavra+"' é escrita em", linha,"linhas." )
        if(conta_palavras):
            print("A palavra '"+palavra+"' ocorre", ocurrences, "vezes.")
    #---------------------------------------------------------------------------------------------------------------------
    criticalZone.acquire() #"inicio da zona critica" - cada processo são apresentados sequencialmente
    if(paralelizaçao==True and paralelizaçao_especial==False): #apenas paralelização normal ativada
        if(numero_paralelizaçao>=len(lista_ficheiros)): #se o numero da paralelizacao for maior ou igual ao numero de ficheiros
            trata_processo_filho(ficheiro, i, palavra, n_palavras, linha, ocurrences)
        elif(numero_paralelizaçao<len(lista_ficheiros)): #se o numero da paralelizacao for menor ao numero de ficheiros
            for x in range(indice, fim): #percorre do indice da lista de ficheiros ate ao fim
                trata_processo_filho(ficheiro[x], i, palavra, n_palavras, linha, ocurrences)
    #---------------------------------------------------------------------------------------------------------------------       
    #paralelização especial só é ativada quando recebe apenas um ficheiro no terminal
    if(paralelizaçao_especial == True and len(lista_ficheiros)==1):
        file = open(lista_ficheiros[0],'r')
        lista_linhas = file.readlines() 

        if(numero_paralelizaçao < len(lista_linhas)): #se o numero da paralelizacao for menor ao numero de linhas do ficheiro
            for x in range(indice, fim): #percorre do indice da lista de ficheiros ate ao fim
                trata_processo(ocurrences, lista_linhas, x, palavra)         
        elif(numero_paralelizaçao >= len(lista_linhas)): #se o numero da paralelizacao for maior ou igual ao numero de linhas do ficheiro
            trata_processo(ocurrences, lista_linhas, indice, palavra)
    criticalZone.release() #"fim da zona critica" 
 #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
if __name__ == "__main__":
    main(sys.argv[1:])
    indice = 0
    lista_ficheiros = []
    conta_palavras = False
    total_linhas = False
    paralelizaçao = False
    paralelizaçao_especial = False
    numero_paralelizaçao = 1
    numero_ficheiros_processo = 0
    i = 0
    while i < len(sys.argv): #percorre a lista de argumentos/parametros do terminal: ./pgrepwc [-c] [-l] [-p n] [-t] [-e] palavra {ficheiros}
        if sys.argv[i] == '-c': #opção que permite contar o número total de ocorrências isoladas da palavra a pesquisar.
            conta_palavras = True     
        elif sys.argv[i] == '-l': #opção que permite obter o número total de linhas que contêm uma ou mais ocorrências da palavra a pesquisar. 
            total_linhas = True
        elif sys.argv[i] == '-p': #opção que permite definir o nível de paralelização n do comando (ou seja, o número de processos (filhos) que são utilizados para efetuar a pesquisa e as contagens). 
            try: # Por omissão, deve ser utilizado apenas um processo (o processo pai) para realizar a pesquisa e contagens.
                numero_paralelizaçao = int(sys.argv[i+1])
                paralelizaçao = True  
            except (ValueError, TypeError):
                print("-------------------------------------------------------------------------------------------------------") 
                print("ERRO! Parametro invalido! Ao usar paralelização tem que indicar o número inteiro de paralelização, \n"+"caso contrário NÃO é ATIVADA!")
        elif sys.argv[i] == '-e': #opção que permite ativar o modo de paralelização especial. Se forem especificados vários ficheiros, esta opção é ignorada.
            paralelizaçao_especial = True
        elif '.txt' in sys.argv[i]: # podem ser dados um ou mais ficheiros, sobre os quais é efetuada a pesquisa e contagem. 
            lista_ficheiros.append(sys.argv[i])
        else : 
            palavra = sys.argv[i] # a palavra a pesquisar no conteúdo do(s) ficheiro(s).
            if(palavra=="pgrepwc_processos.py"):
                palavra=''
        i += 1
        
    if(len(lista_ficheiros)==0): #Caso não sejam dados ficheiros na linha de comandos, estes devem ser lidos de stdin (o comando no início da sua execução pedirá ao utilizador quais são os ficheiros a processar).
        ficheiro = input("Introduza um ficheiro '.txt' \n")
        while True:
            if ".txt" in ficheiro:
                lista_ficheiros.append(ficheiro)
                resposta = str(input("Pretende colocar mais algum ficheiro? [S/N] ")).strip().upper()[0]
                if resposta == "S":
                    ficheiro = input("Introduza um ficheiro '.txt' \n")
                elif resposta == "N":
                    break
                else:
                    print("ERRO! Por favor, responda apenas com S ou N.")
            else:
                ficheiro = input("Introduza um ficheiro '.txt' válido  \n")
                                    
    if(numero_paralelizaçao!=0 and numero_paralelizaçao>0):
        numero_ficheiros_processo = len(lista_ficheiros)//numero_paralelizaçao 
    elif(numero_paralelizaçao<=0):
        erro=1
        print("-------------------------------------------------------------------------------------------------------")
        print("ERRO! Parâmetro/número inválido! Só é aceite um número inteiro positivo para o número da paralelização")
        print("-------------------------------------------------------------------------------------------------------")
        
    if(paralelizaçao_especial==True and len(lista_ficheiros)>1): #Se forem especificados vários ficheiros, esta opção -e é ignorada.
        paralelizaçao_especial=False
        print("-------------------------------------------------------------------------------------------------------")
        print("/**PARALELIZAÇÃO ESPECIAL -e IGNORADA/DESATIVADA (devido ao parametro ter mais que 1 ficheiro)**/")
    try:  
        if(palavra=='' or palavra==" " or (int(palavra)!=palavra) or (float(palavra)!=palavra)): #Caso não exista palavra a pesquisar, pede ao utilizador a palavra para pesquisar
            print("-------------------------------------------------------------------------------------------------------")
            palavra = str(input("ERRO! Não existe palavra, por favor coloque uma palavra para pesquisar: ")).strip() 
            try:
                while palavra=='' or palavra==" " or (int(palavra)!=palavra) or (float(palavra)!=palavra): 
                    print("-------------------------------------------------------------------------------------------------------")
                    palavra = str(input("ERRO! Parâmetro inválido! Por favor, coloque uma PALAVRA para pesquisar: ")).strip()
            except (ValueError, TypeError):
                palavra = palavra
    except (ValueError, TypeError):
        palavra = palavra
        
    for x in lista_ficheiros: #percorre a lista de ficheiros para verificar se existe algum erro de ficheiro nao encontrado
        try:
            teste = open(x, 'r')
        except FileNotFoundError:
            erro=1
            print("-------------------------------------------------------------------------------------------------------")
            print("ERRO! O ficheiro "+x+" não foi encontrado na diretoria! Coloque ou crie um ficheiro válido!")
            print("-------------------------------------------------------------------------------------------------------")
    
    if(erro==0): #caso não tiver erros
        funcao(conta_palavras,total_linhas,paralelizaçao,numero_paralelizaçao,paralelizaçao_especial,lista_ficheiros,palavra,indice,numero_ficheiros_processo)
    