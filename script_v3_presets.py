# -*- coding: utf–8 -*-
import os
import re
import random

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from sys import getdefaultencoding

from PIL import ImageGrab, ImageEnhance



class Main(Tk):

    def __init__(self):
        super().__init__()

        getdefaultencoding()
        self.arial = 'Arial'
        self.font16 = 'Arial 16 bold'
        self.font13 = 'Arial 13 bold'
        self.font10 = 'Arial 10 bold'
        self.font8 = 'Arial 8 bold'
        # main color scheme
        self.majorcolor = "#0e00a3"
        self.minorcolor = "#060080"
        self.rightframecolor = "#d9d9d9"
        # button colors
        self.buttonfgcolor = "black"
        self.buttoncolor = "#cfcfcf"
        self.activebuttoncolor = "#ffffff"
        # label colors
        self.labelfgcolor = "white"
        self.approvecolor = "#14cc00"
        self.deniedcolor = "red"
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
        self.opendirectorybutton = ttk.Button(self.leftframe, text='Выбрать рабочую\nпапку с txt-файлами', 
                                              width=22, command=self.open_dictionary_directory)
        self.opendirectorybutton.grid(row=0, column=0, columnspan=4, pady=5, padx=10, sticky="nsew")
        
        self.dictlistbox = Listbox(self.leftframe, border=3, selectmode=MULTIPLE, height=3, font=self.font10)
        self.dictlistbox.grid(row=1, column=0, columnspan=4, pady=5, padx=10, ipadx=5, ipady=5, sticky="nsew")

        self.presetlistbox = Listbox(self.leftframe, border=3, selectmode=SINGLE, height=3, font=self.font10)
        self.presetlistbox.grid(row=2, column=0, columnspan=4, pady=5, padx=10, ipadx=5, ipady=5, sticky="nsew")

        self.infolabel = ttk.Label(self.leftframe, style="infolabel.TLabel", text=2*'\n')
        self.infolabel.grid(row=3, column=0, columnspan=4, pady=5, padx=10, sticky="nsew")

        self.selectdictbutton = ttk.Button(self.leftframe, text='Загрузить словари',
                                    command=lambda: self.notifiationlabel.config(text='Директория со\nсловарями не выбрана!', 
                                    style="notificationlabel.TLabel", foreground='red'))
        self.selectdictbutton.grid(row=4, column=0, columnspan=4, pady=5, padx=10, sticky="nsew")

        self.notifiationlabel = ttk.Label(self.leftframe, style="notificationlabel.TLabel", text=1*'\n')
        self.notifiationlabel.grid(row=5, column=0, columnspan=4, pady=5, padx=10, sticky="nsew")

        self.sizelabel = ttk.Label(self.leftframe, style="infolabel.TLabel", 
                                   background=self.majorcolor, text='Размер сетки')
        self.sizelabel.grid(row=6, column=0, columnspan=2, pady=5, padx=10, sticky="w")

        

        # Первое поле для ввода
        self.entry1 = Entry(self.leftframe, justify=CENTER, width=10)
        self.entry1.grid(row=7, column=0, padx=10, sticky="e")
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
        self.entry2.grid(row=7, column=2, padx=10, sticky="w")
        self.entry2.insert(0, 'Высота')
        self.entry2.configure(state='normal', fg="#b8b8b8")
        self.entrybind2_in = self.entry2.bind('<Button-1>', lambda x: self.on_focus_in(self.entry2))
        self.entrybind2_out = self.entry2.bind(
            '<FocusOut>', lambda x: self.on_focus_out(self.entry2, 'Высота'))
        self.leftframe.grid_columnconfigure(0, weight=3)
        self.leftframe.grid_columnconfigure(2, weight=3)

        self.check = False
        self.checkbutton = Checkbutton(self.leftframe, bg=self.majorcolor,
                                activebackground=self.majorcolor, command=self.check_change)
        self.checkbutton.grid(row=7, column=3, pady=5, padx=10, sticky='nsew')

        self.gridbutton = ttk.Button(self.leftframe, text='Построить сетку', 
                        command= lambda: self.make_crossword_grid(self.entry1.get(), self.entry2.get()))
        self.gridbutton.grid(row=8, column=0, columnspan=4, pady=5, padx=10, sticky="nsew")

        self.presetbutton = ttk.Button(self.leftframe, text='Сохранить пресет', 
                        command= lambda: self.notifiationlabel.config(text='Сетка отсутствует\nили она пуста', 
                                          style="notificationlabel.TLabel", foreground='red'))
        self.presetbutton.grid(row=9, column=0, columnspan=4, pady=5, padx=10, sticky="nsew")

        self.entry3 = Entry(self.leftframe, justify=CENTER, width=25)
        self.entry3.grid(row=10, column=0, padx=10, columnspan=4)
        self.entry3.insert(0, 'Кол-во итераций (def 100)')
        self.entry3.configure(state='normal', fg="#b8b8b8")
        self.entrybind3_in = self.entry3.bind('<Button-1>', lambda x: self.on_focus_in(self.entry3))
        self.entrybind3_out = self.entry3.bind(
            '<FocusOut>', lambda x: self.on_focus_out(self.entry3, 'Кол-во итераций (def 100)'))

        self.generatorbutton = ttk.Button(self.leftframe, text='Сгенерировать\nкроссворд', 
                                          command=lambda: self.notifiationlabel.config(text='Словарь не загружен\nили не построена сетка', 
                                          style="notificationlabel.TLabel", foreground='red'))
        self.generatorbutton.grid(row=11, column=0, columnspan=4, pady=5, padx=10, sticky="nsew")
        # self.leftframe.grid_rowconfigure(8, weight=1)

        self.savebutton = ttk.Button(self.leftframe, text='Сохранить в\nPDF-файл', 
                        command=lambda: self.notifiationlabel.config(
                        text='Сетка отсутствует\nили она пуста', foreground='red'))
        self.savebutton.grid(row=12, column=0, columnspan=4, pady=5, padx=10, sticky="nsew")
        # self.leftframe.grid_rowconfigure(9, weight=1)


        # Наполнение правой части
        self.crosswordframe = Frame(self.rightframe)
        self.crosswordframe.grid(row=0, column=0, padx=10, pady=10)
        self.rightframe.grid_rowconfigure(0, weight=1)
        self.rightframe.grid_columnconfigure(0, weight=1)
        
    # === Служебные функции и обработчики событий =======================================
    
    # entry изменения
    def on_focus_in(self, entry):
        if entry.cget('state') == 'normal':
            entry.configure(state='normal', fg="black")
            entry.delete(0, 'end')
    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(state='normal', fg="#b8b8b8")
    # функция ограничителя ввода
    def char_valid(self, newval):
        return re.match(u"^\w{0,1}$" , newval, re.UNICODE) is not None # "^\w{0,1}$"
    # функция смены полярности сетки
    def check_change(self):
        if self.check: self.check = False 
        else: self.check = True
        # self.make_crossword_grid(self.entry1.get(), self.entry2.get())
    # функция выбора ячеек
    def cell_picker(self, event, entry, i, j):
        if self.enabledcell[i][j] == '0':
            entry.config(state=NORMAL, validate="key", fg='black', bg=self.cellcolor, 
                        validatecommand=self.char_check)
            self.enabledcell[i][j] = '1'
            self.analized_cell[i][j] = '1'
        else:
            entry.delete(0, END)
            entry.config(state=DISABLED, validate=None, validatecommand=None)
            self.enabledcell[i][j] = '0'
            self.analized_cell[i][j] = '0'

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
            self.analized_cell[i][j] = 'F'
    # функция расфиксации ячеек, заполненных вручную
    def unfixing_cell(self, event, entry, i, j):
        if self.analized_cell[i][j] == 'F':
            entry.delete(0, END)
            entry.config(state=NORMAL, validate="key", fg='black', bg=self.cellcolor, 
                         validatecommand=self.char_check)
            self.analized_cell[i][j] = '1'

    # === Основные функции приложения ==================================================
    
    # функция открытия директории
    def open_dictionary_directory(self):
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
    # функция считывания пресетов
    def read_presets(self):
        self.exe_dir = os.path.split(__file__)[0] + '\\'
        self.presets_path = self.exe_dir + 'presets'
        if not os.path.exists(self.presets_path):
            os.mkdir(self.presets_path)

        # Чтение пресетов и сохранение в массивы
        self.presetsdir = os.listdir(self.presets_path)
        self.presettxts = []
        self.presetlistbox.delete(0, END)
        for filename in self.presetsdir:
            if filename.endswith('preset.txt'):
                self.presetlistbox.insert(END, '- '+filename)
                self.presettxts.append(f'{self.presets_path}\\{filename}')
    # функция сохранения пресета
    def save_preset(self):
        counter = 1
        while counter <100:
            try:
                with open(f'{self.presets_path}\\{self.w}x{self.h}_{counter}_preset.txt', 'x') as preset:
                    for x in range(len(self.enabledcell)):
                        for y in range(len(self.enabledcell[x])):
                            if self.enabledcell[x][y] != '0':
                                preset.write('1', )
                            else:
                                preset.write('0')
                        if x != len(self.enabledcell)-1:
                            preset.write('\n')
                break
            except FileExistsError:
                counter += 1
    # выбор пресета
    def preset_selection(self):
        try:
            ps = self.presetlistbox.curselection()[0]
            with open(self.presettxts[ps], 'r') as preset:
                matrix = []
                file = preset.readlines()
                h = len(file)
                for row in range(h):
                    matrix.append([])
                    file[row] = file[row].replace('\n', '')
                    for char in file[row]:
                        matrix[row].append(char)
                w = len(matrix[0])
            return w, h, matrix
        except:
            pass
    # функция загрузки слов из выбранных файлов в память и формирования словаря
    def make_dictionary(self):
        self.read_presets()
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
        presetparams = self.preset_selection()
        try:
            for widget in self.crosswordframe.winfo_children():
                widget.destroy()
            self.presetlistbox.selection_clear(self.presetlistbox.curselection()[0])
        except: pass

        if (presetparams is not None) or (w.isnumeric() and h.isnumeric()):
            if w.isnumeric() and h.isnumeric():
                self.w = int(w)
                self.h = int(h)
                if not self.check:
                    self.enabledcell = [['1']*self.w]*self.h
                    self.analized_cell = [['1']*self.w]*self.h
                else:
                    self.enabledcell = [['0']*self.w]*self.h
                    self.analized_cell = [['0']*self.w]*self.h
            if presetparams is not None:
                self.w = int(presetparams[0])
                self.h = int(presetparams[1])
                self.enabledcell = presetparams[2]
                self.analized_cell = presetparams[2]

            self.grid = []
            fontcoeff = round(400/max([self.w, self.h]) )
            
            for i in range(self.h):
                self.grid.append([])
                for j in range(self.w):
                    if self.enabledcell[i][j] == '1':
                        tempobj = Entry(self.crosswordframe, justify=CENTER, font=f'{self.arial} {fontcoeff} bold', 
                                    relief='solid', width=2, state=NORMAL, validate="key", bg=self.cellcolor, 
                                    validatecommand=self.char_check, disabledbackground=self.disabledentrycolor)
                    if self.enabledcell[i][j] == '0':
                        tempobj = Entry(self.crosswordframe, justify=CENTER, font=f'{self.arial} {fontcoeff} bold', 
                                    relief='solid', width=2, state=DISABLED, validate=None, 
                                    validatecommand=None, disabledbackground=self.disabledentrycolor) 
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
            self.presetbutton.config(command= self.save_preset)
            # print(f'W: {self.w}, H: {self.h} grid size {len(self.grid[0])}x{len(self.grid)}\n{self.enabledcell}')
            try:
                if len(self.dictionary) != 0:
                    self.generatorbutton.config(command=self.generator)
            except:
                self.notifiationlabel.config(text='Словарь не загружен!\n',
                                style="notificationlabel.TLabel", foreground='red')
        else:
            self.notifiationlabel.config(text='Укажите размер сетки\nили выберете пресет', 
                            style="notificationlabel.TLabel", foreground='red')
            self.generatorbutton.config(command=None)
            #self.enabledcell.clear()
    
    # функция очистки сетки
    def clear_grid(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.enabledcell[x][y] not in ('0', 'F'):
                    self.grid[x][y].delete(0, END)
    
    # функция очистки enabledcell
    def clear_enabledcell_list(self):
        for x in range(0, self.h):
            for y in range(0, self.w):
                if self.analized_cell[x][y] not in ('0', 'F'):
                    self.analized_cell[x][y] = '1'

    # настройка паддингов для analized_cell
    def padding_set(self, mode):
        if mode == 'set':
            # добавление паддингов
            self.analized_cell.insert(0, ['0' for i in range(self.w)])
            for x in range(self.h+1):
                self.analized_cell[x].insert(0, '0')
                self.analized_cell[x].append('0')
            self.analized_cell.append(['0' for i in range(self.w+2)])
        if mode == 'del':
            # удаление паддингов
            self.analized_cell.pop(0)
            for x in range(self.h+1):
                self.analized_cell[x].pop(0)
                self.analized_cell[x].pop()
            self.analized_cell.pop()
        
    
    # вывод результатов анализа сетки
    def analize_results(self, turn='on'):
        """turn: on/off (default "on")"""
        if turn == 'on':
            print('\n=== Результат анализа сетки ===')        
            for x in range(len(self.analized_cell)):
                for y in range(len(self.analized_cell[x])):
                    print(self.analized_cell[x][y].center(2), end=' ')
                print()
            try:
                print('h_words:', self.h_words)
                print('v_words:', self.v_words)
            except AttributeError:
                pass
            print('=== ======================= ===')

    # функция анализа сетки
    def analize_grid(self):
        """
        Aнализ 0 | 1 -> E, H, V, VH, vH, Vh, h, v, +
        Horizontal: H VH vH Vh h +
        Vertical: V VH vH Vh v +
        Other: E F
        """
        self.h_words = []
        self.v_words = []
        self.fixed_words = []
        self.h_signs = ('1', 'h', 'H', 'VH', 'Vh', 'vH', '+', 'F')
        self.v_signs = ('1', 'v', 'V', 'VH', 'Vh', 'vH', '+', 'F')
        # горизонталь
        for x in range(1, len(self.analized_cell)-1):
            length = 0
            intersection = 0
            for y in range(1, len(self.analized_cell[x])-1):
                if self.analized_cell[x][y] in self.h_signs:
                    upper = self.analized_cell[x-1][y]
                    lower = self.analized_cell[x+1][y]
                    left = self.analized_cell[x][y-1]
                    right = self.analized_cell[x][y+1]

                    # Empty 
                    if upper == '0' and lower == '0' and right == '0' and left == '0':
                        self.analized_cell[x][y] = 'E'
                    if left == '0'  and right in self.h_signs:
                        # Начало горизонтального
                        if upper == '0' and lower == '0':
                            self.analized_cell[x][y] = 'H'
                        # Начало горизонтального и вертикального Г
                        if upper == '0' and lower in self.v_signs:
                            self.analized_cell[x][y] = 'VH'
                            intersection += 1
                        # Начало горизонтального из буквы вертикального |-
                        if upper in self.v_signs:
                            self.analized_cell[x][y] = 'vH'
                            intersection += 1
                        self.h_words.append([])
                        self.h_words[-1].append(x-1)
                        self.h_words[-1].append(y-1)
                        length += 1
                    if left in self.h_signs:
                        # Начало вертикального из буквы горизонтального T
                        if upper == '0' and lower in self.v_signs:
                            self.analized_cell[x][y] = 'Vh'
                            intersection += 1
                        # Продолжение горизонтального --
                        if upper == '0' and lower == '0':
                            self.analized_cell[x][y] = 'h'
                        # Пересечение слов в любом месте
                        if upper in self.v_signs:
                            self.analized_cell[x][y] = '+'
                            intersection += 1
                        length += 1
                        if right == '0':
                            self.h_words[-1].append(intersection)
                            self.h_words[-1].append(length)
                            self.h_words[-1].append('h')
                            length = 0

        # вертикаль
        for y in range(1, len(self.analized_cell[0])-1):
            length = 0
            intersection = 0
            for x in range(1, len(self.analized_cell)-1):
                if self.analized_cell[x][y] in self.v_signs:
                    upper = self.analized_cell[x-1][y]
                    lower = self.analized_cell[x+1][y]
                    left = self.analized_cell[x][y-1]
                    right = self.analized_cell[x][y+1]
                    
                    if upper == '0' and lower in self.v_signs:
                        # Начало вертикального
                        if right == '0' and left == '0':
                            self.analized_cell[x][y] = 'V'
                        # Начало горизонтального и вертикального Г
                        if right in self.h_signs and left == '0':
                            self.analized_cell[x][y] = 'VH'
                            intersection += 1
                        # Начало вертикального из буквы горизонтального T
                        if left in self.h_signs:
                            self.analized_cell[x][y] = 'Vh'
                            intersection += 1
                        self.v_words.append([])
                        self.v_words[-1].append(x-1)
                        self.v_words[-1].append(y-1)
                        length += 1
                    if upper in self.v_signs:
                        # Начало горизонтального из буквы вертикального |-
                        if right in self.h_signs and left == '0':
                            self.analized_cell[x][y] = 'vH'
                            intersection += 1
                        # Продолжение вертикального |
                        if right == '0' and left == '0':
                            self.analized_cell[x][y] = 'v'
                        # Пересечение слов в любом месте
                        if left in self.h_signs:
                            self.analized_cell[x][y] = '+'
                            intersection += 1
                        length += 1
                        if lower == '0':
                            self.v_words[-1].append(intersection)
                            self.v_words[-1].append(length)
                            self.v_words[-1].append('v')
                            length = 0

    # установка ограничения на итерации
    def set_interation_limit(self, limit):
        if limit.isnumeric():
            limit = int(limit)
            if limit > 0 and limit <= 10000:
                return limit
            else:
                return 100
        else:
            return 100
    
    # рандомайзер слов и заполнитель сетки
    def word_randomizer(self, X, Y, intersection, length, position, show=True):
        pattern = ''
        words_with_fixed_len = '\n'.join(self.dictionary[length])
        wrong_letters = ('ь', 'ъ')
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
            word = result[random.randint(0, len(result)-1)]
            for l in range(length):
                if position in ('h','H'):
                    self.grid[X][Y+l].insert(0, word[l])
                    if self.analized_cell[X][Y+l] in self.h_signs:
                        self.grid[X][Y+l].config(bg=self.cellcolor)
                    if self.analized_cell[X][Y+l] == 'F':
                        self.grid[X][Y+l].config(bg=self.fixedcellcolor)
                if position in ('v','V'):
                    self.grid[X+l][Y].insert(0, word[l])
                    if self.analized_cell[X+l][Y] in self.v_signs:
                        self.grid[X+l][Y].config(bg=self.cellcolor)
                    if self.analized_cell[X+l][Y] == 'F':
                        self.grid[X+l][Y].config(bg=self.fixedcellcolor)
            if show:
                print('len', length, pattern, word, position)
        except:
            self.stop = False
            self.empty += 1
            for l in range(length):
                if position in ('h','H'):
                    if self.enabledcell[X][Y+l] in self.h_signs:
                        self.grid[X][Y+l].config(bg=self.deniedcolor)
                    if self.enabledcell[X][Y+l] == 'F':
                        self.grid[X][Y+l].config(bg=self.fixedcellcolor)
                if position in ('v','V'):
                    if self.enabledcell[X+l][Y] in self.v_signs:
                        self.grid[X+l][Y].config(bg=self.deniedcolor)
                    if self.enabledcell[X+l][Y] == 'F':
                        self.grid[X+l][Y].config(bg=self.fixedcellcolor)

    # генерация кроссворда
    def generator(self):
        self.notifiationlabel.config(text='\n', foreground=self.deniedcolor)

        #print(f'W: {self.w}, H: {self.h} grid size {len(self.grid[0])}x{len(self.grid)}\n{self.enabledcell}')
        for i in range(len(self.enabledcell)):
            print(self.enabledcell[i])
        print('===')
        for i in range(len(self.analized_cell)):
            print(self.analized_cell[i])

        self.clear_enabledcell_list()
        self.analize_results(turn='off') # on/off
        
        self.padding_set('set')

        self.analize_grid()
        
        self.padding_set('del')
        self.analize_results(turn='off') # on/off
        # сортировка по убыванию длины
        self.all_words = self.h_words + self.v_words
        self.all_words.sort(key = lambda x: x[2], reverse=True)
        # print(self.all_words)
        # настройка количества итераций
        iteration = 1
        self.stop = False
        iteration_limit = self.set_interation_limit(self.entry3.get())
        # алгоритм генерации и заполнения слов
        self.min_empty_count = 10
        best_iteration_count = 0
        while not self.stop and iteration <= iteration_limit:
            self.clear_grid()
            self.empty = 0
            self.stop = True
            print(f'=== Итерация #{iteration} ===')
            for word in (self.all_words):
                self.word_randomizer(word[0], word[1], word[2], word[3], word[4], False)
            if self.empty <= self.min_empty_count:
                if self.min_empty_count == self.empty:
                    best_iteration_count += 1
                else:
                    best_iteration_count = 1
                    self.min_empty_count = self.empty
            iteration += 1
        print(f'Проведено итераций: {iteration-1}')
        print(f'Наилучших попыток {best_iteration_count} с количеством пропусков: {self.min_empty_count} слов')
            

    # Сохранение в pdf файл
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
        snapshot_enhanced.save(f'{self.savefolderpath}/CW_{self.wordscount}_[{self.w}x{self.h}].pdf', 
                        format='PDF', quality=200)


if __name__ == "__main__":
    main = Main()
    main.geometry(f'{900}x{640}') # main.winfo_screenheight()
    main.wm_geometry("+%d+%d" % (50, 10))
    main.title('CSV Convolution')
    main['bg'] = 'white'
    #main.attributes('-fullscreen', True)


    main.mainloop()

    # pyinstaller -F -w -i 'ico.png' script.py