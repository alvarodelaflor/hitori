import problema_espacio_estados as probee

import copy


class CrossOut(probee.Acción):

    def __init__(self, i, j):
        nombre = 'La fila {} y columna {}'.format(i, j)
        super().__init__(nombre)
        self.cell_row = i
        self.cell_colum = j

    # Indica si la casilla ya esta tachada
    def is_cross(self, estado):
        return not estado[self.cell_row][self.cell_colum]

    # Indica si existe el mismo numero en esa fila
    def exist_in_row(self, estado):
        return bool(estado[self.cell_row].count(estado[self.cell_row][self.cell_colum]) > 1)

    # Indica si existe el mismo numero en esa columna
    def exist_in_colum(self, estado):
        # Versión 1
        res = 0
        for i in range(len(estado)):
            if estado[i][self.cell_colum] == estado[self.cell_row][self.cell_colum]:
                res = res + 1
        aux = False
        if res > 1:
            aux = True
        return aux
        # Version 2
#        estado_traspuesta = [[estado[j][i] for j in range(len(estado))] for i in range(len(estado[0]))]
#        return bool(estado_traspuesta[self.cell_row].count(estado_traspuesta[self.cell_row][self.cell_colum]) > 1)

    # Indica si existe ya una casilla tachada en los alrededores
    def exist_black_cell_around(self, estado):
        aux = 0
        res = False

        if self.cell_row != 0 and self.cell_row != 0 and estado[self.cell_row-1][self.cell_colum] == 0:
            aux = aux + 1
        if aux == 0 and self.cell_colum != 0 and estado[self.cell_row][self.cell_colum-1] == 0:
            aux = aux + 1
        if aux == 0 and self.cell_colum != len(estado[self.cell_row])-1 and estado[self.cell_row][self.cell_colum+1] == 0:
            aux = aux + 1
        if aux == 0 and self.cell_row != len(estado)-1 and estado[self.cell_row+1][self.cell_colum] == 0:
            aux = aux + 1
        if aux > 0:
            res = True
        return res

    def is_corner(self, estado , row, colum):
        res = False
        if colum == 0 and row == 0:
            res = True
        elif colum == 0 and row == len(estado)-1:
            res = True
        elif colum == len(estado[0])-1 and row == 0:
            res = True
        elif colum == len(estado[0])-1 and row == len(estado) - 1:
            res = True
        return res

    def is_lateral(self, estado, row, colum):
        res = False
        if colum == 0 or colum == (len(estado[0]) - 1):
            res = True
        elif row == 0 or row == (len(estado) - 1):
            res = True
        return res

    # Indica si, al borrar una celda, si aisla con huecos alguna otra
    def check_isolate_cell(self, estado):
        res = 0
        auxSup = self.get_croos_around(estado,self.cell_row-1,self.cell_colum)
        if self.is_corner(estado,self.cell_row-1,self.cell_colum) and auxSup >= 1:
            res = res + 1
        elif self.is_lateral(estado,self.cell_row-1,self.cell_colum) and auxSup >= 2:
            res = res + 1
        elif auxSup >= 3:
            res = res + 1

        auxInf = self.get_croos_around(estado, self.cell_row + 1, self.cell_colum)
        if self.is_corner(estado, self.cell_row + 1, self.cell_colum) and auxInf >= 1:
            res = res + 1
        elif self.is_lateral(estado, self.cell_row + 1, self.cell_colum) and auxInf >= 2:
            res = res + 1
        elif auxInf >= 3:
            res = res + 1

        auxRight = self.get_croos_around(estado, self.cell_row, self.cell_colum + 1)
        if self.is_corner(estado, self.cell_row, self.cell_colum + 1) and auxRight >= 1:
            res = res + 1
        elif self.is_lateral(estado, self.cell_row, self.cell_colum + 1) and auxRight >= 2:
            res = res + 1
        elif auxRight >= 3:
            res = res + 1

        auxLeft = self.get_croos_around(estado, self.cell_row, self.cell_colum - 1)
        if self.is_corner(estado, self.cell_row, self.cell_colum - 1) and auxLeft >= 1:
            res = res + 1
        elif self.is_lateral(estado, self.cell_row, self.cell_colum - 1) and auxLeft >= 2:
            res = res + 1
        elif auxLeft >= 3:
            res = res + 1

        result = False

        if res > 0:
            result = True
        return result

    # Indica si el numero de huecos que rodea a una casilla
    def get_croos_around(self, estado, cellRow, cellColum):
        copy_estado = self.get_binary(estado)
        to_check = [[cellRow - 1, cellColum],
                    [cellRow, cellColum + 1],
                    [cellRow + 1, cellColum],
                    [cellRow, cellColum - 1]]
        to_check = list(filter(lambda x: x[0] >= 0 and x[1] >= 0, to_check))
        to_check = list(filter(lambda x: x[0] < (len(estado[self.cell_row])-0) and x[1] < (len(estado)-0), to_check))
        aux = 0
        for i in range(len(to_check)):
            aux = aux + copy_estado[to_check[i][0]][to_check[i][1]]
        return aux

    # Convierte el tablero a una variable binaria 0 o 1
    def get_binary(self, estado):
        copy_estado = copy.deepcopy(estado)
        for i in range(len(copy_estado[self.cell_row])):
            for j in range(len(copy_estado)):
                cell = copy_estado[i][j]
                if cell == 0:
                    copy_estado[i][j] = 1
                else:
                    copy_estado[i][j] = 0
        return copy_estado

    def check_black_cell_around(self, estado):
        r = self.cell_row
        c = self.cell_colum
        valid_colum = list(filter(lambda x: 0 <= x < len(estado), [r - 1, r, r + 1]))
        valid_row = list(filter(lambda x: 0 <= x < len(estado), [c - 1, c, c + 1]))
        more_one_zero_row = len(list(filter(lambda x: estado[self.cell_row][x] == 0, valid_row))) > 0
        if not more_one_zero_row:
            return len(list(filter(lambda x: estado[x][self.cell_colum] == 0, valid_colum))) > 0
        else:
            return more_one_zero_row

        # Indica si, al borrar una celda, si aisla con huecos alguna otra

    def squareBetweenAPair(self,estado):
            res = False
            row = self.cell_row
            colum = self.cell_colum
            if(len(estado[0]) - colum >= 2 and colum >= 1):
                if(estado[row][colum - 1] == estado[row][colum + 1] and estado[row][colum] == 0):
                    res = True
            if (len(estado) - row >= 2 and row >= 1):
                if (estado[row + 1][colum] == estado[row - 1][colum] and estado[row][colum] == 0):
                    res = True
            return res

    def es_aplicable(self, estado):
        return not self.is_cross(estado) \
               and not self.exist_black_cell_around(estado) \
               and (self.exist_in_colum(estado) or self.exist_in_row(estado)) \
               and not self.check_isolate_cell(estado) \
               and not self.squareBetweenAPair(estado)

#               and not self.check_black_cell_around(estado)
#               Estos dos últimos métodos también funcionan pero van un poco más lento

    def aplicar(self, estado):
        nuevo_estado = copy.deepcopy(estado)
        nuevo_estado[self.cell_row][self.cell_colum] = 0
        return nuevo_estado

    def coste_de_aplicar(self, estado):
        return self.cell_row * - 10000 + self.cell_colum * - 10
















