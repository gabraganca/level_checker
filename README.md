# Synspec Level Checker

## Introduction

`Level Checker` is a tool for identifying eletronic transition levels of the
atomic data used by
[`Synspec`](http://nova.astro.umd.edu/Synspec43/synspec.html).

`Synspec` does a automatic identification of the levels, but sometimes it can
get one level wrong. Usually, this happens when the energy levels of the right
and the wrong levels are too similar.

## Methodology

This recipe explains how to check if the level of a spectral line is correct.

1. Synthesize the line. The parameters are not important. We just want to
   generate the output files.

2. In the file `fort.12`, look for the desired spectral line. To find it, you
   can use the third, fourth and fifth column that are, respectively, the
   central wavelength, the chemical element and the ionization stage.

   What we need is the number of the lower level (11th column) and the upper
   level (12th column).

   For example, let's identify the Si IV line at 4654.312 angstrons. The line
   on the `fort.12` file refferring to this spectral line is:

   >12     37  4654.312   Si  IV   -0.52  293837.914   1.15E-02     0.7    . **1402 1408**   32

   The values that we want are in boldface.


3. Open the file `/bstar/bstar2013B/BG_CONeSi_20000g400v2.6` and look for the
   section called *EXPLICIT IONS INCLUDED*. Here, it is all levels
   identification used by `Synspec`. Note that the lower level is for Hydrogen
   and the following ones will only stacking over one another. Thus, look for
   the chemical element and ionization stage desired and obtain the values of
   the lowest level (column N0).

   For our example, we have:

   >27  Si 4  **1390**  1442  1443     4     0    16      0.000D+00

4. Subtract the level indifications found on (2) and (3).

   For our little example, we have:

   ```
   lower level : 1402 - 1390 = 13
   upper level : 1408 - 1390 = 19
   ```

   Note that the lower level identification has to be included.

5. With the lower and upper level identified, open the file containing the
   atomica data for the chemical element and ionization stage desired.
   It should be in a folder called `atdata`. In this file, the level are in
   ascending order.

   If we go back to the example, we will look into the file
   `atdata\Si4_53lev.dat` and obtain the 13th and the 19th level:

   >2.10615573E+15     18.    5  **'SiIV 2Ge 1'**  0   0.  -105

   >1.46223047E+15     22.    6  **'SiIV 2Ho 1'**  0   0.  -105

   And the levels are showed in boldface, i.e., the lower level is
   `Si IV 2Ge 1` and the upper level is `SiIV 2Ho 1`. The last term ('1') means
   that it is the the first level with the this term ( '2 Ge' for the lower
   level and '2Ho' for the upper term.

6. Go to NIST or look for a table of eletronic transitions and check if the
   wavelength of the desired line is correct.


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
are using it as a script, just typing `./levelchecker` will print the
documentation help. For the example above, you can type:

```
./levelchecker Si 4 4654.312
```

And it will print all the information explained above.

If you want all levels you cant type without the specific wavelength, i.e.:

```
./levelchecker Si 4
```

To use it as a python package simply import it:

```python
import levelchecker

levelchecker.check('Si', 4, 4654.312, synspec_root_dir)
```

where you have to specify which is the `Synspec` root directory. For example, if you synplot folder 
is set up like this:

```
/home/user/synplot
├── atdata
├── bstar
│   └── bstar2013B
└── synplot
```

You just pass to the code the following:

```python
levelchecker.check('Si', 4, 4654.312, '/home/user/synplot')
```



