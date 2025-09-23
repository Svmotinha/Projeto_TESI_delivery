import sqlite3
from sqlite3 import Error

class Conexao:
    def get_conexao(self):
        caminho = 'banco_tesi1.db'
        try:
            con = sqlite3.connect(caminho)
            return con
        except Error as er:
            print(er)

# obj = Conexao()
# conexao = obj.get_conexao()
# if conexao:
#     sql = 'SELECT * FROM cliente;'
#     try:
#         cursor = conexao.cursor()
#         resultado = cursor.execute(sql).fetchall()
#         for item in resultado:
#             print(item[1])
#     except Error as er:
#         print(er)