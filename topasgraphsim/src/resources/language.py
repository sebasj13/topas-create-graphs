class Text:

    """
    Contains all translatable text in the program.
    """

    def __init__(self):

        self.window_title = {
            "de": "TopasMC Simulationsauswertung",
            "en": "TopasMC Simulation Analysis",
        }
        self.file = {"de": "Datei", "en": "File"}
        self.view = {"de": "Ansicht", "en": "View"}
        self.options = {"de": "Optionen", "en": "Options"}
        self.add = {"de": "Daten hinzufügen", "en": "Add Data"}
        self.loadsim = {"de": "Simulationsergebnis laden", "en": "Load Simulation"}
        self.simulation = {"de": "Simulation", "en": "Simulation"}
        self.loadmeasurement = {"de": "Messung laden", "en": "Load Measurement"}
        self.measurement = {"de": "Messung", "en": "Measurement"}
        self.simulationdata = {"de": "Simulationsdateien", "en": "Simulation Data"}
        self.measurementdata = {"de": "Messdaten", "en": "Measurement Data"}
        self.image = {"de": "Bilder", "en": "Images"}
        self.pdd = {"de": "Tiefendosiskurve", "en": "Depth dose"}
        self.dp = {"de": "Dosisquerverteilung", "en": "Dose profile"}
        self.save = {"de": "Graph abspeichern", "en": "Save graph"}
        self.close = {
            "de": "Derzeitige Simulation schließen",
            "en": "Close current simulation",
        }
        self.revert = {"de": "Rückgängig", "en": "Undo"}
        self.end = {"de": "Beenden", "en": "Close"}
        self.light = {"de": "Hell", "en": "Light"}
        self.dark = {"de": "Dunkel", "en": "Dark"}
        self.startdark = {"de": "Im dunklen Modus starten", "en": "Start in dark mode"}
        self.languageset = {
            "en": "Das geöffnete Projekt wird geschlossen. Fortfahren?",
            "de": "The current project will be closed. Continue?",
        }
        self.histories = {"de": "Historien", "en": "Histories"}
        self.histnum = {
            "de": "Anzahl der Historien in der Simulation:",
            "en": "Histories in Simulation:",
        }
        self.symmetry = {"de": "Symmetrie", "en": "Symmetry"}
        self.fwhm = {"de": "HWB", "en": "FWHM"}
        self.axis = {"de": "Achse", "en": "Axis"}
        self.orr = {"de": "oder", "en": "or"}
        self.language = {"de": "Sprache", "en": "Language"}
        self.german = {"de": "Deutsch", "en": "German"}
        self.english = {"de": "Englisch", "en": "English"}
        self.normalize = {"de": "Normieren", "en": "Normalize"}
        self.increase = {"de": "Vergrößern", "en": "Increase"}
        self.decrease = {"de": "Verkleinern", "en": "Decrease"}
        self.marker = {"de": "Symbolgröße", "en": "Marker Size"}
        self.markerline = {"de": "Liniendicke", "en": "Line Width"}
