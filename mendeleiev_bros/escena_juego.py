#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pilas
import random


archi = open('datos.txt', 'r')
nivel = archi.readline()
pantalla = archi.readline()
idioma = archi.readline()
archi.close()

if idioma == "ES":
    from modulos.ES import *
else:
    from modulos.EN import *


# Definimos la tecla que moverán al personaje
tecla = {pilas.simbolos.w: 'arriba'}


class Iniciar():
    "Representa un estado dentro del juego."

    def actualizar(self):
        self.contador_de_segundos += 1
        if self.contador_de_segundos > 2:

            self.texto.eliminar()
            if self.estado1 == "ganando":
                self.VolverMenu()
            return False
        return True

    def VolverMenu(self):
        import escena_niveles
        pilas.cambiar_escena(escena_niveles.EscenaNiveles())


class Iniciando(Iniciar):
    "Estado que indica que el juego ha comenzado."
    def __init__(self, nivel):
        self.estado1 = "iniciando"
        self.nivel = nivel
        nivel = juego_nivel + str(nivel)
        self.texto = pilas.actores.Texto(nivel, 0, 200, magnitud=30,
            vertical=False, fuente="data/tipo_tabla.ttf", fijo=True)
        self.texto.color = pilas.colores.negro
        self.texto.z = 5
        self.texto.y = [-200]
        self.contador_de_segundos = 0
        # Cada un segundo le avisa al estado que cuente.
        pilas.mundo.agregar_tarea(1, self.actualizar)


class Ganando(Iniciar):
    "Estado que indica que el juego ha comenzado."
    def __init__(self, nivel):
        self.estado1 = "ganando"
        nivel = juego_ganar + str(nivel)
        self.texto = pilas.actores.Texto(nivel, 0, 200, magnitud=30,
            vertical=False, fuente="data/tipo_tabla.ttf", fijo=True)
        self.texto.color = pilas.colores.negro
        self.texto.z = 5
        self.texto.y = [-200]
        self.contador_de_segundos = 0
        # Cada un segundo le avisa al estado que cuente.
        pilas.mundo.agregar_tarea(1, self.actualizar)


class Perdiendo(Iniciar):
    "Estado que indica que el juego ha comenzado."
    def __init__(self, nivel):
        self.estado1 = "ganando"
        nivel = juego_perder
        self.texto = pilas.actores.Texto(nivel, 0, 200, magnitud=30,
            vertical=False, fuente="data/tipo_tabla.ttf", fijo=True)
        self.texto.color = pilas.colores.negro
        self.texto.z = 5
        self.texto.y = [-200]
        self.contador_de_segundos = 0
        # Cada un segundo le avisa al estado que cuente.
        pilas.mundo.agregar_tarea(1, self.actualizar)


class Jacinto(pilas.actores.Actor):
    "Un actor que se mueve con las teclas a, s y ESPACIO y con animación"
    def __init__(self):
        pilas.actores.Actor.__init__(self)
        self.imagen = pilas.imagenes.cargar_grilla("data/grilla.png", 2)
        self.x = -200
        self.radio_de_colision = 30

    def definir_cuadro(self, indice):
        self.imagen.definir_cuadro(indice)


