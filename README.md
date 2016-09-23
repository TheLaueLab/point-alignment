# Coherent Point Drift

A python implementation of rigid and affine coherent point drift alignment.
Includes brute-force search for rigid alignment in global rotation space.

# Installation

A setuptools compatible install script (`setup.py`) is provided to install the
library. Detailed instructions can be found in the
[official documentation][setuptools].

## Dependencies

[Python 3][python] and [Numpy][numpy].

### Demo

The demo script additionally requires [matplotlib][matplotlib].

# Demo

A demo of global alignment is included under the name `test_global.py`.

Usage is as follows:

    test_global.py gen N D R | ./test_global.py plot

where `N` is the number of random points to generate, `D` is the dimensionality
(2 or 3), and `R` is the number of random transforms to generate. Additional
help about parameters can be found with `test_global.py gen --help`.

The first generates and aligns a series of transformations of a random point
cloud. The second plots their locations and RMSDs.

[setuptools]: https://docs.python.org/3.3/install/#the-new-standard-distutils
[Python]: https://python.org
[Numpy]: https://www.numpy.org
[matplotlib]: http://matplotlib.org
