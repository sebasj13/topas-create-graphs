import numpy as np
from .profile import ProfileHandler
from ..resources.language import Text

class TGS_Plot():
    
    def __init__(self, Options, ImportedData, normalize = None):
        
        try:
            self.fail = False
            self.options = Options
            self.lang = self.options.lang
            self.dataObject = ImportedData
            self.direction = self.dataObject.direction
            self.p = ProfileHandler()
            
            if normalize == None: self.normalize = self.p.get_attribute("normalize")
            else: self.normalize = normalize
            self.caxcorrection = self.p.get_attribute("caxcorrection")
            self.normalization = self.p.get_attribute("normtype")
            self.points = self.p.get_attribute("show_points")
            self.error = self.p.get_attribute("show_error")
            
            self.label = self.dataObject.filename
            self.linethickness = self.p.get_attribute("linethickness")
            self.linestyle = self.p.get_attribute("linestyle")
            self.linecolor =  ProfileHandler().get_attribute("default_colors")[len(self.options.parent.plots)%len(ProfileHandler().get_attribute("default_colors"))]
            
            self.dosefactor = self.p.get_attribute("dosefactor")
            self.doseshift = self.p.get_attribute("doseoffset")
            self.axshift = self.p.get_attribute("axshift")
            self.flip = self.p.get_attribute("flip")
            
            self.set_tab_data()
        except Exception as e:
            print(e)
            self.options.bell()
            self.fail = True
            return
        
    def set_tab_data(self):
        
        self.options.normalize.set(self.normalize)
        normtypedict = {"maximum":Text().maximum[self.lang], "plateau":Text().plateau[self.lang], "centeraxis":Text().centeraxis[self.lang]}
        self.options.normalization.set(normtypedict[self.normalization])
        self.options.plottitle.set(self.label)
        self.options.linethicknessslider.set(self.linethickness)
        self.options.linestyle.set({"-.":Text().dashdot[self.lang], "-":Text().dash[self.lang], "dotted":Text().dot[self.lang], " ":Text().none[self.lang]}[self.linestyle])
        self.options.plotcolor.set(self.linecolor)
        self.options.linecolorbutton.configure(fg_color=self.linecolor)
        self.options.doseshift.set(self.doseshift)
        self.options.axshift.set(self.axshift)
        self.options.dosescale.set(self.dosefactor)
        self.options.flip.set(self.flip)
        
    def data(self, allow_normalization=True):
        
        axis = np.add(self.dataObject.axis,self.axshift)
        dose = self.dataObject.dose.copy()
        error = self.dataObject.std_dev.copy()
               
        if (self.normalize==True & allow_normalization==True):
            if self.normalization == "maximum":
                error = np.divide(error,np.max(dose))
                dose = np.divide(dose,np.max(dose))

            elif self.normalization == "plateau":

                plateau = np.max(dose) * self.dataObject.params()[-1]
                error = np.divide(error, plateau)
                dose = np.divide(dose, plateau)
                print(plateau)

            elif self.normalization == "centeraxis":
                error = np.divide(error,dose[len(dose)//2])
                dose = np.divide(dose,dose[len(dose)//2])

        dose = np.add(dose * self.dosefactor, self.doseshift)
        error = np.add(error * self.dosefactor, self.doseshift)
        
        if self.flip:
            dose = np.flip(dose)
            error = np.flip(error)
            
        return axis, dose, error
        
    def plot(self, ax):
    
        axis, dose, error = self.data()
        if self.caxcorrection:
            if self.direction != "Z" and self.direction != "s":
                axis = np.add(axis, self.dataObject.params()[1])
        
        if self.error:
            ax.errorbar(axis, dose, label="_", yerr=error, fmt="none", ecolor="red", elinewidth=0.625, capsize=1.25, capthick=0.25)
            ax.plot(axis, dose, label=self.label, lw=self.linethickness, color=self.linecolor, linestyle = self.linestyle)
        else:
            ax.plot(axis, dose, label=self.label, lw=self.linethickness, color=self.linecolor, linestyle = self.linestyle)
        if self.points:
            ax.scatter(axis, dose, label= "_", s=self.linethickness*20, color=self.linecolor, marker="x")