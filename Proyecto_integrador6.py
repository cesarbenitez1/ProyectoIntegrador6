import os
import random
import readchar
from functools import reduce

class Juego:
    def __init__(self, laberinto_cadena, inicio, fin):
        self.laberinto = self.crear_matriz_laberinto(laberinto_cadena)
        self.inicio = inicio
        self.fin = fin
        self.px, self.py = inicio

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def crear_matriz_laberinto(self, laberinto_cadena):
        laberinto_matriz = list(map(list, laberinto_cadena.strip().split("\n")))
        return laberinto_matriz

    def mostrar_laberinto(self):
        self.limpiar_pantalla()
        for fila in self.laberinto:
            print("".join(fila))

    def main_loop(self):
        numero = 0  # Inicializar la variable 'numero'

        while (self.px, self.py) != self.fin:
            self.mostrar_laberinto()
            tecla = readchar.readkey()

            if tecla == 'n':
                numero += 1
                if numero > 50:
                    numero = 50
                self.limpiar_pantalla()
                print(f"Tecla presionada: {tecla}")
                print(f"Número: {numero}")
            else:
                nueva_px, nueva_py = self.px, self.py  # Valores por defecto si no se presiona una tecla de dirección

                if tecla == readchar.key.UP:
                    nueva_px, nueva_py = self.px - 1, self.py
                elif tecla == readchar.key.DOWN:
                    nueva_px, nueva_py = self.px + 1, self.py
                elif tecla == readchar.key.LEFT:
                    nueva_px, nueva_py = self.px, self.py - 1
                elif tecla == readchar.key.RIGHT:
                    nueva_px, nueva_py = self.px, self.py + 1
                else:
                    continue

                if (
                    0 <= nueva_px < len(self.laberinto)
                    and 0 <= nueva_py < len(self.laberinto[0])
                    and self.laberinto[nueva_px][nueva_py] != "#"
                ):
                    self.laberinto[self.px][self.py] = "."
                    self.px, self.py = nueva_px, nueva_py
                    self.laberinto[self.px][self.py] = "P"

        # El jugador ha llegado al final del laberinto
        self.mostrar_laberinto()
        print("¡Felicidades, lo lograste, has salido del laberinto!")

class JuegoArchivo(Juego):
    def __init__(self, path_a_mapas="maps"):
        # Lista de archivos de mapas en la carpeta "maps"
        map_files = os.listdir(path_a_mapas)

        if not map_files:
            raise Exception("No se encontraron archivos de mapas en la carpeta 'maps'.")

        # Seleccionar un archivo de mapa de forma aleatoria
        nombre_archivo = random.choice(map_files)

        # Componer la ruta completa al archivo
        path_completo = os.path.join(path_a_mapas, nombre_archivo)

        # Leer el mapa y las coordenadas de inicio y fin desde el archivo
        laberinto_cadena, inicio, fin = self.leer_mapa_desde_archivo(path_completo)

        # Llamar al constructor de la clase base (Juego) con los datos del mapa
        super().__init__(laberinto_cadena, inicio, fin)

    def leer_mapa_desde_archivo(self, archivo):
        with open(archivo, 'r') as file:
            lines = file.readlines()

        #coordenadas de inicio y fin
        inicio = tuple(map(int, lines[0].strip().split()))
        fin = tuple(map(int, lines[1].strip().split()))

        # Concatenar las filas del mapa usando reduce
        laberinto_cadena = reduce(lambda x, y: x + y, lines[2:], '').strip()

        return laberinto_cadena, inicio, fin

def main():
    print("¡Bienvenido al juego de laberinto!")
    nombre_jugador = input("Por favor, ingresa tu nombre: ")
    print(f"¡Hola, {nombre_jugador}! Comencemos a jugar.")

    juego = JuegoArchivo()
    juego.main_loop()

if __name__ == "__main__":
    main()
