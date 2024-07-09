from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

from datetime import datetime, date
import calendar

from utils.formatacao import *
from utils.meses import meses_por_indice
from lista_eventos import ListaEventos

#Variável global
Lista_eventos = ListaEventos() #*
#Inicializao do dicionario de eventos - carregando do arquivo de eventos
eventos = Lista_eventos.busca_eventos()


#Defines de Estilo
WIDTH = 100
FONT = ('Calibri', 12)
BUTTONFONT = ('Calibri', 12)
SFONT = ('Calibri', 12)
BFONT = ('Calibri', 12, 'bold')
DFONT = ('Calibri', 14)
BACKGROUND = '#d1d1d1'
TBACKGROUND = '#25272e'
HBACKGROUND = '#3895ff'
FOREGROUND = '#1b1d24'
DFOREGROUND = '#aaaebd'
WFOREGROUND = '#606060'

def estilizar():
    '''
    Função que estiliza o app definindo configurações de estilo gerais do app.

    '''
    ttk.Style(root).theme_use('alt')
    ttk.Style(root).configure('alt', background=BACKGROUND)
    ttk.Style(root).configure('TButton', background=BACKGROUND, foreground = FOREGROUND, font=BUTTONFONT, borderwidth=0, focusthickness=0, focuscolor='none', width = 20)
    ttk.Style(root).map('TButton', background=[('active',BACKGROUND)])
    ttk.Style(root).configure('TMenubutton', font=FONT, border=0, borderwidth=0, borderradius=10, width=9, radius=50, anchor='center', background = BACKGROUND)
    ttk.Style(root).configure('TCheckbutton', font=FONT, borderwidth=0, focusthickness=0, focuscolor='none', background=BACKGROUND)
    ttk.Style(root).map('TCheckbutton', background=[('hover', BACKGROUND)])
    ttk.Style(root).configure('TFrame', background=BACKGROUND)
    ttk.Style(root).configure('TLabel', background=BACKGROUND)
    header_button = ttk.Style(root)
    header_button.configure('header.TButton', background=HBACKGROUND, foreground=FOREGROUND, font=DFONT, borderwidth=0, focusthickness=0, focuscolor='none', width = 20)
    header_button.map('header.TButton', background=[('active',HBACKGROUND)])

