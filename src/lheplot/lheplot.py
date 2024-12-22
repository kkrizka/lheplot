# %% Important imports
import argparse
import importlib

from pathlib import Path

import pylhe

def main():
    # Steering options
    parser = argparse.ArgumentParser(description='Plot the contents of LHE files.')
    parser.add_argument('lhe_file', type=str, nargs='+', help='The LHE file to be plotted.')
    parser.add_argument('--analysis','-a', type=str, default='lheplot.Analysis.ExampleTopAnalysis', help='The analysis class to be used.')

    args = parser.parse_args()

    # Create the analysis class
    module_name, class_name = args.analysis.rsplit('.',1)
    module = importlib.import_module(module_name)
    analysis_class = getattr(module, class_name)

    # Loop over input files
    for lhe_file in args.lhe_file:
        print(f"Processing {lhe_file}")

        # Create the analysis class
        analysis = analysis_class()

        # Open the input file and convert to awkward
        events = pylhe.to_awkward(pylhe.read_lhe_with_attributes(lhe_file))

        # Fill the histograms
        analysis.fill(events)

        # Save the histograms
        path = Path(lhe_file)
        if path.name.endswith('.lhe'):
            out = path.with_suffix('.root')
        elif path.name.endswith('.lhe.gz'):
            out = path.with_suffix('').with_suffix('.root')
        else:
            out = path.with_suffix('.root')

        analysis.save(out.name)

