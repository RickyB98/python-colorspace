
from cslogger import cslogger
log = cslogger(__name__)

# Tkinter was renamed to tkinter Py2->Py3,
# make sure the correct module is loaded.
import sys
if sys.version_info.major < 3:
    from Tkinter import *
else:
    from tkinter import *


class ddObject(object):

    def __init__(self, parent, name, init_args = None):

        self.parent   = parent
        self.master   = parent.master
        self.palettes = parent.palettes
        self.sliders  = parent._sliders_
        self.name     = name

        # Adding options menu
        opts = parent.palettes.get_palette_types()

        # If init args contain type: use this type
        type_ = None # Default/not selected
        if not init_args == None:
            if "type" in init_args.keys():
                type_ = init_args["type"]
                if not type_ in opts:
                    log.error("Selected palette type \"{:s}\" does not exist. Stop.".format(type_))
                    sys.exit(9)
        type_ = opts[0] if type_ is None else type_

        # Adding dropdown menu with default arguments if init_args
        # was empty, or the settings provided by the user stored on
        # init_args (slider settings, selected dropdown item, ...)
        dropOpts = StringVar(parent.master)
        dropOpts.set(type_) # default value
        self.selected(type_, init_args) # Initialize palettes

        #self.dd_type = apply(OptionMenu, (self.master, dropOpts) + tuple(opts))
        self.dd = OptionMenu(parent.master, dropOpts, *opts,
                   command = self.selected)
        self.dd.config(width = 25, pady = 5, padx = 5)
        self.dd.grid(column = 1, row = len(opts))
        self.dd.place(x = 10, y = 30)
    
    def selected(self, val, args = None):

        self._selected_ = val
        pals = self.palettes.get_palettes(val)

        self._set_sliders_(pals[0], args)
        if hasattr(self.parent, "dd_type"):
            self.parent._add_palette_frame_()

    def get(self):
        return self._selected_
    
    def getmethod(self):
        # Simply return the method of the first palette
        # in the list of palettes given the current selection.
        tmp = self.palettes.get_palettes(self.get())
        return tmp[0]._method_

    def _set_sliders_(self, pal, args = None):

        if args is None: args = {}

        # Allowed parameter
        parameter = pal.parameters()

        for key,elem in self.sliders.items():
            slider_id = elem.getid()
            value     = pal.get(slider_id)
            # Disable slider if not in paramter, enable
            # if it is.
            if not slider_id in parameter + ["n"]:
                elem.disable()
            else:
                elem.enable()
            # Take value from "args" if specified, else
            # the one from the palette.
            if slider_id in args.keys():  value = args[slider_id]
            if not value is None:         elem.setvalue(value)


    def _add_dropdown_palettes_(self):

        opts = self.palettes.get_palette_types()

        dropOpts = StringVar(self.master)
        dropOpts.set(opts[0]) # default value

        obj = ddObject("type")

        #self.dd_type = apply(OptionMenu, (self.master, dropOpts) + tuple(opts))
        self.dd_type = OptionMenu(self.master, dropOpts, *opts,
                        command = obj.selected)
        self.dd_type.config(width = 25, pady = 5, padx = 5)
        self.dd_type.grid(column = 1, row = len(opts))
        self.dd_type.place(x = 10, y = 30)


class defaultpalettecanvas(object):

    def __init__(self, parent, pal, n, xpos, figwidth, figheight):  

        self._parent_ = parent
        self._pal_    = pal

        colors = pal.colors(n)
        self._draw_canvas_(colors, xpos, figwidth, figheight)

    def _activate_(self, event):

        # Loading settings of the current palette
        sliders  = self._parent_._sliders_
        settings = self._pal_.get_settings()
        for key,elem in sliders.items():
            sid = elem.getid()
            if sid in settings.keys(): elem.setvalue(settings[sid])

        # Change slider settings
        parent = self._parent_


    def _draw_canvas_(self, colors, xpos, figwidth, figheight):

        offset = 3 # White frame around the palettes
        n = len(colors)
        h = (figheight - 2. * offset) / len(colors)
        w = figwidth  - 2. * offset

        canvas = Canvas(self._parent_._palframe_, width = figwidth,
                        height = figheight, bg = "#ffffff")
        canvas.place(x = xpos, y = 0)
        # Binding for interaction
        canvas.bind("<Button-1>", self._activate_)

        for i in range(0, n):
            canvas.create_rectangle(0, i*h, w, (i+1)*h,
                                    width = 0, fill = colors[i])
            

