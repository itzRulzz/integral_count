import tkinter as tk # GUI.
import matplotlib.pyplot as plt # Построение графиков.
import numpy as np # Математика.
from sympy import * # Математика доп.
from tkinter import messagebox # Вывод ошибок.
from singleton import SingletonClass # Паттерн для создания лишь одного главного окна (защита от дублей).
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Модуль matplotlib для встраивания графиков в интерфейс Tkinter.
import re
import os
import sys



class MainWindow(SingletonClass): # Класс наследует поведение Singleton, чтобы был лишь один экземпляр главного окна.
    '''Хранит все основные переменные в атрибутах объекта.'''
    
    def __init__(self):
        '''Инициализирует переменные, использующиеся в классе.'''

        self.func = None # Сама функция.
        self.a = None # Левая граница интегрирования.
        self.b = None # Правая граница интегрирования.
        self.N = None # Количество точек для Монте-Карло.
        self.btn1 = None # Основная кнопка запуска вычислений
        self.root = None # Основа окна.



    def main_window(self):
        '''Создает графический интерфейс с вводом всех нужных данных.'''

        root = self.root # Не особо хорошая практика, но очень лень везде писать self.
        root = tk.Tk() # Создаем главное окно root.

        frame = tk.Frame(root, width=400, height=300, bg='#EDEDED') # Отдельное место под график цвета фона.
        frame.grid(column=5, row=1, columnspan=3, rowspan=9, padx=30)

        root.title('Численное интегрирование функции методом Монте-Карло') # Меняем название окна в самом верху.
        root.geometry('1000x600+320+180') # Изменяем размер окна и его положение относительно левого верхнего угла.
        root.resizable(False, False) # Запрещаем менять размеры окна.

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except AttributeError:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        logo_path = resource_path("content/logo.png")
        logo = tk.PhotoImage(file=logo_path) # Создаем переменную для логотипа.
        root.iconphoto(False, logo) # Присваиваем новый логотип окну.

        root.config(bg='#EDEDED') # Меняем цвет фона окна.

        text1 = tk.Label(root, text='Функция', # Создаем и настраиваем надпись "Функция".
                            bg='#EDEDED',
                            font=('Corbel', 20))
        text1.grid(row=0,column=0,stick='w') # Располагаем надпись на экране методом pack.

        entry1 = tk.Entry(root, bg='#D7D9DB') # Создаем и настраиваем поле ввода.
        entry1.grid(row=1,column=0,stick='nw') # Располагаем надпись на экране методом pack.

        text2 = tk.Label(root, text='Границы',
                            bg='#EDEDED',
                            font=('Corbel', 20))
        text2.grid(row=2,column=0,stick='w')

        text3 = tk.Label(root, text='a:',
                            bg='#EDEDED',
                            font=('Corbel', 20))
        text3.grid(row=3,column=0,stick='w')

        entry2 = tk.Entry(root, bg='#D7D9DB')
        entry2.grid(row=3,column=1,stick='w')

        text3 = tk.Label(root, text='b:',
                            bg='#EDEDED',
                            font=('Corbel', 20),
                            padx=50)
        text3.grid(row=3,column=2,stick='w')

        entry3 = tk.Entry(root, bg='#D7D9DB')
        entry3.grid(row=3,column=3,stick='w')

        text4 = tk.Label(root, text='Кол-во. точек',
                            bg='#EDEDED',
                            font=('Corbel', 20))
        text4.grid(row=4,column=0,stick='w')

        entry4 = tk.Entry(root, bg='#D7D9DB')
        entry4.grid(row=5,column=0,stick='nw')



        def start(): # Функция, запускающаяся после нажатия на кнопку запуска.
            self.btn1.config(relief='sunken') # Делаем кнопку нажатой.
            self.btn1.config(state='disabled') # Отключаем возможность нажать кнопку.
            self.func = entry1.get() # Сохраняем вводы пользователя в переменные.
            self.a = entry2.get()
            self.b = entry3.get()
            self.N = entry4.get()
            if mw.user_input(): # Если все проверки переменных успешны, то ...
                mw.build_plot() # Запускаем построение графика.



        self.btn1 = tk.Button(root, text='▶️', # Создаем и настраиваем кнопку запуска вычислений.
                            command=start,
                            bg='#EDEDED',
                            activebackground='#D7D9DB')
        self.btn1.grid(row=6,column=0, stick='w') # Располагаем кнопку на экране.

        root.grid_columnconfigure(0, minsize=100) # Настраиваем размер сетки в окне.
        root.grid_columnconfigure(1, minsize=10)
        root.grid_columnconfigure(2, minsize=10)

        root.grid_rowconfigure(1, minsize=30)
        root.grid_rowconfigure(3, minsize=30)
        root.grid_rowconfigure(5, minsize=30)

        def on_close():
            root.destroy()
        
        root.protocol("WM_DELETE_WINDOW", on_close)

        root.mainloop() # Вечный цикл, в течении которого окно будет запущено.



    def user_input(self):
        '''Принимает и проверяет введенные пользователем данные и преобразует их в правильные форматы.'''
        
        # Преобразуем все введенные данные в нужный вид + выполняем базовые проверки.
        # Обработка a.
        try:
            self.a = int(self.a) # Пробуем перевести в целое число.
        except ValueError:
            try:
                self.a = self.a.replace(",", ".") # Замена , на .
                self.a = float(self.a) # Пробуем перевести в десятичное число.
            except ValueError:
                if isinstance(self.a, str): # Если a - строка, то ...
                    if self.a.lower() in ["pi", "пи", "п", "p", "π"]: # Переводим все варианты в строчные буквы и сравниваем.
                        self.a = np.pi
                    elif self.a.lower() in ["inf", "∞", "бесконечность"]:
                        self.a = np.inf
                    else:
                        messagebox.showerror("Ошибка", "Значение 'a' должно быть целым числом/десятичным числом/пи/бесконечностью.")
                        self.btn1.config(relief='raised')
                        self.btn1.config(state='normal')
                        return False
                else:
                    messagebox.showerror("Ошибка", "Значение 'a' должно быть целым числом/десятичным числом/пи/бесконечностью.")
                    self.btn1.config(relief='raised')
                    self.btn1.config(state='normal')
                    return False

        # Обработка значения b.
        try:
            self.b = int(self.b)
        except ValueError:
            try:
                self.b = self.b.replace(",", ".")
                self.b = float(self.b)
            except ValueError:
                if isinstance(self.b, str):
                    if self.b.lower() in ["pi", "пи", "п", "p", "π"]:
                        self.b = np.pi
                    elif self.b.lower() in ["inf", "∞", "бесконечность"]:
                        self.b = np.inf
                    else:
                        messagebox.showerror("Ошибка", "Значение 'a' должно быть целым числом/десятичным числом/пи/бесконечностью.")
                        self.btn1.config(relief='raised')
                        self.btn1.config(state='normal')
                        return False
                else:
                    messagebox.showerror("Ошибка", "Значение 'a' должно быть целым числом/десятичным числом/пи/бесконечностью.")
                    self.btn1.config(relief='raised')
                    self.btn1.config(state='normal')
                    return False

        # Обработка значения N.
        try:
            self.N = int(self.N)
        except ValueError:
            messagebox.showerror("Ошибка", "Значение 'N' должно быть целым числом.")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False
        
        # Проверка N < 100.
        if self.N < 100:
            messagebox.showerror("Ошибка", "Минимальное количество точек: 100!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False
        
        # Проверка корректности границ.
        if self.a >= self.b:
            messagebox.showerror("Ошибка", "'a' должно быть меньше 'b'!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False

        # Проверка корректности func.
        # Удаление пробелов.
        self.func = self.func.replace(" ", "")
        # Удаляем "y=".
        self.func = self.func.replace("y=", "")
        # Заменяем "^" на "**".
        self.func = self.func.replace('^', '**')
        # Заменяем "," на ".".
        self.func = self.func.replace(",", ".")
        
        # Объявляем спец. триганометрические функции через numpy.
        self.func = re.sub(r'\bsin\b', 'np.sin', self.func)
        self.func = re.sub(r'\bcos\b', 'np.cos', self.func)
        self.func = re.sub(r'\btan\b', 'np.tan', self.func)
        self.func = re.sub(r'\bexp\b', 'np.exp', self.func)
        self.func = re.sub(r'\bpi\b', 'np.pi', self.func)
        self.func = re.sub(r'\bsqrt\b', 'np.sqrt', self.func)
        self.func = re.sub(r'\be\b', 'np.e', self.func)

        # Объявляем func "анонимной" функцией через lambda.
        self.func = "lambda x: " + self.func

        # Проверка синтаксиса func.
        try:
            compile(self.func, "<string>", "exec")
        except SyntaxError:
            messagebox.showerror("Ошибка", "Функция написана некорректно!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False

        # Проверка воспроизводимости func.
        try:
            eval(self.func)
        except:
            messagebox.showerror("Ошибка", "Невозможно построить введенную вами функцию!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False

        return True



    def build_plot(self):
        '''Строит график.'''

        # Компилируем строку в объект кода, т.е. создаем из строки функцию.
        self.func = compile(self.func, "<string>", "eval")
        self.func = eval(self.func)

        figure, ax = plt.subplots(figsize=(4.3,4))

        canvas = FigureCanvasTkAgg(figure, self.root)
        canvas.get_tk_widget().grid(column=5, row=1, columnspan=3, rowspan=9, padx=20)

        x = np.linspace(self.a - 10, self.b + 10, 100)
        y = self.func(x)

        # Построение графика функции
        ax.plot(x, y)

        # Добавление условных границ интегрирования
        ax.axvline(self.a, color='red', linestyle='dashed')
        ax.axvline(self.b, color='red', linestyle='dashed')

        # Оси OX и OY
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        # Добавление подписей осей и заголовка
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('График функции')

        ax.set_xlim(-10, 10)
        ax.set_ylim(-100, 100)


        canvas.draw()

        self.btn1.config(relief='raised')
        self.btn1.config(state='normal')

        # Начинаем расчеты.
        mw.math_calculations()



    def math_calculations(self):
        '''Выполняет математические расчеты.'''
        
        # Узнаем максимум и минимум функции на отрезке.
        
        x = np.linspace(self.a, self.b, 100)
        y = np.vectorize(self.func)(x)
        max_y = np.amax(y)
        min_y = np.amin(y)

        # Генерируем случайные X от a до b.

        random_x = np.random.uniform(self.a, self.b, self.N)

        # Генерируем случайные Y от min_y до max_y.

        if min_y >= 0:
            random_y = np.random.uniform(0, max_y, self.N)
        elif max_y < 0:
            random_y = np.random.uniform(min_y, 0, self.N)
        else:
            random_y = np.random.uniform(min_y, max_y, self.N)

        # Считаем значение функции для каждого из сгенерированных x-ов.

        random_xy = []
        for i in random_x:
            random_xy.append(self.func(i))

        # Определяем положение точек, разбивая их на группы и высчитываем долю точек внутри нужных областей. Если max_y > 0: если random_y[i] в random_x[i] меньше или равно random_xy[i], то внутри.
        
        count_g = 0
        count_r = 0
        count_b = 0
        count_y = 0

        # Группа 1 (внутри выше 0).
        for i in range(self.N):
            if random_y[i] >= 0 and random_y[i] < random_xy[i]:
                count_g += 1
        # Группа 2 (внутри ниже 0).
            if random_y[i] < 0 and random_y[i] > random_xy[i]:
                count_b += 1
        # Группа 3 (снаружи выше 0).
            if random_y[i] >= 0 and random_y[i] > random_xy[i]:
                count_r += 1
        # Группа 4 (снаружи ниже 0).
            if random_y[i] < 0 and random_y[i] < random_xy[i]:
                count_y += 1

        # Рассчитываем площадь прямоугольника, получившегося из пределов a - b и OX - y_min/y_max. S_прямоугольника = (x_max-x_min) * (y_max-0 ИЛИ 0-y_min).
        
        s_uprectangle = (self.b - self.a) * (max_y - 0)
        s_downrectangle = (self.b - self.a) * (min_y - 0)

        # Определяем интеграл через integral = s_rectangle * dots_inside
        
        if min_y > 0:
            s_g = s_uprectangle * count_g / (count_g + count_r)
            integral = s_g
        elif max_y <= 0:
            s_b = s_downrectangle * count_b / (count_b + count_y)
            integral = s_b
        else:
            s_g = s_uprectangle * count_g / (count_g + count_r)
            s_b = s_downrectangle * count_b / (count_b + count_y)
            integral = s_g + s_b

        # Визуализация точек и вывод результатов.

        mw.show_results(random_x, random_y, integral, max_y, min_y)



    def show_results(self, random_x, random_y, integral, max_y, min_y):
        '''Визуализирует точки и выводит непосредственный ответ.'''
        
        if hasattr(self, 'figure') and hasattr(self, 'ax'):
            self.ax.clear()
        else:
            self.figure, self.ax = plt.subplots(figsize=(4.3, 4))

        x = np.linspace(self.a - 10, self.b + 10, 100)
        y = self.func(x)
        self.ax.plot(x, y)

        if min_y >= 0:
            is_under_graph = random_y < self.func(random_x)
        elif max_y < 0:
            is_under_graph = random_y > self.func(random_x)
        else:
             is_under_graph = np.logical_or(np.logical_and(random_y < self.func(random_x), random_y >= 0), np.logical_and(random_y > self.func(random_x), random_y < 0))

        self.ax.scatter(random_x, random_y, c=np.where(is_under_graph, 'green', 'red'), marker='o', s=5)

        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.set_title('График функции с точками')

        self.ax.axvline(self.a, color='red', linestyle='dashed')
        self.ax.axvline(self.b, color='red', linestyle='dashed')

        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

        if hasattr(self, 'canvas'):
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.canvas.get_tk_widget().grid(column=5, row=1, columnspan=3, rowspan=9, padx=20)
        self.canvas.draw()

        if hasattr(self, 'text5'):
            self.text5.destroy()

        self.text5 = tk.Label(self.root, text=f'Ответ: {integral}',
                            bg='#EDEDED',
                            font=('Corbel', 20))
        self.text5.grid(row=15,column=5,stick='s',pady=30)

        

if __name__ == "__main__":
    mw = MainWindow() # Создаем объект класса MainWindow.
    mw.main_window() # Вызываем метод на объекте, запускаем цепочку остальных функций.