# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:59:07 2019

@author: tanita

Descripción Visualización de forma de onda mas cálculo de transformadas de ondas
"""

import numpy as np
import matplotlib.pyplot as plt

# Definición de nombre de ensayo a levantar

direccion = 'Registro osciloscopio' + '/'
direccion_salida = 'Espectro ensayos' + '/'
nombre = 'Ensayo s_alim 12'
canal_1 = 'CH1'
canal_2 = 'CH2'
extension = '.npz'
nombre_salida = nombre

archivo_1 = direccion + nombre + ' ' + canal_1 + extension
archivo_2 = direccion + nombre + ' ' + canal_2 + extension
archivo_salida = direccion_salida + nombre_salida

def guardar_plot( tension, tiempo, title=None ):
    """Create a file with data."""
    title = title + '.npz'
    np.savez( title, x=tiempo, y=tension)

with np.load(archivo_1) as archivo:
    time_V1 = archivo['x']
    V1 = archivo['y']

with np.load(archivo_2) as archivo:
    time_V2 = archivo['x']
    V2 = archivo['y']

def fourier_spectrum( nsamples, data, deltat, logdb, power, rms ):
    """Given nsamples of real voltage data spaced deltat seconds apart,
    find the spectrum of the data (its frequency components). If logdb,
    return in dBV, otherwise linear volts. If power, return the power
    spectrum, otherwise the amplitude spectrum. If rms, use RMS volts,
    otherwise use peak-peak volts. Also return the number of frequency
    samples, the frequency sample spacing and maximum frequency. Note:
    The results from this agree pretty much with my HP 3582A FFT
    Spectrum Analyzer,
          although that has higher dynamic range than the 8 bit scope."""
    data_freq = np.fft.rfft(data * np.hanning( nsamples ))
    nfreqs = data_freq.size
    data_freq = data_freq / nfreqs
    ascale = 4
    if( rms ):
        ascale = ascale / ( 2 * np.sqrt(2) )
    if( power ):
        spectrum = ( ascale * absolute(data_freq) )**2
        if( logdb ):
            spectrum = 10.0 * np.log10( spectrum )
    else:
        spectrum = ascale * np.absolute(data_freq)
        if( logdb ):
            spectrum = 20.0 * log10( spectrum )
    freq_step = 1.0 / (deltat * 2 * nfreqs);
    max_freq = nfreqs * freq_step
    return( nfreqs, freq_step, max_freq, spectrum )

def freq_plot( nfreqs, spectrum, freq_step, max_freq, title=None, logdb=False, 
               fmin=0.0, fmax=10000.0, ylo=-60.0, yhi=0.0 ):
    """Create an amplitude versus frequncy plot for data analysed with
    fourier_spectrum()."""
    freqs = np.arange( 0, max_freq, freq_step )
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
    
# Función para dar vuelta datos de las tensiones
"""
V1_inv = np.zeros(V1.size)

V2_inv = np.zeros(V2.size)

print (V2.size)#[V2.size-1]

for i in range(0,(V1.size-1)):
    V1_inv[-i] = V1[i]
    V2_inv[-i] = V2[i]
"""

# Recortador de la imagen

ini_cut = np.empty(1)

ini_cut = 0

fin_cut = np.empty(1)

fin_cut = V1.size - 20

print (V1.size)

print (fin_cut,ini_cut)

V1_cort = V1[ ini_cut: fin_cut]
time_V1_cort = time_V1[ ini_cut: fin_cut ]

V2_cort = V2[ ini_cut: fin_cut]
time_V2_cort = time_V2[ ini_cut: fin_cut ]

# Cálculo de fourier de ambas funciones

## Creación de variables para función fourier_spectrum
    # Para V1
nsamples_V1 = V1_cort.size
deltat_V1 = time_V1_cort[1] - time_V1_cort[0]

    #Para V2

nsamples_V2 = V2_cort.size
deltat_V2 = time_V2_cort[1] - time_V2_cort[0]

## Amplitude spectrum and plot it.

# Cálculo de transformada de fourier para V1
( nfreqs_V1, freq_step_V1, max_freq_V1, spectrum_V1 ) = fourier_spectrum( nsamples_V1, V1_cort, deltat_V1, False, False, True )

# Presentación de datos principales en consola del espectro de V1
print ("Freq step", freq_step_V1, "Max freq", max_freq_V1, "Freq bins",nfreqs_V1)

# Cálcula de transformada de fourier para V2
( nfreqs_V2, freq_step_V2, max_freq_V2, spectrum_V2 ) = fourier_spectrum( nsamples_V2, V2_cort, deltat_V2, False, False, True )


# Presentación de datos principales en consola del espectro de V2
("Freq step", freq_step_V2, "Max freq", max_freq_V2, "Freq bins", nfreqs_V2)



#guardar_plot(V1_inv_cort,time_V1_cort,'Datos ordenados\Ensayo 1
#CH1_acond') guardar_plot(V2_inv_cort,time_V2_cort,'Datos
#ordenados\Ensayo 1 CH2_acond')

# Creación de ejes de frecuencia para plotear espectro

freqs_V1 = np.arange( 0, max_freq_V1, freq_step_V1 )
freqs_V2 = np.arange( 0, max_freq_V2, freq_step_V2 )

freqs_V1 = freqs_V1[0:spectrum_V1.size]
freqs_V2 = freqs_V1[0:spectrum_V2.size]

# Representación en subplot de gráficos como vienen e invertidos

fig, axs = plt.subplots(2, 2, figsize=(15,15))
fig.suptitle(nombre + ' 17/01' )
axs[0,0].plot(time_V1_cort, V1_cort)
axs[0,0].set_title('Long. cabezal (V1)')
axs[0,0].grid(True)
axs[0,1].set_xlim( 0, 100 )
axs[0,1].plot( freqs_V1, spectrum_V1, 'tab:red')
axs[0,1].set_title('Espectro de V1')
axs[0,1].grid(True)
axs[1,0].plot(time_V2_cort, V2_cort, 'tab:orange')
axs[1,0].set_title('Sensor inductivo (V2)')
axs[1,0].grid(True)
axs[1,1].set_xlim( 0, 100 )
axs[1,1].plot( freqs_V2, spectrum_V2, 'tab:green')
axs[1,1].set_title('Espectro de sensor inductivo (V2)')
axs[1,1].grid(True)

#for ax in axs.flat:
#    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right
# plots.
#for ax in axs.flat:
#    ax.label_outer()

plt.savefig(archivo_salida, dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype='a4', format='pdf',quality= 50)

plt.show()


# Ploteo de la información calculada de V1
#freq_plot( nfreqs_V1, spectrum_V1, freq_step_V1, max_freq_V1 )
#freq_plot( nfreqs_V1, spectrum_V1, freq_step_V1, max_freq_V1, 'Espectro de desplazamiento de cabezal', False, 0.0, 100 )

# Ploteo de la información calculada de V2
#freq_plot( nfreqs_V2, spectrum_V2, freq_step_V2, max_freq_V2, 'Espectro de sensor inductivo', False, 0.0, 100 )
