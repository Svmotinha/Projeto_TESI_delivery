# arquivo: tela_usuarios.py
from tkinter import messagebox, LEFT, W, E, CENTER, END
import ttkbootstrap as ttk
import sqlite3

ADMIN_EMAIL = "admin@sistema.com"
ADMIN_SENHA = "admin123"


class TelaAdmin:
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Área Administrativa - Usuários Cadastrados")
        self.janela.geometry("600x400")

        ttk.Label(self.janela, text="Usuários Cadastrados", font=("Arial", 16, "bold")).pack(pady=10)

        # Treeview para exibir usuários
        self.tree = ttk.Treeview(self.janela, columns=('ID', 'Nome', 'CPF', 'Email'), show='headings')
        self.tree.heading('ID', text='ID', anchor=W)
        self.tree.heading('Nome', text='Nome', anchor=W)
        self.tree.heading('CPF', text='CPF', anchor=W)
        self.tree.heading('Email', text='Email', anchor=W)

        self.tree.column('ID', width=30, anchor=CENTER)
        self.tree.column('Nome', width=150, anchor=W)
        self.tree.column('CPF', width=100, anchor=W)
        self.tree.column('Email', width=200, anchor=W)

        frm_botoes_admin = ttk.Frame(self.janela)
        frm_botoes_admin.pack(pady=10)

        btn_editar = ttk.Button(frm_botoes_admin, text="Editar Selecionado", bootstyle="info",
                                command=self.editar_usuario)
        btn_editar.pack(side=LEFT, padx=5)

        btn_excluir = ttk.Button(frm_botoes_admin, text="Excluir Selecionado", bootstyle="danger",
                                 command=self.excluir_usuario)
        btn_excluir.pack(side=LEFT, padx=5)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.carregar_usuarios()
        self.centraliza(self.janela)

    def excluir_usuario(self):
        itens = self.tree.selection()
        if not itens:
            messagebox.showwarning('Aviso', 'Bicho seleciona aew')
            return

        item = itens[0]
        usuario_id = self.tree.item(item, 'values')[0]
        confirmacao = messagebox.askyesno("Confirmação",
                                          "Tem certeza que deseja excluir o usuário selecionado?")
        if confirmacao:
            try:
                self.cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
                self.conn.commit()
                self.tree.delete(item)
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir o usuário: {e}")

    def editar_usuario(self):
        itens = self.tree.selection()
        if len(itens) == 0:
            messagebox.showwarning('Aviso', 'Bicho seleciona aew')
            return
        if len(itens) > 1:
            messagebox.showwarning('Aviso', 'Bicho seleciona só um aew')
            return

        item = itens[0]
        usuario_id = self.tree.item(item, 'values')[0]

        # Buscar dados completos (incluindo senha) do DB
        self.cursor.execute("SELECT id, nome, cpf, email, senha FROM usuarios WHERE id=?", (usuario_id,))
        self.dados = self.cursor.fetchone()
        if not self.dados:
            messagebox.showerror("Erro", "Não foi possível recuperar os dados do usuário.")
            return

        self.top_editar = ttk.Toplevel(self.janela)
        self.top_editar.grab_set()
        self.top_editar.title("Editar Usuário")
        self.top_editar.geometry("350x220")

        ttk.Label(self.top_editar, text='NOME:').grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_editar, text='CPF:').grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_editar, text='EMAIL:').grid(row=2, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_editar, text='SENHA:').grid(row=3, column=0, padx=5, pady=5, sticky=W)

        self.ent_nome = ttk.Entry(self.top_editar)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5)
        self.ent_nome.insert('end', self.dados[1])

        self.ent_cpf = ttk.Entry(self.top_editar)
        self.ent_cpf.grid(row=1, column=1, padx=5, pady=5)
        self.ent_cpf.insert('end', self.dados[2])

        self.ent_email = ttk.Entry(self.top_editar)
        self.ent_email.grid(row=2, column=1, padx=5, pady=5)
        self.ent_email.insert('end', self.dados[3])

        self.ent_senha = ttk.Entry(self.top_editar)
        self.ent_senha.grid(row=3, column=1, padx=5, pady=5)
        self.ent_senha.insert('end', self.dados[4])

        btn_confirmar_edicao = ttk.Button(self.top_editar, text='Confirmar Edição', bootstyle="success",
                                         command=lambda: self.confirmar_edicao(usuario_id))
        btn_confirmar_edicao.grid(row=4, column=0, columnspan=2, sticky='we', padx=5, pady=10)

        self.centraliza(self.top_editar)

    def confirmar_edicao(self, usuario_id):
        nome = self.ent_nome.get().strip()
        cpf = self.ent_cpf.get().strip()
        email = self.ent_email.get().strip()
        senha = self.ent_senha.get().strip()

        if not nome or not cpf or not email or not senha:
            messagebox.showwarning('Aviso', 'Todos os campos são obrigatórios.', parent=self.top_editar)
            return

        try:
            self.cursor.execute("UPDATE usuarios SET nome=?, cpf=?, email=?, senha=? WHERE id=?",
                                (nome, cpf, email, senha, usuario_id))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Usuário atualizado com sucesso.')
            self.top_editar.destroy()
            self.carregar_usuarios()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'CPF ou Email já cadastrados!', parent=self.top_editar)
        except Exception as e:
            messagebox.showerror('Erro', f'Não foi possível atualizar o usuário: {e}', parent=self.top_editar)

    def carregar_usuarios(self):
        # limpa o Treeview antes de carregar novos dados
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            self.cursor.execute("SELECT id, nome, cpf, email FROM usuarios")
            usuarios = self.cursor.fetchall()
            for row in usuarios:
                self.tree.insert('', END, values=row)
        except Exception as erro:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível carregar os usuários: {erro}")

    def centraliza(self, master):
        master.update_idletasks()
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')


