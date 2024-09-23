import os

# Definição do Bloco de Controle de Processos (BCP)
class BCP:
    def __init__(self, nome, prioridade, instrucoes):
        self.nome = nome
        self.prioridade = prioridade
        self.creditos = prioridade  # Número de créditos é igual à prioridade inicialmente
        self.instrucoes = instrucoes  # Instruções do processo
        self.pc = 0  # Contador de Programa: índice da próxima instrução
        self.estado = 'Pronto'  # Estados: 'Pronto', 'Executando', 'Bloqueado'
        self.tempo_espera = 0
        self.registrador_x = 0
        self.registrador_y = 0

# Carregar processos, prioridades e quantum
def carregar_processos(diretorio_programas):
    processos = []
    with open(f"{diretorio_programas}/prioridades.txt") as f:
        prioridades = [int(linha.strip()) for linha in f.readlines()]

    arquivos = sorted(os.listdir(diretorio_programas))
    arquivos.remove('prioridades.txt')
    arquivos.remove('quantum.txt')
    for i, arquivo in enumerate(arquivos):
        with open(os.path.join(diretorio_programas, arquivo)) as f:
            nome = f.readline().strip()  # Nome do processo
            instrucoes = [linha.strip() for linha in f.readlines()]  # Instruções
            processos.append(BCP(nome, prioridades[i], instrucoes))
    return processos

def carregar_quantum(diretorio_programas):
    with open(f"{diretorio_programas}/quantum.txt") as f:
        return int(f.readline().strip())

# Escalonador de processos
class Escalonador:
    def __init__(self, processos, quantum):
        self.quantum = quantum
        self.original = processos
        self.fila_prontos = sorted(processos, key=lambda p: -p.creditos)  # Ordena por créditos
        self.tabela_de_procesos = [processo.nome for processo in self.fila_prontos]
        self.fila_bloqueados = []
        self.log = []  # Log das operações

    def executar(self):
        while self.tabela_de_procesos:
            # Se não houver processo pronto, decrementa o tempo de bloqueio dos bloqueados
            if not self.fila_prontos and self.tabela_de_procesos:
                self.atualizar_bloqueados()
                continue

            # Pega o próximo processo da fila de prontos
            processo = self.fila_prontos.pop(0)
            print(f'Executando {processo.nome}')
            processo.estado = 'Executando'

            # Executa até o fim do quantum ou até encontrar uma instrução de E/S
            instr_executadas = self.executar_quantum(processo)

            # Log da execução
            print(f"Interrompendo {processo.nome} após {instr_executadas} instruções")
            
            # Se o processo não terminou, volta para a fila de prontos
            if processo.pc < len(processo.instrucoes) and processo.estado != 'Bloqueado':
                processo.estado = 'Pronto'
                processo.creditos -= 1
                if processo.creditos == 0:
                    self.redistribuir_creditos()
                self.fila_prontos.append(processo)
                self.fila_prontos.sort(key=lambda p: -p.creditos)

            # Atualiza os processos bloqueados
            self.atualizar_bloqueados()

    def executar_quantum(self, processo):
        instrucoes_executadas = 0
        for _ in range(self.quantum):
            instrucoes_executadas += 1
            if processo.pc >= len(processo.instrucoes):
                break
            instrucao = processo.instrucoes[processo.pc]
            processo.pc += 1
            if instrucao == "SAIDA":
                print('SAIDA')
                print(self.fila_prontos)
                print(processo)
                self.tabela_de_procesos.remove(processo.nome)
                print(f"{processo.nome} terminado. X={processo.registrador_x}, Y={processo.registrador_y}")
                return instrucoes_executadas
            elif instrucao == "E/S":
                processo.estado = 'Bloqueado'
                processo.tempo_espera = 2
                self.fila_bloqueados.append(processo)
                return instrucoes_executadas
            else:
                self.executar_instrucao(processo, instrucao)
            
        return instrucoes_executadas

    def executar_instrucao(self, processo, instrucao):
        print(instrucao)
        if "=" in instrucao:
            reg, valor = instrucao.split("=")
            if reg == "X":
                processo.registrador_x = int(valor)
            elif reg == "Y":
                processo.registrador_y = int(valor)
        elif instrucao == "COM":
            pass  # Comando genérico

    def redistribuir_creditos(self):
        for processo in self.fila_prontos + self.fila_bloqueados:
            if processo.nome in self.tabela_de_procesos:
                processo.creditos = processo.prioridade

    def atualizar_bloqueados(self):
        novos_bloqueados = []
        for processo in self.fila_bloqueados:
            if processo.estado == 'Bloqueado':
                if processo.tempo_espera == 0:
                    processo.estado = 'Pronto'
                    self.fila_prontos.append(processo)
                    self.fila_bloqueados.remove(processo)
                else:
                    novos_bloqueados.append(processo)
                processo.tempo_espera -= 1  # Simulação de tempo de espera de E/S
        self.fila_bloqueados = novos_bloqueados
        self.print_creditos()

    def print_fila(self):
        print("FILA DE BLOQUEADOS")
        for processo in self.fila_bloqueados:
            print(processo.nome, processo.tempo_espera)
        print("FILA DE PRONTOS")
        for processo in self.fila_prontos:
            print(processo.nome, processo.creditos)

            
    def salvar_log(self, nome_arquivo):
        with open(nome_arquivo, "w") as f:
            for linha in self.log:
                f.write(linha + "\n")

# Função principal para iniciar o escalonador
def main():
    diretorio_programas = r"C:\Users\Cliente\Desktop\EP1\programas"
    processos = carregar_processos(diretorio_programas)
    quantum = carregar_quantum(diretorio_programas)
    escalonador = Escalonador(processos, quantum)
    escalonador.executar()
    escalonador.salvar_log(f"log{quantum:02}.txt")

if __name__ == "__main__":
    main()
