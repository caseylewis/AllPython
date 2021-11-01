# from App_BudgetHelper.BudgetHelperApp import *
# from App_BudgetHelper.accounts import *
# from abc import abstractmethod
# from App_BudgetHelper.AbstractData import *
import tkinter as tk


class PieChart(tk.Canvas):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Tkinter Bar and Pie Graph")

    # here is for bar chart............

    tk.Label(root, text='Bar Chart').pack()
    data = [21, 20, 19, 16, 14, 45, 11, 9, 4, 3]
    c_width = 400
    c_height = 350
    c = tk.Canvas(root, width=c_width, height=c_height, bg='white')
    c.pack()

    # experiment with the variables below size to fit your needs

    y_stretch = 15
    y_gap = 20
    x_stretch = 10
    x_width = 20
    x_gap = 20
    for x, y in enumerate(data):
        # calculate reactangle coordinates
        x0 = x * x_stretch + x * x_width + x_gap
        y0 = c_height - (y * y_stretch + y_gap)
        x1 = x * x_stretch + x * x_width + x_width + x_gap
        y1 = c_height - y_gap
        # Here we draw the bar
        c.create_rectangle(x0, y0, x1, y1, fill="red")
        c.create_text(x0 + 2, y0, anchor=tk.SW, text=str(y))

    def prop(n):
        value = 360.0 * n / 1000
        print(value)
        return value


    tk.Label(root, text='Pie Chart').pack()
    c = tk.Canvas(width=154, height=154)
    c.pack()

    colors = [
        'red',
        'blue',
        'green',
        'yellow',
        'orange',
        'purple'
    ]
    data_values = [
        100,
        150,
        300,
        400,
        350,
        500,
        # 600
    ]
    # start = prop(0)
    # for color, value in zip(colors, data_values):
    #     c.create_arc((2, 2, 152, 152), fill=color, outline=color, start=prop(start), extent=prop(value))
    #     start = value
    # start = prop(0)

    # # ORIGINAL CODE
    c.create_arc((2,2,152,152), fill=colors[0], outline="#FAF402", start=prop(0), extent = prop(100))
    c.create_arc((2,2,152,152), fill=colors[1], outline="#2BFFF4", start=prop(100), extent = prop(400))
    c.create_arc((2,2,152,152), fill=colors[2], outline="#E00022", start=prop(600), extent = prop(50))
    c.create_arc((2,2,152,152), fill=colors[3], outline="#7A0871", start=prop(650), extent = prop(200))
    c.create_arc((2,2,152,152), fill=colors[4], outline="#294994", start=prop(850), extent = prop(150))

    root.mainloop()