#Definimos la clase de nuestro juego
class Juego(pilas.escena.Base):

    def __init__(self, nivel):
        pilas.escena.Base.__init__(self)
        self.nivel = nivel

    def iniciar(self):

        self.cambiar_estado(Iniciando(self.nivel))
        pilas.fondos.Fondo('data/fondo2.jpg')
        self.paredes_arriba = []  # paredes a la derecha de jacinto y arriba
        self.paredes_abajo = []  # paredes a la derecha de jacinto y abajo
        self.paredes_puntuadas = []  # paredes a la izquierda de jacinto
        self.MoleculasHidrogeno = []
        self.SinCombustible = False  # Controla el fin del combustible
        self.jacinto = Jacinto()
        self.jacinto.definir_cuadro(1)
        self.dy = -1  # gravedad
        self.altura_diff = 80  # max 60 min 80
        self.altura = 62 + self.altura_diff  # altura de abertura// 62(jacinto)
        self.crear_pared()

        self.cont = pilas.actores.Texto("3", 264, -150, magnitud=50,
            vertical=False, fuente="data/tipo_tabla.ttf", fijo=True)
        self.cont.color = pilas.colores.negro

        pilas.mundo.agregar_tarea(3, self.lets_go)
        pilas.mundo.agregar_tarea(1, self.contador)

        # Creamos un control personalizado con esas teclas
        self.mandos = pilas.control.Control(self, tecla)
        # creamos las barras, barra = h2, barra1 = puntos
        self.barra = pilas.actores.Energia(progreso=100, ancho=150, alto=15,
            con_brillo=False)
        self.barra.x = 200
        self.barra.y = 200
        self.barra1 = pilas.actores.Energia(progreso=0, ancho=150, alto=15,
            color_relleno=pilas.colores.rojo, con_sombra=False,
            con_brillo=False)
        self.barra1.x = 200
        self.barra1.y = 170

        pilas.mundo.colisiones.agregar(self.jacinto, self.MoleculasHidrogeno,
                                                    self.RellenarCombustible)

    def contador(self):
        if self.cont.texto == "0":
            self.cont.eliminar()
            return False
        else:
            self.cont.texto = str(int(self.cont.texto) - 1)
            return True

    def lets_go(self):
        pilas.mundo.agregar_tarea(0.01, self.act)
        pilas.mundo.agregar_tarea(2.5, self.crear_pared)
        pilas.mundo.agregar_tarea(6.5, self.crear_h2)

    def cambiar_estado(self, estado):
        self.estado = estado

    def limpiar(self):
        # se eliminan las paredes fuera de pantalla.

            if self.paredes_arriba[0].x < self.jacinto.x - 25:
                self.paredes_arriba[0].eliminar()
                self.paredes_abajo[0].eliminar()

    def RellenarCombustible(self, jacinto, h2):
        #colisión jacinto->H2
        h2.eliminar()
        self.barra.progreso = 100

    def crear_h2(self):
        molecula = pilas.actores.Actor("data/h2.png")
        molecula.y = random.randrange(-250, 250)
        molecula.x -= 90
        molecula.radio_de_colision = 20
        self.MoleculasHidrogeno.append(molecula)
        return True

    def crear_pared(self):
        pared = pilas.actores.Actor("data/pared.png")
        pared1 = pilas.actores.Actor("data/pared.png")
        random1 = random.randrange(- 250 + self.altura, 250)
        pared.abajo = random1
        pared1.arriba = random1 - self.altura
        self.paredes_arriba.append(pared)
        self.paredes_abajo.append(pared1)
        return True

    def grabartxt(self):
        archi = open('datos.txt', 'r')
        nivel = archi.readline()
        nivel_sumado = int(nivel) + 1
        pantalla = archi.readline()
        archi.close()
        archi = open('datos.txt', 'w')

        archi.write(str(nivel_sumado) + "\n" + pantalla)

        archi.close()
        return False

    def ganar(self):
        if  self.barra1.progreso == 100:
            self.barra1.progreso = 0
            pilas.escena_actual().tareas.eliminar_todas()
            self.grabartxt()

            self.barra.eliminar()
            self.barra1.eliminar()
            self.jacinto.eliminar()
            for pared in self.paredes_abajo:
                pared.eliminar()
            for pared in self.paredes_arriba:
                pared.eliminar()
            for molecula in self.MoleculasHidrogeno:
                molecula.eliminar()
            self.cambiar_estado(Ganando(self.nivel))

    def act(self):
        self.ganar()

        self.colision()
        self.limpiar()
        if not self.SinCombustible:
            progreso = self.barra.progreso
            if progreso <= 0:
                self.SinCombustible = True
            else:
                self.barra.progreso -= 0.05  # resta combustible
            if self.jacinto.arriba <= 250:
                #para que no suba más de lo debido
                if self.mandos.arriba:
                    self.jacinto.definir_cuadro(0)
                    self.jacinto.y += 3
                else:
                    self.jacinto.definir_cuadro(1)

        self.movimiento()

        if self.jacinto.y == -200:  # si toca el suelo
            self.final()

        return True

    def movimiento(self):
        for molecula in self.MoleculasHidrogeno:  # movimiento h2
            molecula.x -= 1

        for pared in self.paredes_arriba:
            pared.x -= 1
        if pared.x == self.jacinto.x:

            if self.jacinto.arriba > pared.abajo:
                if self.barra1.progreso >= 10:
                    self.barra1.progreso -= 10
                else:
                    self.final()
            else:
                self.barra1.progreso += 5

        for pared in self.paredes_abajo:
            pared.x -= 1
            if pared.x == self.jacinto.x:
                if self.jacinto.abajo < pared.arriba:
                    if self.barra1.progreso >= 15:
                        self.barra1.progreso -= 15
                    else:
                        self.barra1.progreso -= 5
                        self.final()

        for pared in self.paredes_puntuadas:
            pared.x -= 1
            #acaba movimiento y empezamos con pj
        self.jacinto.y += self.dy

    def colision(self):  # Jacinto va por donde debe?

        return True

    def final(self):
        # fin del juego, se elimina todo menos el fondo
        pilas.escena_actual().tareas.eliminar_todas()
        self.barra.eliminar()
        self.barra1.eliminar()
        self.jacinto.eliminar()
        for pared in self.paredes_abajo:
            pared.eliminar()
        for pared in self.paredes_arriba:
            pared.eliminar()
        for molecula in self.MoleculasHidrogeno:
            molecula.eliminar()

        self.cambiar_estado(Perdiendo(self.nivel))
