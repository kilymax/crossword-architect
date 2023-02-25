import os
import re
import random

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk

class Main(Tk):

    def __init__(self):
        super().__init__()

        self.font16 = 'Verdana 16'
        self.font13 = 'Verdana 13'
        self.font10 = 'Verdana 10'
        self.font8 = 'Verdana 8'
        self.majorcolor = "#b8eaff"
        self.minorcolor = "#a2cee0"
        self.cellcolor= "#7ade7c"

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
        self.opendirectorybutton = ttk.Button(self.leftframe, text='Выбрать папку\nс словарями (txt)', 
                                              width=17, command=self.open_directory)
        self.opendirectorybutton.grid(row=0, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        
        self.dictlistbox = Listbox(self.leftframe, border=3, selectmode=MULTIPLE, height=5, font=self.font10)
        self.dictlistbox.grid(row=1, column=0, columnspan=3, pady=10, padx=10, ipadx=5, ipady=5, sticky="nsew")

        self.infolabel = ttk.Label(self.leftframe, style="infolabel.TLabel", text=2*'\n')
        self.infolabel.grid(row=2, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.selectdictbutton = ttk.Button(self.leftframe, text='Загрузить словари',
                                    command=lambda: self.notifiationlabel.config(text='Укажите\nразмер сетки', 
                                    style="notificationlabel.TLabel", foreground='red'))
        self.selectdictbutton.grid(row=3, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.notifiationlabel = ttk.Label(self.leftframe, style="notificationlabel.TLabel", text=1*'\n')
        self.notifiationlabel.grid(row=4, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")

        self.sizelabel = ttk.Label(self.leftframe, style="infolabel.TLabel", background=self.majorcolor, text='Укажите размер сетки')
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

        self.generatorbutton = ttk.Button(self.leftframe, text='Сгенерировать\nкроссворд', command=self.generator)
        self.generatorbutton.grid(row=8, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
        # self.leftframe.grid_rowconfigure(8, weight=1)

        self.savebutton = ttk.Button(self.leftframe, text='Сохранить в\nPDF-файл', command="")
        self.savebutton.grid(row=9, column=0, columnspan=3, pady=10, padx=10, sticky="nsew")
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
    # обработчик колеса мыши
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
        return re.match("^\w{0,1}$", newval) is not None
    
    # выбор ячеек
    def cell_picker(self, event, entry, i, j):
        self.char_check = (self.register(self.char_valid), "%P")
        if self.enabledcell[i][j] == 0:
            entry.config(state=NORMAL, validate="key", bg=self.cellcolor, 
                         validatecommand=self.char_check)
            self.enabledcell[i][j] = 1
        else:
            entry.delete(0, END)
            entry.config(state=DISABLED, 
                         validate=None, validatecommand=None)
            self.enabledcell[i][j] = 0



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
            self.shortest = min(self.dictionary.keys())
            self.longest = max(self.dictionary.keys())
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
                self.crosswordframe.config(bg='grey', width=w*2, height=h*5)
                self.grid = []
                self.enabledcell = []
                
                for i in range(self.h):
                    self.grid.append([])
                    self.enabledcell.append([])
                    for j in range(self.w):
                        if self.w > 25 or self.h > 25:
                            CWfont = 'Verdana 12'
                        else:
                            CWfont = self.font16
                        tempobj = Entry(self.crosswordframe, justify=CENTER, font=CWfont, 
                                        relief='solid', state=DISABLED, width=2)
                        tempobj.grid(row=i, column=j, sticky="nsew")
                        self.enabledcell[i].append(0)
                        self.grid[i].append(tempobj)
                        self.grid[i][j].bind('<Button-3>', lambda x, entry=self.grid[i][j], i=i, j=j: self.cell_picker(x, entry, i, j))
                        self.crosswordframe.grid_rowconfigure(i, weight=1)
                        self.crosswordframe.grid_columnconfigure(j, weight=1)
                self.notifiationlabel.config(text='\n', 
                                style="notificationlabel.TLabel", foreground='red')
                self.generatorbutton.config(command=self.generator)
        else:
            self.notifiationlabel.config(text='Укажите размер сетки\n', 
                            style="notificationlabel.TLabel", foreground='red')
            self.generatorbutton.config(command=None)
    
    # генерация кроссворда
    def generator(self):
        # горизонталь
        for i in range(self.h):
            l = 0
            for j in range(self.w):
                if self.enabledcell[i][j] == 1:
                    l += 1
            if l >= self.shortest and l <= self.longest:
                word = self.dictionary[l][random.randint(0, len(self.dictionary[l])-1)]
                print(l, word)
                char_index = 0
            for j in range(self.w):
                if self.enabledcell[i][j] == 1:
                    self.grid[i][j].delete(0, END)
                    self.grid[i][j].insert(0, word[char_index])
                    char_index += 1
                    # word = word.replace(word[0], '')
                
        # вертикаль
        # for j in range(self.w):
        #     for i in range(self.h):
        #         if self.enabledcell[j][i] == 1:
        #             pass


    # Сохранение dataframe в файл
    def save_in_file(self):
        self.original_file_name = self.folderpath.split('/')[-1:][0]
        self.modified_file_path = '/'.join(self.folderpath.split('/')[:-1:1]) + '/modified_' + self.original_file_name
        self.df.to_csv(self.modified_file_path, sep='\t', index= False, float_format="str", encoding="utf-16")
        self.notificationlabel.config(text='Файл успешно сохранен!', style="dynamic.TLabel", foreground='green')
        self.result_path = '/'.join(self.folderpath.split('/')[:-1:1])
        os.startfile(self.result_path)

if __name__ == "__main__":
    main = Main()
    main.geometry(f'{900}x{640}') # main.winfo_screenheight()
    main.title('CSV Convolution')
    main['bg'] = 'white'
    #main.attributes('-fullscreen', True)


    main.mainloop()