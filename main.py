import tkinter as tk # GUI
import matplotlib.pyplot as plt # График.
import numpy as np # Математика для графика.
from tkinter import messagebox # Вывод ошибок.
from singleton import SingletonClass # Паттерн для создания лишь одного главного окна.

class MainWindow(SingletonClass): # Класс наследует поведение Singleton, чтобы был лишь один экземпляр главного окна.
    '''Хранит все основные переменные в атрибутах объекта.'''
    
    def __init__(self):
        '''Инициализирует переменные, использующиеся в классе.'''

        self.func = None
        self.a = None
        self.b = None
        self.N = None
        self.btn1 = None



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
        
        # Проверка корректности N.
        if not self.N.isdigit():
            messagebox.showerror("Ошибка", "Количество точек N должно быть целым числом!")
            self.btn1.config(relief='raised')  # Возвращаем relief в исходное состояние 'raised'
            self.btn1.config(state='normal')  # Возвращаем state в исходное состояние 'normal'
            return False
        elif int(self.N) < 100:
            messagebox.showerror("Ошибка", "Минимальное количество точек: 100!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False

        # Проверка корректности a, b, N.
        variable_names = []  # Инициализируем переменную пустым списком
        try:
            self.a = int(self.a)
            self.b = int(self.b)
            self.N = int(self.N)
        except ValueError as e:
            variables = {'a': self.a, 'b': self.b, 'N': self.N}
            for var_name, var_value in variables.items():
                try:
                    int(var_value)
                except ValueError:
                    variable_names.append(var_name)
            
            error_message = f"Значение {' и '.join(variable_names)} должно быть целым числом!"
            messagebox.showerror("Ошибка", error_message)
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False
        
        # Проверка корректности границ.
        if self.a >= self.b:
            messagebox.showerror("Ошибка", "a должно быть меньше b!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False

        # Проверка корректности func.
        try:
            # Удаление "y=" и замена ^ на **
            self.func = self.func.replace("y=", "")
            self.func = self.func.replace('^', '**')
            x = np.array([0])  # Произвольное значение для проверки синтаксиса
            np.sin(x)
            np.cos(x)
            np.exp(x)
            eval(self.func, {'__builtins__': None}, {'x': x, 'sin': np.sin, 'cos': np.cos, 'exp': np.exp})
        except (SyntaxError, NameError):
            messagebox.showerror("Ошибка", "введена неправильная функция!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False

        # Проверка замкнутости графика.
        x = np.linspace(self.a, self.b, 100)
        try:
            y = eval(self.func)
        except NameError:
            messagebox.showerror("Ошибка", "неправильно задана функция!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False

        fig, ax = plt.subplots()
        ax.plot(x, y)

        if plt.fignum_exists(fig.number):
            plt.close(fig)  # Закрываем временный график
        else:
            messagebox.showerror("Ошибка", "область графика не замкнута!")
            self.btn1.config(relief='raised')
            self.btn1.config(state='normal')
            return False

        return True



    def plot(self):
        '''Строит график.'''

        compiled_func = compile("lambda x: " + self.func, "<string>", "eval")
        self.func = eval(compiled_func)

        x = np.linspace(self.a-10, self.b+10, 100)
        y = self.func(x)

        fig, ax = plt.subplots()

        # Построение графика функции
        ax.plot(x, y)

        # Добавление условных границ интегрирования
        ax.axvline(self.a, color='red', linestyle='dashed')
        ax.axvline(self.b, color='red', linestyle='dashed')

        # Оси OX и OY
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

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
        x = np.linspace(self.a, self.b, self.N)  # Массив точек x
        y = self.func(x)  # Значения функции в точках x

        integral = np.sum(y) * dx  # Площадь под графиком (простая сумма)
        print(integral)

        # Визуализация точек и вывод результатов
        mw.show_results(x, y, integral)



    def show_results(self):
        '''Визуализирует точки и выводит непосредственный ответ.'''
        pass



if __name__ == "__main__":
    mw = MainWindow() # Создаем объект класса MainWindow.
    mw.main_window() # Вызываем метод на объекте, запускаем цепочку остальных функций.