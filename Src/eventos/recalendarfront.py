from tkinter import *
from tkinter import ttk
from datetime import datetime, date
from formatacao import *
from lista_eventos import ListaEventos
import calendar

v = ListaEventos()

WIDTH = 100
FONT = ('Calibri', 12)
BUTTONFONT = ('Calibri', 12)
SFONT = ('Calibri', 12)
BFONT = ('Calibri', 12, 'bold')
BACKGROUND = '#d1d1d1'
FOREGROUND = '#1b1d24'

def estilizar():
    ttk.Style(root).theme_use('alt')
    ttk.Style(root).configure('TButton', background=BACKGROUND, foreground = FOREGROUND, font=BUTTONFONT, borderwidth=0, focusthickness=0, focuscolor='none', width = 20)
    ttk.Style(root).map('TButton', background=[('active',BACKGROUND)])
    ttk.Style(root).configure('TMenubutton', font=FONT, border=0, borderwidth=0, borderradius=10, width=9, radius=50, anchor='center')
    ttk.Style(root).configure('TCheckbutton', font=FONT, borderwidth=0, focusthickness=0, focuscolor='none')
    ttk.Style(root).map('TCheckbutton', background=[('hover', BACKGROUND)])
    ttk.Style(root).configure('TFrame', background=BACKGROUND)