class currentpalettecanvas(object):

    def __init__(self, parent, x, y, width, height):

        self.parent = parent
        self.x      = x
        self.y      = y
        self.width  = width
        self.height = height

        self.canvas = Canvas(self.parent, width = self.width, height = self.height)
        self.canvas.place(x = self.x, y = self.y + 20)


    def _draw_canvas_(self, colors):

        n = len(colors)
        w = float(self.width) / float(len(colors))
        h = self.height
        for i in range(0, n):
            # Dropping Nan's
            if len(str(colors[i])) < 7: continue
            self.canvas.create_rectangle(i*w, 0, (i+1)*w, h,
                    width = 0, fill = colors[i])


class sliderObject(object):

    #FGDISABLED = "#b0b0b0"
    #BGDISABLED = "#b0b0b0"
    #FGACTIVE   = "#dadada"
    #BGACTIVE   = "#efefef"
    FGACTIVE = "#b0b0b0"
    BGACTIVE = "#b0b0b0"
    FGDISABLED   = "#dadada"
    BGDISABLED   = "#efefef"
    DISABLED  = "#b0b0b0"
    BGDEFAULT   = "#d9d9d9"

    def __init__(self, name, parent, bgcolor = "#d9d9d9"):

        self.name      = name
        self.BGDEFAULT = bgcolor
        self.parent    = parent

        # Store the tag
        import re
        mtch = re.match("^slider_(.*)$", name)
        if not mtch:
            log.error("Whoops, slider name does not match \"^slider_(.*)$\".")
            sys.exit(9)
        self.id = mtch.group(1).lower()

    def callback(self, event):
        self.value.delete("1.0", END)
        self.value.insert(INSERT,event)
        self.value.tag_add("right", "1.0", "end")

        self._plot_current_colormap_()

    def _plot_current_colormap_(self):

        self.parent._curpalcanvas_draw_()

    def getname(self):
        return self.name

    def getid(self):
        return self.id

    def setvalue(self, val = None):
        # Reading text value and adjust slider
        if not val:
            val = self.value.get("1.0",END)
        self.slider.set(val)

    def getvalue(self):
        # Reading text value and adjust slider
        return self.value.get("1.0", END)

    def bind(self, slider, label, value, button):
        self.slider = slider
        self.label  = label
        self.value  = value
        self.button = button

    def disable(self):
        self.slider.configure(state = "disabled",
                relief = FLAT,
                bg = self.FGDISABLED,
                activebackground = self.FGDISABLED,
                troughcolor = self.BGDISABLED)
        self.label.configure(fg = self.DISABLED)
        self.value.configure(state = "disabled",
                relief = FLAT,
                fg = self.DISABLED,
                bg = self.BGDISABLED)
        self.button.configure(state = "disabled",
                relief = FLAT,
                fg = self.DISABLED,
                bg = self.BGDISABLED)

    def enable(self):
        self.slider.configure(state = "active",
                bg = self.FGACTIVE,
                activebackground = self.FGACTIVE,
                troughcolor = self.BGACTIVE)
        self.label.configure(fg = "black")
        self.value.configure(state = "normal",
                relief = FLAT,
                fg = "#000000", bg = "white")
        self.button.configure(state = "active",
                relief = RAISED, 
                fg = "#000000", bg = self.BGDEFAULT)

    def is_active(self):

        return self.slider.config()["state"][4] == "active"


