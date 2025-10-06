import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from PIL import Image, ImageTk
import os
import json
from datetime import datetime

ADMIN_EMAIL = "admin@"
ADMIN_SENHA = "admin123"

class TelaGerenciarUsuarios:
    def __init__(self, master, conn, cursor, on_close_callback):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.on_close_callback = on_close_callback
        self.janela.title("Gerenciamento de Usuários")
        self.janela.geometry("700x500")
        self.janela.protocol("WM_DELETE_WINDOW", self.on_close_callback)
        self.janela.grab_set()
        
        self.lbl_tituloAdmin = ttk.Label(self.janela, text="Usuários Cadastrados", font=("Arial", 16, "bold"))
        self.lbl_tituloAdmin.pack(pady=10)

        self.tree = ttk.Treeview(
            self.janela, 
            columns=('ID', 'Nome', 'CPF', 'Email'), 
            show='headings',
            bootstyle="primary"
        )
        self.tree.heading('ID', text='ID', anchor=W)
        self.tree.heading('Nome', text='Nome', anchor=W)
        self.tree.heading('CPF', text='CPF', anchor=W)
        self.tree.heading('Email', text='Email', anchor=W)
        
        self.tree.column('ID', width=30, anchor=CENTER)
        self.tree.column('Nome', width=150, anchor=W)
        self.tree.column('CPF', width=100, anchor=W)
        self.tree.column('Email', width=200, anchor=W)
        
        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.frm_botoes_admin = ttk.Frame(self.janela)
        self.frm_botoes_admin.pack(pady=10)

        self.btn_excluir = ttk.Button(self.frm_botoes_admin, text="Excluir Selecionado", bootstyle="danger", command=self.excluir_usuario)
        self.btn_excluir.pack(side=LEFT, padx=5)

        self.carregar_usuarios()
        self.centraliza(self.janela)

    def excluir_usuario(self):
        item_selecionado = self.tree.selection()
        
        if len(item_selecionado) > 0:
            usuario_id = self.tree.item(item_selecionado, 'values')[0]
            confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir o usuário selecionado?", parent=self.janela)
            
            if confirmacao:
                if usuario_id == '1': 
                    messagebox.showerror("Erro", "Não é possível excluir o administrador principal.", parent=self.janela)
                    return
                self.cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
                self.conn.commit()
                self.tree.delete(item_selecionado)
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.", parent=self.janela)
        else:
            messagebox.showwarning('Aviso', 'Por favor, selecione um usuário para excluir.', parent=self.janela)

    def carregar_usuarios(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        try:
            self.cursor.execute("SELECT id, nome, cpf, email FROM usuarios")
            usuarios = self.cursor.fetchall()
            
            for i in usuarios:
                self.tree.insert('', END, values=i)
        except Exception as erro:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível carregar os usuários: {erro}", parent=self.janela)

    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

class TelaAdmin:
    def __init__(self, master, conn, cursor, on_close_callback):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.on_close_callback = on_close_callback
        self.janela.title("Painel do Administrador")
        self.janela.geometry("400x200")
        self.janela.protocol("WM_DELETE_WINDOW", self.on_close_callback)

        self.lbl_titulo = ttk.Label(self.janela, text="Painel Administrativo", font=("Arial", 16, "bold"))
        self.lbl_titulo.pack(pady=20)
        
        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.pack(pady=10)

        self.btn_gerenciarUsuarios = ttk.Button(self.frm_botoes, text="Gerenciar Usuários", command=self.abrir_gerenciamento_usuarios, bootstyle="primary")
        self.btn_gerenciarUsuarios.pack(pady=5, padx=10, fill=X)
        
        self.btn_gerenciarPedidos = ttk.Button(self.frm_botoes, text="Gerenciar Pedidos", command=self.abrir_gerenciamento_pedidos, bootstyle="info")
        self.btn_gerenciarPedidos.pack(pady=5, padx=10, fill=X)

        self.centraliza(self.janela)
    
    def abrir_gerenciamento_usuarios(self):
        top_usuarios = ttk.Toplevel(self.janela)
        TelaGerenciarUsuarios(top_usuarios, self.conn, self.cursor, top_usuarios.destroy)

    def abrir_gerenciamento_pedidos(self):
        top_pedidos = ttk.Toplevel(self.janela)
        TelaPedidosAdmin(top_pedidos, self.conn, self.cursor)

    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')


class TelaPedidosAdmin:
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Gerenciamento de Pedidos")
        self.janela.geometry("900x600")
        self.janela.grab_set()

        self.main_frame = ttk.Frame(self.janela)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frm_lista = ttk.Labelframe(self.main_frame, text="Pedidos Ativos")
        self.frm_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        self.frm_detalhes = ttk.Labelframe(self.main_frame, text="Detalhes e Ações")
        self.frm_detalhes.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.tree = ttk.Treeview(self.frm_lista, columns=('ID', 'Cliente', 'Data', 'Total', 'Status'), show='headings', bootstyle="info")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Cliente', text='Cliente')
        self.tree.heading('Data', text='Data')
        self.tree.heading('Total', text='Total (R$)')
        self.tree.heading('Status', text='Status')

        self.tree.column('ID', width=40, anchor=CENTER)
        self.tree.column('Cliente', width=150)
        self.tree.column('Data', width=130)
        self.tree.column('Total', width=80, anchor=E)
        self.tree.column('Status', width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.mostrar_detalhes)
        
        self.criar_widgets_detalhes()
        self.carregar_pedidos()
        self.centraliza(self.janela)

    def criar_widgets_detalhes(self):
        self.detalhes_texto = tk.Text(self.frm_detalhes, height=10, state=tk.DISABLED, font=("Courier", 9))
        self.detalhes_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.frm_acoes = ttk.Frame(self.frm_detalhes)
        self.frm_acoes.pack(fill=tk.X, padx=10, pady=10)

        self.lbl_mudarStatus = ttk.Label(self.frm_acoes, text="Mudar status para:")
        self.lbl_mudarStatus.pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar()
        self.combobox_status = ttk.Combobox(self.frm_acoes, textvariable=self.status_var, state='readonly',
                                            values=["Em preparo", "Em rota de entrega", "Finalizado"])
        self.combobox_status.pack(side=tk.LEFT, padx=5)
        
        self.btn_atualizar = ttk.Button(self.frm_acoes, text="Atualizar Status", bootstyle="success", command=self.atualizar_status, state=tk.DISABLED)
        self.btn_atualizar.pack(side=tk.LEFT)

        self.btn_historico = ttk.Button(self.frm_detalhes, text="Ver Pedidos Finalizados", bootstyle="secondary", command=self.abrir_historico_admin)
        self.btn_historico.pack(pady=10)
        

    def carregar_pedidos(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            sql = """
                SELECT p.id, u.nome, p.data_pedido, p.total, p.status
                FROM pedidos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.status != 'Finalizado'
                ORDER BY p.id ASC
            """
            self.cursor.execute(sql)
            for p in self.cursor.fetchall():
                self.tree.insert('', tk.END, values=(p[0], p[1], p[2], f"{p[3]:.2f}", p[4]))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os pedidos: {e}", parent=self.janela)
    
    def mostrar_detalhes(self, event):
        item_selecionado = self.tree.selection()
        if not item_selecionado: 
            self.btn_atualizar.config(state=tk.DISABLED)
            self.status_var.set('')
            return

        self.btn_atualizar.config(state=tk.NORMAL)
        valores = self.tree.item(item_selecionado, 'values')
        pedido_id = valores[0]
        status_atual = valores[4]
        self.status_var.set(status_atual)
        
        self.detalhes_texto.config(state=tk.NORMAL)
        self.detalhes_texto.delete('1.0', tk.END)
        try:
            self.cursor.execute("SELECT produtos FROM pedidos WHERE id=?", (pedido_id,))
            produtos_json = self.cursor.fetchone()[0]
            produtos_dict = json.loads(produtos_json)

            texto_detalhes = ""
            for prod_id, detalhes in produtos_dict.items():
                nome = detalhes.get('nome', 'N/A')
                qtd = detalhes.get('qtd', '?')
                texto_detalhes += f"{nome:<30} Qtd: {qtd}\n"

            self.detalhes_texto.insert('1.0', texto_detalhes)
        except Exception as e:
            self.detalhes_texto.insert('1.0', f"Erro ao carregar detalhes: {e}")
        self.detalhes_texto.config(state=tk.DISABLED)

    def atualizar_status(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Nenhum pedido selecionado.", parent=self.janela)
            return

        pedido_id = self.tree.item(item_selecionado, 'values')[0]
        novo_status = self.status_var.get()
        if not novo_status:
            messagebox.showwarning("Aviso", "Selecione um status.", parent=self.janela)
            return
            
        try:
            self.cursor.execute("UPDATE pedidos SET status=? WHERE id=?", (novo_status, pedido_id))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Status do pedido atualizado!", parent=self.janela)
            self.carregar_pedidos()
            
            self.detalhes_texto.config(state=tk.NORMAL)
            self.detalhes_texto.delete('1.0', tk.END)
            self.detalhes_texto.config(state=tk.DISABLED)
            self.status_var.set('')
            self.btn_atualizar.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar o status: {e}", parent=self.janela)

    def abrir_historico_admin(self):
        top_historico = ttk.Toplevel(self.janela)
        TelaHistoricoAdmin(top_historico, self.conn, self.cursor)

    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')


class TelaHistoricoAdmin:
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Histórico de Pedidos Finalizados")
        self.janela.geometry("800x500")
        self.janela.grab_set()

        self.lbl_titulo = ttk.Label(self.janela, text="Pedidos Finalizados", font=("Arial", 16, "bold"))
        self.lbl_titulo.pack(pady=10)

        self.tree = ttk.Treeview(self.janela, columns=('ID', 'Cliente', 'Data', 'Total'), show='headings', bootstyle="success")
        self.tree.heading('ID', text='ID')
        self.tree.heading('Cliente', text='Cliente')
        self.tree.heading('Data', text='Data')
        self.tree.heading('Total', text='Total (R$)')
        
        self.tree.column('ID', width=50, anchor=CENTER)
        self.tree.column('Cliente', width=200)
        self.tree.column('Data', width=150)
        self.tree.column('Total', width=100, anchor=E)
        
        self.tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.carregar_pedidos_finalizados()
        self.centraliza(self.janela)

    def carregar_pedidos_finalizados(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            sql = """
                SELECT p.id, u.nome, p.data_pedido, p.total
                FROM pedidos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.status = 'Finalizado'
                ORDER BY p.id DESC
            """
            self.cursor.execute(sql)
            for p in self.cursor.fetchall():
                self.tree.insert('', END, values=(p[0], p[1], p[2], f"{p[3]:.2f}"))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o histórico: {e}", parent=self.janela)

    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
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
        self.conectar_db()

        self.lbl_usuario = ttk.Label(self.janela, text="Email:")
        self.lbl_usuario.grid(column=0, row=0, sticky=W, padx=10, pady=10)

        self.ent_usuario = ttk.Entry(self.janela, width=30)
        self.ent_usuario.grid(column=1, row=0, sticky=E, padx=10, pady=10)

        self.lbl_senha = ttk.Label(self.janela, text="Senha:")
        self.lbl_senha.grid(column=0, row=1, sticky=W, padx=10, pady=10)

        self.ent_senha = ttk.Entry(self.janela, show="*", width=30)
        self.ent_senha.grid(column=1, row=1, sticky=E, padx=10, pady=10)

        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.grid(column=1, row=2, sticky=E, padx=10, pady=10)

        self.btn_login = ttk.Button(self.frm_botoes, text="Entrar", bootstyle="primary", command=self.login)
        self.btn_login.pack(side=LEFT, padx=5)

        self.btn_cadastrar = ttk.Button(self.frm_botoes, text="Cadastrar", bootstyle="success-outline", command=self.cadastrar)
        self.btn_cadastrar.pack(side=LEFT)
        
        self.janela.bind("<Return>", self.login)
        self.centraliza(self.janela)

    def conectar_db(self):
        self.conn = sqlite3.connect("Entregai.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS usuarios ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'nome TEXT NOT NULL,'
            'cpf TEXT NOT NULL UNIQUE,'
            'email TEXT NOT NULL UNIQUE,'
            'senha TEXT NOT NULL)'
        )
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS produtos ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'nome TEXT NOT NULL,'
            'descricao TEXT,'
            'preco REAL NOT NULL,'
            'estoque INTEGER NOT NULL,'
            'caminho_imagem TEXT)'
        )
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS pedidos ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'usuario_id INTEGER NOT NULL,'
            'produtos TEXT NOT NULL,'
            'total REAL NOT NULL,'
            'data_pedido TEXT NOT NULL,'
            'status TEXT NOT NULL,'
            'FOREIGN KEY (usuario_id) REFERENCES usuarios(id))'
        )
        self.conn.commit()
        self.popular_produtos_se_vazio()

    def popular_produtos_se_vazio(self):
        self.cursor.execute("SELECT COUNT(*) FROM produtos")
        if self.cursor.fetchone()[0] == 0:
            if not os.path.exists('imagens'):
                os.makedirs('imagens')
            
            produtos_iniciais = [
                ('Combo Hot Philadelphia', '10 Hot Rolls Philadelphia + 1 Refri Lata', 45.90, 20, 'imagens/combo_hot.png'),
                ('Combo Super Temaki', '2 Temakis Salmão completo + 1 porção de sunomono', 55.00, 15, 'imagens/combo_temaki.png'),
                ('Combo Yakisoba Casal', '2 Yakisobas (Frango ou Carne) + 2 Rolinhos Primavera', 65.50, 10, 'imagens/combo_yakisoba.png'),
                ('Combo Sashimi Mix', '15 fatias de sashimi (Salmão, Atum, Peixe Branco)', 75.00, 18, 'imagens/combo_sashimi.png'),
                ('Combo Uramaki Especial', '10 Uramakis Califórnia + 10 Uramakis Skin', 49.90, 25, 'imagens/combo_uramakis.png'),
                ('Combo Poke Fit', '1 Poke de Salmão com base de arroz + 1 Suco Natural', 42.00, 12, 'imagens/combo_pokes.png')
            ]
            self.cursor.executemany("INSERT INTO produtos (nome, descricao, preco, estoque, caminho_imagem) VALUES (?, ?, ?, ?, ?)", produtos_iniciais)
            self.conn.commit()

    def cadastrar(self):
        self.top_cadastrar = ttk.Toplevel(self.janela)
        self.top_cadastrar.grab_set()
        self.top_cadastrar.title("Cadastro de Usuário")
        self.top_cadastrar.geometry("400x250")

        self.lbl_nome_cad = ttk.Label(self.top_cadastrar, text='NOME:')
        self.lbl_nome_cad.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.ent_nome_cad = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_nome_cad.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_cpf_cad = ttk.Label(self.top_cadastrar, text='CPF:')
        self.lbl_cpf_cad.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.ent_cpf_cad = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_cpf_cad.grid(row=1, column=1, padx=5, pady=5)

        self.lbl_email_cad = ttk.Label(self.top_cadastrar, text='EMAIL:')
        self.lbl_email_cad.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.ent_email_cad = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_email_cad.grid(row=2, column=1, padx=5, pady=5)

        self.lbl_senha_cad = ttk.Label(self.top_cadastrar, text='SENHA:')
        self.lbl_senha_cad.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.ent_senha_cad = ttk.Entry(self.top_cadastrar, show="*", width=30)
        self.ent_senha_cad.grid(row=3, column=1, padx=5, pady=5)

        self.btn_confirmarCadastro = ttk.Button(self.top_cadastrar, text='Confirmar Cadastro', bootstyle="success", command=self.confirmar_cadastro)
        self.btn_confirmarCadastro.grid(row=4, column=0, columnspan=2, sticky='we', padx=5, pady=10)
        
        self.centraliza(self.top_cadastrar)


    def confirmar_cadastro(self):
        nome = self.ent_nome_cad.get()
        cpf = self.ent_cpf_cad.get()
        email = self.ent_email_cad.get()
        senha = self.ent_senha_cad.get()

        if nome == '' or cpf == '' or email == '' or senha == '':
            messagebox.showwarning('Aviso', 'Todos os campos são obrigatórios.', parent=self.top_cadastrar)
        else:
            try:
                sql_novo_usuario = "INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)"
                self.cursor.execute(sql_novo_usuario,[nome, cpf, email, senha])
                self.conn.commit()
                messagebox.showinfo('Sucesso', f'Cadastro realizado com sucesso!', parent=self.top_cadastrar)
                self.top_cadastrar.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "CPF ou Email já cadastrados!", parent=self.top_cadastrar)
    
    def abrir_tela_admin(self):
        self.janela.withdraw()
        top_admin = ttk.Toplevel(self.janela)
        TelaAdmin(top_admin, self.conn, self.cursor, lambda: self.fechar_admin(top_admin))

    def abrir_tela_cardapio(self, usuario_id, usuario_nome):
        self.janela.withdraw()
        top_cardapio = ttk.Toplevel(self.janela)
        self.tela_cardapio_inst = TelaCardapio(top_cardapio, self.conn, self.cursor, usuario_id, usuario_nome, lambda: self.fechar_tela_cliente(top_cardapio))
        
    def fechar_admin(self, top_admin):
        top_admin.destroy()
        self.janela.deiconify()
    
    def fechar_tela_cliente(self, top_cardapio):
        try:
            carrinho = self.tela_cardapio_inst.carrinho
            for prod_id, qtd in carrinho.items():
                if qtd > 0:
                    self.cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?", (qtd, prod_id))
            self.conn.commit()
        except AttributeError:
            pass
        
        top_cardapio.destroy()
        self.janela.deiconify()

    def login(self, event=None):
        email = self.ent_usuario.get()
        senha = self.ent_senha.get()

        if email == ADMIN_EMAIL and senha == ADMIN_SENHA:
            messagebox.showinfo("Login", "Bem-vindo, Administrador!")
            self.abrir_tela_admin()
            return

        self.cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        usuario = self.cursor.fetchone()

        if usuario:
            usuario_id = usuario[0]
            usuario_nome = usuario[1]
            messagebox.showinfo("Login", f"Bem-vindo, {usuario_nome}!")
            self.abrir_tela_cardapio(usuario_id, usuario_nome) 
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")
            
    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

class TelaCardapio:
    def __init__(self, master, conn, cursor, usuario_id, usuario_nome, on_close_callback):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.usuario_id = usuario_id 
        self.on_close_callback = on_close_callback
        self.janela.title(f"Cardápio - Bem-vindo, {usuario_nome}!")
        self.janela.geometry("800x600")

        self.carrinho = {} 
        self.imagens_produtos = {} 
        
        self.frm_topo = ttk.Frame(self.janela)
        self.frm_topo.pack(fill=X, padx=10, pady=10)
        self.lbl_tituloCardapio = ttk.Label(self.frm_topo, text="Nosso Cardápio", font=("Arial", 16, "bold"))
        self.lbl_tituloCardapio.pack(side=LEFT)
        self.btn_verCarrinho = ttk.Button(self.frm_topo, text="Ver Carrinho", command=self.abrir_carrinho, bootstyle="info")
        self.btn_verCarrinho.pack(side=RIGHT)
        
        self.btn_historico = ttk.Button(self.frm_topo, text="Histórico de Pedidos", command=self.abrir_historico, bootstyle="primary-outline")
        self.btn_historico.pack(side=RIGHT, padx=5)

        self.btn_logout = ttk.Button(self.frm_topo, text="Logout", command=self.on_close_callback, bootstyle="danger-outline")
        self.btn_logout.pack(side=RIGHT, padx=5)
        
        self.container = ttk.Frame(self.janela)
        self.container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(self.container, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.janela.protocol("WM_DELETE_WINDOW", self.on_close_callback)
        self.carregar_produtos()
        self.atualizar_contador_carrinho()

    def carregar_produtos(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        try:
            self.cursor.execute("SELECT * FROM produtos")
            produtos = self.cursor.fetchall()
            for i, produto in enumerate(produtos):
                self.criar_bloco_produto(produto)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os produtos: {e}")
    
    def criar_bloco_produto(self, produto_data):
        produto_id, nome, desc, preco, estoque, img_path = produto_data
        
        frm_produto = ttk.Labelframe(self.scrollable_frame, text=nome, bootstyle="primary")
        frm_produto.pack(fill=X, padx=10, pady=10)

        try:
            img = Image.open(img_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            self.imagens_produtos[produto_id] = ImageTk.PhotoImage(img)
            lbl_imagem = ttk.Label(frm_produto, image=self.imagens_produtos[produto_id])
            lbl_imagem.pack(side=LEFT, padx=10, pady=10)
        except Exception as e:
            lbl_imagem_fallback = ttk.Label(frm_produto, text="Imagem\nIndisponível", width=12, anchor=CENTER)
            lbl_imagem_fallback.pack(side=LEFT, padx=10, pady=10)

        frm_info = ttk.Frame(frm_produto)
        frm_info.pack(side=LEFT, fill=X, expand=True, padx=10)
        lbl_desc = ttk.Label(frm_info, text=desc, wraplength=400, justify=LEFT, font=("Arial", 9))
        lbl_desc.pack(anchor=W)
        lbl_preco = ttk.Label(frm_info, text=f"R$ {preco:.2f}", font=("Arial", 12, "bold"))
        lbl_preco.pack(anchor=W, pady=5)
        
        frm_controles = ttk.Frame(frm_produto)
        frm_controles.pack(side=RIGHT, padx=10)
        
        btn_menos = ttk.Button(frm_controles, text="-", bootstyle="danger")
        btn_menos.pack()
        btn_menos.bind("<Button-1>", lambda event, p_id=produto_id: self.remover_do_carrinho(event, p_id))
        
        btn_mais = ttk.Button(frm_controles, text="+", bootstyle="success")
        btn_mais.pack(pady=5)
        btn_mais.bind("<Button-1>", lambda event, p_id=produto_id: self.adicionar_ao_carrinho(event, p_id))
        
        if estoque <= 0:
            btn_mais.config(state=DISABLED)
            lbl_esgotado = ttk.Label(frm_info, text="ESGOTADO", bootstyle="danger", font=("Arial", 10, "bold"))
            lbl_esgotado.pack(anchor=W, pady=5)
        self.centraliza(self.janela)

    def adicionar_ao_carrinho(self, event, produto_id):
        self.cursor.execute("SELECT estoque FROM produtos WHERE id=?", (produto_id,))
        estoque_atual = self.cursor.fetchone()[0]

        if estoque_atual > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque - 1 WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carrinho[produto_id] = self.carrinho.get(produto_id, 0) + 1
            self.carregar_produtos() 
            self.atualizar_contador_carrinho()
        else:
            messagebox.showwarning("Estoque", "Produto esgotado!")

    def remover_do_carrinho(self, event, produto_id):
        if produto_id in self.carrinho and self.carrinho[produto_id] > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque + 1 WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carrinho[produto_id] -= 1
            if self.carrinho[produto_id] == 0:
                del self.carrinho[produto_id]
            self.carregar_produtos()
            self.atualizar_contador_carrinho()
        else:
            messagebox.showwarning("Carrinho", "Este produto não está no seu carrinho.")

    def atualizar_contador_carrinho(self):
        total_itens = sum(self.carrinho.values())
        if total_itens > 0:
            self.btn_verCarrinho.config(text=f"Ver Carrinho ({total_itens})")
        else:
            self.btn_verCarrinho.config(text="Ver Carrinho")

    def abrir_carrinho(self):
        if not self.carrinho:
            messagebox.showinfo("Carrinho Vazio", "Seu carrinho está vazio.")
            return
        
        top_carrinho = ttk.Toplevel(self.janela)
        top_carrinho.title("Meu Carrinho")
        TelaCarrinho(top_carrinho, self.conn, self.cursor, self.carrinho, self.usuario_id, self.carregar_produtos, self.atualizar_contador_carrinho)
    
    def abrir_historico(self):
        top_historico = ttk.Toplevel(self.janela)
        TelaHistorico(top_historico, self.conn, self.cursor, self.usuario_id)



    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')


class TelaCarrinho:
    def __init__(self, master, conn, cursor, carrinho_ref, usuario_id, refresh_cardapio_callback, refresh_counter_callback):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.carrinho = carrinho_ref 
        self.usuario_id = usuario_id
        self.refresh_cardapio = refresh_cardapio_callback
        self.refresh_counter = refresh_counter_callback
        self.janela.geometry("550x600")
        self.janela.grab_set()

        self.lbl_resumoPedido = ttk.Label(self.janela, text="Resumo do Pedido", font=("Arial", 16, "bold"))
        self.lbl_resumoPedido.pack(pady=10)

        self.container = ttk.Frame(self.janela)
        self.container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(self.container, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.lbl_total = ttk.Label(self.janela, text="", font=("Arial", 14, "bold"))
        self.lbl_total.pack(pady=10)
        
        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.pack(pady=10)
        self.btn_realizarPedido = ttk.Button(self.frm_botoes, text="Realizar Pedido", bootstyle="success", command=self.finalizar_pedido)
        self.btn_realizarPedido.pack(side=LEFT, padx=5)
        self.btn_voltar = ttk.Button(self.frm_botoes, text="Voltar", bootstyle="secondary-outline", command=self.janela.destroy)
        self.btn_voltar.pack(side=LEFT, padx=5)

        self.atualizar_visualizacao_carrinho()
        self.centraliza(self.janela)


    def atualizar_visualizacao_carrinho(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        total_pedido = 0
        if not self.carrinho:
            lbl_carrinhoVazio = ttk.Label(self.scrollable_frame, text="Carrinho Vazio")
            lbl_carrinhoVazio.pack()
            self.janela.after(100, self.janela.destroy)
        else:
            detalhes_produtos = {}
            for produto_id in self.carrinho.keys():
                self.cursor.execute("SELECT nome, preco FROM produtos WHERE id=?", (produto_id,))
                detalhes_produtos[produto_id] = self.cursor.fetchone()

            for produto_id, quantidade in self.carrinho.items():
                nome, preco = detalhes_produtos[produto_id]
                subtotal = preco * quantidade
                total_pedido += subtotal
                self.criar_bloco_item_carrinho(produto_id, nome, quantidade, subtotal)
        
        self.lbl_total.config(text=f"Total: R$ {total_pedido:.2f}")
        self.refresh_counter()

    def criar_bloco_item_carrinho(self, produto_id, nome, quantidade, subtotal):
        frm_item = ttk.Frame(self.scrollable_frame, relief=SOLID, borderwidth=1)
        frm_item.pack(fill=X, padx=5, pady=5)

        info_txt = f"{nome}\nSubtotal: R$ {subtotal:.2f}"
        lbl_infoItem = ttk.Label(frm_item, text=info_txt, justify=LEFT)
        lbl_infoItem.pack(side=LEFT, expand=True, fill=X, padx=10)
        
        frm_controles = ttk.Frame(frm_item)
        frm_controles.pack(side=RIGHT, padx=10)

        btn_menos = ttk.Button(frm_controles, text="-", width=2, bootstyle="danger")
        btn_menos.pack(side=LEFT, padx=2)
        btn_menos.bind("<Button-1>", lambda event, p_id=produto_id: self.diminuir_quantidade(event, p_id))

        lbl_quantidade = ttk.Label(frm_controles, text=str(quantidade), width=3, anchor=CENTER)
        lbl_quantidade.pack(side=LEFT)
        
        btn_mais = ttk.Button(frm_controles, text="+", width=2, bootstyle="success")
        btn_mais.pack(side=LEFT, padx=2)
        btn_mais.bind("<Button-1>", lambda event, p_id=produto_id: self.aumentar_quantidade(event, p_id))
        
        btn_remover = ttk.Button(frm_controles, text="🗑️", width=2, bootstyle="danger-outline")
        btn_remover.pack(side=LEFT, padx=(10,2))
        btn_remover.bind("<Button-1>", lambda event, p_id=produto_id: self.remover_totalmente(event, p_id))

    def aumentar_quantidade(self, event, produto_id):
        self.cursor.execute("SELECT estoque FROM produtos WHERE id=?", (produto_id,))
        if self.cursor.fetchone()[0] > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque - 1 WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carrinho[produto_id] += 1
            self.atualizar_visualizacao_carrinho()
            self.refresh_cardapio()
        else:
            messagebox.showwarning("Estoque", "Não há mais estoque para este produto.", parent=self.janela)

    def diminuir_quantidade(self, event, produto_id):
        self.cursor.execute("UPDATE produtos SET estoque = estoque + 1 WHERE id=?", (produto_id,))
        self.conn.commit()
        self.carrinho[produto_id] -= 1
        if self.carrinho[produto_id] == 0:
            del self.carrinho[produto_id]
        self.atualizar_visualizacao_carrinho()
        self.refresh_cardapio()

    def remover_totalmente(self, event, produto_id):
        quantidade_a_devolver = self.carrinho[produto_id]
        self.cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id=?", (quantidade_a_devolver, produto_id))
        self.conn.commit()
        del self.carrinho[produto_id]
        self.atualizar_visualizacao_carrinho()
        self.refresh_cardapio()

    def finalizar_pedido(self):
        total_final = 0
        produtos_detalhados = {}
        for prod_id, qtd in self.carrinho.items():
            self.cursor.execute("SELECT nome, preco FROM produtos WHERE id=?", (prod_id,))
            nome, preco = self.cursor.fetchone()
            total_final += preco * qtd
            produtos_detalhados[prod_id] = {'nome': nome, 'qtd': qtd}

        produtos_json = json.dumps(produtos_detalhados)
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            self.cursor.execute(
                "INSERT INTO pedidos (usuario_id, produtos, total, data_pedido, status) VALUES (?, ?, ?, ?, ?)",
                (self.usuario_id, produtos_json, total_final, data_atual, 'Em preparo')
            )
            top_status = ttk.Toplevel(self.janela.master)
            novo_pedido_id = self.cursor.lastrowid
            self.conn.commit()
            TelaStatusPedido(top_status, novo_pedido_id, "Em produção", top_status.destroy)
            self.carrinho.clear()
            self.refresh_cardapio()
            self.refresh_counter()
            self.janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro ao Salvar Pedido", f"Ocorreu um erro: {e}", parent=self.janela)


    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')



class TelaStatusPedido:
    def __init__(self, master, pedido_id, status_inicial, on_close_callback):
        self.janela = master
        self.on_close_callback = on_close_callback
        self.janela.title(f"Status do Pedido #{pedido_id}")
        self.janela.geometry("400x200")
        self.janela.protocol("WM_DELETE_WINDOW", self.on_close_callback)
        self.janela.grab_set()

        self.lbl_id_pedido = ttk.Label(self.janela, text=f"Pedido #{pedido_id}", font=("Arial", 16, "bold"))
        self.lbl_id_pedido.pack(pady=20)

        self.lbl_status = ttk.Label(self.janela, text=f"Status: {status_inicial}", font=("Arial", 12))
        self.lbl_status.pack(pady=10)

        self.btn_voltar = ttk.Button(self.janela, text="Voltar ao Cardápio", command=self.on_close_callback, bootstyle="primary")
        self.btn_voltar.pack(pady=20)

        self.centraliza(self.janela)

    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')



class TelaHistorico:
    def __init__(self, master, conn, cursor, usuario_id):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.usuario_id = usuario_id
        self.janela.title("Meus Pedidos")
        self.janela.geometry("700x500")
        self.janela.grab_set()

        self.main_frame = ttk.Frame(self.janela)
        self.main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.frm_lista = ttk.Labelframe(self.main_frame, text="Pedidos Realizados")
        self.frm_lista.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

        self.frm_detalhes = ttk.Labelframe(self.main_frame, text="Detalhes do Pedido")
        self.frm_detalhes.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
        
        self.tree = ttk.Treeview(self.frm_lista, columns=('ID', 'Data', 'Total'), show='headings', bootstyle="primary")
        self.tree.heading('ID', text='Pedido ID')
        self.tree.heading('Data', text='Data')
        self.tree.heading('Total', text='Total (R$)')

        self.tree.column('ID', width=80, anchor=CENTER)
        self.tree.column('Data', width=150)
        self.tree.column('Total', width=100, anchor=E)
        
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.mostrar_detalhes)

        self.carregar_pedidos()
        self.centraliza(self.janela)

    def carregar_pedidos(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            self.cursor.execute("SELECT id, data_pedido, total FROM pedidos WHERE usuario_id=? ORDER BY id DESC", (self.usuario_id,))
            pedidos = self.cursor.fetchall()
            for p in pedidos:
                self.tree.insert('', END, values=(p[0], p[1], f"{p[2]:.2f}"))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o histórico: {e}", parent=self.janela)
    
    def mostrar_detalhes(self, event):
        for widget in self.frm_detalhes.winfo_children():
            widget.destroy()

        item_selecionado = self.tree.selection()
        if not item_selecionado:
            return

        pedido_id = self.tree.item(item_selecionado, 'values')[0]
        
        try:
            self.cursor.execute("SELECT produtos FROM pedidos WHERE id=?", (pedido_id,))
            produtos_json = self.cursor.fetchone()[0]
            produtos_dict = json.loads(produtos_json)

            if not produtos_dict:
                lbl_semItens = ttk.Label(self.frm_detalhes, text="Não há itens neste pedido.")
                lbl_semItens.pack(padx=10, pady=10)
                return

            frm_cabecalho = ttk.Frame(self.frm_detalhes)
            frm_cabecalho.pack(fill=X, padx=10, pady=(5,0))
            lbl_prodCabecalho = ttk.Label(frm_cabecalho, text="Produto", font=('bold'))
            lbl_prodCabecalho.pack(side=LEFT)
            lbl_qtdCabecalho = ttk.Label(frm_cabecalho, text="Qtd", font=('bold'))
            lbl_qtdCabecalho.pack(side=RIGHT)
            
            sep_cabecalho = ttk.Separator(self.frm_detalhes, orient=HORIZONTAL)
            sep_cabecalho.pack(fill=X, padx=10, pady=5)

            for prod_id, detalhes in produtos_dict.items():
                nome_produto = detalhes.get('nome', 'Produto Removido')
                qtd = detalhes.get('qtd', '?')
                
                frm_item = ttk.Frame(self.frm_detalhes)
                frm_item.pack(fill=X, padx=10, pady=2)
                lbl_nomeProduto = ttk.Label(frm_item, text=nome_produto)
                lbl_nomeProduto.pack(side=LEFT)
                lbl_qtdProduto = ttk.Label(frm_item, text=str(qtd))
                lbl_qtdProduto.pack(side=RIGHT)

        except Exception as e:
            lbl_erroDetalhes = ttk.Label(self.frm_detalhes, text=f"Erro ao carregar detalhes:\n{e}")
            lbl_erroDetalhes.pack(padx=10, pady=10)
    
    def centraliza(self, master):
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