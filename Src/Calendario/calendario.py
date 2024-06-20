from datetime import datetime
from calendar import TextCalendar
#from dateutil.relativedelta import relativedelta

class calendarioEventos(TextCalendar):
    def __init__(self):
        # Data atual, util para pegar o dia, mês e ano assim que inicializar o programa 
        # e quando precisar voltar para o dia atual
        self.__dataAtual: datetime = datetime.now()

        # Data auxiliar para percorrer o calendário
        self.__dataAux: datetime = datetime.now()
        
        # Atributos referentes aos dias, mês, ano e dia da semana, inicialmente são os valores da data atual
        self.__dia: int = self.__dataAtual.day
        self.__mes: int = self.__dataAtual.month
        self.__ano: int = self.__dataAtual.year
        self.__diaSemana: int = self.__dataAtual.weekday()

        # Tenta carregar os eventos cadastrados, se não encontrar o arquivo, cria um dicionário vazio
        try:
            self.__carregarEventos()
        except FileNotFoundError:
            self.__eventosAno: dict[int, dict[int, dict[int, list[tuple[str, str]]]]] = {}

    '''
        self.exemplo_do_evento = {
            2021: {
                6: {
                    1: [(datetime(2021, 6, 1, 12, 0), "Reunião"), (datetime(2021, 6, 1, 15, 0), "Aula")],
                    2: [(datetime(2021, 7, 1, 12, 0), "Reunião"), (datetime(2021, 7, 1, 15, 0), "Aula")],
                },
                7: {
                    2: [(datetime(2021, 7, 1, 12, 0), "Reunião"), (datetime(2021, 7, 1, 15, 0), "Aula")],
                }
            }, 2022: {
                1: {
                    3: [(datetime(2022, 1, 1, 12, 0), "basquete"), (datetime(2022, 1, 1, 15, 0), "futebol")],
                }, 31: {

                    1: [(datetime(2022, 1, 31, 12, 0), "Curso"), (datetime(2022, 1, 31, 15, 0), "Projeto")],
                }
            }
        }
    '''


    # Método auxiliar para adicionar um evento no atributo __eventosAno
    def __adicionaEvento(self, dia: int, mes: int, ano: int, evento: tuple[datetime, str]) -> None:
        # Verifica se o ano, mês e dia já estão no dicionário, caso não estejam, adiciona
        if ano not in self.__eventosAno:
            self.__eventosAno[ano] = {}
        if mes not in self.__eventosAno[ano]:
            self.__eventosAno[ano][mes] = {}
        if dia not in self.__eventosAno[ano][mes]:
            self.__eventosAno[ano][mes][dia] = []

        self.__eventosAno[ano][mes][dia].append(evento)
        

    # Método para cadastrar um evento, retorna True se foi possível cadastrar o evento e False caso contrário
    def cadastraEvento(self, dia: int, mes: int, ano: int, descricao: str = '', hora=0, minuto=0) -> bool:
        self.__dataAtual = datetime.now()
        data = datetime(ano, mes, dia, hora, minuto)
        evento = (data.isoformat(), descricao)

        # Verifica se a data do evento é maior que a data atual
        if self.__dataAtual < data:
            self.__adicionaEvento(dia, mes, ano, evento)
            return True
        
        return False
                
    
    # Método para voltar o mês, a partir de self.__mes
    def voltaMes(self) -> None:
        self.__mes -= 1
        self.__dia = 1
        if self.__mes < 1:
            self.__mes = 12
            self.__ano -= 1
        self.__dataAux = datetime(self.__ano, self.__mes, self.__dia)
        self.__diaSemana = self.__dataAux.weekday()
        

    # Método para avançar o mês, a partir de self.__mes
    def avancaMes(self) -> None:
        self.__mes += 1
        self.__dia = 1
        if self.__mes > 12:
            self.__mes = 1
            self.__ano += 1
        self.__dataAux = datetime(self.__ano, self.__mes, self.__dia)
        self.__diaSemana = self.__dataAux.weekday()


    # Método para voltar o ano, a partir de self.__ano
    def voltaAno(self) -> None:
        self.__ano -= 1
        self.__dia = 1
        self.__mes = 1
        self.__dataAux = datetime(self.__ano, self.__mes, self.__dia)
        self.__diaSemana = self.__dataAux.weekday()


    # Método para avançar o ano, a partir de self.__ano
    def avancaAno(self) -> None:
        self.__ano += 1
        self.__dia = 1
        self.__mes = 1
        self.__dataAux = datetime(self.__ano, self.__mes, self.__dia)
        self.__diaSemana = self.__dataAux.weekday()


    ''' # Método utilizando o relativedelta para voltar o mês
    def voltaMes(self, k: int = 1):
        self.__dataAtual -= relativedelta(months=k)
        self.__dia = self.__dataAtual.day
        self.__mes = self.__dataAtual.month
        self.__ano = self.__dataAtual.year
        self.__diaSemana = self.__dataAtual.weekday()
        self.__listaMesAtual = self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAnoAtual = self.__cal.yeardays2calendar(self.__ano)
'''


    # Método para salvar os eventos em um arquivo
    def salvarEventos(self) -> None:
        with open("eventosAno.txt", 'w') as f:
            f.write((str(self.__eventosAno)))

    def __carregarEventos(self) -> None:
        with open("eventosAno.txt", 'r') as f:
            self.__eventosAno = eval(f.read())

    # Métodos getters
    def getDia(self) -> int:
        return self.__dia
    
    def getMes(self) -> int:
        return self.__mes
    
    def getAno(self) -> int:
        return self.__ano
    
    def getDiaSemana(self) -> int:
        return self.__diaSemana
    
    def getListaMes(self) -> list[list[tuple[int, int]]]:
        return self.__listaMes
    
    def getListaAno(self) -> list[list[tuple[int, int]]]:
        return self.__listaAno
    
    # Método que retorna os eventos do dia, caso não tenha eventos, retorna uma lista None
    def getEventosDia(self, dia: int, mes: int, ano: int) -> list[tuple[datetime, str]]:
        return self.getEventosMes(mes, ano).get(dia, None)

    # Método que retorna os eventos do mês, caso não tenha eventos, retorna um dicionário vazio
    def getEventosMes(self, mes: int, ano: int) -> dict[int, list[tuple[str, str]]]: 
        return self.getEventosAno(ano).get(mes, {})
    
    # Método que retorna os eventos do ano, caso não tenha eventos, retorna um dicionário vazio
    def getEventosAno(self, ano: int) -> dict[int, dict[int, list[tuple[str, str]]]]:
        return self.__eventosAno.get(ano, {})
    
    # Método que retorna todos os eventos cadastrados
    def getEventos(self) -> dict[int, dict[int, dict[int, list[tuple[str, str]]]]]:
        return self.__eventosAno