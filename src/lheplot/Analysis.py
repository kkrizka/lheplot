import numpy as np
import awkward as ak

import uproot
import hist

class Analysis:
    def __init__(self):
        self.histograms={}

    def book(self, name, xbins, xmin, xmax):
        self.histograms[name]=hist.Hist.new.Reg(xbins,xmin,xmax).Int64()
        return self.histograms[name]

    def fill(self, events):
        pass

    def save(self, filename):
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