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
import fnmatch


def find(pattern, path):
    # Looks for files that match a pattern
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def int2roman(number):
    # Convert arabic number to roman.
    numerals = { 1 : "I", 4 : "IV", 5 : "V", 9 : "IX", 10 : "X", 40 : "XL",
                 50 : "L", 90 : "XC", 100 : "C", 400 : "CD", 500 : "D",
                 900 : "CM", 1000 : "M" }
    result = ""
    for value, numeral in sorted(numerals.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result


def main(wave, chem_element, ion):
    """
    Parameters
    ----------

    wave: str;
        Central wavelength as an integer.

    chem_element: str;
        Chemical element,

    ion: str;
        Ionization stage in Arabic numerals.
    """

    print 'Step #2\n'

    # Check if fort.12 is available. If it is, load it.
    try:
        fort12 = open(find('fort.12', '.')[0]).read()
    except TypeError:
        raise IOError('File fort.12 is not available. Plese run synplot to ' + \
                      'generate it.')

    ptrn ='(' + str(wave) + '\.\d{3}).*(' + chem_element + ')\s{2,3}(' + \
            int2roman(int(ion)) + ').*\s(\d+\s+\d+)\s{3}\d{2}\n'

    if re.search(ptrn, fort12):
        full_wave, chem, roman_ion, levels =  re.findall(ptrn, fort12)[0]
        #split levels
        fort12_l_level, fort12_u_level = levels.split()

        print 'In fort.12, ' + \
              'we found that the levels for {} {}'.format(chem, roman_ion) +\
              ' at wavelength {}:\n\n'.format(full_wave) + \
              'lower level: {} \nupper level: {}'.format(fort12_l_level,
                                                         fort12_u_level)
    else:
        raise IOError('There is no such line inside the fort.12 file.\n' + \
                      'Please, synthesize a spectrum with the desired ' + \
                      'spectral line.')

    print '\n\nStep #3\n'

    # Look for Tlusty output with termination .6
    try:
        dot6_fname = find('*.6', '.')[0]
        dot6 = open(dot6_fname).read()
    except TypeError:
        raise IOError('There is no Tlusty output file with `.6` ' + \
                      'termination.\nPlease, obtain one.')

    ptrn = '(' + chem_element + ')\s(' + str(ion) +')\s+(\d+)\s'

    if re.search(ptrn, dot6):
        chem, ion, dot6_l_level =  re.findall(ptrn, dot6)[0]

        print 'In {}, '.format(dot6_fname) + \
              'we found that the levels for {} {}:\n\n'.format(chem, ion) +\
              'lower level: {}'.format(dot6_l_level)
    else:
        raise IOError('There is no such line element and/or ionization ' + \
                      'stage at the Tlusty file.')


if __name__ == '__main__':

    if len(sys.argv) == 1:
        print __doc__
        print '\nUsage\n-----\n\n'+\
              'checkLevels wavelength chemical_element ionization_stage\n\n' + \
              'For our little example, we can use:\n\n' + \
              'checkLevels 4654 Si 4'
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
