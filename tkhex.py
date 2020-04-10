import tkinter

import systemhex

#TODO: Max/Min Zoom
#TODO: Zoom from mouse
#TODO: Avoid double line drawing

class Colors:
    hex = "#a1e2a1"
    background = "white"
    selected = "#53ca53"
    edges = "black"

class SystemDisplay:
    """ Displays the Universe on a hex grid """
    def __init__(self, *args, **kwargs):
        self.hexaSize = 50
        self.click_location = (0, 0)
        self.hexagonlist = {}
        self.selected = None

        tk = tkinter.Tk()

        tk.title("Travellers Universe")
        tk.grid_columnconfigure(0, weight=1)
        tk.grid_rowconfigure(0, weight=1)

        self.canvas = tkinter.Canvas(tk,
                background=Colors.background,
                width=800, height=600,
                *args, **kwargs)

        self.canvas.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.keybindings()

        for system in systemhex.allSystems:
            self.create_hexagon(system.horizontalCoord, system.verticalCoord)
        
        self.info = tkinter.Label(tk, width=50)
        self.info.grid(row=0, column=1)

        tk.mainloop()

    def set_text(self, text):
        """Sets the text for the side panel"""
        self.info.config(text=text)

    def create_hexagon(self, xCell, yCell):
        """
        Creates hexagon at cubic grid location xCell, yCell, -xCell-yCell
        Computes coordinates of 6 points relative to a center position.
        Point are numbered following this schema :

        Points in euclidiean grid:  
                    6

                5       1
                    .
                4       2

                    3

        """
        size = self.hexaSize
        Δx = (size**2 - (size/2)**2)**0.5
        
        #compute pixel coordinate of the center of the cell:
        pixel_x = Δx*(xCell-yCell)+400
        pixel_y = -1.5*size*(xCell+yCell)+300

        point1 = (pixel_x+Δx, pixel_y+size/2)
        point2 = (pixel_x+Δx, pixel_y-size/2)
        point3 = (pixel_x   , pixel_y-size  )
        point4 = (pixel_x-Δx, pixel_y-size/2)
        point5 = (pixel_x-Δx, pixel_y+size/2)
        point6 = (pixel_x   , pixel_y+size  )

        width = 2
        self.canvas.create_line(point1, point2, fill=Colors.edges, width=width)
        self.canvas.create_line(point2, point3, fill=Colors.edges, width=width)
        self.canvas.create_line(point3, point4, fill=Colors.edges, width=width)
        self.canvas.create_line(point4, point5, fill=Colors.edges, width=width)
        self.canvas.create_line(point5, point6, fill=Colors.edges, width=width)
        self.canvas.create_line(point6, point1, fill=Colors.edges, width=width)

        tags = "{},{}".format(xCell, yCell)
        hexagon_id = self.canvas.create_polygon(point1, point2, point3, point4, point5, point6, fill=Colors.hex, tags=tags)
        self.hexagonlist[hexagon_id] = tags

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
        self.click_location = (event.x, event.y)

    def do_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def do_release(self, event):
        xorig, yorig = self.click_location
        distance = abs(xorig - event.x) + abs(yorig - event.y)
        if distance > 5: #Only select a cell if clicked without (much) draggging
            return

        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        for hexagon_id in self.canvas.find_overlapping(x, y, x, y):
            if hexagon_id in self.hexagonlist:
                self.select(hexagon_id)
                break

    def select(self, id):
        """Selects a particular hexigon for information detail by tk id"""
        if self.selected:
            tag = self.hexagonlist[self.selected]
            self.canvas.itemconfigure(tag, fill=Colors.hex)

        self.selected = id
        tag = self.hexagonlist[self.selected]
        self.canvas.itemconfigure(tag, fill=Colors.selected)

        t1, t2 = [int(x) for x in tag.split(",")]
        coord = (t1, t2)
        system = systemhex.allCoordinates[coord]

        text = "Name: {}\n".format(system.name)
        text += "Age: {}\n".format((system.horizontalCoord, system.verticalCoord))

        self.set_text(text)