def adicionar_evento():
    dia_atual = date.today().day
    mes_atual = date.today().month
    ano_atual = date.today().year
   
    anos_possiveis = [ano_atual + i for i in range(0, 11)]

    Adicionar_Evento = Toplevel()
    Adicionar_Evento.configure(background=BACKGROUND)

    ano = StringVar()
    mes = StringVar()
    dia_inicial = StringVar()
    dia_final = StringVar()
    funciona = BooleanVar()

    container_ano = ttk.Frame(Adicionar_Evento)
    container_mes = ttk.Frame(Adicionar_Evento)
    container_dia = ttk.Frame(Adicionar_Evento)
    container_evento = ttk.Frame(Adicionar_Evento)
    
    menu_meses = ttk.OptionMenu(container_mes, mes, '')
    menu_dias = ttk.OptionMenu(container_dia, dia_inicial, '')
    menu_dia_final = ttk.OptionMenu(container_dia, dia_final, '')
    divisor = ttk.Label(container_dia, text='até ', font=FONT)

    def entry():
        nonlocal container_evento
        global info
        nonlocal funciona

        container_evento.destroy()
        container_evento = ttk.Frame(Adicionar_Evento)
        mini_container = ttk.Frame(container_evento)
        info = ttk.Entry(container_evento, font=FONT, width=50)

        desc_request = ttk.Label(mini_container, font=FONT, text=f'Digite a descrição do evento: ', width=50, anchor='w')
        funciona_marcar = ttk.Checkbutton(mini_container, text='Não funciona', variable=funciona)
        send_info = ttk.Button(container_evento, text='Enviar e Continuar', command=send_data)
        enviar_finalizar = ttk.Button(container_evento, text='Enviar e Fechar', command=send_data_2)

        desc_request.pack(side='left', anchor='w')
        funciona_marcar.pack(side='left', anchor='w')
        mini_container.pack(side='top', anchor='w')
        info.pack(side='left')
        send_info.pack(side='left')
        enviar_finalizar.pack(side='left')
        container_evento.pack(side='left')

    def adicionar_ao_dicionario():

        global info
        nonlocal funciona
        nonlocal ano
        nonlocal mes
        nonlocal dia_inicial
        nonlocal dia_final

        ano_int = int(ano.get())
        mes_str = mes.get()

        if len(info.get()):
            if dia_inicial.get() == dia_final.get():
                novo_evento = [[int(dia_inicial.get())], funciona.get(), info.get()]
            else:
                novo_evento = [[int(dia_inicial.get()), int(dia_final.get())], funciona.get(), info.get()]
            if eventos.get(ano_int) is not None:
                if (eventos[ano_int]).get(mes_str) is not None:
                    if novo_evento not in eventos[ano_int][mes_str]:
                        eventos[ano_int][mes_str].append(novo_evento)
                else:
                    eventos[ano_int].update({mes_str: [novo_evento]})
            else:
                eventos.update({ano_int:{mes_str:[novo_evento]}})
            eventos[ano_int][mes_str].sort()

        #Integracao back e front - adicionando evento no arquivo de texto
        data_inicial = f'{dia_inicial.get().zfill(2)}/{str(meses_por_indice[mes_str]).zfill(2)}/{ano_int}'
        data_final = f'{dia_final.get().zfill(2)}/{str(meses_por_indice[mes_str]).zfill(2)}/{ano_int}'
        v.criar_evento(data_inicial, data_final, info.get(), funciona.get())

    def send_data_2():
        nonlocal Adicionar_Evento
        adicionar_ao_dicionario()
        Adicionar_Evento.destroy()
        Adicionar_Evento.update()
        if int(ano.get()) == ano_calendario and meses_por_indice[mes.get()] == mes_calendario:
            atualizarEventos(ano_calendario, mes_calendario)

    def send_data():
        global info
        adicionar_ao_dicionario()
        if int(ano.get()) == ano_calendario and meses_por_indice[mes.get()] == mes_calendario:
            atualizarEventos(ano_calendario, mes_calendario)
        entry()

    def diaFinal(dia_inicial: StringVar):

        month =meses_por_indice[mes.get()]
        year = int(ano.get())
        month == meses_por_indice[month]
        dias_possiveis = [i for i in range(dia_inicial, calendar.monthrange(year, month)[1] + 1)]

        nonlocal menu_dia_final
        nonlocal dia_final
        nonlocal container_dia
        nonlocal divisor

        menu_dia_final.destroy()
        divisor.destroy()

        menu_dia_final = ttk.OptionMenu(container_dia, dia_final, dia_inicial, *dias_possiveis)
        divisor = ttk.Label(container_dia, text='até ', font=FONT)

        divisor.pack(side='left')
        menu_dia_final.pack(side='left')
        container_dia.pack(side='left')

        entry()

    def mostrarMenuDias(mes: StringVar):
        year = int(ano.get())
        month = meses_por_indice[mes]

        if month > mes_atual or (month <= mes_atual and year > ano_atual):
            dias_possiveis = [i for i in range(1, calendar.monthrange(year, month)[1] + 1)]
        else:
            dias_possiveis = [i for i in range(dia_atual, calendar.monthrange(year, month)[1] + 1)]

        nonlocal menu_dias
        nonlocal menu_dia_final
        nonlocal container_dia
        nonlocal container_evento
        nonlocal divisor
        
        container_dia.destroy()
        container_evento.destroy()
        divisor.destroy()
        
        container_dia = ttk.Frame(Adicionar_Evento)
        label_dias = ttk.Label(container_dia, text='Selecione o(s) dia(s): ', font=FONT, anchor='w')
        menu_dias = ttk.OptionMenu(container_dia, dia_inicial, dias_possiveis[0], *dias_possiveis, command=diaFinal)

        label_dias.pack(side='top')
        menu_dias.pack(side='left')

        container_dia.pack(side='left')

    def mostrarMenuMeses(ano):
        if int(ano) > ano_atual:
            meses_possiveis = [meses_por_indice[value] for value in range(1, 13)]
        else:
            meses_possiveis = [meses_por_indice[value] for value in range(mes_atual, 13)]

        nonlocal menu_meses
        nonlocal container_dia
        nonlocal container_mes
        nonlocal container_evento

        container_mes.destroy()
        container_dia.destroy()
        container_evento.destroy()
        
        container_mes = ttk.Frame(Adicionar_Evento)
        label_meses = ttk.Label(container_mes, text='Selecione o mês: ', font=FONT, anchor='w')
        menu_meses = ttk.OptionMenu(container_mes, mes, meses_possiveis[0] ,*list(meses_possiveis), command=mostrarMenuDias)

        label_meses.pack(side='top')
        menu_meses.pack(side='bottom')
        container_mes.pack(side='left')

    label_anos = ttk.Label(container_ano, text='Selecione o Ano: ', font=FONT, anchor='w')
    menu_anos = ttk.OptionMenu(container_ano, ano, anos_possiveis[0], *list(anos_possiveis), command=mostrarMenuMeses)

    label_anos.pack(side='top')
    menu_anos.pack(side='bottom')
    container_ano.pack(side='left')

    Adicionar_Evento.mainloop()

