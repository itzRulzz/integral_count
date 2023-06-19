import tkinter as tk # GUI
import matplotlib.pyplot as plt # График.
import numpy as np # Математика для графика.
from tkinter import messagebox # Вывод ошибок.
from singleton import SingletonClass # Паттерн для создания лишь одного главного окна.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Модуль matplotlib для встраивания графиков в интерфейс Tkinter.

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

        frame = tk.Frame(root, width=400, height=300, bg='#EDEDED') # Отдельное место под график.
        frame.grid(column=5, row=1, columnspan=3, rowspan=9, padx=30)

        root.title('Численное интегрирование функции методом Монте-Карло') # Меняем название окна в самом верху.
        root.geometry('1000x600+320+180') # Изменяем размер окна и его положение относительно левого верхнего угла.
        root.resizable(False, False) # Запрещаем менять размеры окна.

        logo = tk.PhotoImage(file='content\logo.png') # Создаем переменную для логотипа.
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

        root.mainloop() # Вечный цикл, в течении которого окно будет запущено.



    def user_input(self):
        '''Принимает и проверяет введенные пользователем данные и преобразует их в правильные типы.'''
        
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
        
        # Объявляем спец. триганометрические функции через numpy.
        if "sin" in self.func:
            self.func = self.func.replace("sin", "np.sin")
        elif "cos" in self.func:
            self.func = self.func.replace("cos", "np.cos")
        elif "tan" in self.func:
            self.func = self.func.replace("tan", "np.tan")
        elif "arcsin" in self.func:
            self.func = self.func.replace("arcsin", "np.arcsin")
        elif "arccos" in self.func:
            self.func = self.func.replace("arccos", "np.arccos")
        elif "arctan" in self.func:
            self.func = self.func.replace("arctan", "np.arctan")
        elif "exp" in self.func:
            self.func = self.func.replace("exp", "np.exp")
        elif "pi" in self.func:
            self.func = self.func.replace("pi", "np.pi")
        elif "e" in self.func:
            self.func = self.func.replace("e", "np.e")

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

        canvas.draw()

        self.btn1.config(relief='raised')
        self.btn1.config(state='normal')

        # Начинаем расчеты.
        mw.math_calculations()



    def math_calculations(self):
        '''Выполняет математические расчеты.'''
        
        # Генерируем N пар точек x и y через numpy.random.uniform()
        random_x = np.random.uniform(self.a, self.b, self.N)
        random_y = []
        for i in range(len(random_x)):
            random_y.append(self.func(random_x[i]))

        # Вычисляем среднее значение значений функции, суммируя их и деля на N.
        y_mean = np.sum(random_y) / self.N

        # Умножим среднее значение на ширину интервала интегрирования (b - a), чтобы получить приблизительное значение интеграла.
        integral = (self.b - self.a) * y_mean

        # Визуализация точек и вывод результатов
        mw.show_results(random_x, random_y, integral)



    def show_results(self, random_x, random_y, integral):
        '''Визуализирует точки и выводит непосредственный ответ.'''
        
        text5 = tk.Label(self.root, text=f'Ответ: {integral}',
                            bg='#EDEDED',
                            font=('Corbel', 20))
        text5.grid(row=15,column=5,stick='s',pady=30)
        '''
        self.fig, self.ax = plt.subplots()

        # Построение графика функции
        self.ax.plot(x, y)

        # Отображение случайных точек
        self.ax.scatter(random_x, random_y, color='red')

        # Добавление условных границ интегрирования
        self.ax.axvline(self.a, color='red', linestyle='dashed')
        self.ax.axvline(self.b, color='red', linestyle='dashed')

        # Оси OX и OY
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

        # Добавление подписей осей и заголовка
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('График функции с случайными точками')

        # Отображение графика
        plt.show()

        # Вывод результатов
        messagebox.showinfo("Определенный интеграл вашей функции:", integral)
        '''


if __name__ == "__main__":
    mw = MainWindow() # Создаем объект класса MainWindow.
    mw.main_window() # Вызываем метод на объекте, запускаем цепочку остальных функций.