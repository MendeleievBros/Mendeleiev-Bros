# -*- coding: utf-8 -*-
import pilas
pilas.iniciar(ancho=700, alto=500,
                                                     titulo="Medeleiev Bros!")
# Inicia la escena actual.
import escena_menu
pilas.cambiar_escena(escena_menu.EscenaMenu())
pilas.ejecutar()