def remover_evento():

    remover_Evento = Toplevel()
    remover_Evento.configure(background=BACKGROUND)

    mes_atual = date.today().month
    ano_atual = date.today().year

    anos_possiveis = [ano_atual + i for i in range(0, 11)]

    ano = IntVar()
    mes = StringVar()
    container_ano = ttk.Frame(remover_Evento)
    container_mes = ttk.Frame(remover_Evento)
    container = ttk.Frame(remover_Evento)

    menu_meses = ttk.OptionMenu(container_mes, mes, '')
    def mostrarMenuMeses(ano):
        if ano > ano_atual:
            meses_possiveis = [meses_por_indice[mes_busca] for mes_busca in range(1, 13)]
        else:
            meses_possiveis = [meses_por_indice[mes_busca] for mes_busca in range(mes_atual, 13)]
        
        nonlocal container_mes
        nonlocal container
        nonlocal menu_meses

        container_mes.destroy()

        container_mes = ttk.Frame(remover_Evento)
        label_meses = ttk.Label(container_mes, text='Selecione o mês:', font=FONT, anchor='w')
        menu_meses = ttk.OptionMenu(container_mes, mes, meses_possiveis[0], *meses_possiveis, command = criar_lista)
        
        label_meses.pack(side='top')
        menu_meses.pack(side='bottom')
        container_mes.pack(side='left')

    lista_eventos = []
    x = []

    def carregar_lista_eventos(ano_buscado, mes_buscado):
        nonlocal lista_eventos
        nonlocal x 
        if eventos.get(ano_buscado) is not None:
            if eventos[ano_buscado].get(mes_buscado) is not None:
                lista_eventos = eventos[ano_buscado][mes_buscado]
        x = [IntVar() for _ in range(0, len(lista_eventos))]
    
    def criar_lista(*args):
        nonlocal container
        nonlocal lista_eventos

        carregar_lista_eventos(ano.get(), mes.get())
        container.destroy()
        container = ttk.Frame(remover_Evento)
        if len(lista_eventos) == 0:
            ttk.Label(container, text='Nada para ser removido!', font=("Calibri", 12)).pack(side='top', anchor='w')
        for i in range(0, len(lista_eventos)):
            evento = lista_eventos[i]
            evento = f'{format(evento[0])} - {wrap_text(evento[-1])}'
            ttk.Checkbutton(container, text=evento, variable=x[i]).pack(side='top', anchor='w')
        ttk.Button(container, text='Remover', command= remova).pack(side='left', anchor='e')
        ttk.Button(container, text='Fechar', command=remover_Evento.destroy).pack(side='bottom', anchor='w')
        container.pack(side='top', anchor='w')
   
    def remova():
        def check(x):
            remover = 0
            for i in range(0, len(x)):
                remover += x[i].get()
            return remover
        while check(x) > 0:
            for i in range(0, len(x)):
                if x[i].get() == 1:
                    #Integracao back e front - removendo evento do arquivo de texto
                    info_evento = lista_eventos.pop(i)
                    data = f'{str(info_evento[0][0]).zfill(2)}/{str(meses_por_indice[mes.get()]).zfill(2)}/{ano.get()}'
                    v.remover_evento(data, info_evento[-1])
                    x.pop(i)
                    break
        criar_lista()
        if ano.get() == ano_calendario and meses_por_indice[mes.get()] == mes_calendario:
            atualizarEventos(ano_calendario, mes_calendario)

    label_anos = ttk.Label(container_ano, text='Selecione o Ano:', font=FONT, anchor='w')
    menu_anos = ttk.OptionMenu(container_ano, ano, anos_possiveis[0], *anos_possiveis, command=mostrarMenuMeses)

    label_anos.pack(side='top')
    menu_anos.pack(side='bottom')
    container_ano.pack(side='left')

    remover_Evento.mainloop()

    remover_Evento.mainloop()

def anterior():
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
    # Remove todos os widgets existentes no calendario
    for widget in calendario_frame.winfo_children():
        widget.destroy()
    
    # Cabecalho com os dias da semana
    header = ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']
    linha, coluna = 0, 0

    # Adiciona o cabecalho ao calendario
    for day in header:
        ttk.Label(calendario_frame, text=day, font=SFONT, background=BACKGROUND, foreground=FOREGROUND).grid(column=coluna, row=linha, padx=5)
        coluna += 1
        if not coluna % 7:
            coluna = 0
            linha += 1

    # Obtem as semanas do mes com os dias correspondentes
    testing = calendar.Calendar().monthdays2calendar(ano, mes)
    hoje = [date.today().day, date.today().month, date.today().year]
    
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
                ttk.Label(calendario_frame, text=dia[0], font=SFONT, foreground='#1e3194', background=BACKGROUND).grid(row=linha, column=coluna, padx=5)
            elif coluna == 0 or coluna == 6:
                ttk.Label(calendario_frame, text=dia[0], font=SFONT, foreground='#0c0d12', background=BACKGROUND).grid(row=linha, column=coluna, padx=5)
            else:
                ttk.Label(calendario_frame, text=dia[0], font=SFONT, foreground=FOREGROUND, background=BACKGROUND).grid(row=linha, column=coluna, padx=5)
    
    atualizarEventos(ano, mes)

