import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from tkinter import messagebox
from singleton import SingletonClass
import sympy as sp


class MainWindow(SingletonClass): # Класс наследует поведение Singleton, чтобы был лишь один экземпляр главного окна.

    def __init__(self):
        '''Инициализирует переменные, использующиеся в классе.'''
        self.func = None
        self.a = None
        self.b = None
        self.N = None

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
            btn1.config(relief='sunken') # Делаем кнопку нажатой.
            btn1.config(state='disabled') # Отключаем возможность нажать кнопку.
            func = entry1.get() # Сохраняем вводы в глобальные переменные.
            a = entry2.get()
            b = entry3.get()
            N = entry4.get()
            if UserInput().user_input(a, b, N, func):
                print('success') # !!! Передача дальнейших инструкций.


        btn1 = tk.Button(root, text='▶️', # Создаем и настраиваем кнопку запуска вычислений.
                            command=start,
                            bg='#EDEDED',
                            activebackground='#D7D9DB')
        btn1.grid(row=6,column=0, stick='w') # Располагаем кнопку на экране.


        root.grid_columnconfigure(0, minsize=100) # Настраиваем размер сетки в окне.
        root.grid_columnconfigure(1, minsize=10)
        root.grid_columnconfigure(2, minsize=10)

        root.grid_rowconfigure(1, minsize=30)
        root.grid_rowconfigure(3, minsize=30)
        root.grid_rowconfigure(5, minsize=30)


        root.mainloop() # Вечный цикл, в течении которого окно будет запущено.


class UserInput:

    def __init__(self):
        self.x = None
        self.y = None

    def user_input(self, a, b, N, func):
        '''Принимает и проверяет введенные пользователем данные.'''
        # Преобразовываем функцию в нужный matplotlib вид.
        # Строим график (но не выводим), проверяем замкнутость области.
        
        # Проверка корректности N.
        if not N.isdigit():
            messagebox.showerror("Ошибка", "Количество точек N должно быть целым числом!")
            return False
        elif int(N) < 100:
            messagebox.showerror("Ошибка", "Минимальное количество точек: 100!")
            return False

        # Проверка корректности a, b, N.
        variable_names = []  # Инициализируем переменную пустым списком
        try:
            a = int(a)
            b = int(b)
            N = int(N)
        except ValueError as e:
            variables = {'a': a, 'b': b, 'N': N}
            for var_name, var_value in variables.items():
                try:
                    int(var_value)
                except ValueError:
                    variable_names.append(var_name)
            
            error_message = f"Значение {' и '.join(variable_names)} должно быть целым числом!"
            messagebox.showerror("Ошибка", error_message)
            return False
        
        # Проверка корректности func.
        

        return True # !!! ОБРАТНО СДЕЛАТЬ КНОПКУ ДОСТУПНОЙ!!!
        
        x = np.linspace(-40, 40, 10000)
        y = MainWindow.func


class Plot:

    def __init__(self):
        pass


    def plot(self):
        '''Строит график.'''
        pass


class MathCalculations:

    def __init__(self):
        pass


    def math_calculations(self):
        '''Выполняет математические расчеты.'''
        pass


class ShowResults:

    def __init__(self):
        pass


    def show_results(self):
        '''Визуализирует точки и выводит непосредственный ответ.'''
        pass


if __name__ == "__main__":
    mw = MainWindow() # Создаем объект класса MainWindow.
    mw.main_window() # Вызываем метод на объекте.