import copy
import numpy as np
from matplotlib import colors
import matplotlib.pyplot as plt


class Auxiliar():

    def __init__(self, estado):

        self.estado = self.adjacent_triplet(estado)
        self.estado2 = self.square_between_a_pair(estado)

    def adjacent_triplet(status):
        new_status = status
        for j in range(len(new_status[0])):
            for i in range(len(new_status)):
                if len(status) - i >= 3:
                    if new_status[i][j] == new_status[i+1][j] == new_status[i+2][j]:
                        new_status[i][j] = 0
                        new_status[i+2][j] = 0
        for i in range(len(new_status)):
            for j in range(len(new_status[0])):
                if len(status[0]) - j >= 3:
                    if new_status[i][j] == new_status[i][j+1] == new_status[i][j+2]:
                        new_status[i][j] = 0
                        new_status[i][j+2] = 0
        return new_status

    def twoNext(status):
        new_status = copy.deepcopy(status)
        for j in range(len(new_status[0])):
            for i in range(len(new_status)):
                if len(status) - i >= 2:
                    if new_status[i][j] == new_status[i+1][j]:
                        valour = new_status[i][j]

                        for i2 in range(len(new_status)):
                            colum = (new_status[i2][j])
                            if (new_status[i2][j] == valour and i2 != i and i2 != i + 1):
                                new_status[i2][j] = 0
        for i in range(len(new_status)):
            for j in range(len(new_status[0])):
                if len(status[0]) - j >= 2:
                    if new_status[i][j] == new_status[i][j+1]:
                        valour = new_status[i][j]
                        row = new_status[i]
                        for l in range(len(new_status[0])):
                            if(new_status[i][l] == valour and l != j and l != j+1):
                                new_status[i][l] = 0
        return new_status

    def square_between_a_pair(status):
        res = False
        for j in range(len(status[0])):
            for i in range(len(status)):
                if len(status) - i >= 2:
                    if status[i - 1][j] == status[i + 1][j] and status[i][j] == 0:
                        res = True
                        break
        for i in range(len(status)):
            for j in range(len(status[0])):
                if len(status[0]) - j >= 2:
                    if status[i][j - 1] == status[i][j + 1] and status[i][j] == 0:
                        res = True
                        break
        return res

    def pair_induction(estado, estado_traspuesta):
        estado_copy = copy.deepcopy(estado)
        for i in range(len(estado)):
            for j in range(len(estado[0])):
                aux = []
                valid_colum_in_row = list(filter(lambda x: 0 <= x < len(estado[0]), [j, j+1, j + 2, j + 3]))
                for f in valid_colum_in_row:
                    aux.append(estado[i][f])
                if aux.count(estado[i][j]) == 3 and estado[i][j] != 0:
                    if aux[0] == aux[1] == aux[3]:
                      estado_copy[i][j+3] = 0
                    if aux[0] == aux[2] == aux[3]:
                        estado_copy[i][j] = 0
        for i in range(len(estado_traspuesta)):
            for j in range(len(estado_traspuesta[0])):
                aux = []
                valid_colum_in_row = list(filter(lambda x: 0 <= x < len(estado_traspuesta[0]), [j, j+1, j + 2, j + 3]))
                for f in valid_colum_in_row:
                    aux.append(estado_traspuesta[i][f])
                if aux.count(estado_traspuesta[i][j]) == 3 and estado_traspuesta[i][j] != 0:
                    if aux[0] == aux[1] == aux[3]:
                        estado_copy[j + 3][i] = 0
                    if aux[0] == aux[2] == aux[3]:
                        estado_copy[j][i] = 0
        return estado_copy

    def imprime_solucion(estado, mensaje):
        filas = []
        columnas = []
        for i in range(len(estado)):
            filas.append(len(estado) - 1 - i)
        for j in range(len(estado[0])):
            columnas.append(j)
        estado2 = []
        for x in range(len(estado)):
            estado2.append(estado[len(estado) - 1 - x])
        harvest = np.array(estado2)
        fig, ax = plt.subplots()
        # BLANCO Y NEGRO
        cmap = colors.ListedColormap(['black', 'white'])
        bounds = [0, 1, 1]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        im = ax.imshow(harvest, interpolation='nearest', origin='lower',
                       cmap=cmap, norm=norm)
        # BLANCO Y NEGRO
        # COLORES
        # im = ax.imshow(harvest)
        # COLORES
        ax.set_xticks(np.arange(len(columnas)))
        ax.set_yticks(np.arange(len(filas)))
        ax.set_xticklabels(columnas)
        ax.set_yticklabels(filas)
        plt.setp(ax.get_yticklabels(), rotation=0, ha="right", rotation_mode="anchor")
        # plt.grid(which='major', color='black', linestyle='-', linewidth=1)
        for i in range(len(filas)):
            for j in range(len(columnas)):
                text = ax.text(j, i, harvest[i, j],
                               ha="center", va="center", color="black")
        ax.set_title(mensaje)
        fig.tight_layout()
        plt.show()
        return estado

    def detallado(self):
        detallado = "error"
        counter = 0
        while detallado == "error":
            detallado = input("¿Quiere una solución detallada? (si/no): ")
            if detallado == "si":
                detallado = True
            elif detallado == "no":
                detallado = False
            else:
                counter = counter + 1
                detallado = "error"
                print("\nComnando incorrecto la respuesta tiene que ser si ó no")
                print('Este es su error {}. Después de 3 error se realizará una búsqueda sin detallado\n'.format(counter))
                if counter == 3:
                    detallado = False
        print("\nRealizando la búsqueda, sea paciente por favor.\n")
        return detallado

    def inserta_matriz(self):
        status = []
        n = input("Intruduzca su matriz a resolver: ")
        n = list(n.split("],["))
        for i in range(len(n)):
            if i == 0:
                n[0] = n[0][2:]
            if i == len(n) - 1:
                n[i] = n[i][:-2]
            n[i].replace("[", "")
        for i in range(len(n)):
            cells = []
            aux = n[i].split(",")
            for j in range(len(aux)):
                cells.append(int(aux[j]))
            status.append(cells)
        return status

    def elige_algoritmo(self):
        resolucion = 9
        counter = 0

        while resolucion == 9:
            n = (input(
                '\nSeleccione algoritmo de búsqueda\n' +
                '1: Búsqueda en Anchura,\n'
                '2: Búsqueda en Profundidad,\n'
                '3: Búsqueda óptima,\n'
                '4: Búsqueda A*,\n'
                '\nDecisión:'))
            if n == '1':
                resolucion = 1
            elif n == '2':
                resolucion = 2
            elif n == '3':
                resolucion = 3
            elif n == '4':
                resolucion = 4
            else:
                counter = counter + 1
                print("\nSolución no válida. Recuerde que debe introducir un número entre 1 y 4")
                print('Este es su error {}. Después de 3 error se realizará una búsqueda A*'.format(counter))
                if counter == 3:
                    resolucion = 4
                else:
                    resolucion = 9
        return resolucion

    def repeatsNumber(estado):
        filas = 0
        columnas = 0
        for i in range(len(estado)):
            to_check_row = list(filter(lambda x: x != 0, estado[i]))
            to_check_row_distinct = list(set(to_check_row))
            if len(to_check_row) != len(to_check_row_distinct):
                filas = filas + 1
        estado_traspuesta = [[estado[j][i] for j in range(len(estado))] for i in range(len(estado[0]))]
        for i in range(len(estado_traspuesta)):
            to_check_row = list(filter(lambda x: x != 0, estado_traspuesta[i]))
            to_check_row_distinct = list(set(to_check_row))
            if len(to_check_row) != len(to_check_row_distinct):
                columnas = columnas + 1
        res = filas + columnas
        return res

    def multipleCero(status):
        new_status = status
        res = 0
        bool = False
        for i in range(len(new_status)):
            for j in range(len(new_status[0])):
                if new_status[i][j] == 0:
                    cell = new_status[i][j]
                    if(i > 0):
                        valourUp = new_status[i-1][j]
                        row = status[i - 1]
                        for jj in range(len(new_status[0])):
                            if(new_status[i-1][jj] == valourUp and jj != j):
                                new_status[i-1][jj] = 0
                                res = res + 1
                        for i2 in range(len(new_status)):
                            colum = (new_status[i2][j])
                            if(colum == valourUp and i - 1 != i2):
                                new_status[i2][j] = 0
                                res = res + 1
                    if(i < len(new_status) - 1):
                        valourDown = new_status[i + 1][j]
                        row = status[i + 1]
                        for jj in range(len(new_status[0])):
                            if (new_status[i + 1][jj] == valourDown and jj != j):
                                new_status[i + 1][jj] = 0
                                res = res + 1
                        for i2 in range(len(new_status)):
                            colum = (new_status[i2][j])
                            if(colum == valourDown and i + 1 != i2):
                                new_status[i2][j] = 0
                                res = res + 1
                    if (j < len(new_status[0]) - 1):
                        valourRight = new_status[i][j+1]
                        row = status[i]
                        for jj in range(len(new_status[0])):
                            if (new_status[i][jj] == valourRight and jj != j + 1):
                                new_status[i][jj] = 0
                                res = res + 1
                        for i2 in range(len(new_status)):
                            colum = (new_status[i2][j + 1])
                            if(colum == valourRight and i != i2):
                                new_status[i2][j + 1] = 0
                                res = res + 1
                    if(j > 0):
                        valourLeft = new_status[i][j-1]
                        row = status[i]
                        for jj in range(len(new_status[0])):
                            if (new_status[i][jj] == valourLeft and jj != j - 1):
                                new_status[i][jj] = 0
                                res = res + 1
                        for i2 in range(len(new_status)):
                            colum = (new_status[i2][j - 1])
                            if (colum == valourLeft and i != i2):
                                new_status[i2][j - 1] = 0
                                res = res + 1
        if(res > 0):
            bool = True
        return bool

    def no_aplicable(status, fila, columna):
        copy_status = copy.deepcopy(status)
        valor = copy_status[fila][columna]
        for i in range(len(copy_status)):
            if valor == copy_status[i][columna] & i != fila:
                copy_status[i][columna] = 0
        for j in range(len(copy_status[0])):
            if valor == copy_status[fila][j] & i != fila:
                copy_status[fila][j] = 0
        return copy_status

    def check_two_ceros(estado):
        for i in range(len(estado) - 1):
            for j in range(len(estado) - 1):
                if estado[i][j] == estado[i][j + 1] == 0:
                    return True
        estado_traspuesta = [[estado[j][i] for j in range(len(estado))] for i in range(len(estado[0]))]
        for i in range(len(estado_traspuesta) - 1):
            for j in range(len(estado_traspuesta) - 1):
                if estado_traspuesta[i][j] == estado_traspuesta[i][j + 1] == 0:
                    return True
        return False

