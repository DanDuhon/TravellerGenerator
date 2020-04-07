import tkinter
import systemhex

#TODO: Max/Min Zoom
#TODO: Zoom from mouse

class SystemDisplay:
    """ Displays the Universe on a hex grid """
    def __init__(self, *args, **kwargs):
        self.hexaSize = 50
        self.click_loc = (0, 0)
        self.hexagonlist = {}
        self.selected = None

        tk = tkinter.Tk()

        tk.title("Travellers Universe")
        tk.grid_columnconfigure(0, weight=1)
        tk.grid_rowconfigure(0, weight=1)

        self.canvas = tkinter.Canvas(tk,
                background='white',
                width=800, height=600,
                *args, **kwargs)

        self.canvas.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.keybindings()

        for system in systemhex.allSystems:
            self.setCell(system.horizontalCoord, system.verticalCoord)
        
        self.info = tkinter.Label(tk, width=50)
        self.info.grid(row=0, column=1)
        
        tk.mainloop()

    def set_text(self, text):
        self.info.config(text=text)
    
    def create_hexagone(self, x, y, tags, fill="#a1e2a1"):
        """ 
        Creates hexagon at pixel cordinates x, y
        Compute coordinates of 6 points relative to a center position.
        Point are numbered following this schema :

        Points in euclidiean grid:  
                    6

                5       1
                    .
                4       2

                    3

        """
        size = self.hexaSize
        width = 2
        Δx = (size**2 - (size/2)**2)**0.5

        point1 = (x+Δx, y+size/2)
        point2 = (x+Δx, y-size/2)
        point3 = (x   , y-size  )
        point4 = (x-Δx, y-size/2)
        point5 = (x-Δx, y+size/2)
        point6 = (x   , y+size  )

        self.canvas.create_line(point1, point2, width=width)
        self.canvas.create_line(point2, point3, width=width)
        self.canvas.create_line(point3, point4, width=width)
        self.canvas.create_line(point4, point5, width=width)
        self.canvas.create_line(point5, point6, width=width)
        self.canvas.create_line(point6, point1, width=width)

        hexagon = self.canvas.create_polygon(point1, point2, point3, point4, point5, point6, fill=fill, tags=tags)
        self.hexagonlist[hexagon] = tags

    def setCell(self, xCell, yCell, *args, **kwargs ):
        """ Creates hexagon at cubic grid location xCell, yCell, -xCell-yCell"""

        #compute pixel coordinate of the center of the cell:
        size = self.hexaSize
        Δx = (size**2 - (size/2)**2)**0.5

        pix_x = Δx*(xCell-yCell)
        pix_y = -1.5*size*(xCell+yCell)

        tag = "{},{}".format(xCell, yCell)

        self.create_hexagone(pix_x, pix_y, tag, *args, **kwargs)

    def keybindings(self):
        self.canvas.bind("<MouseWheel>", self.do_zoom)
        self.canvas.bind('<ButtonPress-1>', self.do_click)
        self.canvas.bind('<ButtonRelease-1>', self.do_release)
        self.canvas.bind("<B1-Motion>", self.do_drag)

    def do_zoom(self, event):
        factor = 1.001 ** event.delta
        self.canvas.scale(tkinter.ALL, event.x, event.y, factor, factor)

    def do_click(self, event):
        self.canvas.scan_mark(event.x, event.y)
        self.click_loc = (event.x, event.y)

    def do_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def do_release(self, event):
        dist = abs(self.click_loc[0] - event.x) + abs(self.click_loc[1] - event.y)
        if dist > 5:
            return
        clicklist = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for h in clicklist:
            self.select(h)

    def select(self, id):
        if id not in self.hexagonlist:
            return

        if self.selected:
            tag = self.hexagonlist[self.selected]
            self.canvas.itemconfigure(tag, fill="#a1e2a1")

        self.selected = id
        tag = self.hexagonlist[self.selected]
        self.canvas.itemconfigure(tag, fill="#53ca53")

        t1, t2 = [int(x) for x in tag.split(",")]
        coord = (t1, t2, -t1-t2)
        system = systemhex.allCoordinates[coord]

        text = "Name: {}\n".format(system.name)
        text += "Age: {}\n".format(system.age)

        self.set_text(text)
