# lspy

Lspy is a localsearch library implemented in python.
Note that the described procedures don't work yet, also names and such might change the final release.

## Getting Started

Here, you will find a simple guide to install the package on your system.

### Prerequisites

The package is intended to be installed with [pip](https://pip.pypa.io/en/stable/).
Make sure pip is installed on your system. 
(It's probably included with your python implementation, but it doesn't hurt to check.)

After you've made sure pip is installed,
install the following packages:

setuptools

```
pip install setuptools
```

wheel 

```
pip install wheel
```

You will be notified if they are already installed. This isn't be a problem.


### Installing

After the prequisites have been properly installed, it's time to install locsearch.
Do not worry about dependencies and such, setuptools should take care of those.

```
pip install locsearch
```

You can easily test if it's installed by using the [interactive interpreter](https://docs.python.org/3/tutorial/interpreter.html#interactive-mode).

Depending on your local installation, it might also be possible to start the interactive interpreter by using:

```
python
```

or

```
py
```

Once inside the interpreter, try the following command:

```
import lspy
```

If it succeeds without errors, lspy is installed.

## Usage

If you have any questions of how to use the library, you can download the project from github and check the documentation in the docs/html folder.
You can also check the docstrings of a module in the interactive interpreter like this:

```
print(module_alias.__doc__)
```

There are also several [jupyter notebooks](https://jupyter.org/) that demonstrate the use of some classes. These notebooks can be found in the project on github in the notebooks folder.


## Tests

Most of the modules of locsearch have some [doctests](https://docs.python.org/3/library/doctest.html) included.

One can perform these by importing the module and then using the following code in the interactive interpreter:

```
import doctest

doctest.testmod(module_alias)
```

If there are no failed tests, everything is fine.


## Authors

* **Daan Thijs** - *Initial work* - [nobody1570](https://github.com/nobody1570)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/nobody1570/lspy/blob/master/LICENSE) file for details

## Acknowledgments

* Tony Wauters
* Wim Vancroonenburg