# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 16:59:07 2019

@author: tanita
"""

import numpy as np
import matplotlib.pyplot as plt

""" Definición de nombre de ensayo a levantar """

direccion = 'Registro osciloscopio' + '/'
nombre = 'Ensayo s_alim 14'
canal_1 = 'CH1'
canal_2 = 'CH2'
extension = '.npz'

archivo_1 = direccion + nombre + ' ' + canal_1 + extension
archivo_2 = direccion + nombre + ' ' + canal_2 + extension

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
    
""" Función para dar vuelta datos de las tensiones"""
"""
V1_inv = np.zeros(V1.size)

V2_inv = np.zeros(V2.size)

print (V2.size)#[V2.size-1]

for i in range(0,(V1.size-1)):
    V1_inv[-i] = V1[i]
    V2_inv[-i] = V2[i]
"""

""" Recortador de la imagen """

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

#guardar_plot(V1_inv_cort,time_V1_cort,'Datos ordenados\Ensayo 1 CH1_acond')
#guardar_plot(V2_inv_cort,time_V2_cort,'Datos ordenados\Ensayo 1 CH2_acond')

# Representación en subplot de gráficos como vienen e invertidos

fig, axs = plt.subplots(2, 1)
fig.suptitle(nombre)
axs[0].plot(time_V1_cort, V1_cort)
axs[0].set_title('Desplazamiento cabezal (V1)')
axs[1].plot(time_V2_cort, V2_cort, 'tab:orange')
axs[1].set_title('Sensor inductivo (V2)')
"""
axs[1, 0].plot(time_V1, V1, 'tab:green')
axs[1, 0].set_title('V1 sin invertir')
axs[1, 1].plot(time_V2, V2, 'tab:red')
axs[1, 1].set_title('V2 sin invertir')
"""
for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()
"""
plt.plot(time_V1_cort, V1_inv_cort,'b-', label = 'datos' )

#plt.plot( time_V1, V1,'r-', label = 'datos' )

plt.title( 'Time domain data. V1.' )
plt.xlabel( 'Time (s)' )
plt.ylabel( 'Volts' )
plt.grid( True )
plt.show()

plt.figure()
plt.plot(time_V2_cort, V2_inv_cort,'b-', label = 'datos' )

#plt.plot( time_V2, V2,'r-', label = 'datos' )

plt.title( 'Time domain data. V2.' )
plt.xlabel( 'Time (s)' )
plt.ylabel( 'Volts' )
plt.grid( True )
plt.show()

plt.figure()
plt.plot( time_V1, V1,'r-', label = 'datos' )
plt.title( 'Time domain data. V1.' )
plt.xlabel( 'Time (s)' )
plt.ylabel( 'Volts' )
plt.grid( True )
plt.show()

plt.figure()

plt.plot( time_V2, V2,'r-', label = 'datos' )

plt.title( 'Time domain data. V2.' )
plt.xlabel( 'Time (s)' )
plt.ylabel( 'Volts' )
plt.grid( True )
plt.show()
"""
print (np.max(time_V1))
