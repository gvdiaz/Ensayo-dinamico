# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 06:09:11 2019

@author: tanita
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 14:18:40 2019

@author: Gustavo V. Diaz
"""
from ctypes import *
from numpy import *
from time import sleep
import numpy as np
import matplotlib.pyplot as plt

lib = cdll.LoadLibrary( './rigol_ds1000.so' )

nombre_registro = 'Ensayo c_alim 18'

def argerr():
    raise RuntimeError( 'Invalid arguments.' )

class RigolDS(object):
    '''Class that encapsulates some Rigol DS1052E functionality.'''
    def __init__(self):
        self.obj = lib.Rigol_DS1000_new( c_int(0) )

    def callerr(self):
        """If a call fails, get an explanatory error message and show it."""
        lib.Rigol_DS1000_error_string.restype = c_char_p
        cp = lib.Rigol_DS1000_error_string( self.obj )
        if( not ( cp is None ) ):
            print 'Error: ' + cp
            raise RuntimeError( 'rigol_ds1000 call failed.' )

    def error(self):
        """Test for an error having occurred."""
        return( lib.Rigol_DS1000_error( self.obj ) )

    def get_error_info(self):
        """Get an error message."""
        lib.Rigol_DS1000_error_string.restype = c_char_p
        return( lib.Rigol_DS1000_error_string( self.obj ) )

    def command(self,c):
        """Send a low level command to the oscilloscope.
        All commands begin with a colon."""
        if( not lib.Rigol_DS1000_command( self.obj, c_char_p(c) ) ):
            self.callerr()
        return( 1 )

    def multi_command(self,c):
        """Send multiple commands, separated by semi-colons, to the oscilloscope."""
        if( not lib.Rigol_DS1000_command( self.obj, c_char_p(c) ) ):
            self.callerr()
        return( 1 )

    def query(self,q):
        """Send a query command to the oscilloscope and get its response
        back as a string. Query commands should contain a ?"""
        lib.Rigol_DS1000_string_query.restype = c_char_p
        cp = lib.Rigol_DS1000_string_query(self.obj,c_char_p(q))
        if( cp is None ):
            self.callerr()
        return( cp )

    def acquire(self,stopfirst,localafter):
        """Acquire waveform data from the oscilloscope.
        Return the number of data points available in each channel.
        Return 0 if a channel is not available.
        Also return the maximum of the two channels sample counts.
        If stopfirst is not 0, stop sampling before acquiring, then restart.
        If localafter is not 0, leave remote mode after acquisition.
        This function does the hard work of getting the measurements.
        Return tuple (chan1_samples, chan2_samples, maximum_samples)"""
        chan1_samples = c_int(0)
        chan2_samples = c_int(0)
        max_samples = c_int(0)
        if( not lib.Rigol_DS1000_acquire_channels( self.obj,byref(chan1_samples), byref(chan2_samples), byref(max_samples),c_int(stopfirst),c_int(localafter) ) ):
            self.callerr()
        return( chan1_samples.value, chan2_samples.value, max_samples.value )

    def read_channel(self,channel,samples):
        """Return samples number of waveform samples for channel (1 or 2).
        The sampling rate (time between samples), horizontal (time) and vertical (voltage)
        offsets are also returned.
        Return tuple (number_of_samples, sample_data, sample_rate, hoffset, voffset)"""
        sample_buffer = (c_float*samples)()
        deltat = c_float(0.0)
        hoffset = c_float(0.0)
        voffset = c_float(0.0)
        read_samples = lib.Rigol_DS1000_get_channel(self.obj,c_int(channel),byref(sample_buffer),                                           byref(deltat),byref(hoffset),byref(voffset) )
        if( read_samples == 0 ):
            self.callerr()
        data = fromiter( sample_buffer, dtype=float, count=read_samples )
        return( read_samples, data, deltat.value, hoffset.value, voffset.value )

def fourier_spectrum( nsamples, data, deltat, logdb, power, rms ):
    """Given nsamples of real voltage data spaced deltat seconds apart, find the spectrum of the
    data (its frequency components). If logdb, return in dBV, otherwise linear volts.
    If power, return the power spectrum, otherwise the amplitude spectrum.
    If rms, use RMS volts, otherwise use peak-peak volts.
    Also return the number of frequency samples, the frequency sample spacing and maximum frequency.
    Note: The results from this agree pretty much with my HP 3582A FFT Spectrum Analyzer,
          although that has higher dynamic range than the 8 bit scope."""
    data_freq = fft.rfft(data * hanning( nsamples ))
    nfreqs = data_freq.size
    data_freq = data_freq / nfreqs
    ascale = 4
    if( rms ):
        ascale = ascale / ( 2 * sqrt(2) )
    if( power ):
        spectrum = ( ascale * absolute(data_freq) )**2
        if( logdb ):
            spectrum = 10.0 * log10( spectrum )
    else:
        spectrum = ascale * absolute(data_freq)
        if( logdb ):
            spectrum = 20.0 * log10( spectrum )
    freq_step = 1.0 / (deltat * 2 * nfreqs);
    max_freq = nfreqs * freq_step
    return( nfreqs, freq_step, max_freq, spectrum )
    
def time_plot( nsamples, data, deltat, hoff, title=None ):
    """Create a simple amplitude versus time plot using Matplotlib."""
    times = arange( hoff, hoff+deltat*(nsamples-1), deltat )
    plt.plot( times, data[0:nsamples-1] )
    if( title == None ):
        plt.title( 'Time domain data. Volts.' )
    else:
        plt.title( title )
    plt.xlabel( 'Time (s)' )
    plt.ylabel( 'Volts' )
    plt.grid( True )
    plt.show()

def freq_plot( nfreqs, spectrum, freq_step, max_freq,
               title=None, logdb=False, 
               fmin=0.0, fmax=10000.0, ylo=-60.0, yhi=0.0 ):
    """Create an amplitude versus frequncy plot for data analysed with fourier_spectrum()."""
    freqs = arange( 0, max_freq, freq_step )
    plt.xlim( fmin, fmax )
    plt.plot( freqs, spectrum )
    if( title == None ):
        if( logdb ):
            plt.title( 'Frequency domain. Log RMS Volts.' )
        else:
            plt.title( 'Frequency domain. Linear RMS Volts.' )
    else:
        plt.title( title )
    plt.xlabel( 'Freq (Hz)' )
    if( logdb ):
        plt.ylabel( 'dBV RMS' )
        plt.ylim( -60, 0 )
    else:
        plt.ylabel( 'Volts RMS' )
    plt.grid( True )
    plt.show()
    
def guardar_plot( nsamples, data, deltat, hoff, title=None ):
    """Create a file with data."""
    title = title + '.npz'
    times = arange( hoff, hoff+deltat*(nsamples-1), deltat )
    np.savez( title, x=times, y=data[0:nsamples-1])
    



if __name__ == '__main__':
    o = RigolDS()
    print
    """
    print "Profundidad de memoria para canal 1"
    print o.query( ':CHANnel1:MEMoryDepth?' )
    print
    print "Profundidad de memoria para canal 2"
    print o.query( ':CHANnel2:MEMoryDepth?' )
    print
    """
    print "Profundidad de memoria de osciloscopio"
    print o.query( ':ACQ:MEMD?' )
    print
    # Configuración de adquisición promedio
    print "Promedio de adquisiciones"
    print o.query( ':ACQuire:AVERages?' )
    print
    
    print "Modo de la forma de onda de los canales"
    print o.query( ':WAVeform:POINTs:MODE?' )
    print
    print "Frecuencia de muestreo de ondas"
    print o.query( ":ACQ:SAMP? CHAN1" )
    print
    """
    print
    print "DATOS ADQUIRIDOS POR OSCILOSCOPIO"
    print
    print "Frecuencia de muestreo",o.query( ":ACQ:SAMP? CHAN1" )
    """
    """o.command( ':WAVeform:POINTs:MODE NORmal' )"""
    """
    f_muestreo = np.zeros(1)
    f_muestreo = float(o.query( ":ACQ:SAMP? CHAN1" ))
    deltat_osc = np.power(f_muestreo,-1)
    periodo_muestra = 600*deltat_osc
    print "Tiempo de muestreo de osciloscopio", deltat_osc, "seg"
    print "Período de muestra osciloscopio", periodo_muestra,"seg"
    print
    
    print
    print "DATOS CALCULADOS A PARTIR DE BASE DE TIEMPO"
    print
    b_tiempo = 0.00001
    print "Base tiempo configurada",b_tiempo,"seg/div"
    print
    deltat_calc = 12*b_tiempo/8192
    f_muestreo_calc = 1/deltat_calc
    print "Frecuencia de muestro calculada",f_muestreo_calc,"Hz"
    print "Tiempo de muestro calculado", deltat_calc,"seg"
    print "Período de muestra calculada", b_tiempo*12,"seg"
    print
    print "Relaciones entre frecuencias",f_muestreo/f_muestreo_calc
    print
    """
    #Lectura de datos general
    (nch1, nch2, nmax) = o.acquire(1,1)
    print nch1, nch2, nmax
    if( nch1 > 0 ):
        # Read data and plot it.
        (nsamples, data, deltat, hoff, voff ) = o.read_channel(1,nch1)
        print "Time domain data. Volts."
        print "samples", nsamples
        print "time step", deltat
        print "H offset", hoff
        print "V offset", voff
        time_plot( nsamples, data, deltat, hoff, 'Channel 1 Time Data' )
        guardar_plot( nsamples, data, deltat, hoff, nombre_registro + ' CH1')
    if( nch2 > 0 ):
        (nsamples, data, deltat, hoff, voff ) = o.read_channel(2,nch2)
        #print nsamples, deltat, hoff, voff
        print "samples", nsamples
        print "time step", deltat
        print "H offset", hoff
        print "V offset", voff
        time_plot( nsamples, data, deltat, hoff, 'Channel 2 Time Data' )
        guardar_plot( nsamples, data, deltat, hoff, nombre_registro + ' CH2')