def adicionar_evento():   
    '''
    Função que adiciona os eventos do calendário.

    '''
    #Usando a biblioteca calendar para definir a data atual
    dia_atual = date.today().day
    mes_atual = date.today().month
    ano_atual = date.today().year
    
    #Criando uma lista com os anos futuros possíveis
    anos_possiveis = [ano_atual + i for i in range(0, 21)]

    #Cria uma nova janela para adicionar os enventos dos calendários
    Adicionar_Evento = Toplevel(root)
    Adicionar_Evento.wm_geometry(f'+{Adicionar_Evento.winfo_screenmmwidth()//2 + Adicionar_Evento.winfo_width()//2}+{Adicionar_Evento.winfo_screenmmheight()//2 + Adicionar_Evento.winfo_height()//2}')
    Adicionar_Evento.title('Adicionar Evento')
    Adicionar_Evento.resizable(False, False)
    Adicionar_Evento.configure(background=BACKGROUND)

    ano = StringVar()
    mes = StringVar()
    dia_inicial = StringVar()
    dia_final = StringVar()
    info = StringVar()

    #Variável booleana que informa se a Uesc está funcionão ou não
    funciona = BooleanVar()

    #Containers das variáveis
    container_ano = ttk.Frame(Adicionar_Evento)
    container_mes = ttk.Frame(Adicionar_Evento)
    container_dia = ttk.Frame(Adicionar_Evento)
    container_evento = ttk.Frame(Adicionar_Evento)
    
    #Menus supensos selecionáveis
    menu_meses = ttk.OptionMenu(container_mes, mes, '')
    menu_dias = ttk.OptionMenu(container_dia, dia_inicial, '')
    menu_dia_final = ttk.OptionMenu(container_dia, dia_final, '')
    divisor = ttk.Label(container_dia, text='até ', font=FONT)


    def entry():
        '''
        Função que cria e da update no container de eventos

        '''
        nonlocal container_evento
        nonlocal info
        nonlocal funciona

        #Inicialização do container de evento e criação de um input no formato de caixa de texto
        container_evento.destroy()
        container_evento = ttk.Frame(Adicionar_Evento)
        mini_container = ttk.Frame(container_evento)
        info = ttk.Entry(container_evento, font=FONT, width=50)

        #Widgets de input para receber descrição dos eventos, funcionamento da Uesc
        desc_request = ttk.Label(mini_container, font=FONT, text=f'Digite a descrição do evento: ', width=50, anchor='w')
        funciona_marcar = ttk.Checkbutton(mini_container, text='Não funciona', variable=funciona)
        #Salva o evento criado
        send_info = ttk.Button(container_evento, text='Enviar e Continuar', command=send_data)
        enviar_finalizar = ttk.Button(container_evento, text='Enviar e Fechar', command=send_data_2)

        #Pack dos Widgets do container de eventos
        desc_request.pack(side='left', anchor='w')
        funciona_marcar.pack(side='left', anchor='w')
        mini_container.pack(side='top', anchor='w')
        info.pack(side='left')
        send_info.pack(side='left')
        enviar_finalizar.pack(side='left')
        container_evento.pack(side='left')

    def adicionar_ao_dicionario():
        '''
        Função que adiciona o evento ao dicionário temporário de eventos que apenas existe durante a execução do programa.

        '''
        nonlocal info
        nonlocal funciona
        nonlocal ano
        nonlocal mes
        nonlocal dia_inicial
        nonlocal dia_final

        ano_int = int(ano.get())
        mes_str = mes.get()

        #Se houver info
        if len(info.get()):
            #Caso o evento acabe no mesmo dia que começa, basta passar dia_inicial para novo_evento
            if dia_inicial.get() == dia_final.get():
                novo_evento = [[int(dia_inicial.get())], funciona.get(), info.get()]
            #Caso contrário passa dia_inicial e dia_final
            else:
                novo_evento = [[int(dia_inicial.get()), int(dia_final.get())], funciona.get(), info.get()]
            #Se no dicionário houver o ano
            if eventos.get(ano_int) is not None:
                #Se no dicionário houver o mês
                if (eventos[ano_int]).get(mes_str) is not None:
                    #Flag para verificar se já tem o evento
                    possui = False
                    for evento in eventos[ano_int][mes_str]:
                        #Se as datas são iguais e se os nomes são iguais flag = True 
                        possui = (novo_evento[0] == evento[0] and novo_evento[-1].lower() == evento[-1].lower())
                        if possui:
                            break
                    #Se flag for falsa, cadastra passando o mês e o ano de parâmetro
                    if not possui:
                        eventos[ano_int][mes_str].append(novo_evento)
                    #Se flag for verdadeira apresenta um erro ao usuário
                    else:
                        mb.showwarning(title='Erro ao adicionar', message='Não adicionado!\nO evento já existe!')
                #Caso não houver o mês no dicionário, cadastra passando o ano de parâmetro
                else:
                    eventos[ano_int].update({mes_str: [novo_evento]})
            #Caso não houver o ano no dicionário
            else:
                eventos.update({ano_int:{mes_str:[novo_evento]}})
            eventos[ano_int][mes_str].sort()

            #Integracao com o banco de dados - adicionando evento no arquivo de texto
            data_inicial = f'{dia_inicial.get().zfill(2)}/{str(meses_por_indice[mes_str]).zfill(2)}/{ano_int}'
            data_final = f'{dia_final.get().zfill(2)}/{str(meses_por_indice[mes_str]).zfill(2)}/{ano_int}'
            Lista_eventos.criar_evento(data_inicial, data_final, info.get(), funciona.get())
        else:
            mb.showwarning(title='Erro ao adicionar', message="Não adicionado!\nDescrição Vazia!")

    def send_data_2():
        '''
        Funcao que cadastra o evento e fecha a janela.
        '''
        nonlocal Adicionar_Evento  # Usa a variavel Adicionar_Evento definida fora do escopo local
        adicionar_ao_dicionario()  # Chama a funcao que adiciona o evento ao dicionario
        Adicionar_Evento.destroy()  # Fecha a janela de adicao de evento
        Adicionar_Evento.update()  # Atualiza o estado da janela

        # Verifica se o ano e o mes selecionados sao iguais ao ano e mes do calendario atual
        if int(ano.get()) == ano_calendario and meses_por_indice[mes.get()] == mes_calendario:
            atualizarEventos(ano_calendario, mes_calendario)  # Atualiza a visualizacao dos eventos no calendario


    def send_data():
        '''
        Funcao que cadastra o evento e limpa o formulario.
        '''
        nonlocal info  # Usa a variavel info definida fora do escopo local
        adicionar_ao_dicionario()  # Chama a funcao que adiciona o evento ao dicionario
        # Verifica se o ano e o mes selecionados sao iguais ao ano e mes do calendario atual
        if int(ano.get()) == ano_calendario and meses_por_indice[mes.get()] == mes_calendario:
            atualizarEventos(ano_calendario, mes_calendario)  # Atualiza a visualizacao dos eventos no calendario
        entry()  # Chama a funcao que limpa o formulario

    def diaFinal(dia_inicial: StringVar):
        month = meses_por_indice[mes.get()]  # Obtém o mes selecionado
        year = int(ano.get())  # Obtém o ano selecionado
        month == meses_por_indice[month]  # Corrige o valor do mes
        dias_possiveis = [i for i in range(dia_inicial, calendar.monthrange(year, month)[1] + 1)]  # Cria a lista de dias possiveis

        nonlocal menu_dia_final  # Usa variaveis definidas fora do escopo local
        nonlocal dia_final
        nonlocal container_dia
        nonlocal divisor

        menu_dia_final.destroy()  # Destroi o menu de dia final existente
        divisor.destroy()  # Destroi o divisor existente

        # Cria novos widgets para o menu de dia final e o divisor
        menu_dia_final = ttk.OptionMenu(container_dia, dia_final, dia_inicial, *dias_possiveis)
        divisor = ttk.Label(container_dia, text='até ', font=FONT)

        # Adiciona os widgets ao container
        divisor.pack(side='left')
        menu_dia_final.pack(side='left')
        container_dia.pack(side='left')

        entry()  # Chama a funcao que limpa o formulario

    def mostrarMenuDias(mes: StringVar):
        year = int(ano.get())  # Obtém o ano selecionado
        month = meses_por_indice[mes]  # Obtém o mes selecionado

        # Cria a lista de dias possiveis com base no mes e ano selecionados
        if month > mes_atual or (month <= mes_atual and year > ano_atual):
            dias_possiveis = [i for i in range(1, calendar.monthrange(year, month)[1] + 1)]
        else:
            dias_possiveis = [i for i in range(dia_atual, calendar.monthrange(year, month)[1] + 1)]

        nonlocal menu_dias  # Usa variaveis definidas fora do escopo local
        nonlocal menu_dia_final
        nonlocal container_dia
        nonlocal container_evento
        nonlocal divisor
    
        # Destroi os containers e widgets existentes
        container_dia.destroy()
        container_evento.destroy()
        divisor.destroy()
    
        # Cria novos containers e widgets
        container_dia = ttk.Frame(Adicionar_Evento)
        label_dias = ttk.Label(container_dia, text='Selecione o(s) dia(s): ', font=FONT, anchor='w')
        menu_dias = ttk.OptionMenu(container_dia, dia_inicial, dias_possiveis[0], *dias_possiveis, command=diaFinal)

        # Adiciona os widgets ao container
        label_dias.pack(side='top')
        menu_dias.pack(side='left')
        container_dia.pack(side='left')

    def mostrarMenuMeses(ano):
        # Cria a lista de meses possiveis com base no ano selecionado
        if int(ano) > ano_atual:
            meses_possiveis = [meses_por_indice[value] for value in range(1, 13)]
        else:
            meses_possiveis = [meses_por_indice[value] for value in range(mes_atual, 13)]

        nonlocal menu_meses  # Usa variaveis definidas fora do escopo local
        nonlocal container_dia
        nonlocal container_mes
        nonlocal container_evento

        # Destroi os containers e widgets existentes
        container_mes.destroy()
        container_dia.destroy()
        container_evento.destroy()
    
        # Cria novos containers e widgets
        container_mes = ttk.Frame(Adicionar_Evento)
        label_meses = ttk.Label(container_mes, text='Selecione o mês: ', font=FONT, anchor='w')
        menu_meses = ttk.OptionMenu(container_mes, mes, meses_possiveis[0], *list(meses_possiveis), command=mostrarMenuDias)

        # Adiciona os widgets ao container
        label_meses.pack(side='top')
        menu_meses.pack(side='bottom')
        container_mes.pack(side='left')

    #Widgets da janela adcionar eventos
    label_anos = ttk.Label(container_ano, text='Selecione o Ano: ', font=FONT, anchor='w')
    menu_anos = ttk.OptionMenu(container_ano, ano, anos_possiveis[0], *list(anos_possiveis), command=mostrarMenuMeses)

    #Packs dos widgets
    label_anos.pack(side='top')
    menu_anos.pack(side='bottom')
    container_ano.pack(side='left')

    #Looping da janela de adcionar eventos
    Adicionar_Evento.mainloop()

