# -*- coding: utf-8 -*-
import pilas
MENSAJE_AYUDA = u"""
    En Medeleiev Bros eres un científico chiflado
    que quiere construir una bomba para
    destruir el mundo. El objetivo
    del juego es conseguir todas los elementos
    necesarios para construir la bomba.
"""


class Historia(pilas.escena.Base):
    "Es la escena que explica la história."
    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        pilas.fondos.Fondo("data/guarida2.png")
        self.crear_texto_historia()
        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla)

    def crear_texto_historia(self):
        texto = pilas.actores.Texto(MENSAJE_AYUDA, x=-6)
        texto.definir_color(pilas.colores.negro)
        pilas.avisar("Pulsa ESC para regresar")

    def cuando_pulsa_tecla(self, *k, **kw):
        import escena_menu
        pilas.cambiar_escena(escena_menu.EscenaMenu())
