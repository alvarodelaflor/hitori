import problema_espacio_estados as probee

import búsqueda_espacio_estados as busqee

import investiga as investiga

from time import time

import auxiliar as auxiliar

from scipy.ndimage import label

import copy


class hitori(probee.ProblemaEspacioEstados):
    def __init__(self, status):

        acciones = [investiga.CrossOut(i, j) for i in range(0, len(status)) for j in range(0, len(status[0]))]
        self.estado_inicial = status

        super().__init__(acciones, self.estado_inicial)


if __name__ == '__main__':

    # Interactivo
    status = auxiliar.Auxiliar.inserta_matriz(None)
    resolucion = auxiliar.Auxiliar.elige_algoritmo(None)
    # Interactivo

    # Programatico
#    status = [[1,8,2,4,3,9,4,1,5],[6,5,5,1,1,4,9,3,3],[8,4,6,9,5,3,2,6,7],[4,8,3,8,7,8,8,2,9],[1,6,4,2,3,6,5,9,1],[9,5,8,3,5,2,7,6,1],[2,5,3,1,6,4,4,2,8],[5,4,4,2,9,3,7,7,6],[7,9,1,5,1,6,3,8,8]]
#    resolucion = 4
    # Programatico

    start_time1 = time()

    statusChange = auxiliar.Auxiliar.adjacent_triplet(status)
    statusChangeTras = [[statusChange[j][i] for j in range(len(statusChange))] for i in range(len(statusChange[0]))]
    statuschange2 = auxiliar.Auxiliar.pair_induction(statusChange, statusChangeTras)
    pom = hitori(statuschange2)
    hitori_resolver = probee.ProblemaEspacioEstados(pom.acciones, pom.estado_inicial)

    finish_time1 = time()
    execute_time1 = finish_time1 - start_time1

#    print(statusChange)
#    print(statusChangeTras)
#    print(statuschange2)
#    print(len(pom.acciones))
#    print(pom.acciones)

    if resolucion == 1:
        # Búsqueda en anchura
        detallado = auxiliar.Auxiliar.detallado(None)
        start_time2 = time()

        b_anchura = busqee.BúsquedaEnAnchura(detallado)
        print(b_anchura.buscar(hitori_resolver))

        finish_time2 = time()
        execute_time2 = finish_time2 - start_time2
        execute_time = execute_time1 + execute_time2

    elif resolucion == 2:
        # Búsqueda en profundidad
        detallado = auxiliar.Auxiliar.detallado(None)
        start_time2 = time()

        b_profundidad = busqee.BúsquedaEnProfundidad(detallado)
        print(b_profundidad.buscar(hitori_resolver))

        finish_time2 = time()
        execute_time2 = finish_time2 - start_time2
        execute_time = execute_time1 + execute_time2

    elif resolucion == 3:
        # Búsqueda óptima
        detallado = auxiliar.Auxiliar.detallado(None)
        start_time2 = time()

        b_óptima = busqee.BúsquedaÓptima(detallado)
        print(b_óptima.buscar(hitori_resolver))

        finish_time2 = time()
        execute_time2 = finish_time2 - start_time2
        execute_time = execute_time1 + execute_time2

    elif resolucion == 4:
        # Búsqueda A*
        print("\nRealizando la búsqueda, sea paciente por favor.\n")
        start_time2 = time()

        def h(nodo):
            estado = nodo.estado
            row = 100000000000000
            zeros = 0
            for i in range(len(estado)):
                to_check_row = list(estado[i])
                zeros = zeros + 1 * to_check_row.count(0)
                row = row + 10000 * (len(to_check_row) - len(set(to_check_row)))
            square = auxiliar.Auxiliar.square_between_a_pair(estado)
            if square:
                zeros = 0
            return row - 10000 * zeros

        b_a_estrella = busqee.BúsquedaAEstrella(h)
        print(b_a_estrella.buscar(hitori_resolver))

        finish_time2 = time()
        execute_time2 = finish_time2 - start_time2
        execute_time = execute_time1 + execute_time2

print("\nLa ejecución ha tardado: {}\n".format(execute_time))

