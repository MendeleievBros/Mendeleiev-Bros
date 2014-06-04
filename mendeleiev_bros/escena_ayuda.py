# -*- coding: utf-8 -*-
import pilas

archi = open('datos.txt', 'r')
nivel = archi.readline()
pantalla = archi.readline()
idioma = archi.readline()
archi.close()

if idioma == "ES":
    from modulos.ES import *
else:
    from modulos.EN import *


class Ayuda(pilas.escena.Base):
    "Es la escena que da instrucciones de cómo jugar."
    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        pilas.fondos.Fondo("data/guarida2.png")
        self.crear_texto_ayuda()
        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla)

    def crear_texto_ayuda(self):
        texto = pilas.actores.Texto(ayuda_Principal, y=30)
        texto.definir_color(pilas.colores.negro)
        pilas.avisar(ayuda_aviso)

    def cuando_pulsa_tecla(self, *k, **kw):
        import escena_menu
        pilas.cambiar_escena(escena_menu.EscenaMenu())
