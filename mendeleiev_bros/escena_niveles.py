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


class Elemento(pilas.actores.Texto):

    def __init__(self, texto='', x=0, y=0, nivel=0):
        pilas.actores.Texto.__init__(self, texto=texto, x=x, y=y, magnitud=10,
            vertical=False, fuente="data/tipo_tabla.ttf", fijo=True, ancho=0)
        self.color = pilas.colores.negro
        self.nivel = nivel


class EscenaNiveles(pilas.escena.Base):
    "Es la escena de presentación donde se elije el nivel."
    def __init__(self, sonido, repro=False):
        pilas.escena.Base.__init__(self)
        self.sonido = sonido
        if repro:
            self.sonido.reproducir()

    def leertxt(self):
        archi = open('datos.txt', 'r')
        linea = archi.readline()
        archi.close()
        return linea

    def nivel(self, evento):
        #Recorro la lista de banderas para ver si le he dado
        for elemento in self.elementos:
            # Miro si el ratón entra en colisión con el área de la bandera
            if elemento.colisiona_con_un_punto(evento.x, evento.y):
                if elemento.nivel <= int(self.nivel_guardado):
                    self.sonido.detener()
                    import escena_juego
                    pilas.cambiar_escena(escena_juego.Juego(elemento.nivel))

    def cuando_vuelves(self):
        import escena_menu
        pilas.cambiar_escena(escena_menu.EscenaMenu())

    def iniciar(self):
        pilas.fondos.Fondo("data/guarida.jpg")
        pilas.eventos.click_de_mouse.conectar(self.nivel)
        self.elementos = []
        self.candado = []
        self.nivel_guardado = self.leertxt()
        self.mostrar_tabla()
        self.volver = pilas.actores.Boton(ruta_normal='data/volver.png',
             ruta_over='data/volver.png')
        self.volver.x = 50
        self.volver.y = -140
        self.volver.conectar_presionado(self.cuando_vuelves)

    def candados(self):

        # muestra los candados de los niveles no disponibles
        for elemento in self.elementos:

            if elemento.nivel > int(self.nivel_guardado):
                candado1 = pilas.actores.Actor("data/candado.png")
                candado1.x = elemento.x
                candado1.y = elemento.y
                self.candado.append(candado1)
        return True

    def mostrar_tabla(self):

        self.trans1 = pilas.actores.Actor("data/tabla.png")
        self.elementos.append(Elemento(texto="H", x=-230, y=130, nivel=1))
        self.elementos.append(Elemento(texto="Li", x=-230, y=90, nivel=3))
        self.elementos.append(Elemento(texto="Na", x=-230, y=45, nivel=11))
        self.elementos.append(Elemento(texto="K", x=-230, y=0, nivel=19))
        self.elementos.append(Elemento(texto="Be", x=-205, y=90, nivel=4))
        self.elementos.append(Elemento(texto="Mg", x=-205, y=45, nivel=12))
        self.elementos.append(Elemento(texto="Ca", x=-205, y=0, nivel=20))
        self.elementos.append(Elemento(texto="B", x=80, y=90, nivel=5))
        self.elementos.append(Elemento(texto="Al", x=80, y=45, nivel=13))
        self.elementos.append(Elemento(texto="Ge", x=80, y=0, nivel=21))
        self.elementos.append(Elemento(texto="C", x=105, y=90, nivel=6))
        self.elementos.append(Elemento(texto="Si", x=105, y=45, nivel=14))
        self.elementos.append(Elemento(texto="Ga", x=105, y=0, nivel=22))
        self.elementos.append(Elemento(texto="N", x=130, y=90, nivel=7))
        self.elementos.append(Elemento(texto="P", x=130, y=45, nivel=15))
        self.elementos.append(Elemento(texto="As", x=130, y=0, nivel=23))
        self.elementos.append(Elemento(texto="O", x=155, y=90, nivel=8))
        self.elementos.append(Elemento(texto="S", x=155, y=45, nivel=16))
        self.elementos.append(Elemento(texto="Se", x=155, y=0, nivel=24))
        self.elementos.append(Elemento(texto="F", x=180, y=90, nivel=9))
        self.elementos.append(Elemento(texto="Cl", x=180, y=45, nivel=17))
        self.elementos.append(Elemento(texto="Br", x=180, y=0, nivel=25))
        self.elementos.append(Elemento(texto="He", x=210, y=130, nivel=2))
        self.elementos.append(Elemento(texto="Ne", x=210, y=90, nivel=10))
        self.elementos.append(Elemento(texto="Ar", x=210, y=45, nivel=18))
        self.elementos.append(Elemento(texto="Kr", x=210, y=0, nivel=26))
        self.candados()
