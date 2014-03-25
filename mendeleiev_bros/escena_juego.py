#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pilas
import random

# Definimos la tecla que moverán al personaje
teclas = {pilas.simbolos.w: 'arriba'}


#Definimos la clase de nuestro juego
class Juego(pilas.escena.Base):

    def __init__(self):
        pilas.escena.Base.__init__(self)

    def iniciar(self):
        pilas.fondos.Fondo('data/fondo2.jpg')
        self.paredes_arriba = []  # paredes a la derecha de jacinto y arriba
        self.paredes_abajo = []  # paredes a la derecha de jacinto y abajo
        self.paredes_puntuadas = []  # paredes a la izquierda de jacinto
        self.MoleculasHidrogeno = []
        self.SinCombustible = False  # Controla el fin del combustible
        self.jacinto = pilas.actores.Actor("data/jacinto.png")
        self.jacinto.x = -200
        self.jacinto.radio_de_colision = 30
        self.dy = -1  # gravedad
        self.altura_diff = 80  # max 60 min 80
        self.altura = 62 + self.altura_diff  # altura de abertura
        self.crear_pared()
        pilas.mundo.agregar_tarea(0.01, self.act)
        pilas.mundo.agregar_tarea(3, self.crear_pared)
        # Creamos un control personalizado con esas teclas
        self.mandos = pilas.control.Control(self, teclas)
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
        pilas.mundo.agregar_tarea(6, self.crear_h2)
        pilas.mundo.colisiones.agregar(self.jacinto, self.MoleculasHidrogeno,
                                                    self.RellenarCombustible)

    def limpiar(self):
        # se eliminan las paredes fuera de pantalla.
        for pared in self.paredes_puntuadas:
            if pared.x < self.jacinto.x - 150:
                pared.eliminar()

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

    def act(self):
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
                    self.jacinto.y += 3
        for molecula in self.MoleculasHidrogeno:  # movimiento h2
            molecula.x -= 0.7

        for pared in self.paredes_arriba:
            pared.x -= 0.7
            if pared.x <= self.jacinto.x:
                if self.colision(pared, "a"):
                    self.barra1.progreso += 5  # barra puntos
                    self.paredes_arriba.remove(pared)
                    self.paredes_puntuadas.append(pared)

        for pared in self.paredes_abajo:
            pared.x -= 0.7
            if pared.x <= self.jacinto.x:
                if self.colision(pared, "b"):
                    self.paredes_abajo.remove(pared)
                    self.paredes_puntuadas.append(pared)

        for pared in self.paredes_puntuadas:
            pared.x -= 0.7
            #acaba movimiento y empezamos con pj
        self.jacinto.y += self.dy

        if self.jacinto.y == -200:
            self.final()

        return True

    def colision(self, pared, pos):  # Jacinto va por donde debe?
        if pos == "a":
            if self.jacinto.arriba > pared.abajo:
                self.final()
            else:
                return True
        if pos == "b":
            if self.jacinto.abajo < pared.arriba:
                self.final()
            else:
                return True

    def final(self):
        # fin del juego, se elimina todo menos el fondo
        pilas.avisar("Has perdido")
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
