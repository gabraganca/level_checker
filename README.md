# Synspec Level Checker

## Introduction

`Level Checker` is a tool for identifying eletronic transition levels of the
atomic data used by
[`Synspec`](http://nova.astro.umd.edu/Synspec43/synspec.html).

`Synspec` does a automatic identification of the levels, but sometimes it can
get one level wrong. Usually, this happens when the energy levels of the right
and the wrong levels are too similar.

The routine does not check if the levels are correct, it just returns the
levels. To see hot to verify the levels, please read the
[Methodoloy](METHODOLOGY.md).

## Installation

To install it, you will need to have [`git`](http://git-scm.com/) installed in
your machine. If you already have it, first clone it:

```
git clone git@github.com:gabraganca/level_checker.git
```

And the install it. There are two ways. I recommend using the second one because
you can upgrade and uninstall it easily.

1. Using only python:

        python setup.py install

2. Using [`pip`](https://pypi.python.org/pypi/pip):

        python setup.py build
        pip install .

## Usage

The is two ways to run the code: as a script or as a python package. If you
are using it as a script, just typing `levelchecker` will print the
documentation help. For the example explained in the
[Methodolgy](METHODOLOGY.md) file, you can type:

```
levelchecker Si 4 4116.104
```

And it will print all the information explained above.

If you want all levels you cant type without the specific wavelength, i.e.:

```
levelchecker Si 4
```

To use it as a python package simply import it:

```python
import levelchecker

levelchecker.check('Si', 4, 4116.104, synspec_root_dir)
```

where you have to specify which is the `Synspec` root directory. For example,
if your synplot folder is set up like this:

```
/home/user/synplot
├── atdata
├── bstar
│   └── bstar2013B
└── synplot
```

You just pass to the code the following:

```python
levelchecker.check('Si', 4, 4116.104, '/home/user/synplot')
```



