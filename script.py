import pandas as pd
import numpy as np
import matplotlib
import os

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as ticker

class Main(Tk):

    def __init__(self):
        super().__init__()

        self.font12 = 'Verdana 12'
        self.font10 = 'Verdana 10'
        self.font8 = 'Verdana 8'

        self.folderpath = ''

        # Стили виджетов ttk
        buttonstyle = ttk.Style()
        buttonstyle.configure("TButton", background="grey", foreground="black", 
                                font=self.font12, justify="center")
        infolabel = ttk.Style()
        infolabel.configure("infolabel.TLabel", foreground="black", 
                                    background="#99ffa7", font=self.font10, padding=[10, 0])
        notificationlabel = ttk.Style()
        notificationlabel.configure("notificationlabel.TLabel", 
                                    background="#fdff99", font=self.font12,
                                    padding=[0, 0], anchor=TOP)
        
        # Левая и правая части интерфейса
        self.leftframe = Frame(self, bg='#bababa')
        self.leftframe.grid(row=0, column=0, sticky="nsew")
        self.rightframe = Frame(self, bg='white')
        self.rightframe.grid(row=0, column=1, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=7)

        # Наполнение левой части
        self.opendirectorybutton = ttk.Button(self.leftframe, text='Выбрать папку\nс словарями (txt)', command=self.open_directory)
        self.opendirectorybutton.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        
        self.dictlistbox = Listbox(self.leftframe, border=3, selectmode=MULTIPLE, font=self.font10)
        self.dictlistbox.grid(row=1, column=0, pady=10, padx=10, ipadx=5, ipady=5, sticky="nsew")

        self.infolabel = ttk.Label(self.leftframe, style="infolabel.TLabel", text=2*'\n')
        self.infolabel.grid(row=2, column=0, pady=10, padx=10, sticky="nsew")

        self.selectdictbutton = ttk.Button(self.leftframe, text='Загрузить словари')
        self.selectdictbutton.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

        self.notifiationlabel = ttk.Label(self.leftframe, style="notificationlabel.TLabel", text=1*'\n')
        self.notifiationlabel.grid(row=4, column=0, pady=10, padx=10, sticky="nsew")

        self.button2 = ttk.Button(self.leftframe, text='Сгенерировать кроссворд', command="")
        self.button2.grid(row=5, column=0, pady=10, padx=10, sticky="nsew")

        self.savebutton = ttk.Button(self.leftframe, text='Сохранить в PDF-файл', width=20, command="")
        self.savebutton.grid(row=6, column=0, pady=10, padx=10, sticky="nsew")


        # Наполнение правой части
        self.figure = plt.Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, self.rightframe)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        
        
        
        # self.scale1.bind("<MouseWheel>", self.sc1_mouse_wheel)
        # self.scale1.bind("<Button-4>", self.sc1_mouse_wheel)
        # self.scale1.bind("<Button-5>", self.sc1_mouse_wheel)
    def sc1_mouse_wheel(self, event):
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.scale1.set(self.scale1.get()-1)
        if event.num == 4 or event.delta == 120:
            self.scale1.set(self.scale1.get()+1)


    # функция с основным функционалом
    def open_directory(self):
        try:
            # выбор и открытие папки
            # self.folderpath = fd.askdirectory()
            self.folderpath = 'c:/.My/Freelance/Crossword-Architect'
            self.notifiationlabel.config(text=1*'\n', 
                            style="notificationlabel.TLabel", foreground='red')
            # Чтение данных и сохранение в массивы
            self.dictdir = os.listdir(self.folderpath)
            for filename in self.dictdir:
                self.dictlistbox.insert(END, '- '+filename)

                self.selectdictbutton.config(command=self.select_files)

        except FileNotFoundError:
            self.selectdictbutton.config(command=None)
            self.notifiationlabel.config(text='Директория не выбрана\n', 
                            style="notificationlabel.TLabel", foreground='red')
    
    def make_dictionary(self):
        self.shortest = 100
        self.longest = 0
        if len(self.selected) != 0:
            for fileindex in self.selected:
                if self.dictdir[fileindex].endswith('.txt'):
                    with open(self.dictdir[fileindex], 'r', encoding='utf-8') as file:
                        for word in file:
                            word = word.replace('\n', '')
                            l = len(word)
                            if l < self.shortest:
                                self.shortest = l
                            if l > self.longest:
                                self.longest = l
                            self.dictionary.append(word)
                    self.notifiationlabel.config(text='Словарь загружен\n', 
                                    style="notificationlabel.TLabel", foreground='green')
                else:
                    self.infolabel.config(text=2*'\n') 
                    self.notifiationlabel.config(text='Словарь должен\nбыть в формате .txt', 
                                    style="notificationlabel.TLabel", foreground='red')
        else:
            self.shortest = '-'
            self.longest = '-'
            self.infolabel.config(text=2*'\n')  
            self.notifiationlabel.config(text='Словари не выбраны\n', 
                            style="notificationlabel.TLabel", foreground='red')
        self.wordcount = len(self.dictionary)

    
    # загрузка выбранных словарей в память
    def select_files(self):
        self.dictionary = []
        self.selected = self.dictlistbox.curselection()
        self.make_dictionary()

        
        self.infolabel.config(text=f'Общее кол-во слов: {self.wordcount}\nМин. длина слова: {self.shortest}\nМакс. длина слова: {self.longest}')



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
    main.geometry(f'{1200}x{600}')
    main.title('CSV Convolution')
    main['bg'] = 'white'


    main.mainloop()