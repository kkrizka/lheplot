import numpy as np
import awkward as ak

import uproot
import hist

class Analysis:
    """
    The base class for plotting the events stored in an LHE file.

    This class is meant to be subclassed by the user to implement the desired analysis.
    """
    def __init__(self):
        self.histograms={}

    def book(self, name, xbins, xmin, xmax):
        """
        Book a histogram with the given name, number of bins, and range. The histograms
        will be saved as part of the `save` method.

        The histogram is created as an `hist.Hist` object of type `Int64`.        

        Parameters
        ----------
        name : str
            The name of the histogram.
        xbins : int
            The number of bins.
        xmin : float
            The minimum value of the histogram.
        xmax : float
            The maximum value of the histogram.

        Returns
        -------
        hist.Hist
            The histogram object.
        """
        self.histograms[name]=hist.Hist.new.Reg(xbins,xmin,xmax).Int64()
        return self.histograms[name]

    def fill(self, events):
        """
        Fill the histograms with the events.

        This method should be implemented by the user to fill the histograms with the
        desired events.

        Parameters
        ----------
        events : awkward.array
            The events to be used to fill the histograms.
        """
        pass

    def save(self, filename):
        """
        Save the histograms to a ROOT file.

        The histograms are saved to a ROOT file with the given filename. The histograms
        are saved in a directory called `ANALYSIS`.

        Parameters
        ----------
        filename : str
            The name of the ROOT file to be created.
        """
        print(f"Saving to {filename}")
        fh = uproot.recreate(filename)

        mydir=fh.mkdir("ANALYSIS")
        for name, h in self.histograms.items():
            mydir[name]=h.to_numpy()

        fh.close()

class ExampleTopAnalysis(Analysis):
    def __init__(self):
        super().__init__()

        self.h_top_pt = self.book("/top_pt",100,0,2000)

    def fill(self, events):
        particles=events['particles']

        top=particles[np.abs(particles['id'])==6]
        top_pt=np.sqrt(top['vector']['x']**2+top['vector']['y']**2)

        self.h_top_pt.fill(ak.flatten(top_pt))