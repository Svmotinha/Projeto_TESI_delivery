import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("500x300")
        self.janela.title('Tela de Login')

        # Conexão com o banco de dados
        self.conectar_db()

        self.lbl_usuario = ttk.Label(self.janela, text="Usuário (Email):")
        self.lbl_usuario.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        self.ent_usuario = ttk.Entry(self.janela)
        self.ent_usuario.grid(column=1, row=0, sticky=E, padx=5, pady=5)

        self.lbl_senha = ttk.Label(self.janela, text="Senha:")
        self.lbl_senha.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        self.ent_senha = ttk.Entry(self.janela, show="*")
        self.ent_senha.grid(column=1, row=1, sticky=E, padx=5, pady=5)

        # Frame para botões
        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.grid(column=1, row=2, columnspan=2, pady=5)

        # Botão de Login
        self.btn_login = ttk.Button(self.frm_botoes, text="Entrar", bootstyle="primary", command=self.login)
        self.btn_login.pack(side=LEFT, padx=5)

        # Botão de Cadastro
        self.btn_cadastrar = ttk.Button(self.frm_botoes, text="Cadastrar", bootstyle="success", command=self.cadastrar)
        self.btn_cadastrar.pack(side=LEFT)

        self.centraliza(self.janela)

    def conectar_db(self):
        """Conecta ao banco e cria tabela se não existir"""
        self.conn = sqlite3.connect("usuarios.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def cadastrar(self):
        """Abre janela para cadastro"""
        self.top_cadastrar = tk.Toplevel(self.janela)
        self.top_cadastrar.title("Cadastro de Usuário")
        self.top_cadastrar.grab_set()

        ttk.Label(self.top_cadastrar, text='NOME:').grid(row=0, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='CPF:').grid(row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='EMAIL:').grid(row=2, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='SENHA:').grid(row=3, column=0, padx=5, pady=5, sticky=W)

        self.ent_nome = ttk.Entry(self.top_cadastrar)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5)

        self.ent_cpf = ttk.Entry(self.top_cadastrar)
        self.ent_cpf.grid(row=1, column=1, padx=5, pady=5)

        self.ent_email = ttk.Entry(self.top_cadastrar)
        self.ent_email.grid(row=2, column=1, padx=5, pady=5)

        self.ent_senha_cad = ttk.Entry(self.top_cadastrar, show="*")
        self.ent_senha_cad.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(
            self.top_cadastrar,
            text='Confirmar Cadastro',
            bootstyle="success",
            command=self.confirmar_cadastro
        ).grid(row=4, column=0, columnspan=2, sticky='we', padx=5, pady=10)

        self.centraliza(self.top_cadastrar)

    def confirmar_cadastro(self):
        """Valida e salva os dados no banco"""
        nome = self.ent_nome.get()
        cpf = self.ent_cpf.get()
        email = self.ent_email.get()
        senha = self.ent_senha_cad.get()

        if nome == '' or cpf == '' or email == '' or senha == '':
            messagebox.showwarning('Aviso', 'Todos os campos são obrigatórios.', parent=self.top_cadastrar)
        else:
            try:
                self.cursor.execute(
                    "INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)",
                    (nome, cpf, email, senha)
                )
                self.conn.commit()
                messagebox.showinfo('Sucesso', f'Cadastro realizado com sucesso!\n\nNome: {nome}\nEmail: {email}')
                self.top_cadastrar.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "CPF ou Email já cadastrados!", parent=self.top_cadastrar)

    def login(self):
        """Verifica login com banco de dados"""
        email = self.ent_usuario.get()
        senha = self.ent_senha.get()

        self.cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        usuario = self.cursor.fetchone()

        if usuario:
            messagebox.showinfo("Login", f"Bem-vindo, {usuario[1]}!")
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def centraliza(self, master):
        """Centraliza a janela na tela"""
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

app = ttk.Window(themename='darkly')
Tela(app)
app.mainloop()