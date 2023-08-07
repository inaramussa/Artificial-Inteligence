# bimaru.py: Template para implementacao do projeto de Inteligencia Artificial 2022/2023.
# Devem alterar as classes e funcoes neste ficheiro de acordo com as instrucoes do enunciado.
# Alem das funcoes e classes je definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 21:
# 99214 Ema Oliveira
# 91110 Inara Parbato

import search
from copy import deepcopy
import sys
from sys import stdin

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representacao interna de um tabuleiro de Bimaru."""

    def __init__(self, rows_val, cols_val, hint_num, hints):
        size = 10
        self.size = size
        self.board = []
        i, j = 0, 0
        self.rows_val = rows_val
        self.cols_val = cols_val
        self.hint_num = hint_num
        self.hints = hints
        #inicializa o tabuleiro vazio
        for i in range(size): 
            row = []
            for j in range(size):
                row.append('-')
            self.board.append(row)
        #preenche o tabuleiro com as hints
        i = 0
        for i in range(hint_num): 
            row_index = hints[i][0]
            col_index = hints[i][1]
            value = hints[i][2]
            self.board[row_index][col_index] = value

    def adjacent_vertical_values(self, row: int, col: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""

        if row < self.size - 1:
            below = self.board[row + 1][col]
        else:
            below = None
        if row > 0:
            above  = self.board[row - 1][col]
        else:
            above = None
        return (below, above)

    def adjacent_horizontal_values(self, row: int, col: int):
        """Devolve os valores imediatamente a esquerda e a direita,
        respectivamente."""

        if col > 0:
            left = self.board[row][col - 1]
        else:
            left = None
        if col < self.size - 1:
            right = self.board[row][col + 1]
        else:
            right = None
        return (left, right)
    
    def copy_board(b):
        "Devolve uma copia do board"
        rows_val = b.get_rows_val()
        cols_val = b.get_cols_val()
        hint_num = b.get_hint_num()
        hints = b.get_hints()
        board = Board(rows_val, cols_val, hint_num, hints)
        return board
    
    def fill_restrictions_water(self, row, col): 
        "preenche as posicoes livres da linha ou coluna com agua"
        b = self.board
        cols = []
        if row != None:
            line = b[row]
            for i in range(10):
                if line[i] == '-':
                    self.put_value(row, i, '.')
        if col != None:
            l = 0
            for l in range(10):
                cols.append(b[l][col])
            for j in range(10):
                if cols[j] == '-':
                    self.put_value(j, col, '.')
        return self

    def verify_line_completed(self, row):
        "verifica se a linha esta toda preenchida devolvendo True"
        b = self.board
        line = b[row]
        for i in range(10):
            if line[i] == '-':
                return False
        return True

    def verify_col_completed(self, col):
        "verifica se a linha esta toda preenchida devolvendo True"
        b = self.board
        c = []
        for l in range(10):
            c.append(b[l][col])
        for i in range(10):
            if c[i] == '-':
                return False
        return True
    
    def fill_restrictions_piece(self, row, col):
        """preenche o board de acordo com as restricoes completas 
        (ex1: uma linha com valor 1 q ja tenha uma peca de um barco
        pode ser preenchida toda com agua); (ex2: uma linha com duas posicoes vazias
        que tenha valor 2 pode preencher as duas posicoes com pecas de barco"""
        b = self.board
        if row != None: 
            line = b[row]
            for k in range(10):
                if line[k] == '-':
                    adj_vertical = self.adjacent_vertical_values(row ,k)
                    adj_horizontal = self.adjacent_horizontal_values(row, k)
                    if adj_vertical[1] == None: 
                        if adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                            if (adj_horizontal[0] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[0] == None):
                                if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    self.put_value(row, k, 'c')
                                elif adj_horizontal[1] != '-':
                                    self.put_value(row, k, 'l')
                            elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_horizontal[0] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[0] == None:
                                    self.put_value(row, k, 'c')
                                elif adj_horizontal[0] != '-':
                                    self.put_value(row, k, 'r')
                        elif adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                            if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                                    self.put_value(row, k, 'c')
                                elif adj_vertical[0] != '-':
                                    self.put_value(row, k, 't')
                        elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                            if adj_vertical[0] != '-':
                                self.put_value(row, k, 't')
                            elif adj_horizontal[0] != '-' and adj_horizontal[0] != None:
                                self.put_value(row, k, 'r')
                    elif adj_horizontal[0] == None:
                        if adj_vertical[0] == '.' or adj_vertical[0] == 'W' or adj_vertical[0] == None:
                            if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                    self.put_value(row, k, 'c')
                                elif adj_vertical[1] != '-':
                                    self.put_value(row, k, 'b')
                                else:
                                    self.put_value(row, k, 'bc')
                            elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    self.put_value(row, k, 'c')
                                elif adj_horizontal[1] != '-':
                                    self.put_value(row, k, 'l')
                                elif adj_horizontal[1] == '-':
                                    self.put_value(row,k,'lc')
                        elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                            if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_vertical[0] == '-' and adj_vertical[0] != None:
                                    self.put_value(row, k, 't')
                            if adj_vertical[1] == 't' or adj_vertical[1] == 'T':
                                if adj_vertical[0] == '.':
                                    self.put_value(row, k, 'b')
                                else:
                                    self.put_value(row, k, 'mb')
                        elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                            if adj_horizontal[1] != '-' and adj_horizontal[1] != '.' and adj_horizontal[1] != 'W':
                                self.put_value(row, k, 'l')
                            elif adj_vertical[0] != '-' and adj_vertical[0] != None:
                                self.put_value(row, k, 't')
                    elif adj_vertical[0] == None:
                        if adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                            if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W' or adj_horizontal[1] == None:
                                if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                    self.put_value(row, k, 'c')
                                elif adj_vertical[1] != '-':
                                    self.put_value(row, k, 'b')
                                elif adj_vertical[1] == '-':
                                    self.put_value(row,k,'bc')
                            elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[1] != '-' and adj_horizontal[1] != None:
                                    self.put_value(row, k, 'l')
                            elif adj_horizontal[1] != '-' and adj_horizontal[1] != None:
                                self.put_value(row, k, 'l')
                            elif adj_vertical[1] != '-':
                                self.put_value(row, k, 'b')
                        elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W' or adj_horizontal[1] == None:
                            if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[0] != '-':
                                    self.put_value(row, k, 'r')
                            elif adj_vertical[1] != '-':
                                self.put_value(row, k, 'b')
                            elif adj_horizontal[0] != '-':
                                self.put_value(row, k, 'r')
                        elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                            if adj_horizontal[0] != '-' and adj_horizontal[1] != '-' or adj_horizontal[1] != None:
                                self.put_value(row, k, 'm')
                    elif adj_horizontal[1] == None:
                        if adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                            if adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                                if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                    self.put_value(row, k, 'c')
                                elif adj_vertical[1] != '-':
                                    self.put_value(row, k, 'b')
                                elif adj_vertical[1] == '-':
                                    self.put_value(row,k, 'bc')
                            elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_vertical[0] != '-':
                                    self.put_value(row, k, 't')
                                else:
                                    self.put_value(row, k, 'tc')
                            elif adj_vertical[1] == 't' or adj_vertical[1] == 'T':
                                self.put_value(row, k, 'mb')
                            elif adj_vertical[1] == 'tc': 
                                self.put_value(row, k, 'mb')
                                self.put_value(row-1, k, 't')
                            elif adj_vertical[1] == 'mb':
                                self.put_value(row, k, 'mb')
                                self.put_value(row-1,k,'m')
                        elif adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                            if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[0] != '-':
                                    self.put_value(row, k, 'r')
                            elif adj_horizontal[0] != '-':
                                self.put_value(row, k, 'r')
                        elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                            if adj_horizontal[0] != '-':
                                self.put_value(row, k, 'r')
                            elif adj_vertical[0] != '-':
                                self.put_value(row, k, 't')
                    else:
                        if adj_vertical[1] == 't' or adj_vertical[1] == 'T':
                            if adj_vertical[0] == '.':
                                self.put_value(row, k, 'b')
                            else:
                                self.put_value(row, k, 'mb')
                        elif adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                            if adj_horizontal[0] == 'lc':
                                self.put_value(row,k,'mr')
                                self.put_value(row,k-1,'l')
                            elif adj_horizontal[0] == 'mr' and b[row][k-2] == 'l':
                                self.put_value(row,k,'mr')
                                self.put_value(row,k-1,'m')
                            elif adj_horizontal[0] == 'mr' and b[row][k-2] == 'm':
                                self.put_value(row,k,'r')
                                self.put_value(row,k-1,'m')
                            elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                                    if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                        self.put_value(row, k, 'c')
                                    elif adj_horizontal[1] != '-':
                                        self.put_value(row, k, 'l')
                                    elif adj_horizontal[1] == '-':
                                        self.put_value(row,k,'lc')
                                elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    if adj_horizontal[0] != '.':
                                        self.put_value(row, k, 'r')
                                elif adj_horizontal[0] != '-' and adj_horizontal[1] != '-' and adj_horizontal[0] != '.' and adj_horizontal[1] != '.' and adj_horizontal[0] != 'W' and adj_horizontal[0] != 'W':
                                    self.put_value(row,k,'m')
                            elif adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                                if adj_vertical[1] != '-':
                                    self.put_value(row, k, 'b')
                                elif adj_horizontal[1] != '.' and adj_horizontal[1] != 'W' and adj_horizontal[1] != '-':
                                    self.put_value(row, k, 'l')
                                elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    self.put_value(row,k,'bc')
                                elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                    self.put_value(row,k,'lc')
                                elif adj_horizontal[1] == '-':
                                    count = 0
                                    for i in range(10):
                                        if b[row][i] != '.' and b[row][i] != 'W':
                                            count +=1
                                    if count == self.rows_val[row]:
                                        self.put_value(row,k,'lc')
                            elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_horizontal[0] != '-':
                                    self.put_value(row, k, 'r')
                                elif adj_vertical[1] != '-':
                                    self.put_value(row, k, 'b')
                        elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                            if adj_horizontal[0] == '.' and adj_horizontal[1] == '.':
                                self.put_value(row, k, 't')
                            if adj_vertical[0] != '-':
                                self.put_value(row, k, 't')
                            elif adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                                if adj_horizontal[1] != '.' and adj_horizontal[1] != 'W' and adj_horizontal[1] != '-':
                                    self.put_value(row, k, 'l')
                            elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_horizontal[0] != '-':
                                    self.put_value(row, k, 'r')
                        elif adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                            if adj_vertical[0] != '-' and adj_vertical[1] != '-':
                                self.put_value(row, k, 'm')
                            elif adj_horizontal[1] != '.' and adj_horizontal[1] != 'W' and adj_horizontal[1] != '-':
                                self.put_value(row, k, 'l')
                        elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                            if adj_horizontal[0] != '-':
                                self.put_value(row, k, 'r')
                            elif adj_vertical[0] != '-' and adj_vertical[1] != '-':
                                self.put_value(row, k, 'm')
        if col != None:
            cols = []
            l = 0
            for l in range(10):
                cols.append(b[l][col])
            k = 0 
            for k in range(10):
                if cols[k] == '-':
                    adj_vertical = self.adjacent_vertical_values(k, col)
                    adj_horizontal = self.adjacent_horizontal_values(k, col)
                    if adj_vertical[1] == None: 
                        if adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                            if (adj_horizontal[0] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[0] == None):
                                if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    self.put_value(k, col, 'c')
                                elif adj_horizontal[1] != '-':
                                    self.put_value(k, col, 'l')
                            elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_horizontal[0] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[0] == None:
                                    self.put_value(k, col, 'c')
                                elif adj_horizontal[0] != '-':
                                    self.put_value(k, col, 'r')
                        elif adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                            if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                                    self.put_value(k, col, 'c')
                                elif adj_vertical[0] != '-':
                                    self.put_value(k, col, 't')
                        elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                            if adj_vertical[0] != '-':
                                self.put_value(k, col, 't')
                            elif adj_horizontal[0] != '-' and adj_horizontal[0] != None:
                                self.put_value(k, col, 'r')
                    elif adj_horizontal[0] == None:
                        if adj_vertical[0] == '.' or adj_vertical[0] == 'W' or adj_vertical[0] == None:
                            if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                    self.put_value(k, col, 'c')
                                elif adj_vertical[1] != '-':
                                    self.put_value(k, col, 'b')
                            elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    self.put_value(k, col, 'c')
                                elif adj_horizontal[1] != '-':
                                    self.put_value(k, col, 'l')
                        elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                            if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_vertical[0] != '-' and adj_vertical[0] != None:
                                    self.put_value(k, col, 't')
                        elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                            if adj_horizontal[1] != '-':
                                self.put_value(k, col, 'l')
                            elif adj_vertical[0] != '-' and adj_vertical[0] != None:
                                self.put_value(k, col, 't')
                    elif adj_vertical[0] == None:
                        if adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                            if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W' or adj_horizontal[1] == None:
                                if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                    self.put_value(k, col, 'c')
                                elif adj_vertical[1] != '-':
                                    self.put_value(k, col, 'b')
                            elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[1] != '-' and adj_horizontal[1] != None:
                                    self.put_value(k, col, 'l')
                            elif adj_horizontal[1] != '-' and adj_horizontal[1] != None:
                                self.put_value(k, col, 'l')
                            elif adj_vertical[1] != '-':
                                self.put_value(k, col, 'b')
                        elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W' or adj_horizontal[1] == None:
                            if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[0] != '-':
                                    self.put_value(k, col, 'r')
                            elif adj_vertical[1] != '-':
                                self.put_value(k, col, 'b')
                            elif adj_horizontal[0] != '-':
                                self.put_value(k, col, 'r')
                        elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                            if adj_horizontal[0] != '-' and adj_horizontal[1] != '-' or adj_horizontal[1] != None:
                                self.put_value(k, col, 'm')
                    elif adj_horizontal[1] == None:
                        if adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                            if adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                                if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                    self.put_value(k, col, 'c')
                                elif adj_vertical[1] != '-':
                                    self.put_value(k, col, 'b')
                            elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_vertical[0] != '-':
                                    self.put_value(k, col, 't')
                        elif adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                            if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[0] != '-':
                                    self.put_value(k, col, 'r')
                            elif adj_horizontal[0] != '-':
                                self.put_value(k, col, 'r')
                        elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                            if adj_horizontal[0] != '-':
                                self.put_value(k, col, 'r')
                            elif adj_vertical[0] != '-':
                                self.put_value(k, col, 't')
                    else:
                        if adj_vertical[0] == '.' or adj_vertical[0] == 'W':
                            if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                                if adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                                    if adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                        self.put_value(k, col, 'c')
                                    elif adj_horizontal[1] != '-':
                                        self.put_value(k, col, 'l')
                                    elif adj_horizontal[1] == '-':
                                        self.put_value(k, col, 'lc')
                                elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    if adj_horizontal[0] != '.':
                                        self.put_value(k, col, 'r')
                            elif adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                                if adj_vertical[1] != '-':
                                    self.put_value(k, col, 'b')
                                elif adj_horizontal[1] != '.' and adj_horizontal[1] != 'W' and adj_horizontal[1] != '-':
                                    self.put_value(k, col, 'l')
                                elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    self.put_value(k, col, 'bc')
                            elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_horizontal[0] != '-':
                                    self.put_value(k, col, 'r')
                                elif adj_vertical[1] != '-':
                                    self.put_value(k, col, 'b')
                        elif adj_vertical[1] == '.' or adj_vertical[1] == 'W':
                            if adj_vertical[0] != '-':
                                self.put_value(k, col, 't')
                            elif adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                                if adj_horizontal[1] != '.' and adj_horizontal[1] != 'W' and adj_horizontal[1] != '-':
                                    self.put_value(k, col, 'l')
                                elif adj_horizontal[1] == '-' and b[k][col+2] != '-' and b[k][col+2] != '.'and b[k][col+2] != 'W':
                                    self.put_value(k, col, 'tc')
                                elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                    self.put_value(k,col,'tc')
                            elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                                if adj_horizontal[0] != '-':
                                    self.put_value(k, col, 'r')
                        elif adj_vertical[1] == 'tc':
                            self.put_value(k, col, 'mb')
                            self.put_value(k-1, col, 't')
                        elif adj_vertical[1] == 'mb': 
                            self.put_value(k,col,'mb')
                            self.put_value(k-1,col,'m')
                        elif adj_horizontal[0] == '.' or adj_horizontal[0] == 'W':
                            if adj_vertical[0] != '-' and adj_vertical[1] != '-':
                                self.put_value(k, col, 'm')
                            elif adj_horizontal[1] != '.' and adj_horizontal[1] != 'W' and adj_horizontal[1] != '-':
                                self.put_value(k, col, 'l')
                        elif adj_horizontal[1] == '.' or adj_horizontal[1] == 'W':
                            if adj_horizontal[0] != '-':
                                self.put_value(k, col, 'r')
                            elif adj_vertical[0] != '-' and adj_vertical[1] != '-':
                                self.put_value(k, col, 'm')

        return self

    @staticmethod
    def parse_instance():
        """Le o test do standard input (stdin) que e passado como argumento
        e retorna uma instancia da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        lines = []
        lines.insert(0,stdin.readline().split())  #linhas
        lines.insert(1,stdin.readline().split())  #colunas
        lines.insert(2,stdin.readline().split())  #hint number
        hint_number = int(lines[2][0])
    
        #le hints
        print(lines)
        lines_hints = []
        i = 0
        for i in range(hint_number):
            lines_hints.insert(i,stdin.readline().split())
     
        rows = [] #lista com os valores de cada linha (numero de posicoes diferentes de agua)
        rows.insert(0, int(lines[0][1]))
        rows.insert(1, int(lines[0][2]))
        rows.insert(2, int(lines[0][3]))
        rows.insert(3, int(lines[0][4]))
        rows.insert(4, int(lines[0][5]))
        rows.insert(5, int(lines[0][6]))
        rows.insert(6, int(lines[0][7]))
        rows.insert(7, int(lines[0][8]))
        rows.insert(8, int(lines[0][9]))
        rows.insert(9, int(lines[0][10]))

        cols = [] #lista com os valores de cada coluna (numero de posicoes diferentes de agua)
        cols.insert(0, int(lines[1][1]))
        cols.insert(1, int(lines[1][2]))
        cols.insert(2, int(lines[1][3]))
        cols.insert(3, int(lines[1][4]))
        cols.insert(4, int(lines[1][5]))
        cols.insert(5, int(lines[1][6]))
        cols.insert(6, int(lines[1][7]))
        cols.insert(7, int(lines[1][8]))
        cols.insert(8, int(lines[1][9]))
        cols.insert(9, int(lines[1][10]))
        hints = [] #lista de listas com as hints

        for l in range(hint_number):
            hint = []
            hint.append(int(lines_hints[l][1])) 
            hint.append(int(lines_hints[l][2]))
            hint.append(lines_hints[l][3])
            hints.append(hint)
        
        board = Board(rows, cols, hint_number, hints)
        return board
    
    def to_string(self):
        for i in self.board:
            row_string = ''.join(i)
            print(row_string)

    def get_hint_num(self):
        return self.hint_num
    
    def get_hints(self):
        return self.hints
    
    def get_rows_val(self):
        return self.rows_val
    
    def get_cols_val(self):
        return self.cols_val
    
    def get_board(self):
        return self.board

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posicao do tabuleiro."""
        return str(self.board[row][col])
    
    def put_value(self , row:int, col: int, value: str) :
        "Altera o board na posicao (row,col) por value"
        self.board[row][col] = value

    def completed_board(self):
        "Devolve true se o board tem as posicoes todas preenchidas e false caso contrario"
        for i in range(10):
            for j in range(10):
                if self.board[i][j] == '-' or self.board[i][j] == 'ml' or self.board[i][j] == 'mr' or self.board[i][j] == 'mt' or self.board[i][j] == 'mb' or self.board[i][j] == 'tc' or self.board[i][j] == 'bc' or self.board[i][j] == 'lc':
                    return False
        return True

    def rows_value_check(self):
        "Devolve true se as linhas tem as restricoes todas cumpridas"
        b = self.board
        rows_val = self.get_rows_val()
        for i in range(10):
            value = rows_val[i]
            line = b[i]
            count = 0
            j = 0
            for j in range(10):
                if line[j] != '.' and line[j] != 'W':
                    count += 1
            if count != value: 
                return False
        return True
            
    
    def cols_value_check(self):
        "Devolve true se as colunas tem as restricoes todas cumpridas"
        b = self.board
        cols_val = self.get_cols_val()
        for i in range(10):
            value = cols_val[i]
            count = 0
            col=[]
            l = 0
            for l in range(10):
                col.append(b[l][i])
            j = 0
            for j in range(10):
                if col[j] != '.' and col[j] != 'W':
                    count += 1
            if count != value: 
                return False
        return True

    def count_ships_check(self):
        b = self.board
        count_1x1 = 0
        count_2x2 = 0
        count_3x3 = 0
        count_4x4 = 0
        for i in range(10):
            for j in range(10):
                if b[i][j] == 'c' or b[i][j] == 'C':
                    count_1x1 += 1
                if i <= 8:
                    if (b[i][j] == 't' or b[i][j] == 'T') and (b[i+1][j] == 'b' or b[i+1][j] == 'B'):
                        count_2x2 += 1
                if i <= 7:
                    if (b[i][j] == 't' or b[i][j] == 'T') and (b[i+1][j] == 'm' or b[i+1][j] == 'M') and (b[i+2][j] == 'b' or b[i+2][j] == 'B'):
                        count_3x3 += 1
                if i <= 6:
                    if (b[i][j] == 't' or b[i][j] == 'T') and (b[i+1][j] == 'm' or b[i+1][j] == 'M') and (b[i+2][j] == 'm' or b[i+2][j] == 'M') and (b[i+3][j] == 'b' or b[i+3][j] == 'B'):
                        count_4x4 += 1
                if j<= 8:
                    if (b[i][j] == 'l' or b[i][j] == 'L') and (b[i][j+1] == 'r' or b[i][j+1] == 'R'):
                        count_2x2 += 1
                if j <= 7:
                    if (b[i][j] == 'L' or b[i][j] == 'l') and (b[i][j+1] == 'm' or b[i][j+1] == 'M') and (b[i][j+2] == 'r' or b[i][j+2] == 'R'):
                        count_3x3 += 1
                if j <= 6:
                    if (b[i][j] == 'l' or b[i][j] == 'L') and (b[i][j+1] == 'm' or b[i][j+1] == 'M') and (b[i][j+2] == 'm' or b[i][j+2] == 'M') and (b[i][j+3] == 'r' or b[i][j+3] == 'R'):
                        count_4x4 += 1
        #print("1x1:\n", count_1x1)
        #print("2x2:\n", count_2x2)
        #print("3x3:\n", count_3x3)
        #print("4x4:\n", count_4x4)
        if count_1x1 != 4:
            return False
        if count_2x2 != 3:
            return False
        if count_3x3 != 2:
            return False
        if count_4x4 != 1:
            return False
        return True

    def verify_T(self,row,col):    
        "verifica se a hint T esta preenchida a volta devolvendo true caso contrario devolve false"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        adj_vertical = self.adjacent_vertical_values(row,col)
        if (adj_horizontal[0] == '-' or adj_horizontal[1] == '-' or adj_vertical[0]=='-' or adj_vertical[1]=='-') and (adj_horizontal[0]!=None and adj_horizontal[1] != None and adj_vertical[0] != None and adj_vertical[1] != None) :
            return False
        return True
    
    def verify_M(self,row,col):    
        "verifica se a hint M tem todas as posicoes vazias a volta devolvendo True e False caso contrario"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        adj_vertical = self.adjacent_vertical_values(row,col)
        if adj_horizontal[0] != '-' and adj_horizontal[1] != '-' and adj_vertical[0] != '-' and adj_vertical[1] != '-':
            return True
        if (adj_horizontal[0] != '-' or adj_horizontal[1] != '-' or adj_vertical[0]!='-' or adj_vertical[1]!='-') or (adj_horizontal[0]==None and adj_horizontal[1] == None and adj_vertical[0] == None and adj_vertical[1] == None):
            return False
        return True
    
    def verify_C(self,row,col):    
        "verifica se a hint C esta preenchida a volta devolvendo true caso contrario devolve false"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        adj_vertical = self.adjacent_vertical_values(row,col)
        if (adj_horizontal[0] == '-' or adj_horizontal[1] == '-' or adj_vertical[0]=='-' or adj_vertical[1]=='-') and (adj_horizontal[0]!=None and adj_horizontal[1] != None and adj_vertical[0] != None and adj_vertical[1] != None) : 
            return False
        return True
    
    def verify_L(self,row,col):    
        "verifica se a hint L esta preenchida a volta devolvendo true caso contrario devolve false"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        adj_vertical = self.adjacent_vertical_values(row,col)
        if (adj_horizontal[0] == '-' or adj_horizontal[1] == '-' or adj_vertical[0]=='-' or adj_vertical[1]=='-') or (adj_horizontal[0]==None and adj_horizontal[1] == None and adj_vertical[0] == None and adj_vertical[1] == None) :
            return False
        return True
    
    def verify_R(self,row,col):    
        "verifica se a hint R esta preenchida a volta devolvendo true caso contrario devolve false"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        adj_vertical = self.adjacent_vertical_values(row,col)
        if (adj_horizontal[0] == '-' or adj_horizontal[1] == '-' or adj_vertical[0]=='-' or adj_vertical[1]=='-') and (adj_horizontal[0]!=None and adj_horizontal[1] != None and adj_vertical[0] != None and adj_vertical[1] != None) :
            return False
        return True
    
    def verify_B(self,row,col):    
        "verifica se a hint B esta preenchida a volta devolvendo true caso contrario devolve false"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        adj_vertical = self.adjacent_vertical_values(row,col)
        if (adj_horizontal[0] == '-' or adj_horizontal[1] == '-' or adj_vertical[0]=='-' or adj_vertical[1]=='-') and (adj_horizontal[0]!=None and adj_horizontal[1] != None and adj_vertical[0] != None and adj_vertical[1] != None) :
            return False
        return True
    
    def verify_MT(self,row, col):
        "verifica se a hint mt tem agua ou uma peca de um barco em cima devolvendo True, caso contrario devolve False"
        adj_vertical = self.adjacent_vertical_values(row,col)
        if adj_vertical[1] != '-':
            return True
        return False
    
    def verify_MB(self,row, col):
        "verifica se a hint mb tem agua ou uma peca de um barco em baixo devolvendo True, caso contrario devolve False"
        adj_vertical = self.adjacent_vertical_values(row,col)
        if adj_vertical[0] != '-':
            return True
        return False
    
    def verify_MR(self,row, col):
        "verifica se a hint mr tem agua ou uma peca de um barco em cima devolvendo True, caso contrario devolve False"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        if adj_horizontal[1] != '-':
            return True
        return False
    
    def verify_ML(self,row, col):
        "verifica se a hint ml tem agua ou uma peca de um barco em cima devolvendo True, caso contrario devolve False"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        if adj_horizontal[0] != '-':
            return True
        return False
    
    def verify_TC(self, row, col):
        "verifica se a hint tc tem agua ou uma peca de um barco em baixo devolvendo True, caso contrario devolve False"
        adj_vertical = self.adjacent_vertical_values(row,col)
        if adj_vertical[0] != '-':
            return True
        return False

    def verify_BC(self, row, col):
        "verifica se a hint bc tem agua ou uma peca de um barco em cima devolvendo True, caso contrario devolve False"
        adj_vertical = self.adjacent_vertical_values(row,col)
        if adj_vertical[1] != '-':
            return True
        return False


    def verify_LC(self, row, col):
        "verifica se a hint bc tem agua ou uma peca de um barco em cima devolvendo True, caso contrario devolve False"
        adj_horizontal = self.adjacent_horizontal_values(row,col)
        if adj_horizontal[1] != '-':
            return True
        return False
    
    def fill_restriction_zero(self): 
        "Devolve um board alterado com as linhas/colunas com restricao 0, preenchidas com agua"
        rows = self.get_rows_val()
        cols = self.get_cols_val()
        
        for i in range(10):   #percorrer os valores das linhas e colocar agua nas linhas com valor zero
            if (rows[i] == 0):
                for j in range(10):
                    self.put_value(i, j, '.')
           

        for j in range(10): #percorrer os valores das colunas e colocar agua nas colunas com valor zero
            if(cols[j] == 0):
                for k in range(10):
                    self.put_value(k,j,'.')

        return self
    
    def fill_hints_C(self,i,j):
        if (i != 0 and i != 9 ) and (j != 0 and j != 9): #em nenhuma das margens (meio do board)
            self.put_value(i - 1, j, '.')
            self.put_value(i + 1, j, '.')
            self.put_value(i, j+1, '.')
            self.put_value(i, j - 1, '.')
            self.put_value(i - 1, j-1, '.')
            self.put_value(i - 1, j+1, '.')
            self.put_value(i + 1, j - 1, '.')
            self.put_value(i + 1, j + 1, '.')
        elif  (i == 0 and j == 0): # canto superior esquerdo
            self.put_value(i + 1,j, '.') 
            self.put_value(i, j + 1, '.')
            self.put_value(i + 1, j + 1, '.')
        elif i == 0 and (j != 0 and j != 9): # primeira linha sem contar com os cantos
            self.put_value(i + 1,j, '.')
            self.put_value(i, j + 1, '.')
            self.put_value(i, j - 1, '.')
            self.put_value(i+1, j + 1, '.')
            self.put_value(i+1, j - 1, '.')
                
        elif (i == 0 and j == 9): #canto superior direito
            self.put_value(i + 1,j, '.')
            self.put_value(i,j-1, '.')
            self.put_value(i + 1,j-1, '.')    

        elif (i == 9 and j == 0): # canto inferior esquerdo
            self.put_value(i - 1,j, '.') 
            self.put_value(i, j + 1, '.')
            self.put_value(i - 1, j + 1, '.')
        elif i == 9 and (j != 0 and j != 9): # ultima linha sem contar com os cantos
            self.put_value(i - 1,j, '.')
            self.put_value(i, j + 1, '.')
            self.put_value(i, j - 1, '.')
            self.put_value(i-1, j + 1, '.')
            self.put_value(i-1, j - 1, '.')
        elif (i == 9 and j == 9): # canto inferior direito
            self.put_value(i,j-1, '.')
            self.put_value(i-1,j, '.')
            self.put_value(i - 1,j-1, '.')
        
        elif j == 0 and (i != 0 and i != 9): #primeira coluna sem os cantos
            self.put_value(i-1, j, '.')
            self.put_value(i, j + 1, '.')
            self.put_value(i-1, j + 1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j + 1, '.')
                    
        elif j == 9 and (i != 0 and i != 9): #ultima coluna sem os cantos
            self.put_value(i - 1, j, '.')
            self.put_value(i - 1, j-1, '.')
            self.put_value(i, j-1, '.')
            self.put_value(i + 1, j-1, '.')
            self.put_value(i + 1, j, '.')
        return self
    
    def fill_hints_T(self, row,col):
        b = self.board
        if row == 0 and col == 0: # canto superior esquerdo
            if b[row+1][col] == 'M' or b[row+1][col] == 'B':
                self.put_value(row, col + 1, '.')
                self.put_value(row + 1, col + 1, '.') #coloca agua a volta do navio
                self.put_value(row + 2, col + 1, '.')
            else:
                self.put_value(row + 1,col, 'mb') #Middle ou Bottom para indicar que tem uma peca de barco (barco de 2 ou 3 ou 4)
                self.put_value(row, col + 1, '.')
                self.put_value(row + 1, col + 1, '.') #coloca agua a volta do navio
                self.put_value(row + 2, col + 1, '.')
        elif row == 0  and col == 9: #canto superior direito
            if b[row+1][col] == 'M' or b[row+1][col] == 'B':
                self.put_value(row,col-1, '.')
                self.put_value(row + 1,col-1, '.')
                self.put_value(row + 2,col-1, '.')
            else:
                self.put_value(row + 1,col, 'mb')
                self.put_value(row,col-1, '.')
                self.put_value(row + 1,col-1, '.')
                self.put_value(row + 2,col-1, '.')
                
        elif (row == 0 and (col != 0 and col != 9)): # primeira linha sem contar com os cantos
            if b[row+1][col] == 'M' or b[row+1][col] == 'B':
                self.put_value(row,col-1, '.')
                self.put_value(row + 1,col-1, '.')
                self.put_value(row + 2,col-1, '.')
                self.put_value(row,col+1, '.')
                self.put_value(row + 1,col+1, '.')
                self.put_value(row + 2,col+1, '.')
            else:
                self.put_value(row + 1, col, 'mb')
                self.put_value(row,col-1, '.')
                self.put_value(row + 1,col-1, '.')
                self.put_value(row + 2,col-1, '.')
                self.put_value(row,col+1, '.')
                self.put_value(row + 1,col+1, '.')
                self.put_value(row + 2,col+1, '.')

        elif(row == 8 and (col != 0 and col != 9)): #ultima linha sem contar com os cantos
            self.put_value(row+1,col, 'b')
            self.put_value(row,col-1, '.')
            self.put_value(row,col+1, '.')
            self.put_value(row-1,col-1, '.')
            self.put_value(row+1,col-1, '.')
            self.put_value(row-1,col+1, '.')
            self.put_value(row+1,col+1, '.')
            self.put_value(row-1,col, '.')
        elif(row!=0 and row !=9) and col==0 and row != 8: #primeira coluna sem os cantos 
            if b[row+1][col] == 'M' or b[row+1][col] == 'B':
                self.put_value(row-1,col, '.')
                self.put_value(row,col+1, '.')
                self.put_value(row+1,col+1, '.')
                self.put_value(row-1,col+1, '.')
                self.put_value(row+2,col+1, '.')
            else:
                self.put_value(row-1,col, '.')
                self.put_value(row+1,col, 'mb')
                self.put_value(row,col+1, '.')
                self.put_value(row+1,col+1, '.')
                self.put_value(row-1,col+1, '.')
                self.put_value(row+2,col+1, '.')
        
        elif (col == 0 and row == 8):
            self.put_value(row-1,col, '.')
            self.put_value(row+1,col, 'b')
            self.put_value(row,col+1, '.')
            self.put_value(row+1,col+1, '.')
            self.put_value(row-1,col+1, '.')

        elif(row!=0 and row !=9) and col == 9 and row != 8: #ultima coluna sem os cantos
            self.put_value(row+1,col, 'mb')
            if b[row+1][col] == 'M' or b[row+1][col] == 'B':
                self.put_value(row,col-1, '.')
                self.put_value(row-1,col-1, '.')
                self.put_value(row+1,col-1, '.')
                self.put_value(row+2,col-1, '.')
                self.put_value(row-1,col, '.')
            else:
                self.put_value(row+1,col, 'mb')
                self.put_value(row,col-1, '.')
                self.put_value(row-1,col-1, '.')
                self.put_value(row+1,col-1, '.')
                self.put_value(row+2,col-1, '.')
                self.put_value(row-1,col, '.')
        elif (col == 9 and row == 8):
            self.put_value(row-1,col, '.')
            self.put_value(row+1,col, 'b')
            self.put_value(row,col-1, '.')
            self.put_value(row-1,col-1, '.')
            self.put_value(row+1,col-1, '.')

        elif(row != 0 and row != 9 and row != 8) and (col != 0 and col != 9):
            if b[row+1][col] == 'M' or b[row+1][col] == 'B':
                self.put_value(row + 1, col - 1, '.')
                self.put_value(row + 1, col + 1, '.')
                self.put_value(row + 2, col - 1, '.')
                self.put_value(row + 2, col + 1, '.')
                self.put_value(row, col - 1, '.')
                self.put_value(row, col + 1, '.')
                self.put_value(row - 1, col - 1, '.')
                self.put_value(row - 1, col + 1, '.')
            else:
                self.put_value(row + 1, col, 'mb')
                self.put_value(row + 1, col - 1, '.')
                self.put_value(row + 1, col + 1, '.')
                self.put_value(row + 2, col - 1, '.')
                self.put_value(row + 2, col + 1, '.')
                self.put_value(row, col - 1, '.')
                self.put_value(row, col + 1, '.')
                self.put_value(row - 1, col - 1, '.')
                self.put_value(row - 1, col + 1, '.')
        return self
    
    def fill_hints_B(self,i,j):
        "Percorre o board e a medida que encontra pecas de barco completa-as com informacao"
        b = self.board
        if (i==1 and j== 0) : #primeira coluna segunda linha
            self.put_value(i - 1, j, 't')
            self.put_value(i + 1, j, '.')
            self.put_value(i-1, j + 1, '.')
            self.put_value(i, j + 1, '.')
            self.put_value(i+1, j+1 , '.')
                
        elif i == 1 and (j != 0 and j!=9): #segunda linha sem as margens
            self.put_value(i - 1, j, 't')
            self.put_value(i - 1, j-1, '.')
            self.put_value(i, j-1, '.')
            self.put_value(i + 1, j-1, '.')
            self.put_value(i + 1, j, '.')
            self.put_value(i + 1, j+1, '.')
            self.put_value(i, j+1, '.')
            self.put_value(i - 1, j+1, '.')

        elif i == 1 and j == 9: #ultima coluna segunda linha
            self.put_value(i - 1, j, 't')
            self.put_value(i - 1, j-1, '.')
            self.put_value(i, j-1, '.')
            self.put_value(i + 1, j-1, '.')
            self.put_value(i + 1, j, '.')
        
        elif(i != 9 and i != 1) and (j != 9 and j != 0): #quando B nao esta nas margens
            if b[i-1][j]  == 'M' or b[i-1][j] == 'T':
                self.put_value(i+1, j, '.')
                self.put_value(i-1, j-1, '.')
                self.put_value(i-1, j+1, '.')
                self.put_value(i, j-1, '.')
                self.put_value(i, j+1, '.')
                self.put_value(i+1, j-1, '.')
                self.put_value(i+1, j+1, '.')
                self.put_value(i-2, j-1, '.')
                self.put_value(i-2, j+1, '.')
            else:
                self.put_value(i-1, j, 'mt')
                self.put_value(i+1, j, '.')
                self.put_value(i-1, j-1, '.')
                self.put_value(i-1, j+1, '.')
                self.put_value(i, j-1, '.')
                self.put_value(i, j+1, '.')
                self.put_value(i+1, j-1, '.')
                self.put_value(i+1, j+1, '.')
                self.put_value(i-2, j-1, '.')
                self.put_value(i-2, j+1, '.')
        
        elif i == 9 and (j != 0 and j != 9): #ultima linha sem os cantos
            if b[i-1][j]  == 'M' or b[i-1][j] == 'T':
                self.put_value(i-1, j-1, '.')
                self.put_value(i, j-1, '.')
                self.put_value(i, j+1, '.')
                self.put_value(i-1, j+1, '.')
                self.put_value(i-2, j-1, '.')
                self.put_value(i-2, j+1, '.')
            else:
                self.put_value(i-1, j, 'mt')
                self.put_value(i-1, j-1, '.')
                self.put_value(i, j-1, '.')
                self.put_value(i, j+1, '.')
                self.put_value(i-1, j+1, '.')
                self.put_value(i-2, j-1, '.')
                self.put_value(i-2, j+1, '.')

        elif (i == 9 and j == 0): #ultima linha primeira coluna
            if b[i-1][j]  == 'M' or b[i-1][j] == 'T':
                self.put_value(i, j+1, '.')
                self.put_value(i-1, j+1, '.')
                self.put_value(i-2, j+1, '.')
            else:
                self.put_value(i-1, j, 'mt')
                self.put_value(i, j+1, '.')
                self.put_value(i-1, j+1, '.')
                self.put_value(i-2, j+1, '.')
                
        elif i == 9 and j == 9: #ultima linha ultima coluna
            if b[i-1][j]  == 'M' or b[i-1][j] == 'T':
                self.put_value(i, j-1, '.')
                self.put_value(i-1, j-1, '.')
                self.put_value(i-2, j-1, '.')
            else:
                self.put_value(i-1, j, 'mt')
                self.put_value(i, j-1, '.')
                self.put_value(i-1, j-1, '.')
                self.put_value(i-2, j-1, '.')
                
        elif (j == 0 and (i != 0 and i != 1 and i != 9)):
            if b[i-1][j]  == 'M' or b[i-1][j] == 'T':
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i, j + 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 2, j + 1, '.')
            else:
                self.put_value(i - 1, j, 'mt')
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i, j + 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 2, j + 1, '.')
        elif(j == 9 and i != 0 and i != 1 and i != 9):
            if b[i-1][j]  == 'M' or b[i-1][j] == 'T':
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i, j - 1, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 2, j - 1, '.')
            else:
                self.put_value(i - 1, j, 'mt')
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i, j - 1, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 2, j - 1, '.')

        return self


    def fill_hints_R(self,i,j):

        if i==0 and j==9: # ultima coluna primeira linha
            self.put_value(i, j-1, 'ml')
            self.put_value(i + 1, j, '.')
            self.put_value(i + 1, j-1, '.')
            self.put_value(i + 1, j-2, '.')

        elif (i != 0 and i!=9) and j == 1: #segunda coluna sem os extremos
            self.put_value(i, j-1, 'l')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j+1, '.')
            self.put_value(i, j+1, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')
                
        elif i == 0 and j == 1: #primeira linha segunda coluna
            self.put_value(i, j-1, 'l')
            self.put_value(i, j+1, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')

        elif i == 9 and j == 1: #ultima linha segunda coluna
            self.put_value(i, j-1, 'l')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j+1, '.')
            self.put_value(i, j+1, '.')

        elif (i != 0 and i != 9) and (j != 9 and j != 1): #meio do board
            self.put_value(i, j-1, 'ml')
            self.put_value(i-1, j, '.')
            self.put_value(i, j+1, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j+1, '.')
            self.put_value(i+1, j+1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j-2, '.')
            self.put_value(i-1, j-2, '.')

        elif j == 9 and (i !=0 and i!=9): #ultima coluna sem os extremos
            self.put_value(i, j-1, 'ml')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i+1, j-2, '.')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j-2, '.')

        elif i == 9 and j == 9: #canto inferior direito
            self.put_value(i, j-1, 'ml')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j-2, '.')
                
        elif i == 0 and (j != 1 and j!= 9): #primeira linha sem os extremos
            self.put_value(i, j-1, 'ml')
            self.put_value(i, j+1, '.')
            self.put_value(i+1, j-2, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')
                
        elif i == 9 and (j != 9 and j != 1): #ultima linha sem os extremos
            self.put_value(i, j-1, 'ml')
            self.put_value(i, j+1, '.')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j-2, '.')

        return self
    
    def fill_hints_L(self,i,j):
        if i == 0 and j == 0: #canto superior esquerdo
            self.put_value(i, j+1, 'mr')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')
            self.put_value(i+1, j+2, '.')

        elif  i== 9 and j == 0: #canto inferior esquerdo
            self.put_value(i, j+1, 'mr')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j+1, '.')
            self.put_value(i-1, j+2, '.')

        elif j == 0 and (i != 0 and i!= 9): #primeira coluna sem os cantos
            self.put_value(i, j+1, 'mr')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j+1, '.')
            self.put_value(i-1, j+2, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')
            self.put_value(i+1, j+2, '.')
                
        elif(i != 0 and i !=9) and (j != 0 and j !=9 and j != 8): #MEIO DO BOARD
            self.put_value(i, j+1, 'mr')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j+1, '.')
            self.put_value(i-1, j+2, '.')
            self.put_value(i, j-1, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')
            self.put_value(i+1, j+2, '.')
            self.put_value(i-1, j, '.')

        elif i == 9 and (j != 0 and j !=8): #ultima linha sem os extremos
            self.put_value(i, j+1, 'mr')
            self.put_value(i, j-1, '.')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j+1, '.')
            self.put_value(i-1, j+2, '.')
        elif i == 0 and (j != 0 and j !=8): #primeira linha sem os extremos
            self.put_value(i, j+1, 'mr')
            self.put_value(i, j-1, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')
            self.put_value(i+1, j+2, '.')
                
        elif j == 8 and (i != 0 and i != 9): #penultima coluna sem os extremos
            self.put_value(i, j+1, 'r')
            self.put_value(i-1, j+1, '.')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j-1, '.')
            self.put_value(i, j-1, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')
 
        elif j == 8 and i == 0: #penultima coluna primeira linha
            self.put_value(i, j+1, 'r')
            self.put_value(i, j-1, '.')
            self.put_value(i+1, j-1, '.')
            self.put_value(i+1, j, '.')
            self.put_value(i+1, j+1, '.')

        elif j == 8 and i == 9: #penultima coluna ultima linha
            self.put_value(i, j+1, 'r')
            self.put_value(i, j-1, '.')
            self.put_value(i-1, j-1, '.')
            self.put_value(i-1, j, '.')
            self.put_value(i-1, j+1, '.')
        elif j == 9 and (i != 0 and i != 9):
            self.put_value(i, j - 1, 'mr')
            self.put_value(i - 1, j, '.')
            self.put_value(i - 1, j - 1, '.')
            self.put_value(i - 1, j - 2, '.')
            self.put_value(i + 1, j, '.')
            self.put_value(i + 1, j - 1, '.')
            self.put_value(i + 1, j - 2, '.')
        return self
        
    def fill_hints_M(self, i, j):
       
        if  i == 0 and (j != 1 and j != 8): #primeira linha sem as duas primeiras colunas e ultimas duas colunas
            self.put_value(i, j - 1, 'ml') 
            self.put_value(i, j + 1, 'mr') 
            self.put_value(i+1, j - 2, '.') 
            self.put_value(i+1, j - 1, '.') 
            self.put_value(i+1, j, '.') 
            self.put_value(i+1, j + 1, '.') 
            self.put_value(i+1, j + 2, '.') 
        elif i == 0 and j == 1: #primeira linha e segunda coluna
            self.put_value(i, j - 1, 'l') 
            self.put_value(i, j + 1, 'mr') 
            self.put_value(i+1, j - 1, '.') 
            self.put_value(i+1, j, '.') 
            self.put_value(i+1, j + 1, '.') 
            self.put_value(i+1, j + 2, '.')  
        elif i == 0 and j == 8: #primeira linha penultima coluna
            self.put_value(i, j + 1, 'r') 
            self.put_value(i, j - 1, 'ml') 
            self.put_value(i+1, j - 1, '.')
            self.put_value(i+1, j - 2, '.')
            self.put_value(i+1, j, '.') 
            self.put_value(i+1, j + 1, '.') 

        elif i == 9 and (j != 1 and j != 8): #ultima linha sem as duas primeiras colunas e ultimas duas colunas
            self.put_value(i, j + 1, 'mr')
            self.put_value(i, j - 1, 'ml')
            self.put_value(i-1, j, '.') 
            self.put_value(i-1, j + 1, '.') 
            self.put_value(i-1, j + 2, '.') 
            self.put_value(i-1, j - 1, '.') 
            self.put_value(i-1, j - 2, '.') 

        elif i == 9 and j == 1: #ultima linha e segunda coluna
            self.put_value(i, j - 1, 'l')
            self.put_value(i, j + 1, 'mr')
            self.put_value(i-1, j, '.') 
            self.put_value(i-1, j - 1, '.') 
            self.put_value(i-1, j + 1, '.') 
            self.put_value(i-1, j + 2, '.')

        elif i == 9 and j == 8: #ultima linha penultima coluna
            self.put_value(i, j + 1, 'r')
            self.put_value(i, j - 1, 'ml')
            self.put_value(i-1, j, '.') 
            self.put_value(i-1, j + 1, '.') 
            self.put_value(i-1, j - 1, '.') 
            self.put_value(i-1, j - 2, '.') 

            #Vertical
        elif i ==1 and j == 0: #primeira coluna e segunda linha
            self.put_value(i + 1, j, 't')
            self.put_value(i - 1, j, 'mb')
            self.put_value(i + 1, j + 1, '.')
            self.put_value(i, j + 1, '.')
            self.put_value(i - 1, j + 1, '.')
            self.put_value(i + 2, j + 1, '.')
                
        elif i ==8 and j == 0: #primeira coluna e penultima linha
            self.put_value(i - 1, j, 'mt')
            self.put_value(i + 1, j, 'b')
            self.put_value(i + 1, j + 1, '.')
            self.put_value(i, j + 1, '.')
            self.put_value(i - 1, j + 1, '.')
            self.put_value(i - 2, j + 1, '.')

        elif  j == 0 and (i != 1 and i != 8): #primeira coluna sem contar com a segunda linha e a penultima linha
            self.put_value(i - 1, j, 'mt')
            self.put_value(i + 1, j, 'mb')
            self.put_value(i, j + 1, '.')
            self.put_value(i - 1, j + 1, '.')
            self.put_value(i - 2, j + 1, '.')
            self.put_value(i + 1, j + 1, '.')
            self.put_value(i + 2, j + 1, '.')

        elif i == 1 and j == 9: #segunda linha e ultima coluna
            self.put_value(i - 1, j, 't')
            self.put_value(i + 1, j, 'mb')
            self.put_value(i - 1, j - 1, '.')
            self.put_value(i, j - 1, '.')
            self.put_value(i + 1, j - 1, '.')
            self.put_value(i + 2, j - 1, '.')

        elif i == 8 and j == 9: #penultima linha e ultima coluna
            self.put_value(i + 1, j, 'b')
            self.put_value(i - 1, j, 'mt')
            self.put_value(i + 1, j - 1, '.')
            self.put_value(i, j - 1, '.')
            self.put_value(i - 1, j - 1, '.')
            self.put_value(i - 2, j - 1, '.')
        
        elif j == 9 and (i != 1 and i != 8): #ultima coluna sem contar com a segunda e penultima linha
            self.put_value(i + 1, j, 'mb')
            self.put_value(i - 1, j, 'mt')
            self.put_value(i, j - 1, '.')
            self.put_value(i + 1, j - 1, '.')
            self.put_value(i + 2, j - 1, '.')
            self.put_value(i - 1, j - 1, '.')
            self.put_value(i - 2, j - 1, '.')

        elif (j != 0 and j != 9) and i == 1:
            adj_horizontal = self.adjacent_horizontal_values(i, j)
            adj_vertical = self.adjacent_vertical_values(i, j)
            if adj_horizontal[0] == '.' or adj_horizontal[1] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[1] == 'W': #navio na vertical
                self.put_value(i - 1, j, 't')
                self.put_value(i + 1, j, 'mb')
                self.put_value(i, j - 1, '.')
                self.put_value(i, j + 1, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 2, j - 1, '.')
                self.put_value(i + 2, j + 1, '.')
            elif adj_vertical[0] == '.' or adj_vertical[1] == '.' or adj_vertical[0] == 'W' or adj_vertical[1] == 'W': #navio na horizontal
                if j == 1: 
                    self.put_value(i, j - 1, 'l')
                    self.put_value(i, j + 1, 'mr')
                    self.put_value(i - 1, j, '.')
                    self.put_value(i - 1, j - 1, '.')
                    self.put_value(i - 1, j + 1, '.')
                    self.put_value(i - 1, j + 2, '.')
                    self.put_value(i + 1, j, '.')
                    self.put_value(i + 1, j - 1, '.')
                    self.put_value(i + 1, j + 1, '.')
                    self.put_value(i + 1, j + 2, '.')
                elif j == 8:
                    self.put_value(i, j - 1, 'ml')
                    self.put_value(i, j + 1, 'r')
                    self.put_value(i - 1, j, '.')
                    self.put_value(i - 1, j - 1, '.')
                    self.put_value(i - 1, j + 1, '.')
                    self.put_value(i - 1, j - 2, '.')
                    self.put_value(i + 1, j, '.')
                    self.put_value(i + 1, j - 1, '.')
                    self.put_value(i + 1, j + 1, '.')
                    self.put_value(i + 1, j - 2, '.')
                else: 
                    self.put_value(i, j - 1, 'ml')
                    self.put_value(i, j + 1, 'mr')
                    self.put_value(i - 1, j, '.')
                    self.put_value(i - 1, j - 1, '.')
                    self.put_value(i - 1, j - 2, '.')
                    self.put_value(i - 1, j + 1, '.')
                    self.put_value(i - 1, j + 2, '.')
                    self.put_value(i + 1, j, '.')
                    self.put_value(i + 1, j - 1, '.')
                    self.put_value(i + 1, j + 1, '.')
                    self.put_value(i + 1, j - 2, '.')
                    self.put_value(i + 1, j + 2, '.')
                        
        elif (j != 0 and j != 9) and i == 8:
            adj_horizontal = self.adjacent_horizontal_values(i, j)
            adj_vertical = self.adjacent_vertical_values(i, j)
            if adj_horizontal[0] == '.' or adj_horizontal[1] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[1] == 'W': #navio na vertical
                self.put_value(i - 1, j, 'mt')
                self.put_value(i + 1, j, 'b')
                self.put_value(i, j - 1, '.')
                self.put_value(i, j + 1, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 2, j - 1, '.')
                self.put_value(i - 2, j + 1, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j + 1, '.')
            elif adj_vertical[0] == '.' or adj_vertical[1] == '.' or adj_vertical[0] == 'W' or adj_vertical[1] == 'W': #navio na horizontal
                if j == 1: 
                    self.put_value(i, j - 1, 'l')
                    self.put_value(i, j + 1, 'mr')
                    self.put_value(i - 1, j, '.')
                    self.put_value(i - 1, j - 1, '.')
                    self.put_value(i - 1, j + 1, '.')
                    self.put_value(i - 1, j + 2, '.')
                    self.put_value(i + 1, j, '.')
                    self.put_value(i + 1, j - 1, '.')
                    self.put_value(i + 1, j + 1, '.')
                    self.put_value(i + 1, j + 2, '.')
                elif j == 8: 
                    self.put_value(i, j - 1, 'ml')
                    self.put_value(i, j + 1, 'r')
                    self.put_value(i - 1, j, '.')
                    self.put_value(i - 1, j - 1, '.')
                    self.put_value(i - 1, j + 1, '.')
                    self.put_value(i - 1, j - 2, '.')
                    self.put_value(i + 1, j, '.')
                    self.put_value(i + 1, j - 1, '.')
        
                    self.put_value(i + 1, j + 1, '.')
                    self.put_value(i + 1, j - 2, '.')
                else: 
                    self.put_value(i, j - 1, 'ml')
                    self.put_value(i, j + 1, 'mr')
                    self.put_value(i - 1, j, '.')
                    self.put_value(i - 1, j - 1, '.')
                    self.put_value(i - 1, j - 2, '.')
                    self.put_value(i - 1, j + 1, '.')
                    self.put_value(i - 1, j + 2, '.')
                    self.put_value(i + 1, j, '.')
                    self.put_value(i + 1, j - 1, '.')
                    self.put_value(i + 1, j + 1, '.')
                    self.put_value(i + 1, j - 2, '.')
                    self.put_value(i + 1, j + 2, '.')
        elif i == 1 and j == 1:
            adj_horizontal = self.adjacent_horizontal_values(i, j)
            adj_vertical = self.adjacent_vertical_values(i, j)
            if adj_horizontal[0] == '.' or adj_horizontal[1] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[1] == 'W': #navio na vertical
                self.put_value(i - 1, j, 't')
                self.put_value(i + 1, j, 'mb')
                self.put_value(i, j - 1, '.')
                self.put_value(i, j + 1, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 2, j - 1, '.')
                self.put_value(i + 2, j + 1, '.')
            elif adj_vertical[0] == '.' or adj_vertical[1] == '.' or adj_vertical[0] == 'W' or adj_vertical[1] == 'W': #navio na horizontal
                self.put_value(i, j - 1, 'l')
                self.put_value(i, j + 1, 'mr')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 1, j + 2, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 1, j + 2, '.')
        elif i == 1 and j == 8:
            adj_horizontal = self.adjacent_horizontal_values(i, j)
            adj_vertical = self.adjacent_vertical_values(i, j)
            if adj_horizontal[0] == '.' or adj_horizontal[1] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[1] == 'W': #navio na vertical
                self.put_value(i - 1, j, 't')
                self.put_value(i + 1, j, 'mb')
                self.put_value(i, j - 1, '.')
                self.put_value(i, j + 1, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 2, j - 1, '.')
                self.put_value(i + 2, j + 1, '.')
            elif adj_vertical[0] == '.' or adj_vertical[1] == '.' or adj_vertical[0] == 'W' or adj_vertical[1] == 'W': #navio na horizontal
                self.put_value(i, j - 1, 'ml')
                self.put_value(i, j + 1, 'r')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 1, j - 2, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 1, j - 2, '.')
        elif j != 0 and j != 9 and j != 1 and j != 8 and i != 0 and i != 9 and i != 1 and i != 8:
            adj_horizontal = self.adjacent_horizontal_values(i, j)
            adj_vertical = self.adjacent_vertical_values(i, j)
            if adj_horizontal[0] == '.' or adj_horizontal[1] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[1] == 'W': #verifica se o barco e vertical
                self.put_value(i - 1, j, 'mt')
                self.put_value(i + 1, j, 'mb')
                self.put_value(i, j - 1, '.')
                self.put_value(i, j + 1, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 2, j - 1, '.')
                self.put_value(i - 2, j + 1, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 2, j - 1, '.')
                self.put_value(i + 2, j + 1, '.')
            elif adj_vertical[0] == '.' or adj_vertical[1] == '.' or adj_vertical[0] == 'W' or adj_vertical[1] == 'W': #verifica se o barco e horizontal
                self.put_value(i, j - 1, 'ml')
                self.put_value(i, j + 1, 'mr')
                self.put_value(i - 1, j, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j - 2, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j - 2, '.')
                self.put_value(i + 1, j + 1, '.')
        elif j == 1 and (i != 0 and i != 1 and i != 8 and i != 9):
            adj_horizontal = self.adjacent_horizontal_values(i, j)
            adj_vertical = self.adjacent_vertical_values(i, j)
            if adj_horizontal[0] == '.' or adj_horizontal[1] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[1] == 'W': #navio na vertical
                self.put_value(i - 1, j, 'mt')
                self.put_value(i + 1, j, 'mb')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 2, j - 1, '.')
                self.put_value(i - 2, j + 1, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 2, j - 1, '.')
                self.put_value(i + 2, j + 1, '.')
            elif adj_vertical[0] == '.' or adj_vertical[1] == '.' or adj_vertical[0] == 'W' or adj_vertical[1] == 'W': #barco na horizontal
                self.put_value(i, j - 1, 'l')
                self.put_value(i, j + 1, 'mr')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 1, j + 2, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 1, j + 2, '.')
        elif j == 8 and (i != 0 and i != 1 and i != 8 and i != 9):
            adj_horizontal = self.adjacent_horizontal_values(i, j)
            adj_vertical = self.adjacent_vertical_values(i, j)
            if adj_horizontal[0] == '.' or adj_horizontal[1] == '.' or adj_horizontal[0] == 'W' or adj_horizontal[1] == 'W': #navio na vertical
                self.put_value(i - 1, j, 'mt')
                self.put_value(i + 1, j, 'mb')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 2, j - 1, '.')
                self.put_value(i - 2, j + 1, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 2, j - 1, '.')
                self.put_value(i + 2, j + 1, '.')
            elif adj_vertical[0] == '.' or adj_vertical[1] == '.' or adj_vertical[0] == 'W' or adj_vertical[1] == 'W':
                self.put_value(i, j + 1, 'r')
                self.put_value(i, j - 1, 'ml')
                self.put_value(i - 1, j, '.')
                self.put_value(i - 1, j + 1, '.')
                self.put_value(i - 1, j - 1, '.')
                self.put_value(i - 1, j - 2, '.')
                self.put_value(i + 1, j, '.')
                self.put_value(i + 1, j + 1, '.')
                self.put_value(i + 1, j - 1, '.')
                self.put_value(i + 1, j - 2, '.')

        return self

    def fill_hints_MT(self,i,j):
        if(i != 0 and i != 9):
            adj = self.adjacent_vertical_values(i, j) 
            adj1 = self.adjacent_vertical_values(i + 1, j)
            if adj[1] == '.' or adj[1] == 'W':
                self.put_value(i, j, 't')
            elif (adj[0] == 'm' or adj[0] == 'M') and (adj1[0] == 'm' or adj1[0] == 'M'): #barco de 4 vertical
                self.put_value(i, j, 't')
            elif adj[1] == 't':
                self.put_value(i,j,'m')
            elif adj[0] == 'b':
                self.put_value(i,j,'m')
        return self
    
    def fill_hints_MB(self,i,j):
       
        if (i != 0 and i != 9):
            adj = self.adjacent_vertical_values(i, j) 
            adj1 = self.adjacent_vertical_values(i - 1, j)
            if adj[0] == '.' or adj[0] == 'W': 
                self.put_value(i, j, 'b')
            elif (adj[1] == 'm' or adj[1] == 'M') and (adj1[1] == 'm' or adj1[1] == 'M'): #barco de 4 vertical
                self.put_value(i, j, 'b')
            elif adj[0] == 'b':
                self.put_value(i, j, 'm')
            elif adj[1] == 't' and adj[0] != '-' and adj[0] != '.' and adj[0] != 'W': 
                self.put_value(i,j,'m')
            elif adj[0] == 'bc':
                self.put_value(i,j,'m')
                self.put_value(i+1,j,'b')
        return self
                
    def fill_hints_ML(self,i,j):
        b = self.board
        if(b[i][j] == 'ml') and (j != 0 and j != 9):
            adj = self.adjacent_horizontal_values(i, j)
            adj1 = self.adjacent_horizontal_values(i, j + 1)
            if adj[0] == '.' or adj[0] == 'W':
                self.put_value(i, j, 'l')
            elif(adj[1] == 'm' and adj[1] == 'M') and (adj1[1] == 'm' and adj1[1] == 'M'): #barco de 4 horizontal
                self.put_value(i, j, 'l')
            elif adj[0] == 'l' or adj[0] == 'L':
                self.put_value(i,j,'m')
            elif adj[1] == 'R' or adj[1] == 'r':
                self.put_value(i,j,'m')
        return self

    def fill_hints_MR(self,i,j):
       
        if (j != 0 and j != 9):
            adj = self.adjacent_horizontal_values(i, j)
            adj1 = self.adjacent_horizontal_values(i, j - 1)
            if adj[1] == '.' or adj[1] == 'W':
                self.put_value(i,j,'r')
            elif(adj[0] == 'm'or adj[0] == 'M') and (adj1[0] == 'm' or adj1[0] == 'M'):
                self.put_value(i,j,'r')
            elif(adj[1] == 'r' or adj[1] == 'R'):
                self.put_value(i,j,'m')
        return self
        
    def fill_hints_TC(self,i,j):
        adj_vertical = self.adjacent_vertical_values(i,j)
        if adj_vertical[0] == '.' or adj_vertical[0] == 'W':
            self.put_value(i, j, 'c')
        elif adj_vertical[0] != '-' and adj_vertical[0] != '.' and adj_vertical[0] != 'W':
            self.put_value(i, j, 't')
        return self
    
    def fill_hints_BC(self,i,j):
        adj_vertical = self.adjacent_vertical_values(i,j)
        if adj_vertical[1] == '.' or adj_vertical[1] == 'W':
            self.put_value(i, j, 'c')
        elif adj_vertical[1] == 'M' or adj_vertical[1] == 'm' or adj_vertical[1] == 't' or adj_vertical[1] == 'T':
            self.put_value(i, j, 'b')
        elif adj_vertical[1] == 'b':
            self.put_value(i,j,'b')
            self.put_value(i-1,j,'m')
        return self

    def fill_hints_LC(self,i ,j):
        adj_horizontal = self.adjacent_horizontal_values(i,j)
        if adj_horizontal[1] == '.':
            self.put_value(i,j,'c')
        elif adj_horizontal[1] != '-':
            self.put_value(i,j,'l')
        return self
    
    def fill_4x4_horizontal(self,i,j):
        self.put_value(i,j,'l')
        self.put_value(i,j+1,'m')
        self.put_value(i,j+2,'m')
        self.put_value(i,j+3,'r')
        return self

    def fill_4x4_vertical(self,i,j):
        self.put_value(i,j,'t')
        self.put_value(i+1,j,'m')
        self.put_value(i+2,j,'m')
        self.put_value(i+3,j,'b')
        return self
    
    def fill_3x3_horizontal(self,i,j):
        self.put_value(i,j,'l')
        self.put_value(i,j+1,'m')
        self.put_value(i,j+2,'r')
        return self
    
    def fill_3x3_vertical(self,i,j):
        self.put_value(i,j,'t')
        self.put_value(i+1,j,'m')
        self.put_value(i+2,j,'b')
        return self
    
    def fill_2x2_horizontal(self,i,j):
        self.put_value(i,j,'l')
        self.put_value(i,j+1,'r')
        return self
    
    def fill_2x2_vertical(self,i,j):
        self.put_value(i,j,'t')
        self.put_value(i+1,j,'b')
        return self

class Bimaru(Problem):
    
    "Representacao interna de um tabuleiro de bimaru"

    def __init__(self, board: Board):
        #O construtor especifica o estado inicial.
        super().__init__(BimaruState(board))

    def actions(self, state: BimaruState):
        #Retorna uma lista de acoes que podem ser executadas a
        #partir do estado passado como argumento.
        actions = []
        actions_hints = []
        newBoard = state.board
        b = newBoard.board
        rows_val = newBoard.get_rows_val()
        cols_val = newBoard.get_cols_val()
        i = 0
        for i in range(10): 
            value_rows = rows_val[i]
            value_col = cols_val[i]
            line = b[i]
            col=[]
            count_rows = 0
            count_col = 0
            count_1 = 0
            count_2 = 0
            l = 0
            for l in range(10):
                col.append(b[l][i])
            j = 0
            for j in range(10):
                if line[j] != '.'and line[j] != '-' and line[j] != 'W':  #verifica se o numero de pecas de barco na linha e igual ao valor da mesma
                    count_rows += 1
                if col[j] != '.' and col[j] != '-' and col[j] != 'W':  #verifica se o numero de pecas de barco na coluna e igual ao valor da mesma
                    count_col+=1
                if line[j] == '-' or (line[j] != '.' and line[j] != 'W'): #verifica se o numero de posicoes livres + numero de pecas de barco e igual ao valor da linha 
                    count_1 += 1
                if col[j] == '-' or (col[j] != '.' and col[j] != 'W'): #verifica se o numero de posicoes livres + numero de pecas de barco e igual ao valor da linha 
                    count_2 += 1
                if (b[i][j] == 'c' or b[i][j] == 'C') and newBoard.verify_C(i, j) == False:
                    actions_hints.append((i, j, 'c'))
                if (b[i][j] == 't' or b[i][j] == 'T') and newBoard.verify_T(i, j) == False:
                    actions_hints.append((i, j, 't'))
                if (b[i][j] == 'b' or b[i][j] == 'B') and newBoard.verify_B(i, j) == False:
                    actions_hints.append((i, j, 'b'))
                if (b[i][j] == 'r' or b[i][j] == 'R') and newBoard.verify_R(i, j) == False:
                    actions_hints.append((i, j, 'r'))
                if (b[i][j] == 'l' or b[i][j] == 'L') and newBoard.verify_L(i, j) == False:
                    actions_hints.append((i, j, 'l'))
                if (b[i][j] == 'm' or b[i][j] == 'M') and newBoard.verify_M(i, j) == False:
                    actions_hints.append((i, j, 'm'))
                if (b[i][j] == 'mt' and newBoard.verify_MT(i,j) == True):
                    actions.append((i, j, 'mt'))
                if (b[i][j] == 'mb' and newBoard.verify_MB(i,j) == True):
                    actions.append((i, j, 'mb'))
                if (b[i][j] == 'mr' and newBoard.verify_MR(i,j) == True):
                    actions.append((i, j, 'mr'))
                if (b[i][j] == 'ml' and newBoard.verify_ML(i,j) == True):
                    actions.append((i, j, 'ml'))
                if (b[i][j] == 'tc' and newBoard.verify_TC(i,j) == True):
                    actions.append((i, j, 'tc'))
                if (b[i][j] == 'bc' and newBoard.verify_BC(i,j) == True):
                    actions.append((i, j, 'bc'))
                if (b[i][j] == 'lc' and newBoard.verify_LC(i,j) == True):
                    actions.append((i, j, 'lc'))

            if count_rows == value_rows and newBoard.verify_line_completed(i) == False:
                actions.append((i, None, 'fill_restrictions_water'))
            if count_col == value_col and newBoard.verify_col_completed(i) == False:
                 actions.append((None, i, 'fill_restrictions_water'))
            if count_1 == value_rows and newBoard.verify_line_completed(i) == False: 
                actions.append((i, None, 'fill_restrictions_piece'))
            if count_2 == value_col and newBoard.verify_col_completed(i) == False:
                actions.append((None, i, 'fill_restrictions_piece'))
        if actions == []:
            actions = actions_hints
        if actions == []:
            for i in range(10):
                for j in range(10):
                    if b[i][j] == '-':
                        value_row = rows_val[i]
                        value_col = cols_val[j]
                        if j <= 6: #posssibilidade de 4x4 horizontal
                            if value_row >= 4 and b[i][j+1] != '.' and b[i][j+1] != 'W' and b[i][j+2] != '.' and b[i][j+2] != 'W' and b[i][j+3] != '.' and b[i][j+3] != 'W' and (b[i][j+4] ==None or b[i][j+4] == '.' or b[i][j+4] == '-'):
                                actions.append((i,j,'ship 4x4 horizontal'))
                                break
                        if i <= 6: #posssibilidade de 4x4 vertical
                            if value_col >= 4 and b[i+1][j] != '.' and b[i+1][j] != 'W' and b[i+2][j] != '.' and b[i+2][j] != 'W' and b[i+3][j] != '.' and b[i+3][j] != 'W' and (b[i+4][j] ==None or b[i+4][j] == '.' or b[i+4][j] == '-'):
                                actions.append((i,j,'ship 4x4 vertical'))
                                break
                        if j <= 7: #posssibilidade de 3x3 horizontal
                            if value_row >= 3 and b[i][j+1] != '.' and b[i][j+1] != 'W' and b[i][j+2] != '.' and b[i][j+2] != 'W' and (b[i][j+3] ==None or b[i][j+3] == '.' or b[i][j+3] == '-'): 
                                actions.append((i,j,'ship 3x3 horizontal'))
                                break
                        if i <= 7: #posssibilidade de 3x3 vertical
                            if value_col >= 3 and b[i+1][j] != '.' and b[i+1][j] != 'W' and b[i+2][j] != '.' and b[i+2][j] != 'W' and (b[i+3][j] ==None or b[i+3][j] == '.' or b[i+3][j] == '-'):
                                actions.append((i,j,'ship 3x3 vertical'))
                                break
                        if j <= 8: #posssibilidade de 2x2 horizontal
                            if value_row >= 2 and b[i][j+1] != '.' and b[i][j+1] != 'W' and (b[i][j+2] ==None or b[i][j+2] == '.' or b[i][j+2] == '-'): 
                                actions.append((i,j,'ship 2x2 horizontal'))
                                break
                        if i <= 8: #posssibilidade de 2x2 vertical
                            if value_col >= 2 and b[i+1][j] != '.' and b[i+1][j] != 'W' and (b[i+2][j] ==None or b[i+2][j] == '.' or b[i+2][j] == '-'): 
                                actions.append((i,j,'ship 2x2 vertical'))
                                break
                if actions != []:
                    break
        print ("ACTIONS:\n", actions)               
        return actions      
          
    def result(self, state: BimaruState, action):
        #Retorna o estado resultante de executar a 'action' sobre
        'state' #passado como argumento. A acao a executar deve ser uma
        #das presentes na lista obtida pela execucao de
        row,col,piece = action
        newState = state.board
        if  piece == 't':
            newState.fill_hints_T(row,col)
        elif piece == 'm':
            newState.fill_hints_M(row,col)
        elif piece == 'c':
            newState.fill_hints_C(row,col)
        elif piece == 'b':
            newState.fill_hints_B(row,col)
        elif piece == 'r':
            newState.fill_hints_R(row,col)
        elif piece == 'l':
            newState.fill_hints_L(row,col)
        elif piece == 'mt':
            newState.fill_hints_MT(row,col)
        elif piece == 'mb':
            newState.fill_hints_MB(row,col)
        elif piece == 'mr':
            newState.fill_hints_MR(row,col)
        elif piece == 'ml':
            newState.fill_hints_ML(row,col)
        elif piece == 'bc':
            newState.fill_hints_BC(row,col)
        elif piece == 'tc':
            newState.fill_hints_TC(row,col)
        elif piece == 'lc':
            newState.fill_hints_LC(row,col)
        elif piece == 'fill_restrictions_water':
            newState.fill_restrictions_water(row, col)
        elif piece == 'fill_restrictions_piece':
            newState.fill_restrictions_piece(row, col)
        elif piece == 'ship 4x4 horizontal':
            newState.fill_4x4_horizontal(row,col)
        elif piece == 'ship 4x4 vertical':
            newState.fill_4x4_vertical(row,col)
        elif piece == 'ship 3x3 horizontal':
            newState.fill_3x3_horizontal(row,col)
        elif piece == 'ship 3x3 vertical':
            newState.fill_3x3_vertical(row,col)
        elif piece == 'ship 2x2 horizontal':
            newState.fill_2x2_horizontal(row,col)
        elif piece == 'ship 2x2 vertical':
            newState.fill_2x2_vertical(row,col)
        newState1 = BimaruState(newState)
        newState.to_string()
        return newState1
        

    def goal_test(self, state: BimaruState):
        #Retorna True se e so se o estado passado como argumento e
        #um estado objetivo. Deve verificar se todas as posicoes do tabuleiro
        #estao preenchidas de acordo com as regras do problema.
        if state.board.completed_board() == False:
            #print("complete\n")
            return False
        if state.board.rows_value_check() == False:
            #print("rows check\n")
            return False
        if state.board.cols_value_check() == False:
            #print("cols check\n")
            return False
        if state.board.count_ships_check() == False:
            #print("ship check\n")
            return False
        return True

    def h(self, node: Node):
        #Funcao heuristica utilizada para a procura A*.
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    board= Board.parse_instance()
    newBoard = board.fill_restriction_zero()
    bimaru = Bimaru(newBoard)
    goal_node = depth_first_tree_search(bimaru)
    goal_node.state.board.to_string()