class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("500x300")
        self.janela.title('Tela de Login')

        ttk.Label(self.janela, text="Email:").grid(column=0, row=0, sticky=W, padx=5, pady=5)
        self.ent_usuario = ttk.Entry(self.janela)
        self.ent_usuario.grid(column=1, row=0, sticky=E, padx=5, pady=5)

        ttk.Label(self.janela, text="Senha:").grid(column=0, row=1, sticky=W, padx=5, pady=5)
        self.ent_senha = ttk.Entry(self.janela, show="*")
        self.ent_senha.grid(column=1, row=1, sticky=E, padx=5, pady=5)

        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.grid(column=1, row=2, columnspan=2, pady=5)

        self.btn_login = ttk.Button(self.frm_botoes, text="Entrar", bootstyle="primary", command=self.login)
        self.btn_login.pack(side=LEFT, padx=5)

        self.btn_cadastrar = ttk.Button(self.frm_botoes, text="Cadastrar", bootstyle="success",
                                        command=self.cadastrar)
        self.btn_cadastrar.pack(side=LEFT)

        self.centraliza(self.janela)
        self.conectar_db()

    def conectar_db(self):
        self.conn = sqlite3.connect("usuarios.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )'''
        )
        self.conn.commit()

        self.cursor.execute("SELECT * FROM usuarios WHERE email=?", (ADMIN_EMAIL,))
        if not self.cursor.fetchone():
            try:
                sql_admin = "INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)"
                self.cursor.execute(sql_admin, ("Admin Master", "00000000000", ADMIN_EMAIL, ADMIN_SENHA))
                self.conn.commit()
            except Exception:
                pass

    def cadastrar(self):
        self.top_cadastrar = ttk.Toplevel(self.janela)
        self.top_cadastrar.grab_set()
        self.top_cadastrar.title("Cadastro de Usuário")

        ttk.Label(self.top_cadastrar, text='NOME:').grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='CPF:').grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='EMAIL:').grid(row=2, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='SENHA:')._