class choose_palette(object):

    FRAMEHEIGHT = 100
    FRAMEWIDTH  = 280
    WIDTH = 300
    HEIGHT = 600

    _sliders_ = {}
    _demoTk_ = None

    def __init__(self, **kwargs):

        from . import hclpalettes
        self.palettes = hclpalettes()

        # Initialization arguments, if any
        init_args = {}
        # Default if no inputs are set
        if not "palette" in kwargs.keys():  palette = "Blue-Red"
        else:                               palette = kwargs["palette"]

        # Find initial values
        pal = self.palettes.get_palette(palette)
        # Store palette name and palette type to select
        # the correct dropdown entries
        init_args["name"] = pal.name()
        init_args["type"] = pal.type()
        for key,val in pal.get_settings().items():
            init_args[key] = val

        # Custom user arguments on top
        for key,val in kwargs.items(): init_args[key] = val

        # Initialize gui
        self._init_master_()
        # Adding current palette has to be before the sliders
        # as they need the current palette canvas for the
        # to be able to be reactive.
        self._add_current_palette_canvas_()
        self._add_sliders_()
        self._add_demo_options_()
        self._add_close_button_()
        self._add_return_button_()
        # Has to be called _after_ sliders have been added
        self._add_dropdown_type_(init_args = init_args)
        # Drawing default palettes
        self._add_palette_frame_()


        mainloop()


    def _init_master_(self):

        # initialize mater TK interface
        self.master = Tk()
        self.master.wm_title("Colorspace - Choose Color Palette")
        self.master.configure()
        self.master.resizable(width=False, height=False)
        self.master.geometry("{:d}x{:d}".format(self.WIDTH, self.HEIGHT))


    def _add_palette_frame_(self):

        if hasattr(self, "_palframe_"): self._palframe_.destroy()

        self._palframe_ = Frame(self.master, bg = "#ffffff", height = self.FRAMEHEIGHT,
                                width = self.FRAMEWIDTH)
        self._palframe_.place(x = 10, y = 80)

        # Loading palettes of currently selected palette type
        from numpy import min
        pals = self.palettes.get_palettes(self.dd_type.get())
        for child in self._palframe_.winfo_children():
            child.destroy()

        # Adding new canvas
        figwidth = max([30, self.FRAMEWIDTH / len(pals)])
        xpos = 0
        for pal in pals:
            defaultpalettecanvas(self, pal, 5, xpos, figwidth, self.FRAMEHEIGHT)
            xpos += figwidth

    def _add_current_palette_canvas_(self):

        self._curpalcanvas_ = currentpalettecanvas(self.master,
               x = 20, y = 500, width = 260, height = 30) 

    def _curpalcanvas_draw_(self):

        # Re-draw the canvas.
        self._curpalcanvas_._draw_canvas_(self.get_colors())
        # Is the demo running?

        if self._demoTk_ is None:        return
        if self._demoTk_.winfo_exists(): self._show_demo_(True)

    def get_colors(self):

        # Getting current arguments
        params = {}
        for key,elem in self._sliders_.items():
            if elem.is_active():
                params[elem.getid()] = float(elem.getvalue())

        # Manipulate params
        for dim in ["h", "c", "l","p"]:
            dim1 = "{:s}1".format(dim)
            dim2 = "{:s}2".format(dim)
            dim = "power" if dim == "p" else dim
            check = [dim1 in params.keys(), dim2 in params.keys()]
            if check[0] and check[1]:
                params[dim] = [params[dim1], params[dim2]]
                del params[dim1]
                del params[dim2]
            elif check[0]:
                params[dim] = params[dim1]
                del params[dim1]

        n = self._sliders_["slider_N"].getvalue()
        if "n" in params: del params["n"]

        # Craw colors from current color map
        import palettes
        # Color function
        colorfun = self.dd_type.getmethod()
        fun      = getattr(palettes, colorfun)
        print "Params",; print params
        colors   = fun(n, **params)
        return colors.colors()


    def _add_dropdown_type_(self, init_args = None):

        self.dd_type = ddObject(self, "type", init_args = init_args)

    def _add_sliders_(self):

        self._add_slider_("slider_H1", -360, 360, "H1")
        self._add_slider_("slider_H2", -360, 360, "H2")

        self._add_slider_("slider_C1",    0, 100, "C1")
        self._add_slider_("slider_C2",    0, 100, "C2")

        self._add_slider_("slider_L1",    0, 100, "L1")
        self._add_slider_("slider_L2",    0, 100, "L2")

        self._add_slider_("slider_P1",    0,   3, "P1", resolution = 0.1)
        self._add_slider_("slider_P2",    0,   3, "P2", resolution = 0.1)

        self._add_slider_("slider_N",     1,  30, "N")
        self._sliders_["slider_N"].setvalue(7)

    def _add_slider_(self, name, from_, to, label, resolution = 1, orient = HORIZONTAL):

        # Position of the current slider
        ypos = len(self._sliders_) * 30 + 100 + self.FRAMEHEIGHT

        # Object handling slider actions/callbacks
        obj = sliderObject(name, self, self.master.cget("bg"))

        # Slider element
        scale = Scale(self.master, var = name, from_ = from_, to = to,
                  command = obj.callback, showvalue = 0,
                  length = 150, width = 15,
                  resolution = resolution, orient = orient)
        scale.place(x = 50, y = ypos)

        # Label (static text)
        lab = Label(self.master, text = label)
        lab.config(anchor = CENTER)
        lab.place(x = 20, y = ypos) 

        # Button to change the value
        but = Button(self.master, text = "SET", command = obj.setvalue,
                pady = 0, padx = 0)
        but.place(x = 250, y = ypos)

        # Value (shows current slider value)
        val = Text(self.master, bd = 0, height = 1, width = 4)
        val.insert(INSERT, 0)
        val.tag_configure("right", justify="right")
        val.place(x = 210, y = ypos) 
        val.tag_add("right", "1.0", "end")

        obj.bind(scale, lab, val, but)

        # Append slider object
        self._sliders_[name] = obj #.append(obj)


    def _add_demo_options_(self):

        but = Button(self.master, text = "Demo", command = self._show_demo_,
                pady = 5, padx = 5)
        but.place(x = 30, y = 560)

    def _add_close_button_(self):

        but = Button(self.master, text = "Cancel", command = sys.exit,
                pady = 5, padx = 5)
        but.place(x = 200, y = 560)

    def _add_return_button_(self):

        but = Button(self.master, text = "Ok", command = sys.exit,
                pady = 5, padx = 5)
        but.place(x = 150, y = 560)


    def bing(self):

        print "BING"

    def _show_demo_(self, update = False):


        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasAgg
            import matplotlib.backends.tkagg as tkagg
            from matplotlib.figure import Figure
            hasmatplotlib = True
        except:
            hasmatplotlib = False

        # If has matplotlib: plot
        if hasmatplotlib:

            def draw_figure(canvas, figure, loc=(0, 0)):
                """ Draw a matplotlib figure onto a Tk canvas
            
                loc: location of top-left corner of figure on canvas in pixels.
            
                Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
                """
                figure_canvas_agg = FigureCanvasAgg(figure)
                figure_canvas_agg.draw()
                figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
                figure_w, figure_h = int(figure_w), int(figure_h)
                photo = PhotoImage(master=canvas, width=figure_w, height=figure_h)

                print photo
            
                # Position: convert from top-left anchor to center anchor
                canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
            
                # Unfortunately, there's no accessor for the pointer to the native renderer
                tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
            
                # Return a handle which contains a reference to the photo object
                # which must be kept live or else the picture disappears
                return photo

            if not update:
                self._demoTk_ = Tk()#Toplevel()
                self._demoTk_.title("Demo Plot")
                self._demoTk_.geometry("{:d}x{:d}".format(500, 500))
                self._democanvas_ = Canvas(self._demoTk_, width=500, height=500)
                self._democanvas_.pack()


            # Create the figure we desire to add to an existing canvas
            import matplotlib as mpl
            if not update:
                self._demofig_ = mpl.figure.Figure(figsize=(2, 1))
            ## Keep this handle alive, or else figure will disappear
            from .specplot import specplot
            self._demofig_ = specplot(self.get_colors(), fig = "dummy")
            fig_photo = draw_figure(self._democanvas_, self._demofig_, loc=(0, 0))
            print " xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx "
            
            # Let Tk take over
            mainloop()

            #canvas = Canvas(self._demowindow_, width = 400, height = 400)
            #canvas.pack()

            #from .specplot import specplot
            #fig = specplot(self.get_colors(), fig = "foo")
            #draw_figure(canvas, fig)
            #canvas.pack()
            #mainloop()

            #fig = Figure(figsize=(6,6))
            #ax  = fig.add_subplot(111)
            #if update: ax.clear()
            #print "Update figure"
            #from .specplot import specplot
            #fig = specplot(self.get_colors(), fig = fig)
            #canvas = FigureCanvasTkAgg(fig, master = self._demowindow_)
            #canvas.get_tk_widget().pack()
            #canvas.draw()

        else:

            info = [""]
            info.append("To be able to run the demo plots")
            info.append("the python matplotlib package has to be")
            info.append("installed.")
            info.append("")
            info.append("Install matplotlib and try again!")

            txt = Text(self._demowindow_, height=10, width=45)
            txt.pack()
            txt.insert(END, "\n".join(info))











