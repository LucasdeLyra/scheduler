import auxiliar

class BCP:
    """
    Clase utilizada para descrever um Bloco de Controle de Processos, tendo os requisitos mínimos descritos na descrição do trabalho
    (Contador de Programa, estado do processo, sua prioridade, seus registradores (X e Y), nome, instruções); além de 
    PS: Esta classe poderia muito bem ser um dicionário ou uma lista, mas achei mais elegante ser uma classe separada
    """
    def __init__(self, nome, prioridade, instrucoes):
        self.contador_programa = 0
        self.estado = 'Pronto'
        self.prioridade = prioridade
        self.X = 0
        self.Y = 0
        self.instrucoes = instrucoes
        self.nome = nome
        # Os atributos acima foram descritas no trabalho. Adicionei o atributo creditos para facilitar na contagem de créditos do escalonador.
        self.creditos = prioridade  # "1. Inicialmente, distribua um número de créditos, a cada processo, igual à sua prioridade"
        self.numero = int(self.nome.split('-')[1])
        
        



# Escalonador de processos
class Escalonador:
    def __init__(self, processos, quantum):
        self.quantum = quantum
        
        self.fila_prontos = auxiliar.quickSort(processos)  # "2. Ordene, então, a fila de processos prontos, conforme o número de créditos"
        self.fila_bloqueados = [] # "Assim, sua implementação deve contemplar uma lista de processos PRONTOS(acima) e outra de BLOQUEADOS."
        self.log = []  # Log das operações
        self.tabela_de_procesos = [processo.nome for processo in self.fila_prontos]
        
        self.trocas_de_contexto = [0]*10
        self.instrucoes_por_quantum = []
        
        

    def escalona(self):
        numero_processo_anterior = -1
        while self.tabela_de_procesos:   
            if not self.fila_prontos and self.tabela_de_procesos: # "5. Se não houver nenhum processo em condição de ser executado...
                self.__atualizar_bloqueados() # ...deve-se decrementar os tempos de espera de todos os processos na fila de bloqueados"
                continue
            
            processo = self.__executa_programa(self.fila_prontos.pop(0))

            self.__executar_quantum(processo)
            
            self.__realoca_processo_na_fila(processo)

            self.__atualizar_bloqueados()
            
            if numero_processo_anterior != processo.numero:
                self.trocas_de_contexto[processo.numero-1] +=1
            numero_processo_anterior = processo.numero
            
            
    def __executa_programa(self, processo):
        processo.creditos -= 1 #"3.a Ao começar a rodar, o processo perde um crédito"
        self.log.append(f'Executando {processo.nome}')
        processo.estado = 'Executando' 
        return processo

    def __realoca_processo_na_fila(self, processo):
        if processo.contador_programa < len(processo.instrucoes) and processo.estado != 'Bloqueado': # "3.b Findado o quantum, ..."
            processo.estado = 'Pronto'
            self.fila_prontos.append(processo) # "...o processo é reposicionado na fila de processos prontos..."
            self.fila_prontos = auxiliar.quickSort(self.fila_prontos) # "3.b ...conforme seu número de créditos restantes"
            if self.__testa_fila_sem_creditos(): # "3.d Quanto todos os processos estiverem com zero crédito, ..."
                self.__redistribuir_creditos() # ...então os créditos são redistribuídos, conforme sua prioridade"
    
    def __executar_quantum(self, processo):
        aux = 0
        for _ in range(self.quantum):
            aux += 1
            if processo.contador_programa >= len(processo.instrucoes):
                break
            instrucao = processo.instrucoes[processo.contador_programa]
            processo.contador_programa += 1 # Faço este incremento antes de saber qual o tipo de instrução para garantir que a contagem está correta, como no 4.f e na seção 1.2
            
            if instrucao == "SAIDA": # "6. Ao encontrar o comando SAIDA...
                self.tabela_de_procesos.remove(processo.nome) # ...e da tabela de processos"
                self.log.append(f"{processo.nome} terminado. X={processo.X}, Y={processo.Y}")
                break
                
            elif instrucao == "E/S": # "4. Se, durante a execução de um quantum, o processo fizer uma entrada ou saída"
                processo.estado = 'Bloqueado' # "4.a Ele será marcado como bloqueado...
                self.log.append(f"E/S iniciada em {processo.nome}")
                self.fila_bloqueados.append(processo) # ...sendo então transferido para o final da lista de bloqueados"
                processo.tempo_espera = 2 # "4.b A ele é atribuído um tempo de espera"
                                          # "4.d Cada processo fica bloqueado até que *DOIS* outros processos passem pelo estado executando"
                break
                                          
            else:
                if "=" in instrucao:
                    reg, valor = instrucao.split("=")
                    if reg == "X":
                        processo.X = int(valor)
                    elif reg == "Y":
                        processo.Y = int(valor)
                elif instrucao == "COM":
                    pass
                
        self.instrucoes_por_quantum.append(aux)
        self.log.append(f"Interrompendo {processo.nome} após {aux} instruções")

    def __testa_fila_sem_creditos(self):
        for processo in self.fila_prontos + self.fila_bloqueados:
            if processo.creditos != 0:
                return False
        return True
    
    def __redistribuir_creditos(self):
        for processo in self.fila_prontos + self.fila_bloqueados:
            if processo.nome in self.tabela_de_procesos: # Testei também se é um processo ainda vivo
                processo.creditos = processo.prioridade 

    def __atualizar_bloqueados(self):
        for processo in self.fila_bloqueados:
                if processo.tempo_espera == 0: # "4.e Quando o tempo de espera de algum processo bloqueado chegar a zero...
                    processo.estado = 'Pronto' # ...este deve receber o status de pronto...
                    self.fila_bloqueados.remove(processo) # ...sendo então removido da fila de bloqueados...
                    self.fila_prontos.append(processo) # ...e inserido na fila de processos prontos...
                    self.fila_prontos = auxiliar.quickSort(self.fila_prontos) #na posição correspondente ao seu número atual de créditos"

                processo.tempo_espera -= 1  # "4.c A cada processo que passe pelo estado executando esse tempo de espera é decrementado"

            
    def salvar_log(self, nome_arquivo):
        self.log.append(f"MÉDIA DE TROCAS: {sum(self.trocas_de_contexto)/len(self.trocas_de_contexto)}")
        self.log.append(f"MÉDIA DE INSTRUÇÕES: {sum(self.instrucoes_por_quantum)/len(self.instrucoes_por_quantum)}")
        self.log.append(f"QUANTUM: {self.quantum}")
        with open(rf"./logs/{nome_arquivo}", "w") as f:
            for linha in self.log:
                f.write(linha + "\n")


def criar_lista_BCP(prioridades, nome, instrucoes):
    lista_BCP = []
    for i in range(len(instrucoes)):
        bloco = BCP(nome[i], prioridades[i], instrucoes[i])
        lista_BCP.append(bloco)
    return lista_BCP

# Função principal para iniciar o escalonador
def main():

    pasta = r'C:\Users\Cliente\Desktop\EP1\programas'
    prioridades = auxiliar.le_prioridades(pasta)
    processos = criar_lista_BCP(prioridades, *auxiliar.le_processos(pasta))
    quantum = auxiliar.le_quantum(pasta)
    escalonador = Escalonador(processos, quantum)
    escalonador.escalona()
    escalonador.salvar_log(f"log{quantum:02}.txt")
    
    """
    #Usei este loop abaixo para gerar o log dos 21 possíveis quanta automaticamente
    for quantum in range(1,22):
        prioridades = auxiliar.le_prioridades(pasta)
        processos = criar_lista_BCP(prioridades, *auxiliar.le_processos(pasta))
        escalonador = Escalonador(processos, quantum)
        escalonador.escalona()
        escalonador.salvar_log(f"log{quantum:02}.txt")"""

if __name__ == "__main__":
    main()