def separarListas(ano, mes):
    global lista_genericos
    global lista_sem_funcionamento
    lista_genericos = []
    lista_sem_funcionamento = []
    if eventos.get(ano) is not None:
        if meses_por_indice.get(mes) is not None:
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

    if lista_genericos is not None and len(lista_genericos) > 0:
        eventos_genericos = ttk.Frame(eventos_frame)
        for evento in lista_genericos:
            container = ttk.Frame(eventos_genericos)
            ttk.Label(container, text=f'{format(evento[0])}', background='#E0E0E0', font=BFONT, width= 7, justify='center').pack(side='left', anchor='w', ipadx=2)
            ttk.Label(container, text=wrap_text(evento[-1], 50, WIDTH), background='#F3F3F3', font=FONT, width=WIDTH).pack(side='left', anchor='w')
            container.pack(side='top', anchor='w',pady=1)
        eventos_genericos.pack(side='top', anchor='w')

    if lista_sem_funcionamento is not None and len(lista_sem_funcionamento) > 0:
        eventos_sem_funcionamento = ttk.Frame(eventos_frame)
        ttk.Label(eventos_sem_funcionamento, text='Dias que a UESC não funciona: '.upper(), font=BFONT).pack(side='top', anchor='w')
        for evento in lista_sem_funcionamento:
            container = ttk.Frame(eventos_sem_funcionamento)
            ttk.Label(container, text=f'{format(evento[0])}', background='#FFCED1', foreground='#C00' ,font=BFONT, width= 7, justify='center',).pack(side='left', anchor='center', ipadx=2)
            ttk.Label(container, text=wrap_text(evento[-1], 50, WIDTH), background='#FFF0F1', foreground='#C00', font=BFONT, width=WIDTH).pack(side='left', anchor='w')
            container.pack(side='top', anchor='w',pady=1)
        eventos_sem_funcionamento.pack(side='top', anchor='w')
    
    eventos_frame.pack(side='left', anchor='n')

#Inicializao do dicionario de eventos - carregando do arquivo de eventos
eventos = v.busca_eventos()

root = Tk()
root.config(background=BACKGROUND)

mes_calendario = date.today().month
ano_calendario = date.today().year
data = StringVar()
data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')
lista_genericos = []
lista_sem_funcionamento = []

frame_mestre = Frame(root, background=BACKGROUND)
calendario_frame = Frame(frame_mestre, background=BACKGROUND)
btn_frame = Frame(frame_mestre, background=BACKGROUND)
eventos_frame = Frame(root, background=BACKGROUND)

anterior_btn = ttk.Button(btn_frame, text='<', command=anterior, width=5)
anterior_btn.pack(side='left')

voltar_inicio = ttk.Button(btn_frame, textvariable=data, command=voltar)
voltar_inicio.pack(side='left', padx=2)

proximo_btn = ttk.Button(btn_frame, text='>', command=proximo, width=5)
proximo_btn.pack(side='left')

add_remover_deck = ttk.Frame(frame_mestre)

adicionar_btn = ttk.Button(add_remover_deck, text='Adicionar Evento', command= adicionar_evento)
adicionar_btn.pack(side='left')

remover_btn = ttk.Button(add_remover_deck, text='Remover Evento', command= remover_evento)
remover_btn.pack(side='left', anchor='w')

add_remover_deck.pack(side='bottom', anchor='center')

btn_frame.pack(side='top', pady=5)
calendario_frame.pack(side='top', anchor='center',fill='none', expand=True)
frame_mestre.pack(side='left')

# Inicializa o calendario com o mes e ano atuais
atualizar_calendario(ano_calendario, mes_calendario)
estilizar()
root.mainloop()