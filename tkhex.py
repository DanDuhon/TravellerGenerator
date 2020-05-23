import inspect
import itertools
import tkinter

import systemhex

# TODO: Max/Min Zoom
# TODO: Zoom from mouse
# TODO: Avoid double line drawing


class Colors:
    hex = "#a1e2a1"
    hexoutline = 'black'
    background = "white"
    selected = "#53ca53"
    star1 = "Yellow"
    star2 = "Yellow3"
    systembackground = "black"
    hexhover = "#53e2a1"
    planet = 'brown'
    luminosity = {
            "A": ("#CDDBFF", "#A4B0CD"),
            "F": ("#EFEFFD", "#C1C1CD"),
            "G": ("#FDEEE7", "#CDC1BA"),
            "K": ("#FFDBB8", "#CDB093"),
            "M": ("#FFB366", "#CD8F52"),
            "L": ("#FF7E11", "#CD670E"),
            "D": ("white", "#CDCDCD")
    }

class SystemDisplay:
    """ Displays the Universe on a hex grid """

    def __init__(self):
        self.hexaSize = 50
        self.click_location = (0, 0)
        self.hexagonlist = {}
        self.starlist = {}
        self.selected = None
        self.selectmarks = []
        self.planet_selectmarks = []

        tk = tkinter.Tk()

        tk.title("Travellers Universe")
        tk.grid_columnconfigure(0, weight=1)
        tk.grid_rowconfigure(4, weight=1)

        def hello():
            pass

        menubar = tkinter.Menu(tk)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=hello)
        filemenu.add_command(label="Save", command=hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=tk.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # create more pulldown menus
        editmenu = tkinter.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=hello)
        editmenu.add_command(label="Copy", command=hello)
        editmenu.add_command(label="Paste", command=hello)
        menubar.add_cascade(label="Edit", menu=editmenu)

        helpmenu = tkinter.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About", command=hello)
        menubar.add_cascade(label="Help", menu=helpmenu)

        tk.config(menu=menubar)

        # Galaxy Screen
        self.galaxy = tkinter.Canvas(tk,
                                     background=Colors.background,
                                     width=600, height=600)

        self.galaxy.grid(row=0, column=0, rowspan=5, sticky='nsew')

        self.galaxykeybindings()

        for system in systemhex.allSystems:
            self.create_hexagon(system)

        # System Label
        self.systemlabel = tkinter.Label(tk, width=40, height=1)
        self.systemlabel.grid(row=0, column=1)

        # System Screen
        self.system = tkinter.Canvas(tk,
                background=Colors.systembackground,
                width=300, height=200)
        self.system.grid(row=1, column=1, sticky='n')

        # Star Label
        self.starlabel = tkinter.Label(tk, width=40, height=1)
        self.starlabel.grid(row=2, column=1)

        # Star Screen
        self.star = tkinter.Canvas(tk,
                background='green',
                width=300, height=200)
        self.star.grid(row=3, column=1, sticky='n')

        # Planet Label
        self.planetlabel = tkinter.Label(tk, width=40, height=1, anchor="n")
        self.planetlabel.grid(row=4, column=1)

        # Info Panel
        self.info = tkinter.Label(tk, width=40, justify="left", wraplength=250, anchor="nw")
        self.info.grid(row=0, column=2, rowspan=5)

        tk.mainloop()

    def set_info(self, object):
        infotext = []
        for x in inspect.getmembers(object):
            if x[0].startswith('_'):
                continue
            if inspect.ismethod(x[1]):
                continue
            infotext.append(": ".join(str(i)[:200] for i in x))
        self.info.config(text="\n".join(infotext))

    def create_hexagon(self, system):
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
        xCell, yCell = system.horizontalCoord, system.verticalCoord

        size = self.hexaSize
        Δx = (size**2 - (size / 2)**2)**0.5
        # compute pixel coordinate of the center of the cell:
        pixel_x = Δx * (xCell - yCell) + 300
        pixel_y = -1.5 * size * (xCell + yCell) + 300

        p1 = (pixel_x + Δx, pixel_y + size / 2)
        p2 = (pixel_x + Δx, pixel_y - size / 2)
        p3 = (pixel_x, pixel_y - size)
        p4 = (pixel_x - Δx, pixel_y - size / 2)
        p5 = (pixel_x - Δx, pixel_y + size / 2)
        p6 = (pixel_x, pixel_y + size)

        tag = "{},{}".format(xCell, yCell)
        hexagon_id = self.galaxy.create_polygon(
            p1, p2, p3, p4, p5, p6,
            fill=Colors.hex,
            outline=Colors.hexoutline,
            width=2,
            tags=tag)
        self.hexagonlist[hexagon_id] = tag

        osize = 5
        for i, star in enumerate(system.stars):
            centerx = pixel_x - Δx / 2 + (2 * i + (4 - len(system.stars))) * Δx / 6
            centery = pixel_y + size / 3
            self.galaxy.create_oval(
                    centerx - osize, centery - osize,
                    centerx + osize, centery + osize,
                    fill=Colors.luminosity[star.luminosityClass[0]][0],
                    width=0, state="disabled")

        def clickhex_create(hexagon_id):
            def clickhex(event):
                xorig, yorig = self.click_location
                distance = abs(xorig - event.x) + abs(yorig - event.y)
                # Only select a cell if clicked without (much) dragging
                if distance > 5:
                    return
                self.selectsystem(hexagon_id)
            return clickhex

        self.galaxy.tag_bind(hexagon_id, '<ButtonRelease-1>', clickhex_create(hexagon_id))
        # self.galaxy.tag_bind(hexagon_id, '<Enter>', lambda event,id=hexagon_id:clickhex(event,id))

        def hoverhex_create(hexagon_id):
            def hoverhex(event):
                if hexagon_id != self.selected:
                    self.galaxy.itemconfigure(hexagon_id, fill=Colors.hexhover)
            return hoverhex

        self.galaxy.tag_bind(hexagon_id, '<Enter>', hoverhex_create(hexagon_id))

        def hoverhexleave_create(hexagon_id):
            def hoverhex(event):
                if hexagon_id != self.selected:
                    self.galaxy.itemconfigure(hexagon_id, fill=Colors.hex)
            return hoverhex

        self.galaxy.tag_bind(hexagon_id, '<Leave>', hoverhexleave_create(hexagon_id))

    def galaxykeybindings(self):
        self.galaxy.bind("<MouseWheel>", self.do_zoom)
        self.galaxy.bind('<ButtonPress-1>', self.do_click)
        self.galaxy.bind("<B1-Motion>", self.do_drag)

    def do_zoom(self, event):
        factor = 1.001 ** event.delta
        self.galaxy.scale(tkinter.ALL, event.x, event.y, factor, factor)

    def do_click(self, event):
        self.galaxy.scan_mark(event.x, event.y)
        self.click_location = (event.x, event.y)

    def do_drag(self, event):
        self.galaxy.scan_dragto(event.x, event.y, gain=1)

    def selectsystem(self, id):
        """Selects a particular hexigon for information detail by tk id"""
        if self.selected:
            tag = self.hexagonlist[self.selected]
            self.galaxy.itemconfigure(tag, fill=Colors.hex)
            self.clearsystem()

        self.selected = id
        tag = self.hexagonlist[self.selected]
        self.galaxy.itemconfigure(tag, fill=Colors.selected)

        t1, t2 = [int(x) for x in tag.split(",")]
        coord = (t1, t2, -t1 - t2)
        system = systemhex.allCoordinates[coord]

        text = "Name: {}\n".format(system.name)
        text += "Coordinates: {}\n".format((system.horizontalCoord, system.verticalCoord))

        self.info.config(text=text)
        self.systemlabel.config(text=system.name)

        def clicksystem_create(star):
            def clicksystem(event):
                self.selectstar(star)
            return clicksystem

        x, y = 60, -50
        size = 20
        for i, star in enumerate(system.stars):
            star_id = self.system.create_oval(
                    x-size, 100+y-size, x+size, 100+y+size,
                    fill=Colors.luminosity[star.luminosityClass[0]][0],
                    outline=Colors.luminosity[star.luminosityClass[0]][1],
                    width=2, tags=str(i))
            self.starlist[star_id] = star
            self.system.tag_bind(star_id, '<Button-1>', clicksystem_create(star))
            x += 60
            y = -y

        self.set_info(system)

    def selectstar(self, star):
        self.clearstar()
        self.starlabel.config(text=star.name)
        x_center = 60 * star.starNumber
        y_center = 100 + 50 * (-1)**star.starNumber
        outer = 30
        inner = 20

        for adj_x, adj_y in itertools.product((-1,1), repeat=2):
            selectionmark_id = self.system.create_line(
                    (x_center + inner * adj_x, y_center + outer * adj_y),
                    (x_center + outer * adj_x, y_center + outer * adj_y),
                    (x_center + outer * adj_x, y_center + inner * adj_y),
                    fill="white", width=3)
            self.selectmarks.append(selectionmark_id)

        size = 600
        overhang = 30
        self.star.create_oval(
                overhang - size, 100 - size / 2,
                overhang, 100 + size / 2,
                fill=Colors.luminosity[star.luminosityClass[0]][0],
                outline=Colors.luminosity[star.luminosityClass[0]][1],
                width = 10)

        def clickstar_create(planet):
            def clickstar(event):
                self.selectplanet(planet)
            return clickstar

        size = 15
        for planet in star.planets:
            row, column = divmod(planet.order, 10)
            x_center = 20 * column + 50 + 10 * row
            y_center = 30 * row + 20
            planet_id = self.star.create_oval(
                    x_center + size / 2, y_center + size / 2,
                    x_center - size / 2, y_center - size / 2,
                    fill=Colors.planet)
            self.star.tag_bind(planet_id, '<Button-1>', clickstar_create(planet))

        self.set_info(star)

    def selectplanet(self, planet):
        for id in self.planet_selectmarks:
            self.star.delete(id)
        self.planet_selectmarks = []

        row, column = divmod(planet.order, 10)
        x_center = 20 * column + 50 + 10 * row
        y_center = 30 * row + 20
        outer = 11
        inner = 8

        for adj_x, adj_y in itertools.product((-1,1), repeat=2):
            selectionmark_id = self.star.create_line(
                    (x_center + inner * adj_x, y_center + outer * adj_y),
                    (x_center + outer * adj_x, y_center + outer * adj_y),
                    (x_center + outer * adj_x, y_center + inner * adj_y),
                    fill="white", width=2)
            self.planet_selectmarks.append(selectionmark_id)

        self.set_info(planet)
        self.planetlabel.config(text=planet.name)

    def clearsystem(self):
        self.systemlabel.config(text="")
        self.system.delete("all")
        self.starlist = {}

        self.clearstar()

    def clearstar(self):
        for id in self.selectmarks:
            self.system.delete(id)
        self.selectmarks = []
        self.starlabel.config(text="")
        self.star.delete("all")
        self.planet_selectmarks = []
        self.planetlabel.config(text="")

