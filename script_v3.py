# -*- coding: utf–8 -*-
import os
import re
import random
import time

from fpdf import FPDF
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter import messagebox

from PIL import ImageGrab, ImageEnhance


class Main(Tk):

    def __init__(self):
        super().__init__()

        self.arial = 'Arial'
        self.font16 = 'Arial 16 bold'
        self.font13 = 'Arial 13 bold'
        self.font10 = 'Arial 10 bold'
        self.font8 = 'Arial 8 bold'
        # main color scheme
        self.majorcolor = "#0e00a3"
        self.minorcolor = "#060080"
        self.rightframecolor = "white"
        # button colors
        self.buttonfgcolor = "black"
        self.buttoncolor = "#cfcfcf"
        self.activebuttoncolor = "#ffffff"
        # label colors
        self.labelfgcolor = "white"
        self.approvecolor = "#14cc00"
        self.deniedcolor = "red"
        self.waitcolor = "#ffe600"
        #entry colors
        self.disabledentrycolor = "#242424"
        self.cellcolor = "#91bbff"
        self.fixedcellcolor = "#57ff47"

        self.eng_alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
                             'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        self.ENG_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.rus_alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 
                             'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 
                             'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ы', 'ъ', 'э', 'ю', 'я']
        self.RUS_alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 
                             'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 
                             'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ы', 'Ъ', 'Э', 'Ю', 'Я', '_']
        self.tatar_extension = {'1': 'Ә',  '2': 'Җ',  '3': 'Ң', '4': 'Ө',  '5': 'Ү',  '6': 'Һ'}
        self.digits = [str(i) for i in range(10)]
        self.global_alphabet = (self.eng_alphabet + self.ENG_alphabet + self.rus_alphabet + 
                                    self.RUS_alphabet + self.digits)

        self.char_check = (self.register(self.char_valid), "%P")

        # Стили виджетов ttk
        buttonstyle = ttk.Style()
        buttonstyle.theme_use('alt')
        buttonstyle.configure("TButton", background=self.buttoncolor, color=self.buttoncolor, relief='solid',
                              foreground=self.buttonfgcolor, focusthickness=0, focuscolor='none', 
                                font=self.font13, justify="center")
        buttonstyle.map('TButton', background=[('active', self.activebuttoncolor)])

        infolabel = ttk.Style()
        infolabel.configure("infolabel.TLabel", foreground=self.labelfgcolor, 
                                    background=self.minorcolor, font=self.font10, padding=[0, 0])
        notificationlabel = ttk.Style()
        notificationlabel.configure("notificationlabel.TLabel", 
                                    background=self.minorcolor, font=self.font13,
                                    padding=[0, 0], anchor=TOP)
        
        # Левая и правая части интерфейса
        self.leftframe = Frame(self, bg=self.majorcolor)
        self.leftframe.grid(row=0, column=0, sticky="nsew")
        self.rightframe = Frame(self, bg=self.rightframecolor)
        self.rightframe.grid(row=0, column=1, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Наполнение левой части
        self.opendirectorybutton = ttk.Button(self.leftframe, text='Выбрать папку\nсо словарями (txt)', 
                                              width=22, command=self.open_directory)
        self.opendirectorybutton.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")
        
        self.dictlistbox = Listbox(self.leftframe, border=3, selectmode=MULTIPLE, height=5, font=self.font10)
        self.dictlistbox.grid(row=1, column=0, columnspan=4, pady=0, padx=10, ipadx=5, ipady=5, sticky="nsew")

        self.infolabel = ttk.Label(self.leftframe, style="infolabel.TLabel", text=2*'\n')
        self.infolabel.grid(row=2, column=0, columnspan=4, pady=0, padx=10, sticky="nsew")

        self.selectdictbutton = ttk.Button(self.leftframe, text='Загрузить словари',
                                    command=lambda: self.notifiationlabel.config(
                                        text='Директория со\nсловарями не выбрана!', 
                                    style="notificationlabel.TLabel", foreground='red'))
        self.selectdictbutton.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        self.notifiationlabel = ttk.Label(self.leftframe, style="notificationlabel.TLabel", text=1*'\n')
        self.notifiationlabel.grid(row=4, column=0, columnspan=4, pady=0, padx=10, sticky="nsew")
        
        self.hintlabel = ttk.Label(self.leftframe, font=self.font8, foreground="yellow", 
                                background=self.majorcolor, text="1: Ә     2: Җ     3: Ң     4: Ө     5: Ү     6: Һ\n")
        self.hintlabel.grid(row=5, column=0, columnspan=4, pady=0, padx=10, sticky="nsew")

        self.sizelabel = ttk.Label(self.leftframe, style="infolabel.TLabel", 
                                   background=self.majorcolor, text='Размер сетки:')
        self.sizelabel.grid(row=6, column=0, columnspan=4, pady=0, padx=10, sticky="w")

        # Первое поле для ввода
        self.entry1 = Entry(self.leftframe, justify=CENTER, width=10)
        self.entry1.grid(row=7, column=0, padx=5, sticky="e")
        self.entry1.insert(0, 'Ширина')
        self.entry1.configure(state='normal', fg="#b8b8b8")
        self.entrybind1_in = self.entry1.bind('<Button-1>', lambda x: self.on_focus_in(self.entry1))
        self.entrybind1_out = self.entry1.bind(
            '<FocusOut>', lambda x: self.on_focus_out(self.entry1, 'Ширина'))

        self.minilabel = ttk.Label(self.leftframe, background=self.majorcolor, 
                                   foreground=self.labelfgcolor, text='X')
        self.minilabel.grid(row=7, column=1)
        # Второе поле для ввода
        self.entry2 = Entry(self.leftframe, justify=CENTER, width=10)
        self.entry2.grid(row=7, column=2, padx=5, sticky="w")
        self.entry2.insert(0, 'Высота')
        self.entry2.configure(state='normal', fg="#b8b8b8")
        self.entrybind2_in = self.entry2.bind('<Button-1>', lambda x: self.on_focus_in(self.entry2))
        self.entrybind2_out = self.entry2.bind(
            '<FocusOut>', lambda x: self.on_focus_out(self.entry2, 'Высота'))
        self.leftframe.grid_columnconfigure(0, weight=3)
        self.leftframe.grid_columnconfigure(2, weight=3)

        self.check = False
        self.checkbutton = Checkbutton(self.leftframe, bg=self.majorcolor, text='⮁', fg="white",
                        font=self.font13, activebackground=self.majorcolor, command=self.check_change)
        self.checkbutton.grid(row=7, column=3, pady=0, padx=0, sticky='nsew')

        self.gridbutton = ttk.Button(self.leftframe, text='Построить сетку', 
                        command= lambda: self.make_crossword_grid(self.entry1.get(), self.entry2.get()))
        self.gridbutton.grid(row=8, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")

        self.iterationlabel = ttk.Label(self.leftframe, style="infolabel.TLabel", 
                                   background=self.majorcolor, text='Кол-во итераций:')
        self.iterationlabel.grid(row=9, column=0, columnspan=3, pady=0, padx=10, sticky="w")

        self.entry3 = Entry(self.leftframe, justify=CENTER, width=8)
        self.entry3.grid(row=9, column=2, pady=5, padx=10, columnspan=2)
        self.entry3.insert(0, 'def 1000')
        self.entry3.configure(state='normal', fg="#b8b8b8")
        self.entrybind3_in = self.entry3.bind('<Button-1>', lambda x: self.on_focus_in(self.entry3))
        self.entrybind3_out = self.entry3.bind(
            '<FocusOut>', lambda x: self.on_focus_out(self.entry3, 'def 1000'))

        self.generatorbutton = ttk.Button(self.leftframe, text='Сгенерировать\nкроссворд', 
                                command=lambda: self.notifiationlabel.config(
                                    text='Словарь не загружен\nили не построена сетка', 
                                style="notificationlabel.TLabel", foreground='red'))
        self.generatorbutton.grid(row=11, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")
        # self.leftframe.grid_rowconfigure(8, weight=1)

        self.savebutton = ttk.Button(self.leftframe, text='Сохранить в\nPDF-файл', 
                        command=lambda: self.notifiationlabel.config(
                        text='Сетка отсутствует\nили она пуста', foreground='red'))
        self.savebutton.grid(row=12, column=0, columnspan=4, pady=10, padx=10, sticky="nsew")
        # self.leftframe.grid_rowconfigure(9, weight=1)


        # Наполнение правой части
        self.crosswordframe = Frame(self.rightframe)
        self.crosswordframe.grid(row=0, column=0, padx=10, pady=10)
        self.rightframe.grid_rowconfigure(0, weight=1)
        self.rightframe.grid_columnconfigure(0, weight=1)
        

    # === СЛУЖЕБНЫЕ ФУНКЦИИ И ОБРАБОТЧИКИ СОБЫТИЙ =======================================
    # функции оформления entry 1/2
    def on_focus_in(self, entry):
        if entry.cget('state') == 'normal':
            entry.configure(state='normal', fg="black")
            entry.delete(0, 'end')
    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(state='normal', fg="#b8b8b8")
    # функция валидации и ограничения ввода
    def char_valid(self, newval):
        return re.match(u"^\w{0,1}$" , newval, re.UNICODE) is not None # "^\w{0,1}$"
    # функция смены полярности сетки
    def check_change(self):
        if self.check: 
            self.check = False
            self.checkbutton.config(fg="white")
        else: 
            self.check = True
            self.checkbutton.config(fg="red")
        self.make_crossword_grid(self.entry1.get(), self.entry2.get())
    # функция выбора ячеек
    def cell_picker(self, event, entry, i, j):
        if self.check == False:
            if self.enabledcell[i][j] == '0':
                entry.config(state=NORMAL, validate="key", fg='black', bg=self.cellcolor, 
                            validatecommand=self.char_check)
                self.enabledcell[i][j] = '1'
            else:
                entry.delete(0, END)
                entry.config(state=DISABLED, fg='black',
                            validate=None, validatecommand=None)
                self.enabledcell[i][j] = '0'
        else:
            if self.enabledcell[i][j] != '0':
                entry.delete(0, END)
                entry.config(state=DISABLED, fg='black',
                            validate=None, validatecommand=None)
                self.enabledcell[i][j] = '0'
            else:
                entry.config(state=NORMAL, validate="key", fg='black', bg=self.cellcolor, 
                            validatecommand=self.char_check)
                self.enabledcell[i][j] = '1'
    # функция фиксации ячеек, заполненных вручную
    def fixing_cell(self, event, entry, i, j):
        if event.char in self.global_alphabet:
            entry.delete(0, END)
            if event.char in self.tatar_extension:
                entry.insert(0, self.tatar_extension[event.char].upper())
            else:
                entry.insert(0, event.char.upper())
            entry.config(validate="key", fg='black', bg=self.fixedcellcolor, 
                        validatecommand=self.char_check)
    # функция расфиксации ячеек, заполненных вручную
    def unfixing_cell(self, event, entry, i, j):
        if self.grid[i][j]['bg'] == self.fixedcellcolor:
            entry.delete(0, END)
            entry.config(state=NORMAL, validate="key", fg='black', bg=self.cellcolor, 
                         validatecommand=self.char_check)
            self.enabledcell[i][j] = '1'


    # === ОСНОВНЫЕ ФУНКЦИИ ПРИЛОЖЕНИЯ ==================================================================
    # функция открытия директории
    def open_directory(self):
        try:
            # выбор и открытие папки
            # self.folderpath = fd.askdirectory()
            self.folderpath = 'c:/.My/Freelance/CrosswordArchitect'
            self.notifiationlabel.config(text=1*'\n', 
                            style="notificationlabel.TLabel", foreground='red')
            # Чтение данных и сохранение в массивы
            self.dictdir = os.listdir(self.folderpath)
            self.txts = []
            self.dictlistbox.delete(0, END)
            for filename in self.dictdir:
                if filename.endswith('.txt'):
                    self.dictlistbox.insert(END, '- '+filename)
                    self.txts.append(f'{self.folderpath}/{filename}')
            
                self.selectdictbutton.config(command=self.make_dictionary)

        except FileNotFoundError:
            self.selectdictbutton.config(command=None)
            self.notifiationlabel.config(text='Директория не выбрана\n', 
                            style="notificationlabel.TLabel", foreground='red')
    
    # функция загрузки слов из выбранных файлов в память и формирования словаря
    def make_dictionary(self):
        self.dictionary = {}
        self.wordsarray = []
        self.selected = self.dictlistbox.curselection()
        if len(self.selected) != 0:
            for fileindex in self.selected:
                with open(self.txts[fileindex], 'r', encoding='utf-8') as file:
                    for word in file:
                        word = word.replace('\n', '')
                        word = word.replace(' ', '-')
                        word = word.upper()
                        # проверка на наличие нежеланных символов (' ', '-')
                        if '-' in word:
                            splitedwords = word.split('-')
                        else:
                            splitedwords = [word]
                        for sw in splitedwords:
                            if sw != '' and sw != ' ' and len(sw)>1 and sw not in self.wordsarray:
                                l = len(sw)
                                self.wordsarray.append(sw)
                                if l not in self.dictionary.keys():
                                    self.dictionary[l] = []
                                temp = self.dictionary[l]
                                temp.append(sw)
                                self.dictionary[l] = temp
            print(self.dictionary.keys())
            #print(self.dictionary.keys())
            self.shortest = min(self.dictionary.keys())
            self.longest = max(self.dictionary.keys())
            
            try:
                if self.w > 0:
                    self.generatorbutton.config(command=self.generator)
            except:
                pass
            finally:
                self.notifiationlabel.config(text='Словарь загружен\n', 
                                style="notificationlabel.TLabel", foreground=self.approvecolor)
        else:
            self.shortest = '-'
            self.longest = '-'
            self.infolabel.config(text=2*'\n')  
            self.notifiationlabel.config(text='Словари не выбраны\n', 
                            style="notificationlabel.TLabel", foreground='red')
        
        self.infolabel.config(text=f' Общее кол-во слов: {len(self.wordsarray)}\n Мин. длина слова: {self.shortest}\n Макс. длина слова: {self.longest}')
    
    # функция создания сетки
    def make_crossword_grid(self, w, h):
        if w.isdigit() and h.isdigit():
            try:
                for widget in self.crosswordframe.winfo_children():
                    widget.destroy()
            finally:
                self.w = int(w)
                self.h = int(h)
                self.grid = []
                self.enabledcell = []
                #self.crosswordframe.config(width=self.w*2, height=self.h*5)
                fontcoeff = round( 400/max([self.w, self.h]) )
                
                for i in range(self.h):
                    self.grid.append([])
                    self.enabledcell.append([])
                    for j in range(self.w):
                        if not self.check:
                            tempobj = Entry(self.crosswordframe, justify=CENTER, font=f'{self.arial} {fontcoeff} bold', 
                                        relief='solid', width=2, state=NORMAL, validate="key", bg=self.cellcolor, 
                                        validatecommand=self.char_check, disabledbackground=self.disabledentrycolor)
                            self.enabledcell[i].append('1')
                        else:
                            tempobj = Entry(self.crosswordframe, justify=CENTER, font=f'{self.arial} {fontcoeff} bold', 
                                        relief='solid', width=2, state=DISABLED, validate=None, 
                                        validatecommand=None, disabledbackground=self.disabledentrycolor) 
                            self.enabledcell[i].append('0')
                        tempobj.grid(row=i, column=j, sticky="nsew")
                        self.grid[i].append(tempobj)
                        self.grid[i][j].insert(0, '')
                        self.grid[i][j].bind('<Button-3>', lambda x, entry=self.grid[i][j], i=i, j=j: self.cell_picker(x, entry, i, j))
                        self.grid[i][j].bind('<Key>', lambda x, entry=self.grid[i][j], i=i, j=j: self.fixing_cell(x, entry, i, j))
                        self.grid[i][j].bind('<BackSpace>', lambda x, entry=self.grid[i][j], i=i, j=j: self.unfixing_cell(x, entry, i, j))
                        self.grid[i][j].bind('<Delete>', lambda x, entry=self.grid[i][j], i=i, j=j: self.unfixing_cell(x, entry, i, j))
                        self.crosswordframe.grid_rowconfigure(i, weight=1)
                        self.crosswordframe.grid_columnconfigure(j, weight=1)
                self.notifiationlabel.config(text='\n',
                                style="notificationlabel.TLabel", foreground='red')
                try:
                    if len(self.dictionary) != 0:
                        self.generatorbutton.config(command=self.generator)
                except:
                    self.notifiationlabel.config(text='Словарь не загружен!\n',
                                    style="notificationlabel.TLabel", foreground='red')
        else:
            self.notifiationlabel.config(text='Укажите размер сетки\n', 
                            style="notificationlabel.TLabel", foreground='red')
            self.generatorbutton.config(command=None)
    
    # функция очистки сетки от букв
    def clear_grid(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.enabledcell[x][y] != '0':
                    if self.grid[x][y]['bg'] != self.fixedcellcolor:
                        self.grid[x][y].delete(0, END)
    
    # функция очистки enabledcell
    def clear_enabledcell_list(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.enabledcell[x][y] != '0':
                    self.enabledcell[x][y] = '1'

    # функция настройки паддингов для enabledcell
    def set_paddings(self, mode):
        if mode == 'set':
            # добавление паддингов
            self.enabledcell.insert(0, ['0' for i in range(self.w)])
            for x in range(self.h+1):
                self.enabledcell[x].insert(0, '0')
                self.enabledcell[x].append('0')
            self.enabledcell.append(['0' for i in range(self.w+2)])
        if mode == 'del':
            # удаление паддингов
            self.enabledcell.pop(0)
            for x in range(self.h+1):
                self.enabledcell[x].pop(0)
                self.enabledcell[x].pop()
            self.enabledcell.pop()
    
    # опциональная функция вывода результатов анализа сетки
    def show_analize_results(self, turn='on'):
        """turn: on/off (default "on")"""
        if turn == 'on':
            print('\n=== Результат анализа сетки ===')        
            for x in range(len(self.enabledcell)):
                for y in range(len(self.enabledcell[x])):
                    print(self.enabledcell[x][y].center(2), end=' ')
                print()
            try:
                print('h_words:', self.h_params)
                print('v_words:', self.v_params)
            except AttributeError:
                pass
            print('=== ======================= ===')

    # функция анализа сетки
    def analize_grid(self):
        """
        Aнализ 0 | 1 -> E, H, V, VH, vH, Vh, h, v, +
        Horizontal: H VH vH Vh h +
        Vertical: V VH vH Vh v +
        Other: E
        """
        self.h_params = []
        self.v_params = []
        self.fixed_words = []
        self.max_length = 0
        self.h_signs = ('1', 'h', 'H', 'VH', 'Vh', 'vH', '+')
        self.v_signs = ('1', 'v', 'V', 'VH', 'Vh', 'vH', '+')
        # горизонталь
        for x in range(1, len(self.enabledcell)-1):
            l = 0
            intersection = 0
            status = "c"
            for y in range(1, len(self.enabledcell[x])-1):
                if self.enabledcell[x][y] in self.h_signs:
                    upper = self.enabledcell[x-1][y]
                    lower = self.enabledcell[x+1][y]
                    left = self.enabledcell[x][y-1]
                    right = self.enabledcell[x][y+1]

                    # Empty 
                    if upper == '0' and lower == '0' and right == '0' and left == '0':
                        self.enabledcell[x][y] = 'E'
                    if left == '0'  and right in self.h_signs:
                        # Начало горизонтального
                        if upper == '0' and lower == '0':
                            self.enabledcell[x][y] = 'H'
                        # Начало горизонтального и вертикального Г
                        if upper == '0' and lower in self.v_signs:
                            self.enabledcell[x][y] = 'VH'
                            intersection += 1
                        # Начало горизонтального из буквы вертикального |-
                        if upper in self.v_signs:
                            self.enabledcell[x][y] = 'vH'
                            intersection += 1
                        self.h_params.append([])
                        self.h_params[-1].append(x-1)
                        self.h_params[-1].append(y-1)
                        l += 1
                    if left in self.h_signs:
                        # Начало вертикального из буквы горизонтального T
                        if upper == '0' and lower in self.v_signs:
                            self.enabledcell[x][y] = 'Vh'
                            intersection += 1
                            
                        # Продолжение горизонтального --
                        if upper == '0' and lower == '0':
                            self.enabledcell[x][y] = 'h'
                            if self.grid[x-1][y-1]['bg'] == self.fixedcellcolor:
                                status = "f"
                        # Пересечение слов в любом месте
                        if upper in self.v_signs:
                            self.enabledcell[x][y] = '+'
                            intersection += 1
                        l += 1
                        if right == '0':
                            self.h_params[-1].append(intersection)
                            self.h_params[-1].append(l)
                            self.h_params[-1].append('h')
                            self.h_params[-1].append(status)
                            if self.max_length < l:
                                self.max_length = l
                            l = 0
                            intersection = 0

        # вертикаль
        for y in range(1, len(self.enabledcell[0])-1):
            l = 0
            intersection = 0
            status = "c"
            for x in range(1, len(self.enabledcell)-1):
                if self.enabledcell[x][y] in self.v_signs:
                    upper = self.enabledcell[x-1][y]
                    lower = self.enabledcell[x+1][y]
                    left = self.enabledcell[x][y-1]
                    right = self.enabledcell[x][y+1]
                    
                    if upper == '0' and lower in self.v_signs:
                        # Начало вертикального
                        if right == '0' and left == '0':
                            self.enabledcell[x][y] = 'V'
                        # Начало горизонтального и вертикального Г
                        if right in self.h_signs and left == '0':
                            self.enabledcell[x][y] = 'VH'
                            intersection += 1
                        # Начало вертикального из буквы горизонтального T
                        if left in self.h_signs:
                            self.enabledcell[x][y] = 'Vh'
                            intersection += 1
                        self.v_params.append([])
                        self.v_params[-1].append(x-1)
                        self.v_params[-1].append(y-1)
                        l += 1
                    if upper in self.v_signs:
                        # Начало горизонтального из буквы вертикального |-
                        if right in self.h_signs and left == '0':
                            self.enabledcell[x][y] = 'vH'
                            intersection += 1
                        # Продолжение вертикального |
                        if right == '0' and left == '0':
                            self.enabledcell[x][y] = 'v'
                            if self.grid[x-1][y-1]['bg'] == self.fixedcellcolor:
                                status = "f"
                        # Пересечение слов в любом месте
                        if left in self.h_signs:
                            self.enabledcell[x][y] = '+'
                            intersection += 1
                        l += 1
                        if lower == '0':
                            self.v_params[-1].append(intersection)
                            self.v_params[-1].append(l)
                            self.v_params[-1].append('v')
                            self.v_params[-1].append(status)
                            if self.max_length < l:
                                self.max_length = l
                            l = 0
                            intersection = 0

    # функция установки ограничения на итерации
    def set_interation_limit(self, limit):
        if limit.isdigit():
            limit = int(limit)
            if limit < 0:
                return 1
            elif limit > 10000:
                return 10000
            else:
                return limit
        else:
            return 1000
    
    # функция настройки конфигов сетки
    def set_config(self, X, Y, length, position):
        for l in range(length):
            if position in ('h','H') and self.enabledcell[X][Y+l] in self.h_signs:
                if self.grid[X][Y+l]['bg'] != self.fixedcellcolor:
                    self.grid[X][Y+l].config(bg=self.deniedcolor)
            if position in ('v','V') and self.enabledcell[X+l][Y] in self.v_signs: 
                if self.grid[X+l][Y]['bg'] != self.fixedcellcolor:
                    self.grid[X+l][Y].config(bg=self.deniedcolor)

    # функция показа уведомления о завершении
    def show_messagebox(self, finish, best):
        self.notifiationlabel.config(text='\n')
        if self.min_empty_count == 0:
            messagebox.showinfo(title="Кроссворд успешно сгенерирован!", 
                message=f'Проведено итераций — {self.iteration-1}/{self.iteration_limit} '
                        f'({int(finish//60)} мин {round(finish%60, 1)} сек)\n'
                        f'Всего слов — {len(self.h_words+self.v_words)} '
                        f'({len(self.h_words)} горизонтальных, {len(self.v_words)} вертикальных)')
        else:
            answer = messagebox.askokcancel(title="Кроссворд не был заполнен :(", 
                message=f'Проведено итераций — {self.iteration-1}/{self.iteration_limit} '
                        f'({int(finish//60)} мин {round(finish%60, 1)} сек)\n'
                        f'Наилучших попыток {best} '
                        f'с количеством пропусков — {self.min_empty_count} слов\n\n'
                        f'Желаете попробовать снова? (OK)')
            if answer:
                self.generator()
    
    # функция добавления полученных слов в массивы
    def word_adding(self, word, position, status='c'):
        if status == 'c':
            if position in ('h','H'):
                self.h_words.append(word)
            if position in ('v','V'):
                self.v_words.append(word)
        else:
            if position in ('h','H'):
                self.h_words.append(word+' (f)')
            if position in ('v','V'):
                self.v_words.append(word+' (f)')
        
    # функция подбора слов и заполнения сетки
    def word_randomizer(self, X, Y, length, position, status):
        if status == "c":
            pattern = ''
            words_with_fixed_len = '\n'.join(self.dictionary[length])
            for l in range(length):
                if position in ('h','H'):
                    char = self.grid[X][Y+l].get()
                    if char == '':
                        pattern += '.'
                    else:
                        pattern += char
                if position in ('v','V'):
                    char = self.grid[X+l][Y].get()
                    if char == '':
                        pattern += '.'
                    else:
                        pattern += char
            pattern = re.compile(pattern)
            result = pattern.findall(words_with_fixed_len)
            try:
                # генерация слова с учетом неправильных начальных букв (Ъ, Ь)
                is_not_okay = True
                while is_not_okay:
                    is_not_okay = False
                    word = result[random.randint(0, len(result)-1)]
                    if word in (self.h_words + self.v_words):
                        if len(self.h_words + self.v_words) > 1:
                            continue
                        else:
                            is_not_okay = True
                            continue
                    if 'ь' in word or 'ъ' in word:
                        if position in ('h','H'):
                            for l in range(length):
                                if word[l] in self.wrong_letters and self.enabledcell[X][Y+l] == 'Vh':
                                    is_not_okay = True
                                    break
                        if position in ('v','V'):
                            for l in range(length):
                                if word[l] in self.wrong_letters and self.enabledcell[X+l][Y] == 'vH':
                                    is_not_okay = True
                                    break
                # побуквенная вставка в сетку
                for l in range(length):
                    if position in ('h','H'):
                        self.grid[X][Y+l].insert(0, word[l])
                    if position in ('v','V'):
                        self.grid[X+l][Y].insert(0, word[l])
                # добавление слов в H/V списки
                self.word_adding(word, position)
                #print('len', length, pattern, word, position)
            except:
                self.stop = False
                self.empty += 1
                if self.iteration == self.iteration_limit:
                    self.set_config(X, Y, length, position)
        # обработка фиксированных слов
        else:
            word = ''
            for l in range(length):
                if position in ('h','H'):
                    word = word + self.grid[X][Y+l].get()
                if position in ('v','V'):
                    word = word + self.grid[X+l][Y].get()
            self.word_adding(word, position, status)
            

    # основная функция генерации кроссворда
    def generator(self):
        self.notifiationlabel.config(text='Ожидание...\n', foreground=self.waitcolor)
        self.clear_enabledcell_list()

        # анализ сетки
        self.show_analize_results(turn='off') # on/off
        self.set_paddings('set')
        self.analize_grid()
        self.set_paddings('del')
        self.show_analize_results(turn='on') # on/off

        # сортировка
        self.sum_params = self.h_params + self.v_params
        self.sum_params.sort(key = lambda x: x[3], reverse=True) # по длина
        self.sum_params.sort(key = lambda x: x[2], reverse=True) # по кол-ву пересечений

        # настройка количества итераций
        self.iteration = 1
        self.stop = False
        self.iteration_limit = self.set_interation_limit(self.entry3.get())
        for x in range(len(self.enabledcell)):
            for y in range(len(self.enabledcell[x])):
                if self.enabledcell[x][y] in (self.h_signs + self.v_signs):
                    if self.grid[x][y]['bg'] != self.fixedcellcolor:
                        self.grid[x][y].config(bg=self.cellcolor)
        
        # алгоритм генерации и заполнения слов
        start_time = time.time()
        self.min_empty_count = 10
        best_iteration_count = 0
        self.wrong_letters = ('ь', 'ъ')
        if self.max_length <= self.longest:
            while not self.stop and self.iteration <= self.iteration_limit:
                self.clear_grid()
                self.h_words = []
                self.v_words = []
                self.empty = 0
                self.stop = True
                #print(f'=== Итерация #{self.iteration} ===')
                for word in (self.sum_params):
                    self.word_randomizer(word[0], word[1], word[3], word[4], word[5])
                if self.empty <= self.min_empty_count:
                    if self.min_empty_count == self.empty:
                        best_iteration_count += 1
                    else:
                        best_iteration_count = 1
                        self.min_empty_count = self.empty
                self.iteration += 1
            self.show_messagebox(time.time()-start_time, best_iteration_count)
            print(f'\nhorizontal {self.h_words}')
            print(f'vertical {self.v_words}')
            self.savebutton.config(command=self.save_in_file)
        else:
            self.h_words = []
            self.v_words = []
            self.notifiationlabel.config(
                                text='В словаре отсутствуют\nслова такой длины!', 
                                foreground=self.deniedcolor)

    # функция сохранения в pdf файл
    def save_in_file(self):
        self.wm_geometry("+%d+%d" % (100, 50))

        self.savefolderpath = fd.askdirectory()

        x1 = self.winfo_x() + self.rightframe.winfo_x() + self.crosswordframe.winfo_x() + 4
        y1 = self.winfo_y() + self.rightframe.winfo_y() + self.crosswordframe.winfo_y() + 27
        x2 = x1 + self.crosswordframe.winfo_width() + 8
        y2 = y1 + self.crosswordframe.winfo_height() + 9

        snapshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        enhancer = ImageEnhance.Sharpness(snapshot)
        snapshot_enhanced = enhancer.enhance(2)
        koefw = 567/snapshot_enhanced.size[0]
        koefh = 500/snapshot_enhanced.size[1]
        if koefw < koefh:
            new_size = (round(snapshot_enhanced.size[0]*koefw), 
                        round(snapshot_enhanced.size[1]*koefw))
        else:
            new_size = (round(snapshot_enhanced.size[0]*koefh), 
                        round(snapshot_enhanced.size[1]*koefh))
        snapshot_enhanced = snapshot_enhanced.resize(new_size)
        tempscreenpath = f'{self.savefolderpath}/tempscreen.png'
        snapshot_enhanced.save(tempscreenpath)

        pdf = FPDF()
        pdf.add_page()
        #pdf.set_doc_option('windows-1252')
        pdf.image(tempscreenpath, x=5, y=5)
        # line
        pdf.set_draw_color(255, 0, 0)
        pdf.set_line_width(1)
        pdf.line(10, 185, 200, 185)

        pdf.set_font("Arial", 'B', size=16, uni=True)
        pdf.cell(0, 175, txt="", ln=1)
        pdf.set_text_color(0, 15, 181)
        pdf.cell(70, 10, txt="Horizontal", ln=0, align="L")
        pdf.cell(20)
        pdf.cell(70, 10, txt="Vertical", ln=1, align="L")

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", size=12)
        longer = max((len(self.h_words), len(self.v_words)))
        for i in range(longer):
            try:
                pdf.cell(70, 5, txt="{}".format(i+1), ln=0, align="L")
            except: pass
            pdf.cell(20)
            try:
                pdf.cell(70, 5, txt="{}".format(i+1), ln=1, align="L")
            except: pass

        counter = 1
        while counter < 100:
            file_name = f'{self.w}x{self.h}_crossword_[{len(self.h_words)}h, {len(self.v_words)}v]_{counter}.pdf'
            if not os.path.exists(f'{self.savefolderpath}/{file_name}'):
                pdf.output(f'{self.savefolderpath}/{file_name}')
                os.remove(tempscreenpath)
                break
            else:
                counter += 1



if __name__ == "__main__":
    main = Main()
    main.geometry(f'{860}x{620}') # main.winfo_screenheight()
    main.wm_geometry("+%d+%d" % (50, 10))
    main.title('CSV Convolution')
    main['bg'] = 'white'
    #main.attributes('-fullscreen', True)


    main.mainloop()

    # pyinstaller -F -w -i 'ico.png' script.py