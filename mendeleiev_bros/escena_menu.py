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


class EscenaMenu(pilas.escena.Base):
    "Es la escena de presentación donde se elijen las opciones del juego."

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):

        pilas.fondos.Fondo("data/guarida.jpg")

        pilas.avisar(menu_aviso)
        self.crear_el_menu_principal()
        pilas.mundo.agregar_tarea(0.1, self.act)
        self.sonido = pilas.sonidos.cargar("data/menu.ogg")
        self.sonido.reproducir()

    def crear_el_menu_principal(self):
        opciones = [

        (menu1, self.comenzar_a_jugar),
        (menu2, self.mostrar_ayuda_del_juego),
        (menu3, self.mostrar_historia),
        (menu4, self.mostrar_opciones),
        (menu5, self.salir_del_juego)
        ]
        self.trans = pilas.actores.Actor("data/trans.png")
        self.trans.x = -155
        self.trans.arriba = 85
        self.menu = pilas.actores.Menu(opciones, x=-150, y=70, color_normal=
        pilas.colores.negro, color_resaltado=pilas.colores.rojo)
        self.menu.x = -150

    def act(self):
        if self.menu.x == -500:
            if self.donde == "jugar":
                import escena_niveles
                pilas.cambiar_escena(escena_niveles.EscenaNiveles(self.sonido))
                return False
            elif self.donde == "historia":
                import escena_historia
                pilas.cambiar_escena(escena_historia.Historia())
            elif self.donde == "ayuda":
                import escena_ayuda
                pilas.cambiar_escena(escena_ayuda.Ayuda())
            elif self.donde == "opciones":
                import escena_opciones
                pilas.cambiar_escena(escena_opciones.Opciones())

        return True

    def mostrar_historia(self):
        self.menu.x = [-500]
        self.trans.x = [-500]
        self.donde = "historia"

    def mostrar_opciones(self):
        self.menu.x = [-500]
        self.trans.x = [-500]
        self.donde = "opciones"

    def comenzar_a_jugar(self):
        self.menu.x = [-500]
        self.trans.x = [-500]
        self.donde = "jugar"

    def mostrar_ayuda_del_juego(self):
        self.menu.x = [-500]
        self.trans.x = [-500]
        self.donde = "ayuda"

    def salir_del_juego(self):
        pilas.terminar()
