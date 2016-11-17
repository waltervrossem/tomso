"""
Functions for manipulating MESA input and output files.
"""

import numpy as np


def load_history(filename):
    """Reads a MESA history file and returns the global data and history
    data in two structured arrays.

    Parameters
    ----------
    filename: str
        Filename of the MESA history file to load.

    Returns
    -------
    header: structured array
        Global data for the evolutionary run. e.g. initial parameters.
        The keys for the array are the MESA variable names as in
        history.columns.

    data: structured array
        History data for the run. e.g. age, effective temperature.
        The keys for the array are the MESA variable names as in
        history.columns.
    """

    with open(filename, 'r') as f: lines = f.readlines()

    header = np.genfromtxt(lines[1:3], names=True)
    data = np.genfromtxt(lines[5:], names=True)

    return header, data


def load_profile(filename):
    """Reads a MESA profile and returns the global data and profile
    data in two structured arrays.

    Parameters
    ----------
    filename: str
        Filename of the MESA profile to load.

    Returns
    -------
    header: structured array
        Global data for the stellar model. e.g. total mass, luminosity.
        The keys for the array are the MESA variable names as in
        profile.columns.

    data: structured array
        Profile data for the stellar model. e.g. radius, pressure.
        The keys for the array are the MESA variable names as in
        profile.columns.
    """

    with open(filename, 'r') as f: lines = f.readlines()

    header = np.genfromtxt(lines[1:3], names=True)
    data = np.genfromtxt(lines[5:], names=True)

    return header, data


def load_results_data(filename):
    """Reads a set of MESA results from one of the optimization routines
    in the astero module.

    Parameters
    ----------
    filename: str
        Filename of the file containing the results.

    Returns
    -------
    data: structured array
        Array with all the results.
    """
    with open(filename, 'r') as f:
        lines = [line.replace('D', 'E') for line in f.readlines()]

    dtypes = [(word, 'float') for word in lines[1].split()]
    dtypes[0] = ('sample', 'int')
    for i in range(4): dtypes[31+i] = ('nl%i' % i, 'int')

    data = np.genfromtxt(lines[2:-4], dtype=dtypes,
                         usecols=range(len(dtypes)))

    return data


def load_sample(filename):
    with open(filename,'r') as f:
        lines = [line.split() for line in f.readlines() if line.strip()]

    d = {}
    ell = 0
    for line in lines:
        if line[0][:2] == 'l=':
            ell = int(line[0][-1])
            d['l%i' % ell] = {'n':[], 'chi2':[], 'mdl':[], 'cor':[],
                              'obs':[], 'err':[], 'logE':[]}
        elif len(line) == 7:
            d['l%i' % ell]['n'].append(int(line[0]))
            d['l%i' % ell]['chi2'].append(float(line[1]))
            d['l%i' % ell]['mdl'].append(float(line[2]))
            d['l%i' % ell]['cor'].append(float(line[3]))
            d['l%i' % ell]['obs'].append(float(line[4]))
            d['l%i' % ell]['err'].append(float(line[5]))
            d['l%i' % ell]['logE'].append(float(line[6]))
        else:
            key = ''.join([word + ' ' for word in line[:-1]])[:-1]
            # if key == 'mass/Msun':
            #     key = 'initial mass'

            value = float(line[-1].replace('D', 'e'))
            d[key] = value

    return d