def remover_evento():
    '''
    Função que remove um evento.

    '''
    #Cria uma nova janela para adicionar os enventos do calendário
    remover_Evento = Toplevel(root)
    remover_Evento.wm_geometry(f'+{remover_Evento.winfo_screenmmwidth()//2 + remover_Evento.winfo_width()//2}+{remover_Evento.winfo_screenmmheight()//2 + remover_Evento.winfo_height()//2}')
    remover_Evento.title('Remover Evento')
    remover_Evento.resizable(False, False)
    remover_Evento.configure(background=BACKGROUND)

    #Usando a biblioteca datetime para definir a data atual
    ano_atual = date.today().year

    #Criando uma lista com os anos futuros possíveis
    anos_possiveis = [ano_atual + i for i in range(0, 21)]

    #Variáveis de controle de data/evento
    ano = IntVar()
    mes = StringVar()

    #Containers das variáveis
    container_ano = ttk.Frame(remover_Evento)
    container_mes = ttk.Frame(remover_Evento)
    container = ttk.Frame(remover_Evento)

    #Menu supenso com selecionáveis
    menu_meses = ttk.OptionMenu(container_mes, mes, '')
    def mostrarMenuMeses(ano):
        '''
        Função que define quais meses irão ser apresentados como opção ao usuário.
        '''
        
        meses_possiveis = [meses_por_indice[mes_busca] for mes_busca in range(1, 13)]
        
        nonlocal container_mes
        nonlocal container
        nonlocal menu_meses
        nonlocal container

        container_mes.destroy()
        container.destroy()

        #Widgets do menu suspenso
        container_mes = ttk.Frame(remover_Evento)
        label_meses = ttk.Label(container_mes, text='Selecione o mês:', font=FONT, anchor='w')
        menu_meses = ttk.OptionMenu(container_mes, mes, meses_possiveis[0], *meses_possiveis, command = criar_lista)
        
        #Pack dos widgets do menu suspenso
        label_meses.pack(side='top')
        menu_meses.pack(side='bottom')
        container_mes.pack(side='left')

    #Cria uma lista vazia que será preenchida em carregar_lista_eventos
    lista_eventos = []
    #Cria uma lista vazia que armazenará instancias de InstVar() que terão valores: zero se o evento não deve ser removido e um para deve ser removido
    x = []

    def carregar_lista_eventos(ano_buscado, mes_buscado):
        ''' 
        Função que preenche a lista de eventos a partir do banco de dados e uma lista de instancias IntVar().
        '''
        nonlocal lista_eventos
        nonlocal x 
        lista_eventos = []
        x = []
        #Se o ano buscado e o mês buscado existe no dicionário de eventos preenche a lista de eventos
        if eventos.get(ano_buscado) is not None:
            if eventos[ano_buscado].get(mes_buscado) is not None:
                lista_eventos = eventos[ano_buscado][mes_buscado]
        #Ordena a lista de eventos
        lista_eventos.sort()
        #Instancia em cada posição da lista um IntVar para cada evento.
        x = [IntVar() for _ in range(0, len(lista_eventos))]
    
    def criar_lista(*args):
        '''
        Função que cria lista de eventos que podem ser removidas.
        '''
        nonlocal container
        nonlocal lista_eventos

        carregar_lista_eventos(ano.get(), mes.get())
        container.destroy()
        container = ttk.Frame(remover_Evento)
        
        #Widgets da lista de eventos
        canvas = Canvas(container, width=(remover_Evento.winfo_screenwidth() - WIDTH)//2, height=80, background=BACKGROUND, border=0, borderwidth=0, )
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        visualizador = ttk.Frame(canvas, height=150)

        visualizador.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=visualizador, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        #Se lista de eventos estiver vazia não há nada para ser removido
        if len(lista_eventos) == 0:
            visualizador.destroy()
            canvas.destroy()
            scrollbar.destroy()
            container.destroy()
            container = ttk.Frame(remover_Evento)
            ttk.Label(container, text='Nada para ser removido!', font=FONT, anchor='center').pack(side='top', anchor='w')

        #Apresenta os códigos passíveis para remoção e um checkbox para cada
        for i in range(0, len(lista_eventos)):
            evento = lista_eventos[i]
            evento = f'{format(evento[0])} - {wrap_text(evento[-1], 50, (WIDTH - 10))}'
            ttk.Checkbutton(visualizador, text=evento, variable=x[i], width=WIDTH).pack(side='top', anchor='w')
        button_frame = ttk.Frame(container)
        ttk.Button(button_frame, text='Remover', command= remova).pack(side='left', anchor='w')
        ttk.Button(button_frame, text='Fechar', command=remover_Evento.destroy).pack(side='left', anchor='w')
        
        #Packs dos widgets
        button_frame.pack(side='bottom')
        container.pack(side='right', anchor='w')
        if len(lista_eventos) > 0:
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
   
    def remova():
        '''
        Função que realiza a remoção no banco de dados e no dicionário
        '''
        def check(x):
            '''
            Função que retorna a quantidade de eventos a serem removidos.
            '''
            remover = 0
            for i in range(0, len(x)):
                remover += x[i].get()
            return remover
        
        #Enquanto houver eventos a serem removidos, remove o evento do dicionário e do banco de dados.
        while check(x) > 0:
            for i in range(0, len(x)):
                if x[i].get() == 1:
                    #Integracao back e front - removendo evento do arquivo de texto
                    info_evento = lista_eventos.pop(i)
                    data = f'{str(info_evento[0][0]).zfill(2)}/{str(meses_por_indice[mes.get()]).zfill(2)}/{ano.get()}'
                    Lista_eventos.remover_evento(data, info_evento[-1])
                    x.pop(i)
                    break
        criar_lista()

        #Atualiza o calendário na janela principal
        if ano.get() == ano_calendario and meses_por_indice[mes.get()] == mes_calendario:
            atualizarEventos(ano_calendario, mes_calendario)

    #Widgets da janela de remoção de eventos
    label_anos = ttk.Label(container_ano, text='Selecione o Ano:', font=FONT, anchor='w')
    menu_anos = ttk.OptionMenu(container_ano, ano, anos_possiveis[0], *anos_possiveis, command=mostrarMenuMeses)

    #Pack dos widgets
    label_anos.pack(side='top')
    menu_anos.pack(side='bottom')
    container_ano.pack(side='left')

    #Loop da janela de remoção
    remover_Evento.mainloop()

def anterior():
    '''
    Função que volta com os meses.

    '''
    global mes_calendario
    global ano_calendario
    global data
    # Verifica se o mes anterior é menor que 1 (Janeiro), se sim, volta para Dezembro do ano anterior
    if mes_calendario - 1 < 1:
        mes_calendario = 12
        ano_calendario -= 1
    else:
        mes_calendario -= 1
    # Atualiza a string da data e o calendario com o novo mes e ano
    data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')
    atualizar_calendario(ano_calendario, mes_calendario)

def proximo():
    '''
    Função que avança com os meses.

    '''
    global mes_calendario
    global ano_calendario
    global data
    # Verifica se o proximo mes é maior que 12 (Dezembro), se sim, avança para Janeiro do proximo ano
    if mes_calendario + 1 > 12:
        mes_calendario = 1
        ano_calendario += 1
    else:
        mes_calendario += 1
    # Atualiza a string da data e o calendario com o novo mes e ano
    data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')
    atualizar_calendario(ano_calendario, mes_calendario)

def voltar():
    '''
    Função que volta para a data em que o usuário está.

    '''
    global mes_calendario
    global ano_calendario
    global data
    # Reseta o mes e ano para o mes e ano atual
    mes_calendario = date.today().month
    ano_calendario = date.today().year
    # Atualiza a string da data e o calendario com o mes e ano atuais
    data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')
    atualizar_calendario(ano_calendario, mes_calendario)

def atualizar_calendario(ano, mes):
    global header_container
    # Remove todos os widgets existentes no calendario
    for widget in calendario_frame.winfo_children(): 
        widget.destroy()
    
    # Cabecalho com os dias da semana
    header = ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']
    linha, coluna = 0, 0

    # Adiciona o cabecalho ao calendario
    header_container.destroy()
    header_container = Frame(top_frame, background=HBACKGROUND, width=50)
    for day in header:
        ttk.Label(header_container, text=day, font=DFONT, background=HBACKGROUND, foreground=FOREGROUND, width=3, anchor='center', justify='center').grid(column=coluna, row=linha, padx=5)
        coluna += 1
        if not coluna % 7:
            coluna = 0
            linha += 1
    header_container.pack()

    # Obtem as semanas do mes com os dias correspondentes
    testing = calendar.Calendar().monthdays2calendar(ano, mes)
    hoje = [date.today().day, date.today().month, date.today().year]
    
    month_container = Frame(calendario_frame, background=BACKGROUND)
    # Preenche o calendario com os dias do mes
    for semana in testing:
        for dia in semana:
            coluna = (dia[1] + 1) % 7  # Calcula a coluna do dia da semana
            if coluna == 0:
                linha += 1  # Move para a proxima linha a cada domingo
            if dia[0] == 0:
                continue  # Ignora dias que nao pertencem ao mes atual
            # Marca o dia atual com uma cor diferente
            if dia[0] == hoje[0] and mes == hoje[1] and ano == hoje[2]:
                ttk.Label(month_container, text=dia[0], font=DFONT, foreground=DFOREGROUND, background=TBACKGROUND, width=3, anchor='center', justify='center').grid(row=linha, column=coluna, padx=5)
            # Colore os fim de semanas de outra cor
            elif coluna == 0 or coluna == 6:
                ttk.Label(month_container, text=dia[0], font=DFONT, foreground=WFOREGROUND, background=BACKGROUND, width=3, anchor='center', justify='center').grid(row=linha, column=coluna, padx=5)
            else:
                ttk.Label(month_container, text=dia[0], font=DFONT, foreground=FOREGROUND, background=BACKGROUND, width=3, anchor='center', justify='center').grid(row=linha, column=coluna, padx=5)
    month_container.pack()
    
    atualizarEventos(ano, mes)

def separarListas(ano, mes):
    global lista_genericos
    global lista_sem_funcionamento
    lista_genericos = []
    lista_sem_funcionamento = []
    #Se a uesc estiver funcionando adiciona o evento a lista genérica do contrário adiciona a outra lista.
    if eventos.get(ano) is not None:
        if (eventos[ano]).get(meses_por_indice[mes]) is not None:
            lista_genericos = [evento for evento in (eventos[ano]).get(meses_por_indice[mes]) if evento[1] is False]
            lista_sem_funcionamento = [evento for evento in (eventos[ano]).get(meses_por_indice[mes]) if evento[1] is True]

def atualizarEventos(ano, mes):

    separarListas(ano, mes)
    global eventos_frame
    global lista_genericos
    global lista_sem_funcionamento

    eventos_frame.destroy()
    eventos_frame = ttk.Frame(root)
    
    canvas = Canvas(eventos_frame, width=(root.winfo_screenwidth() + WIDTH)//2, background=BACKGROUND)
    scrollbar = ttk.Scrollbar(eventos_frame, orient='vertical', command=canvas.yview)
    visualizador = ttk.Frame(canvas, width=WIDTH)

    visualizador.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=visualizador, anchor='nw')
    canvas.configure(yscrollcommand=scrollbar.set)

    #Se lista de genéricos não está vazia cria um container para a lista com seus devidos widgets
    if lista_genericos is not None and len(lista_genericos) > 0:
        lista_genericos.sort()
        eventos_genericos = ttk.Frame(visualizador)
        for evento in lista_genericos:
            container = ttk.Frame(eventos_genericos)
            Label(container, text=f'{format(evento[0])}', background='#E0E0E0', font=BFONT, width= 7, justify='center', height=height_text(wrap_text(evento[-1], 50, (WIDTH -10)))).pack(side='left', anchor='w', ipadx=2)
            Label(container, text=wrap_text(evento[-1], 50, (WIDTH - 10)), background='#F3F3F3', font=FONT, width=WIDTH, anchor='w', justify='left',height=height_text(wrap_text(evento[-1], 50, (WIDTH - 10)))).pack(side='left', anchor='w')
            container.pack(side='top', anchor='w',pady=1)
        eventos_genericos.pack(side='top', anchor='w')

    #Se lista de feriados não está vazia cria um container para a lista com seus devidos widgets
    if lista_sem_funcionamento is not None and len(lista_sem_funcionamento) > 0:
        lista_sem_funcionamento.sort()
        eventos_sem_funcionamento = ttk.Frame(visualizador)
        ttk.Label(eventos_sem_funcionamento, text='Dias que a UESC não funciona: '.upper(), font=BFONT, background=BACKGROUND).pack(side='top', anchor='w')
        for evento in lista_sem_funcionamento:
            container = ttk.Frame(eventos_sem_funcionamento)
            Label(container, text=f'{format(evento[0])}', background='#FFCED1', foreground='#C00' ,font=BFONT, width= 7, justify='center', height=height_text(wrap_text(evento[-1], 50, (WIDTH - 10)))).pack(side='left', anchor='center', ipadx=2)
            Label(container, text=wrap_text(evento[-1], 50, (WIDTH - 10)), background='#FFF0F1', foreground='#C00', font=BFONT, width=WIDTH, justify='left', anchor='w',height=height_text(wrap_text(evento[-1], 50, (WIDTH - 10)))).pack(side='left', anchor='w')
            container.pack(side='top', anchor='w',pady=1)
        eventos_sem_funcionamento.pack(side='top', anchor='w')
    
    #Pack do container de eventos
    eventos_frame.pack(side='left', anchor='w')
    if lista_genericos is not None and len(lista_genericos) or lista_sem_funcionamento is not None and len(lista_sem_funcionamento):
        canvas.pack(side='left',fill = 'both', expand=True, anchor='w')
        scrollbar.pack(side='right', fill='y')

#Instancia o root
root = Tk()
#Configurações do root
root.title('Calendário')
root.wm_geometry(f'+{root.winfo_screenmmwidth()//2 + root.winfo_width()//2}+{root.winfo_screenmmheight()//2 + root.winfo_height()//2}')
root.configure(height=255)
root.resizable(False, False)
root.config(background=BACKGROUND)

#Mês e ano atual
mes_calendario = date.today().month
ano_calendario = date.today().year

#Instancia data
data = StringVar()
data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')

lista_genericos = []
lista_sem_funcionamento = []

#Containers
frame_mestre = Frame(root, background=BACKGROUND)
eventos_frame = Frame(root, background=BACKGROUND)
add_remover_deck = ttk.Frame(frame_mestre)
calendario_frame = Frame(frame_mestre, background=BACKGROUND)
top_frame = Frame(frame_mestre, background=HBACKGROUND)
btn_frame = Frame(top_frame, background=HBACKGROUND)
header_container = Frame(top_frame, background=HBACKGROUND)

#Botões e seus respectivos packs
anterior_btn = ttk.Button(btn_frame, text='<', command=anterior, width=5, style='header.TButton')
anterior_btn.pack(side='left')

voltar_inicio = ttk.Button(btn_frame, textvariable=data, command=voltar, style='header.TButton')
voltar_inicio.pack(side='left', padx=2)

proximo_btn = ttk.Button(btn_frame, text='>', command=proximo, width=5, style='header.TButton')
proximo_btn.pack(side='left')


adicionar_btn = ttk.Button(add_remover_deck, text='Adicionar Evento', command= adicionar_evento)
adicionar_btn.pack(side='left')

remover_btn = ttk.Button(add_remover_deck, text='Remover Evento', command= remover_evento)
remover_btn.pack(side='left', anchor='w')

#Pack dos Widgets
add_remover_deck.pack(side='bottom', anchor='center')
btn_frame.pack(side='top')
top_frame.pack(side='top')
calendario_frame.pack(side='top', anchor='center',fill='none', expand=True)
frame_mestre.pack(side='left', anchor='n')

# Inicializa o calendario com o mes e ano atuais
atualizar_calendario(ano_calendario, mes_calendario)
estilizar()
#Loop da janela principal
root.mainloop()