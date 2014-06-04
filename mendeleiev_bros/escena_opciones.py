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


class texto(pilas.actores.Texto):

    def __init__(self, texto='', x=0, y=0, valor=0):
        pilas.actores.Texto.__init__(self, texto=texto, x=x, y=y, magnitud=15)
        self.color = pilas.colores.negro
        self.valor = valor


class Opciones(pilas.escena.Base):
    "Es la escena que explica la história."
    def __init__(self):
        pilas.escena.Base.__init__(self)

    def cambiar(self, valor):

        if valor == "F":
            self.pantalla = valor + "\n"
            self.texto1.texto = opciones_pantallaF
        elif valor == "T":
            self.pantalla = valor + "\n"
            self.texto1.texto = opciones_pantallaT

        elif valor == "EN":
            self.idioma = valor
            self.texto3.texto = "English"
        elif valor == "ES":
            self.idioma = valor
            self.texto3.texto = u"Español"
        self.guardar()

    def guardar(self):
        archi = open('datos.txt', 'w')
        archi.write(str(self.nivel) + self.pantalla + self.idioma)
        archi.close()

    def opcion(self, evento):
        #Recorro la lista de banderas para ver si le he dado
        for elemento in self.opciones:
            # Miro si el ratón entra en colisión con el área de la bandera
            if elemento.colisiona_con_un_punto(evento.x, evento.y):
                self.cambiar(elemento.valor)

    def act(self):

        if self.creditos.x == -200.0:
            self.creditos.x = 205
            self.creditos.x = [-200], 8
        return True

    def iniciar(self):
        pilas.fondos.Fondo("data/guarida2.png")

        archi = open('datos.txt', 'r')
        self.nivel = archi.readline()
        self.pantalla = archi.readline()
        self.idioma = archi.readline()
        archi.close()

        self.opciones = []

        self.crear_opciones()

        self.pulsa_tecla_escape.conectar(self.cuando_pulsa_tecla)
        pilas.eventos.mueve_mouse.conectar(self.CambiarColor)
        pilas.eventos.click_de_mouse.conectar(self.opcion)
        pilas.mundo.agregar_tarea(0.1, self.act)

        self.texto = pilas.actores.Texto(opciones_op1,
                                                    magnitud=18, x=-150, y=100)
        self.texto.definir_color(pilas.colores.negro)
        self.texto2 = pilas.actores.Texto(opciones_op2, magnitud=18,
                                                             x=-150, y=0)
        self.texto2.definir_color(pilas.colores.negro)

    def CambiarColor(self, evento):

        if self.texto1.colisiona_con_un_punto(evento.x, evento.y):
            self.texto1.definir_color(pilas.colores.blanco)
        else:
            self.texto1.definir_color(pilas.colores.negro)

        if self.texto3.colisiona_con_un_punto(evento.x, evento.y):
            self.texto3.definir_color(pilas.colores.blanco)
        else:
            self.texto3.definir_color(pilas.colores.negro)

    def crear_opciones(self):
        if self.pantalla[0] == "F":
            self.texto1 = texto(opciones_pantallaF, -50, 100, "T")
        else:
            self.texto1 = texto(opciones_pantallaT, -50, 100, "F")

        if self.idioma[1] == "S":
            self.texto3 = texto(u"Español", -50, 0, "EN")
        else:
            self.texto3 = texto("English", -50, 0, "ES")

        self.opciones.append(self.texto1)
        self.opciones.append(self.texto3)
        self.scroll()
        pilas.avisar(opciones_aviso)

    def scroll(self):
        self.creditos = pilas.actores.Texto("Fernando Mola", magnitud=15,
             x=205, y=-188)
        self.creditos.definir_color(pilas.colores.negro)
        self.creditos.x = [-200], 8

    def cuando_pulsa_tecla(self, *k, **kw):
        import escena_menu
        pilas.cambiar_escena(escena_menu.EscenaMenu())
