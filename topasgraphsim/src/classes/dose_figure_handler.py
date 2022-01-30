import tkinter as tk
import tkinter.simpledialog as sd

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from matplotlib.ticker import AutoMinorLocator
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from PIL import Image, ImageTk
from win32api import GetSystemMetrics

from ..resources.language import Text
from .measurement_import import Measurement
from .ptw_import import PTWMultimporter
from .sim_import import Simulation


class DoseFigureHandler:
    def __init__(self, parent):

        self.parent = parent

        self.norm = self.parent.norm.get()
        self.normvalue = "max"
        self.errorbars = True
        self.caxcorrection = False
        self.zoom = self.parent.zoom.get()
        self.half = self.parent.half.get()
        self.axlims = (self.parent.axlims.get(), self.parent.axlims.get())
        self.addmenu = False

        # Initialize the current settings
        self.lang = self.parent.lang
        self.text = Text()
        self.style = plt.style.use("default")
        self.colors = ["#009F6B", "#C40233", "#00008B", "#BCA136", "#654321"]
        self.marker = "o--"
        self.markersize = self.parent.profile.get_attribute("markersize")
        self.linewidth = self.parent.profile.get_attribute("linewidth")

        # Initialize necessary variables
        self.props = dict(boxstyle="round", facecolor="wheat", alpha=0.6)
        self.plots = []
        self.data = []

    def add_plot_data(self, datanames):

        """Adds data to the plot queue
        """

        test = [plotdata.direction for plotdata in self.plots]
        for tuple in datanames:
            filename = tuple[0]
            type = tuple[1]
            if filename not in [plotdata.filepath for plotdata in self.plots]:
                if type == "simulation":
                    sim = Simulation(filename)
                    if test == []:
                        self.plots += [sim]
                    elif sim.direction == "Z" and "Z" in test:
                        self.plots += [sim]
                    elif sim.direction == "X" and "X" in test or "Y" in test:
                        self.plots += [sim]
                    elif sim.direction == "Y" and "X" in test or "Y" in test:
                        self.plots += [sim]

                    else:
                        sd.messagebox.showinfo(
                            "", f"{sim.filename}" + self.text.incordata[self.lang][1]
                        )
                elif type == "ptw":
                    importer = PTWMultimporter(filename, self.parent.parent)
                    importer.window.mainloop()
                    importer.window.destroy()
                    measurements = [plot for plot in importer.plots]
                    fails = []
                    for plot in measurements:
                        if test == []:
                            self.plots += [plot]
                        elif plot.direction == "Z" and "Z" in test:
                            self.plots += [plot]
                        elif plot.direction == "X" and "X" in test or "Y" in test:
                            self.plots += [plot]
                        elif plot.direction == "Y" and "X" in test or "Y" in test:
                            self.plots += [plot]
                        else:
                            fails += [plot]

                    if fails != []:
                        self.parent.filenames.pop(-1)
                        names = ""
                        for f in fails:
                            names += str(f.filename) + ", "
                        names = names[:-2]
                        var = 1
                        if len(fails) >= 2:
                            var = 2
                        sd.messagebox.showinfo(
                            "", f"{names}" + self.text.incordata[self.lang][var],
                        )

                    del importer

                else:
                    self.plots += [Measurement(filename, type)]

        if self.plots[0].direction == "Z":
            self.half = False

        for plotdata in self.plots:
            if self.norm == True:
                if self.normvalue == "max":
                    plotdata.normpoint = max(plotdata.dose[self.half])
                elif self.normvalue == "flank":
                    plotdata.normpoint = max(plotdata.dose[self.half]) * 0.5
                else:
                    plotdata.normpoint = plotdata.dose[self.half][
                        len(plotdata.dose) // 2
                    ]

            else:
                plotdata.normpoint = 1
            self.data += [
                [
                    plotdata.axis[self.half],
                    plotdata.direction,
                    plotdata.dose[self.half] / plotdata.normpoint,
                    plotdata.std_dev[self.half] / plotdata.normpoint,
                ]
                + plotdata.params
            ]

        if self.plots[0].direction == "Z":
            figsize = (10, 5)
        else:
            figsize = (10, 6)

        # Initialize the figure and axes
        self.fig = Figure(figsize, constrained_layout=True, dpi=600)
        self.canvas = FigureCanvasAgg(self.fig)
        self.fig.set_canvas(self.canvas)
        self.ax = self.fig.add_subplot(111)

        return

    def set_style(self):

        """Switches the plotting style according to the current theme
        """

        if self.parent.dark.get() == True:
            self.ax.set_facecolor("#363636")
            self.fig.set_facecolor("#363636")
        else:

            self.ax.set_facecolor("#ffffff")
            self.fig.set_facecolor("#ffffff")

        return

    def flush(self):

        """Clears the data
        """

        self.data = []

        return

    def fits(self, image):

        """Scales an image to the width of the screen.
        """

        scr_width = GetSystemMetrics(0)
        width = int(scr_width)
        scale_factor = image.shape[1] / width
        image = cv2.resize(
            image,
            (width, int(image.shape[0] / scale_factor)),
            interpolation=cv2.INTER_AREA,
        )

        return image

    def set_axis(self):

        """Defines the layout and gridlines of the plot 
        """

        self.ax.clear()
        self.ax.grid(True, which="major")
        self.ax.grid(True, which="minor", color="grey", linewidth=0.1)
        self.ax.xaxis.set_minor_locator(AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(AutoMinorLocator())
        self.ax.tick_params(axis="both", which="minor", length=2)

        return

    def add_legend(self):

        """Adds the legend
        """

        self.ax.legend(
            loc="upper right",
            framealpha=0.6,
            facecolor="wheat",
            edgecolor="black",
            fancybox=True,
        )

        return

    def add_descriptors(self):

        """Adds the calculated parameters as descriptors
        """

        if self.plots[0].direction != "Z":

            if self.half == False:
                positionsx = [
                    0.1,
                    0.1,
                    0.901,
                    0.901,
                    0.1,
                ]
                positionsy = [0.98, 0.68, 0.75, 0.45, 0.38]
            else:
                positionsx = [
                    0.7,
                    0.7,
                    0.901,
                    0.901,
                    0.7,
                ]
                positionsy = [0.98, 0.68, 0.68, 0.38, 0.38]

        for index, plot_data in enumerate(self.data):

            if len(plot_data) == 7:
                Q, dQ, zmax = plot_data[4], plot_data[5], plot_data[6]
                textstr = "Q     = {} ± {}\n{} = {} mm".format(Q, dQ, "$z_{max}$", zmax)
                space = 0
                if dQ == 0:
                    space = 0.05
                if len(str(Q)) == 6:
                    space += 0.01
                if len(str(dQ)) == 6:
                    space += 0.01
                self.ax.text(
                    0.795 + space,
                    0.955 - len(self.plots) * 0.0475 - 0.1 * index,
                    textstr,
                    transform=self.ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=self.props,
                    color=self.colors[index],
                )
            else:
                (
                    HWB,
                    CAXdev,
                    flat_krieger,
                    flat_stddev,
                    S,
                    Lpenumbra,
                    Rpenumbra,
                    Lintegral,
                    Rintegral,
                ) = (
                    plot_data[4],
                    plot_data[5],
                    plot_data[6],
                    plot_data[7],
                    plot_data[8],
                    plot_data[9],
                    plot_data[10],
                    plot_data[11],
                    plot_data[12],
                )

                if self.caxcorrection == True:
                    CAXdev = 0

                textstr = "{} = {} mm\n{} = {} mm\n{} = {}\n{} = {}\n{} = {} mm\n{} = {} mm\n{} = {}\n{} = {}\n{} = {}".format(
                    self.text.fwhm[self.lang],
                    HWB,
                    "$CAX_{dev}$",
                    CAXdev,
                    "$FLAT_{Krieger}$",
                    flat_krieger,
                    "$FLAT_{stddev}$",
                    flat_stddev,
                    "$Penumbra_{L}$",
                    Lpenumbra,
                    "$Penumbra_{R}$",
                    Rpenumbra,
                    "$Integral_{L}$",
                    Lintegral,
                    "$Integral_{R}$",
                    Rintegral,
                    self.text.symmetry[self.lang],
                    S,
                )
                self.ax.text(
                    positionsx[index],
                    positionsy[index],
                    textstr,
                    transform=self.ax.transAxes,
                    fontsize=10,
                    verticalalignment="top",
                    bbox=self.props,
                    horizontalalignment="center",
                    color=self.colors[index],
                )

        return

    def set_x_label(self):

        """Names the x-axis according to the plot type
        """

        directions = [plot.direction for plot in self.plots]
        if directions.count(directions[0]) == len(directions):

            xlabel = f"{directions[0]}-{self.text.axis[self.lang]} [mm]"
        else:
            xlabel = f"X- {self.text.orr[self.lang]} Y-{self.text.axis[self.lang]}"

        self.ax.set_xlabel(xlabel, size=12)
        if self.norm == False:
            self.ax.set_ylabel(self.plots[0].unit, size=12)

        return

    def create_plots_from_data(self):

        """Creates the plots from the queue
        """

        for index, plot_data in enumerate(self.data):
            if self.caxcorrection == True:
                plot_data[0] = [x - plot_data[5] for x in plot_data[0]]

            if self.errorbars == True:
                try:
                    self.ax.errorbar(
                        x=plot_data[0],
                        y=plot_data[2],
                        yerr=plot_data[3],
                        fmt="none",
                        ecolor=self.colors[index],
                        elinewidth=0.625,
                        capsize=1.25,
                        capthick=0.25,
                        ms=2.5,
                    )
                except ValueError:
                    pass
            self.ax.plot(
                plot_data[0],
                plot_data[2],
                self.marker,
                markersize=self.markersize,
                color=self.colors[index],
                linewidth=self.linewidth,
                label=f"{self.plots[index].filename}",
            )

        try:
            self.axins.remove()
        except:
            pass

        self.axlims = (self.parent.axlims.get(), self.parent.axlims.get())
        if self.plots[0].direction == "Z" or self.half == True:
            self.axlims = (0, self.axlims[1])
        self.ax.set_xlim(
            left=self.ax.get_xlim()[0] - self.axlims[0],
            right=self.ax.get_xlim()[1] + self.axlims[1],
        )
        self.ax.set_xbound(
            lower=self.ax.get_xlim()[0] - self.axlims[0],
            upper=self.ax.get_xlim()[1] + self.axlims[1],
        )

        if self.zoom == True:

            self.canvas.draw()
            self.transform = self.ax.transData
            self.inverted_transform = self.ax.transData.inverted()
            width, height = self.fig.canvas.get_width_height()

            self.focuspoint = self.plots[-1].axis[self.half][
                len(self.plots[-1].axis[self.half]) // 2
            ]
            try:
                self.focuspoint = self.inverted_transform.transform(
                    (
                        width
                        * (self.parent.canvas.coords(self.parent.oval)[0] + 5)
                        / self.parent.canvas.image.width(),
                        1,
                    )
                )
                self.focuspoint = self.plots[-1].axis[self.half][
                    np.abs(
                        np.asarray(self.plots[-1].axis[self.half] - self.focuspoint[0])
                    ).argmin()
                ]
            except AttributeError:
                pass
            except IndexError:
                pass

            pixels = self.transform.transform(np.vstack([plot_data[0], plot_data[2]]).T)
            x, y = pixels.T
            y = height - y

            self.pixelx = (
                x[self.plots[-1].axis[self.half].index(self.focuspoint)] / width
            )
            self.pixely = (
                y[self.plots[-1].axis[self.half].index(self.focuspoint)] / height
            )

            loc = "lower left"
            if self.half == False and self.plots[0].direction != "Z":
                loc = "lower center"

            self.axins = inset_axes(self.ax, "28%", "28%", loc=loc)
            yvalsat195 = []
            yvalsat205 = []
            for index, plot_data in enumerate(self.data):
                if self.errorbars == True:
                    try:
                        self.axins.errorbar(
                            x=plot_data[0],
                            y=plot_data[2],
                            yerr=plot_data[3],
                            fmt="none",
                            ecolor=self.colors[index],
                            elinewidth=0.625,
                            capsize=1.25,
                            capthick=0.25,
                            ms=2.5,
                        )
                    except ValueError:
                        pass
                self.axins.plot(
                    plot_data[0],
                    plot_data[2],
                    self.marker,
                    markersize=self.markersize,
                    color=self.colors[index],
                    linewidth=self.linewidth,
                    label=f"{self.plots[index].filename}",
                )
                yvalsat195 += [
                    plot_data[2][
                        plot_data[0].index(
                            min(
                                plot_data[0],
                                key=lambda x: abs(x - (self.focuspoint - 5)),
                            )
                        )
                    ]
                ]
                yvalsat205 += [
                    plot_data[2][
                        plot_data[0].index(
                            min(
                                plot_data[0],
                                key=lambda x: abs(x - (self.focuspoint + 5)),
                            )
                        )
                    ]
                ]

            # sub region of the original image
            x1, x2, y1, y2 = (
                self.focuspoint - 6,
                self.focuspoint + 6,
                0.99 * min(yvalsat205),
                1.01 * max(yvalsat195),
            )
            if self.half == True:
                x1, x2 = x1 + 3, x2 - 3

            self.axins.set_xlim(x1, x2)
            self.axins.set_ylim(y1, y2)
            self.axins.tick_params(
                labelleft=False, labelbottom=False, bottom=False, left=False
            )

            mark_inset(self.ax, self.axins, loc1=2, loc2=4, fc="none", ec="0.5")

        return

    def return_figure(self, filenames):

        """Passes the image of the plot and the plot type to the MainApplication
        """

        self.half = self.parent.half.get()
        self.add_plot_data(filenames)

        self.set_axis()
        self.set_x_label()
        self.create_plots_from_data()
        self.add_descriptors()
        self.add_legend()
        self.ax.set_aspect("auto")
        self.set_style()

        self.canvas.draw()
        buffer = self.canvas.buffer_rgba()
        image_array = np.asarray(buffer)
        fit_array = self.fits(image_array)
        image = Image.fromarray(fit_array)
        photoimage = ImageTk.PhotoImage(image)

        return photoimage, self.data[0][1]
