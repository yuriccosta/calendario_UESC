from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

from datetime import datetime, date
import calendar

from utils.formatacao import *
from utils.meses import meses_por_indice
from lista_eventos import ListaEventos

Lista_eventos = ListaEventos()
eventos = Lista_eventos.busca_eventos()

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
    dia_atual = date.today().day
    mes_atual = date.today().month
    ano_atual = date.today().year
    
    anos_possiveis = [ano_atual + i for i in range(0, 21)]

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
        nonlocal info
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
        nonlocal info
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
                    possui = False
                    for evento in eventos[ano_int][mes_str]:
                        possui = (novo_evento[0] == evento[0] and novo_evento[-1].lower() == evento[-1].lower())
                        if possui:
                            break
                    if not possui:
                        eventos[ano_int][mes_str].append(novo_evento)
                    else:
                        mb.showwarning(title='Erro ao adicionar', message='Não adicionado!\nO evento já existe!')
                else:
                    eventos[ano_int].update({mes_str: [novo_evento]})
            else:
                eventos.update({ano_int:{mes_str:[novo_evento]}})

            eventos[ano_int][mes_str].sort()
            data_inicial = f'{dia_inicial.get().zfill(2)}/{str(meses_por_indice[mes_str]).zfill(2)}/{ano_int}'
            data_final = f'{dia_final.get().zfill(2)}/{str(meses_por_indice[mes_str]).zfill(2)}/{ano_int}'
            Lista_eventos.criar_evento(data_inicial, data_final, info.get(), funciona.get())
        else:
            mb.showwarning(title='Erro ao adicionar', message="Não adicionado!\nDescrição Vazia!")

    def send_data_2():
        nonlocal Adicionar_Evento
        adicionar_ao_dicionario()
        Adicionar_Evento.destroy()
        Adicionar_Evento.update()
        if int(ano.get()) == ano_calendario and meses_por_indice[mes.get()] == mes_calendario:
            atualizarEventos(ano_calendario, mes_calendario)

    def send_data():
        nonlocal info
        adicionar_ao_dicionario()
        if int(ano.get()) == ano_calendario and meses_por_indice[mes.get()] == mes_calendario:
            atualizarEventos(ano_calendario, mes_calendario)
        entry()

    def diaFinal(dia_inicial: StringVar):
        month = meses_por_indice[mes.get()]
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
    remover_Evento = Toplevel(root)
    remover_Evento.wm_geometry(f'+{remover_Evento.winfo_screenmmwidth()//2 + remover_Evento.winfo_width()//2}+{remover_Evento.winfo_screenmmheight()//2 + remover_Evento.winfo_height()//2}')
    remover_Evento.title('Remover Evento')
    remover_Evento.resizable(False, False)
    remover_Evento.configure(background=BACKGROUND)

    ano_atual = date.today().year

    anos_possiveis = [ano_atual + i for i in range(0, 21)]

    ano = IntVar()
    mes = StringVar()
    container_ano = ttk.Frame(remover_Evento)
    container_mes = ttk.Frame(remover_Evento)
    container = ttk.Frame(remover_Evento)

    menu_meses = ttk.OptionMenu(container_mes, mes, '')
    def mostrarMenuMeses(ano):
        meses_possiveis = [meses_por_indice[mes_busca] for mes_busca in range(1, 13)]
        
        nonlocal container_mes
        nonlocal container
        nonlocal menu_meses
        nonlocal container

        container_mes.destroy()
        container.destroy()

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
        lista_eventos = []
        x = []
        if eventos.get(ano_buscado) is not None:
            if eventos[ano_buscado].get(mes_buscado) is not None:
                lista_eventos = eventos[ano_buscado][mes_buscado]
        lista_eventos.sort()
        x = [IntVar() for _ in range(0, len(lista_eventos))]
    
    def criar_lista(*args):
        nonlocal container
        nonlocal lista_eventos

        carregar_lista_eventos(ano.get(), mes.get())
        container.destroy()
        container = ttk.Frame(remover_Evento)
        
        canvas = Canvas(container, width=(remover_Evento.winfo_screenwidth() - WIDTH)//2, height=80, background=BACKGROUND, border=0, borderwidth=0, )
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        visualizador = ttk.Frame(canvas, height=150)

        visualizador.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=visualizador, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        if len(lista_eventos) == 0:
            visualizador.destroy()
            canvas.destroy()
            scrollbar.destroy()
            container.destroy()
            container = ttk.Frame(remover_Evento)
            ttk.Label(container, text='Nada para ser removido!', font=FONT, anchor='center').pack(side='top', anchor='w')

        for i in range(0, len(lista_eventos)):
            evento = lista_eventos[i]
            evento = f'{format(evento[0])} - {wrap_text(evento[-1], 50, (WIDTH - 10))}'
            ttk.Checkbutton(visualizador, text=evento, variable=x[i], width=WIDTH).pack(side='top', anchor='w')
        button_frame = ttk.Frame(container)
        ttk.Button(button_frame, text='Remover', command= remova).pack(side='left', anchor='w')
        ttk.Button(button_frame, text='Fechar', command=remover_Evento.destroy).pack(side='left', anchor='w')
        
        button_frame.pack(side='bottom')
        container.pack(side='right', anchor='w')
        if len(lista_eventos) > 0:
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
        
   
    def remova():
        def check(x):
            remover = 0
            for i in range(0, len(x)):
                remover += x[i].get()
            return remover
        while check(x) > 0:
            for i in range(0, len(x)):
                if x[i].get() == 1:
                    info_evento = lista_eventos.pop(i)
                    data = f'{str(info_evento[0][0]).zfill(2)}/{str(meses_por_indice[mes.get()]).zfill(2)}/{ano.get()}'
                    Lista_eventos.remover_evento(data, info_evento[-1])
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

def anterior():
    global mes_calendario
    global ano_calendario
    global data

    if mes_calendario - 1 < 1:
        mes_calendario = 12
        ano_calendario -= 1
    else:
        mes_calendario -= 1
    data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')
    atualizar_calendario(ano_calendario, mes_calendario)

def proximo():
    global mes_calendario
    global ano_calendario
    global data
    if mes_calendario + 1 > 12:
        mes_calendario = 1
        ano_calendario += 1
    else:
        mes_calendario += 1
    data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')
    atualizar_calendario(ano_calendario, mes_calendario)

def voltar():
    global mes_calendario
    global ano_calendario
    global data

    mes_calendario = date.today().month
    ano_calendario = date.today().year
    data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')
    atualizar_calendario(ano_calendario, mes_calendario)

def atualizar_calendario(ano, mes):
    global header_container

    for widget in calendario_frame.winfo_children(): 
        widget.destroy()
    
    header = ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']
    linha, coluna = 0, 0

    header_container.destroy()
    header_container = Frame(top_frame, background=HBACKGROUND, width=50)
    for day in header:
        ttk.Label(header_container, text=day, font=DFONT, background=HBACKGROUND, foreground=FOREGROUND, width=3, anchor='center', justify='center').grid(column=coluna, row=linha, padx=5)
        coluna += 1
        if not coluna % 7:
            coluna = 0
            linha += 1
    header_container.pack()

    testing = calendar.Calendar().monthdays2calendar(ano, mes)
    hoje = [date.today().day, date.today().month, date.today().year]
    
    month_container = Frame(calendario_frame, background=BACKGROUND)
    for semana in testing:
        for dia in semana:
            coluna = (dia[1] + 1) % 7
            if coluna == 0:
                linha += 1
            if dia[0] == 0:
                continue
            if dia[0] == hoje[0] and mes == hoje[1] and ano == hoje[2]:
                ttk.Label(month_container, text=dia[0], font=DFONT, foreground=DFOREGROUND, background=TBACKGROUND, width=3, anchor='center', justify='center').grid(row=linha, column=coluna, padx=5)
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

    if lista_genericos is not None and len(lista_genericos) > 0:
        lista_genericos.sort()
        eventos_genericos = ttk.Frame(visualizador)
        for evento in lista_genericos:
            container = ttk.Frame(eventos_genericos)
            Label(container, text=f'{format(evento[0])}', background='#E0E0E0', font=BFONT, width= 7, justify='center', height=height_text(wrap_text(evento[-1], 50, (WIDTH -10)))).pack(side='left', anchor='w', ipadx=2)
            Label(container, text=wrap_text(evento[-1], 50, (WIDTH - 10)), background='#F3F3F3', font=FONT, width=WIDTH, anchor='w', justify='left',height=height_text(wrap_text(evento[-1], 50, (WIDTH - 10)))).pack(side='left', anchor='w')
            container.pack(side='top', anchor='w',pady=1)
        eventos_genericos.pack(side='top', anchor='w')

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
    
    eventos_frame.pack(side='left', anchor='w')
    if lista_genericos is not None and len(lista_genericos) or lista_sem_funcionamento is not None and len(lista_sem_funcionamento):
        canvas.pack(side='left',fill = 'both', expand=True, anchor='w')
        scrollbar.pack(side='right', fill='y')

root = Tk()
root.title('Calendário')
root.wm_geometry(f'+{root.winfo_screenmmwidth()//2 + root.winfo_width()//2}+{root.winfo_screenmmheight()//2 + root.winfo_height()//2}')
root.configure(height=255)
root.resizable(False, False)
root.config(background=BACKGROUND)

mes_calendario = date.today().month
ano_calendario = date.today().year
data = StringVar()
data.set(f'{meses_por_indice[mes_calendario]} {ano_calendario}')
lista_genericos = []
lista_sem_funcionamento = []

frame_mestre = Frame(root, background=BACKGROUND)
eventos_frame = Frame(root, background=BACKGROUND)
add_remover_deck = ttk.Frame(frame_mestre)
calendario_frame = Frame(frame_mestre, background=BACKGROUND)
top_frame = Frame(frame_mestre, background=HBACKGROUND)
btn_frame = Frame(top_frame, background=HBACKGROUND)
header_container = Frame(top_frame, background=HBACKGROUND)

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

add_remover_deck.pack(side='bottom', anchor='center')
btn_frame.pack(side='top')
top_frame.pack(side='top')
calendario_frame.pack(side='top', anchor='center',fill='none', expand=True)
frame_mestre.pack(side='left', anchor='n')

atualizar_calendario(ano_calendario, mes_calendario)
estilizar()
root.mainloop()