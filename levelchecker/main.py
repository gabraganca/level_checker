"""
Main module functions.
"""

import os
import re
import fnmatch
import json


def find(pattern, path):
    """
    Looks for files that match a pattern

    Parameters
    ----------

    pattern: str;
        Pattern to look for.

    path: str;
        Where to look.

    Returns
    -------

    result: list;
        A list containing the files found.
    """
    result = []
    for root, _, files in os.walk(path):
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

def get_energy_levels(chem_element, ion, wave, spath):
    """
    Obtain the energy levels of a spectral line on the line list.

    Parameters
    ----------

    chem_element: str;
        Chemical element,

    ion: str;
        Ionization stage in Arabic numerals.

    wave: float, str;
        Central wavelength.

    spath: str;
        Path to syn(spec|plot) root directory.
        Usually it is `/home/user/synplot/`.
    """
    # Check if fort.19 is available. If it is, load it.
    try:
        fort19 = open(find('fort.19', spath)[0]).read()
    except TypeError:
        raise IOError('File fort.19 is not available.')

    periodic = json.load(open(os.getenv('HOME') +
                              '/.levelchecker/chemical_elements.json'))
    # The wavelength in fort.19 is in nanometers
    wave = float(wave)/10

    # Get atomic number
    atom = str(periodic[chem_element])

    #The ion contuing on fort. starts from 0, being 0 the neutral atom.
    ion = str(int(ion) - 1)

    ptrn = '(' + str(wave) + '\d*)\s+(' + atom + '\.0' + ion + \
           ').+\s(\d{4,}\.\d{3}).+\s(\d{4,}\.\d{3})'

    wave_nm, atom_ion, low_energy, high_energy = re.findall(ptrn, fort19)[0]

    return wave_nm, atom_ion, low_energy, high_energy


def get_levels(chem_element, ion, wave, spath, verbose=False):
    """
    Parameters
    ----------

    chem_element: str;
        Chemical element,

    ion: str;
        Ionization stage in Arabic numerals.

    wave: float, str;
        Central wavelength.

    spath: str;
        Path to syn(spec|plot) root directory.
        Usually it is `/home/user/synplot/`.

    verbose: bool;
        If True, print log.
    """

    #open log to write:
    log = open('checklevels.log', 'w')

    log.write('Step #2\n')

    # Check if fort.12 is available. If it is, load it.
    try:
        fort12 = open(find('fort.12', spath)[0]).read()
    except TypeError:
        raise IOError('File fort.12 is not available. Plese run synplot to ' + \
                      'generate it.')

    ptrn ='(' + str(wave) + '(?:\.\d{3}|\d*)).*(' + chem_element + ')\s{2,3}('+\
           int2roman(int(ion)) + ').*\s(\d+\s+\d+)\s{3}\d{2}\n'

    if re.search(ptrn, fort12):
        full_wave, chem, roman_ion, levels =  re.findall(ptrn, fort12)[0]
        #split levels
        fort12_l_level, fort12_u_level = levels.split()

        log.write('In fort.12, ' + \
                  'we found that the levels for {} {}'.format(chem, roman_ion)+\
                  ' at wavelength {}:\n\n'.format(full_wave) + \
                  'lower level: {} \nupper level: {}'.format(fort12_l_level,
                                                             fort12_u_level))
    else:
        raise IOError('There is no such line inside the fort.12 file.\n' + \
                      'Please, synthesize a spectrum with the desired ' + \
                      'spectral line.')

    log.write('\n\nStep #3\n')

    # Look for Tlusty output with termination .6
    try:
        dot6_fname = find('*.6', spath)[0]
        dot6 = open(dot6_fname).read()
    except TypeError:
        raise IOError('There is no Tlusty output file with `.6` ' + \
                      'termination.\nPlease, obtain one.')

    ptrn = '(' + chem_element + ')\s(' + str(ion) +')\s+(\d+)\s'

    if re.search(ptrn, dot6):
        chem, ion, dot6_l_level =  re.findall(ptrn, dot6)[0]

        log.write('In {}, '.format(dot6_fname) + \
                  'we found that the levels for {} {}:\n\n'.format(chem, ion) +\
                  'lower level: {}'.format(dot6_l_level))
    else:
        raise IOError('There is no such line element and/or ionization ' + \
                      'stage at the Tlusty file.')

    log.write('\nStep #4\n\n')

    lower_level = int(fort12_l_level) - int(dot6_l_level) + 1
    upper_level = int(fort12_u_level) - int(dot6_l_level) + 1

    log.write('The ion upper and lowe level are:\n\n' + \
              'Lower level: {} - {} = {}\n'.format(fort12_l_level,  \
                                                   dot6_l_level, lower_level) +\
              'Upper level: {} - {} = {}\n'.format(fort12_u_level, \
                                                    dot6_l_level, upper_level))

    log.write('\nStep #5\n\n')

    try:
        ptrn = chem_element.lower()+ion+'*.dat'
        atomic_data_file = find(ptrn, spath+r'atdata')[0]
        atomic_data = open(atomic_data_file).read().split('\n')
        log.write('The atomic data file is {}\n\n'.format(atomic_data_file))
    except TypeError:
        raise IOError('There is no atomica data for this element and/or ' + \
                      'this ionization stage.')

    real_lower_level = atomic_data[lower_level].split("'")[1]
    real_upper_level = atomic_data[upper_level].split("'")[1]

    log.write('The eletronic levels are:\n\n' +\
              'Lower level: {}\n'.format(real_lower_level) + \
              'Upper level: {}'.format(real_upper_level))

    log.close()

    if verbose:
        print open('checklevels.log').read()

    return real_lower_level, real_upper_level
