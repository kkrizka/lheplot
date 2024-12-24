# Plot LHE Files

A lightweight framework for making plots from LHE files that are the output of many fixed order generators. It leverages the [pylhe](https://github.com/scikit-hep/pylhe) package for input.

## Installation

The package can be installed using Pip.

```shell
pip install lheplot
```

## Usage

The following will create two output files `singletop.root` and `singleantitop.root` following the plots defined in the example `lheplot.Analysis.ExampleTopAnalysis` analysis.

```shell
lheplot -a lheplot.Analysis.ExampleTopAnalysis singletop.lhe.gz singleantitop.lhe.gz
```

The LHE files can be compressed (`.lhe.gz`) or uncompressed (`.lhe`).

### Converting to YODA files

The ROOT files are formatted in a way to make it possible to use the output with Rivet. Only caveat is to convert to the YODA format first. This is useful one does not have to reinvent the pretty plotting functionality.

```shell
root2yoda singletop.root
root2yoda singleantitop.root
rivet-mkhtml singletop.yoda singleantitop.yoda
```

## Custom Plots

Custom plots can be created by making a custom class inheriting from the `lheplot.Analysis.Analysis` class. An examples is provided in the same module as `ExampleTopAnalysis`. It is

```python
class ExampleTopAnalysis(Analysis):
    def __init__(self):
        super().__init__()

        self.h_top_pt = self.book("/top_pt",100,0,2000)

    def fill(self, events):
        particles=events['particles']

        top=particles[np.abs(particles['id'])==6]
        top_pt=np.sqrt(top['vector']['x']**2+top['vector']['y']**2)

        self.h_top_pt.fill(ak.flatten(top_pt))
```

The key parts are:
- Use the `book` method to create a histogram in the class initializer. The three arguments are the path, number of bins and histogram range. The path is prepended by an `"/ANALYSIS"` string.
- Implement the `fill` function that takes on argument: `events`. The events are the result of opening an LHE file using `pylhe` and converting to an awkward array.