import tkinter as tk # GUI
import matplotlib.pyplot as plt # График.
import numpy as np # Математика для графика.
from tkinter import messagebox # Вывод ошибок.
from singleton import SingletonClass # Паттерн для создания лишь одного главного окна.

class MainWindow(SingletonClass): # Класс наследует поведение Singleton, чтобы был лишь один экземпляр главного окна.
    '''Хранит все основные переменные в атрибутах объекта.'''
    
    def __init__(self):
        '''Инициализирует переменные, использующиеся в классе.'''

        self.func = None # Сама функция.
        self.a = None # Левая граница интегрирования.
        self.b = None # Правая граница интегрирования.
        self.N = None # Количество точек для Монте-Карло.
        self.btn1 = None # Основная кнопка запуска вычислений
        self.fig = None #
        self.ax = None



    def main_window(self):
        '''Создает графический интерфейс с вводом всех нужных данных.'''

        root = tk.Tk() # Создаем главное окно root.

        root.title('Численное интегрирование функции методом Монте-Карло') # Меняем название окна в самом верху.
        root.geometry('900x600+320+180') # Изменяем размер окна и его положение относительно левого верхнего угла.
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
                mw.plot() # Запускаем построение графика.



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



    def plot(self):
        '''Строит график.'''

        compiled_func = compile(self.func, "<string>", "eval")
        self.func = eval(compiled_func)

        x = np.linspace(self.a-10, self.b+10, 100)
        y = self.func(x)

        self.fig, self.ax = plt.subplots()

        # Построение графика функции
        self.ax.plot(x, y)

        # Добавление условных границ интегрирования
        self.ax.axvline(self.a, color='red', linestyle='dashed')
        self.ax.axvline(self.b, color='red', linestyle='dashed')

        # Оси OX и OY
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)

        # Добавление подписей осей и заголовка
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('График функции')

        # Отображение графика
        plt.show()

        mw.math_calculations()

        self.btn1.config(relief='raised')
        self.btn1.config(state='normal')



    def math_calculations(self):
        '''Выполняет математические расчеты.'''
        
        dx = (self.b - self.a) / self.N  # Шаг интегрирования
        x = np.linspace(self.a, self.b, 100)  # Массив точек x
        y = self.func(x)  # Значения функции в точках x

        integral = np.sum(y) * dx  # Площадь под графиком (простая сумма)

        # Создание случайных точек для визуализации
        random_x = np.random.uniform(self.a, self.b, self.N)
        random_y = self.func(random_x)

        # Визуализация точек и вывод результатов
        mw.show_results(x, y, integral, random_x, random_y)



    def show_results(self, x, y, integral, random_x, random_y):
        '''Визуализирует точки и выводит непосредственный ответ.'''
        
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



if __name__ == "__main__":
    mw = MainWindow() # Создаем объект класса MainWindow.
    mw.main_window() # Вызываем метод на объекте, запускаем цепочку остальных функций.