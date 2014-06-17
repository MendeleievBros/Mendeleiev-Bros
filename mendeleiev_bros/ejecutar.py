# -*- coding: utf-8 -*-
import pilas
import os

if os.path.exists("datos.txt"):
    archi = open('datos.txt', 'r')
    nivel = archi.readline()
    pantalla = archi.readline()
    idioma = archi.readline()
    archi.close()
    if pantalla[0] == "F":

        pilas.iniciar(ancho=700, alto=500, pantalla_completa=False,
                            titulo="Medeleiev Bros!")
    else:
        pilas.iniciar(ancho=700, alto=500, pantalla_completa=True,
                            titulo="Medeleiev Bros!")
else:
    archi = open('datos.txt', 'w')

    archi.write("1\nT\nES")

    archi.close()

    pilas.iniciar(ancho=700, alto=500, pantalla_completa=True,
                   titulo="Medeleiev Bros!")

# Inicia la escena actual.
import escena_menu
pilas.cambiar_escena(escena_menu.EscenaMenu(True))
pilas.ejecutar()
