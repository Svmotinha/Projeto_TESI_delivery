import model

class ControllerCliente:
    def __init__(self):
        self.model = model.Model()

    def criar_tabelas(self):
        self.model.create_db()

    def inserir_clientes(self, nome, cpf, email):
        sql = (f"INSERT INTO cliente (nome, cpf, email) VALUES('{nome}', "
               f"'{cpf}','{email}');")
        return self.model.insert(sql)

    def listar_clientes(self, nome=''):
        sql = f"SELECT * FROM cliente WHERE nome LIKE '%{nome}%';"
        return self.model.get(sql)

    def excluir_clientes(self, id):
        sql = f"DELETE FROM cliente WHERE id={id};"
        return self.model.delete(sql)

    def editar_clientes(self, id, nome, cpf, email):
        sql = f"UPDATE cliente SET nome='{nome}', cpf='{cpf}', email='{email}' WHERE id={id};"
        return self.model.update(sql)
