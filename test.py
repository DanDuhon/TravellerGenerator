import tkinter as tk

class HexGrid(tk.Canvas):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.lines = set()  # set to store lines that have already been drawn

    def draw_hex(self, x, y, r):
        points = [(x + r * math.cos(angle), y + r * math.sin(angle))
                for angle in (0, math.pi/3, 2*math.pi/3, math.pi, 4*math.pi/3, 5*math.pi/3, 0)]
        for i in range(6):
            self.create_line(points[i], points[i+1])
        if x % (2*r) != 0:
            y += r * math.sin(math.pi/3) * 2  # add an offset to y for every other column


if __name__ == '__main__':
    import math

    root = tk.Tk()
    canvas = HexGrid(root, width=500, height=500)
    canvas.pack()

    r = 50
    for i in range(10):
        for j in range(10):
            x = (i + (j % 2) / 2) * r * math.sqrt(3)
            y = j * r * 1.5
            canvas.draw_hex(x, y, r)

    root.mainloop()
