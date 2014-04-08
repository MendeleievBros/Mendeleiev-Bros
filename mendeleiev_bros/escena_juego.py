#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pilas
import random

# Definimos la tecla que moverán al personaje
tecla = {pilas.simbolos.w: 'arriba'}


class Iniciar:
    "Representa un estado dentro del juego."
    def actualizar(self):
        self.contador_de_segundos += 1
        if self.contador_de_segundos > 2:

            self.texto.eliminar()
            return False
        return True


class Iniciando(Iniciar):
    "Estado que indica que el juego ha comenzado."
    def __init__(self, nivel):
        nivel = "Nivel" + str(nivel)
        self.texto = pilas.actores.Texto(nivel, 0, 200, magnitud=30,
            vertical=False, fuente="data/tipo_tabla.ttf", fijo=True)
        self.texto.color = pilas.colores.negro
        self.texto.z = 5
        self.texto.y = [-200]
        self.contador_de_segundos = 0
        # Cada un segundo le avisa al estado que cuente.
        pilas.mundo.agregar_tarea(1, self.actualizar)


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
        self.jacinto = pilas.actores.Actor("data/jacinto.png")
        self.jacinto.x = -200
        self.jacinto.radio_de_colision = 30
        self.dy = -1  # gravedad
        self.altura_diff = 80  # max 60 min 80
        self.altura = 62 + self.altura_diff  # altura de abertura// 62(jacinto)
        self.crear_pared()
        pilas.mundo.agregar_tarea(0.01, self.act)

        pilas.mundo.agregar_tarea(2.5, self.crear_pared)
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
        pilas.mundo.agregar_tarea(6.5, self.crear_h2)
        pilas.mundo.colisiones.agregar(self.jacinto, self.MoleculasHidrogeno,
                                                    self.RellenarCombustible)

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

    def act(self):
        print self.barra1.progreso
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
                    self.jacinto.y += 3

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
                self.barra1.progreso -= 10
            else:
                self.barra1.progreso += 5

        for pared in self.paredes_abajo:
            pared.x -= 1
            if pared.x == self.jacinto.x:
                if self.jacinto.abajo < pared.arriba:
                    self.barra1.progreso -= 15

        for pared in self.paredes_puntuadas:
            pared.x -= 1
            #acaba movimiento y empezamos con pj
        self.jacinto.y += self.dy

    def colision(self):  # Jacinto va por donde debe?

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
