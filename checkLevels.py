'''
Check Line Levels
=================

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

5. With thw lower and upper level indefied, open the file containing the
   atomica data for the chemical element and ionization stage desired.
   It should be in a folder called `atdata`. In this file, the level are in
   ascending order.

   If we go back to the example, we will look into the file
   `atdata\Si4_53lev.dat` and obtain the 13th and the 19th level:

   >2.10615573E+15     18.    5  **'SiIV 2Ge 1'**  0   0.  -105

   >1.46223047E+15     22.    6  **'SiIV 2Ho 1'**  0   0.  -105

   And the levels are showed in boldface, i.e., the lower level is
   `Si IV 2Ge 1` and the upper level is `SiIV 2Ho 1`.

6. Go to NIST or look for a table of eletronic trasnsitions and check if the
   wavelength of the desired line is correct.
'''

import sys
import os
import re


def find(name, path):
    # find a file
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def main(wave, chem_element, ion):
    """
    Parameters
    ----------

    wave: str;
        Central wavelength as an integer.

    chem_element: str;
        Chemical element,

    ion: str;
        Ionization stage in Roman numerals.
    """

    print 'Step #2\n'

    # Check if fort.12 is available. If it is, load it.
    fort12 = find('fort.12', '.')

    try:
        fort12 = open(fort12).read()
    except TypeError:
        raise IOError('File fort.12 is not available. Plese run synplot to ' + \
                      'generate it.')

    ptrn ='(' + str(wave) + '\.\d{3}).*(' + chem_element + ')\s{2,3}(' + ion + \
         ').*\s(\d+\s+\d+)\s{3}\d{2}\n'

    if re.search(ptrn, fort12):
        full_wave, chem, ioni, levels =  re.findall(ptrn, fort12)[0]
        #split levels
        levels = levels.split()

        print 'In fort.12,' + \
              'we found that the levels for {} {}'.format(chem, ioni) +\
              ' at wavelength {}:\n\n'.format(full_wave) + \
              'lower level: {} \nupper level: {}'.format(levels[0], levels[1])
    else:
        raise IOError('There is no such line insie the fort.12 file.\n' + \
                      'Please, synthesize a spectrum with the desired ' + \
                      'spectral line.')

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print __doc__
        print '\nUsage\n-----\n\n'+\
              'checkLevels wavelength chemical_element ionization_stage\n\n' + \
              'For our little example, we can use:\n\n' + \
              'checkLevels 4654 Si IV'
    WAVE = int(sys.argv[1])
    CHEM_ELEMENT = sys.argv[2]
    ION = sys.argv[3]
#    WEND = float(sys.argv[4])
#    if len(sys.argv) == 6:
#        SPATH = sys.argv[5] # Synplot path
#    else:
#        SPATH = None
#
#    main(V_PARAM, VALUES, WSTART, WEND, SPATH)
