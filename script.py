# -*- coding: utf–8 -*-
import os
import re
import random

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk

from PIL import ImageGrab, ImageEnhance



class Main(Tk):

    def __init__(self):
        super().__init__()

        self.arial = 'Arial'
        self.font16 = 'Arial 16'
        self.font13 = 'Arial 13'
        self.font10 = 'Arial 10'
        self.font8 = 'Arial 8'
        self.majorcolor = "#b8eaff"
        self.minorcolor = "#a2cee0"
        self.cellcolor= "#91bbff"
        self.fixedcellcolor = "#57ff47"
        self.not_found_textcolor = 'red'

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
        self.tatar_extension = ['Ә', 'ә', 'Ө', 'ө', 'Ү', 'ү', 'Җ', 'җ', 'Ң', 'ң', 'Һ', 'һ']
        self.digits = [str(i) for i in range(10)]
        self.global_alphabet = (self.eng_alphabet + self.ENG_alphabet + self.rus_alphabet + 
                                    self.RUS_alphabet + self.tatar_extension + self.digits)

        # Стили виджетов ttk
        buttonstyle = ttk.Style()
        buttonstyle.configure("TButton", background="grey", foreground="black", 
                                font=self.font13, justify="center")
        infolabel = ttk.Style()
        infolabel.configure("infolabel.TLabel", foreground="black", 
                                    background=self.minorcolor, font=self.font10, padding=[0, 0])
        notificationlabel = ttk.Style()
        notificationlabel.configure("notificationlabel.TLabel", 
                                    background=self.minorcolor, font=self.font13,
                                    padding=[0, 0], anchor=TOP)
        
        # Левая и правая части интерфейса
        self.leftframe = Frame(self, bg=self.majorcolor)
        self.leftframe.grid(row=0, column=0, sticky="nsew")
        self.rightframe = Frame(self, bg='white')
        self.rightframe.grid(row=0, column=1, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Наполнение левой части
        self.opendirectorybutton = ttk.Button(self.leftframe, text='Выбрать папку\nсо словарями (txt)', 
                                              width=22, command=self.open_directory)
        self.opendirectorybutton.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        
        self.dictlistbox = Listbox(self.leftframe, border=3, selectmode=MULTIPLE, height=5, font=self.font10)
        self.dictlistbox.grid(row=1, column=0, columnspan=3, pady=10, padx=10, ipadx=5, ipady=5, sticky="nsew")

        self.infolabel = ttk.Label(self.leftframe, style="infolabel.TLabel", text=2*'\n')
        self.infolabel.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.selectdictbutton = ttk.Button(self.leftframe, text='Загрузить словари',
                                    command=lambda: self.notifiationlabel.config(text='Директория с\nсловарями не выбрана!', 
                                    style="notificationlabel.TLabel", foreground='red'))
        self.selectdictbutton.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.notifiationlabel = ttk.Label(self.leftframe, style="notificationlabel.TLabel", text=1*'\n')
        self.notifiationlabel.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.sizelabel = ttk.Label(self.leftframe, style="infolabel.TLabel", 
                                   background=self.majorcolor, text='Укажите размер сетки')
        self.sizelabel.grid(row=5, column=0, columnspan=3, pady=5, padx=10, sticky="nsew")
        
        # Первое поле для ввода
        self.entry1 = Entry(self.leftframe, justify=CENTER, width=10)
        self.entry1.grid(row=6, column=0, padx=10, sticky="e")
        self.entry1.insert(0, 'Ширина')
        self.entry1.configure(state='normal', fg="#b8b8b8")
        self.entrybind1_in = self.entry1.bind('<Button-1>', lambda x: self.on_focus_in(self.entry1))
        self.entrybind1_out = self.entry1.bind(
            '<FocusOut>', lambda x: self.on_focus_out(self.entry1, 'Ширина'))

        self.minilabel = ttk.Label(self.leftframe, background=self.majorcolor, text=' X ')
        self.minilabel.grid(row=6, column=1)
        # Второе поле для ввода
        self.entry2 = Entry(self.leftframe, justify=CENTER, width=10)
        self.entry2.grid(row=6, column=2, padx=10, sticky="w")
        self.entry2.insert(0, 'Высота')
        self.entry2.configure(state='normal', fg="#b8b8b8")
        self.entrybind2_in = self.entry2.bind('<Button-1>', lambda x: self.on_focus_in(self.entry2))
        self.entrybind2_out = self.entry2.bind(
            '<FocusOut>', lambda x: self.on_focus_out(self.entry2, 'Высота'))
        self.leftframe.grid_columnconfigure(0, weight=3)
        self.leftframe.grid_columnconfigure(2, weight=3)

        self.gridbutton = ttk.Button(self.leftframe, text='Построить сетку', 
                        command= lambda: self.make_crossword_grid(self.entry1.get(), self.entry2.get()))
        self.gridbutton.grid(row=7, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.entry3 = Entry(self.leftframe, justify=CENTER, width=25)
        self.entry3.grid(row=8, column=0, padx=10, columnspan=3)
        self.entry3.insert(0, 'Кол-во итераций (def 20)')
        self.entry3.configure(state='normal', fg="#b8b8b8")
        self.entrybind3_in = self.entry3.bind('<Button-1>', lambda x: self.on_focus_in(self.entry3))
        self.entrybind3_out = self.entry3.bind(
            '<FocusOut>', lambda x: self.on_focus_out(self.entry3, 'Кол-во итераций (def 20)'))

        self.generatorbutton = ttk.Button(self.leftframe, text='Сгенерировать\nкроссворд', 
                                          command=lambda: self.notifiationlabel.config(text='Словарь не загружен\nили не построена сетка', 
                                          style="notificationlabel.TLabel", foreground='red'))
        self.generatorbutton.grid(row=9, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        # self.leftframe.grid_rowconfigure(8, weight=1)

        self.savebutton = ttk.Button(self.leftframe, text='Сохранить в\nPDF-файл',
                                     command=lambda: self.notifiationlabel.config(text='Сетка отсутствует\nили она пуста',
                                                                                  foreground='red',))
        self.savebutton.grid(row=10, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        # self.leftframe.grid_rowconfigure(9, weight=1)


        # Наполнение правой части
        self.crosswordframe = Frame(self.rightframe)
        self.crosswordframe.grid(row=0, column=0, padx=10, pady=10)
        self.rightframe.grid_rowconfigure(0, weight=1)
        self.rightframe.grid_columnconfigure(0, weight=1)
        
    # Служебные функции и обработчики событий
    # entry изменения
    def on_focus_in(self, entry):
        if entry.cget('state') == 'normal':
            entry.configure(state='normal', fg="black")
            entry.delete(0, 'end')
    def on_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.configure(state='normal', fg="#b8b8b8")
    
    # обработчик колеса мыши (unused)
    def sc1_mouse_wheel(self, event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.scale1.set(self.scale1.get()-1)
        if event.num == 4 or event.delta == 120:
            self.scale1.set(self.scale1.get()+1)

        # self.scale1.bind("<MouseWheel>", self.sc1_mouse_wheel)
        # self.scale1.bind("<Button-4>", self.sc1_mouse_wheel)
        # self.scale1.bind("<Button-5>", self.sc1_mouse_wheel)
    
    # ограничитель ввода
    def char_valid(self, newval):
        return re.match(u"^\w{0,1}$" , newval, re.UNICODE) is not None 
    
    # выбор ячеек
    def cell_picker(self, event, entry, i, j):
        self.char_check = (self.register(self.char_valid), "%P")
        if self.enabledcell[i][j] == 0:
            entry.config(state=NORMAL, validate="key", fg='black', bg=self.cellcolor, 
                         validatecommand=self.char_check)
            self.enabledcell[i][j] = 1
        else:
            entry.delete(0, END)
            entry.config(state=DISABLED, fg='black',
                         validate=None, validatecommand=None)
            self.enabledcell[i][j] = 0

    # фиксация ячеек, заполненных вручную
    def fixing_cell(self, event, entry, i, j):
        if event.char in self.global_alphabet:
            entry.delete(0, END)
            entry.insert(0, event.char.upper())
            entry.config(validate="key", fg='black', bg=self.fixedcellcolor, 
                        validatecommand=self.char_check)
            self.enabledcell[i][j] = 2
    
    # расфиксация ячеек, заполненных вручную
    def unfixing_cell(self, event, entry, i, j):
        if self.enabledcell[i][j] == 2:
            entry.delete(0, END)
            entry.config(state=NORMAL, validate="key", fg='black', bg=self.cellcolor, 
                         validatecommand=self.char_check)
            self.enabledcell[i][j] = 1

    # функция с основным функционалом
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
    
    # загрузка слов из выбранных файлов в память и формирование словаря
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
                            if sw != '' and sw != ' ' and sw not in self.wordsarray:
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
                                style="notificationlabel.TLabel", foreground='green')
        else:
            self.shortest = '-'
            self.longest = '-'
            self.infolabel.config(text=2*'\n')  
            self.notifiationlabel.config(text='Словари не выбраны\n', 
                            style="notificationlabel.TLabel", foreground='red')
        
        self.infolabel.config(text=f'Общее кол-во слов: {len(self.wordsarray)}\nМин. длина слова: {self.shortest}\nМакс. длина слова: {self.longest}')

    def make_crossword_grid(self, w, h):
        if w.isnumeric() and h.isnumeric():
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
                        tempobj = Entry(self.crosswordframe, justify=CENTER, font=f'{self.arial} {fontcoeff} bold', 
                                        relief='solid', state=DISABLED, width=2)
                        tempobj.grid(row=i, column=j, sticky="nsew")
                        self.enabledcell[i].append(0)
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
    
    # генерация кроссворда
    def generator(self):
        iteration = 1
        enablecellcheck = 0
        horizontal_is_full = False
        vertical_is_full = False
        self.notifiationlabel.config(text='\n', foreground=self.not_found_textcolor)
        
        # проверка валидности лимитирующего значения для количества итераций
        iteration_limit = self.entry3.get()
        if iteration_limit.isnumeric():
            iteration_limit = int(iteration_limit)
            if iteration_limit > 0 and iteration_limit < 10000:
                iteration_limit = iteration_limit
            else:
                iteration_limit = 20
        else:
            iteration_limit = 20
        
        # алгоритм заполнения сетки
        while iteration <= iteration_limit and not horizontal_is_full and not vertical_is_full:
            vertical_is_full = True
            self.wordscount = 0
            print(f'=== {iteration} итерация ===')
            # горизонталь
            for i in range(self.h):
                gridindexes = []
                gridletters = []
                full_word_is_fixed = 0
                for j in range(self.w):
                    if self.enabledcell[i][j] == 1:
                        enablecellcheck += 1
                        gridindexes.append(j)
                        self.grid[i][j].delete(0, END)
                        gridletters.append(self.grid[i][j].get())
                        full_word_is_fixed = 0
                    self.grid[i][j].config(bg=self.cellcolor)
                    if self.enabledcell[i][j] == 2:
                        enablecellcheck += 1
                        gridindexes.append(j)
                        gridletters.append(self.grid[i][j].get())
                        full_word_is_fixed += 1
                        self.grid[i][j].config(bg=self.fixedcellcolor)

                    if (self.enabledcell[i][j] == 0 or j+1 == len(self.enabledcell[i])) and len(gridindexes)>0:
                        if len(gridindexes) >= self.shortest and len(gridindexes) <= self.longest:
                            pattern = ''
                            words_with_fixed_len = '\n'.join(self.dictionary[len(gridindexes)])
                            for letter in gridletters:
                                if letter == '':
                                    pattern += '.'
                                else:
                                    pattern += letter
                            pattern = re.compile(pattern)
                            result = pattern.findall(words_with_fixed_len)
                            try:
                                word = result[random.randint(0, len(result)-1)]
                                self.wordscount += 1
                                print('len', len(gridindexes), pattern, word, '(h)')
                                for elem in gridindexes:
                                    self.grid[i][elem].insert(0, word[gridindexes.index(elem)])
                                    if self.enabledcell[i][elem] == 1:
                                        self.grid[i][elem].config(bg=self.cellcolor)
                                    else:
                                        self.grid[i][elem].config(bg=self.fixedcellcolor)
                            except:
                                horizontal_is_full = False
                                if full_word_is_fixed != len(gridindexes):
                                    for elem in gridindexes:
                                        self.grid[i][elem].config(bg=self.not_found_textcolor)
                                else:
                                    self.wordscount += 1
                        else:
                            self.grid[i][j].delete(0, END)
                        gridindexes.clear()
                        gridletters.clear()
                        pattern = ''
                        
            # вертикаль
            for j in range(self.w):
                gridindexes = []
                gridletters = []
                full_word_is_fixed = 0
                for i in range(self.h):
                    if self.enabledcell[i][j] == 1:
                        enablecellcheck += 1
                        gridindexes.append(i)
                        gridletters.append(self.grid[i][j].get())
                        full_word_is_fixed = 0
                        self.grid[i][j].config(bg=self.cellcolor)
                    if self.enabledcell[i][j] == 2:
                        enablecellcheck += 1
                        gridindexes.append(i)
                        gridletters.append(self.grid[i][j].get())
                        full_word_is_fixed += 1
                        self.grid[i][j].config(bg=self.fixedcellcolor)
                    
                    if (self.enabledcell[i][j] == 0 or i+1 == len(self.enabledcell)) and len(gridindexes)>0:
                        if len(gridindexes) >= self.shortest and len(gridindexes) <= self.longest:
                            pattern = ''
                            words_with_fixed_len = '\n'.join(self.dictionary[len(gridindexes)])
                            for letter in gridletters:
                                if letter == '':
                                    pattern += '.'
                                else:
                                    pattern += letter
                            pattern = re.compile(pattern)
                            result = pattern.findall(words_with_fixed_len)
                            try:
                                word = result[random.randint(0, len(result)-1)]
                                self.wordscount += 1
                                print('len', len(gridindexes), pattern, word, '(v)')
                                for elem in gridindexes:
                                    self.grid[elem][j].insert(0, word[gridindexes.index(elem)])
                                    if self.enabledcell[elem][j] == 1:
                                        self.grid[elem][j].config(bg=self.cellcolor)
                                    else:
                                        self.grid[elem][j].config(bg=self.fixedcellcolor)
                            except:
                                if full_word_is_fixed != len(gridindexes):
                                    for elem in gridindexes:
                                        self.grid[elem][j].config(bg=self.not_found_textcolor)
                                    vertical_is_full = False
                                else:
                                    self.wordscount += 1
                        else:
                            pass
                        gridindexes.clear()
                        gridletters.clear()
                        pattern = ''
            iteration += 1
        
        if iteration > iteration_limit:
            self.notifiationlabel.config(text='В базе нет\nподходящих слов!', foreground=self.not_found_textcolor)
        if enablecellcheck < self.shortest:
            self.notifiationlabel.config(text='Некорректно\nвыбраны ячейки!', foreground=self.not_found_textcolor)
        self.savebutton.config(command=self.save_in_file)

    # Сохранение в pdf файл
    def save_in_file(self):
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
    main.wm_geometry("+%d+%d" % (30, 30))
    main.title('CSV Convolution')
    main['bg'] = 'white'
    #main.attributes('-fullscreen', True)


    main.mainloop()