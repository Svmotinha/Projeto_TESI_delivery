import tkinter as tk
from tkinter import messagebox, ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from PIL import Image, ImageTk
import os
import json
from datetime import datetime

# --- CREDENCIAIS DO ADMINISTRADOR ---
ADMIN_EMAIL = "admin@"
ADMIN_SENHA = "admin123"


class TelaAdmin:
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Área Administrativa")
        self.janela.geometry("800x500")

        # Frame principal
        main_frame = ttk.Frame(self.janela)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Frame de gerenciamento de usuários
        frm_usuarios = ttk.Labelframe(main_frame, text="Usuários Cadastrados")
        frm_usuarios.pack(fill=BOTH, expand=True, pady=(0, 10))
        
        # --- Botão para gerenciar pedidos ---
        frm_botoes_admin = ttk.Frame(self.janela)
        frm_botoes_admin.pack(pady=10)

        btn_gerenciar_pedidos = ttk.Button(frm_botoes_admin, text="Gerenciar Pedidos",
                                           bootstyle="info", command=self.abrir_tela_pedidos)
        btn_gerenciar_pedidos.pack(side=LEFT, padx=5)
        
        btn_excluir = ttk.Button(frm_botoes_admin, text="Excluir Usuário Selecionado",
                                 bootstyle="danger", command=self.excluir_usuario)
        btn_excluir.pack(side=LEFT, padx=5)

        self.tree = ttk.Treeview(
            frm_usuarios,
            columns=('ID', 'Nome', 'CPF', 'Email'),
            show='headings',
            bootstyle="primary"
        )
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('CPF', text='CPF')
        self.tree.heading('Email', text='Email')

        self.tree.column('ID', width=30, anchor=CENTER)
        self.tree.column('Nome', width=150)
        self.tree.column('CPF', width=100)
        self.tree.column('Email', width=200)

        self.tree.pack(fill='both', expand=True, padx=10, pady=10)

        self.carregar_usuarios()
        self.centraliza(self.janela)
    
    def abrir_tela_pedidos(self):
        top_pedidos = ttk.Toplevel(self.janela)
        TelaAdminPedidos(top_pedidos, self.conn, self.cursor)

    def excluir_usuario(self):
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning('Aviso', 'Por favor, selecione um usuário para excluir.')
            return
            
        usuario_id = self.tree.item(item_selecionado, 'values')[0]
        confirmacao = messagebox.askyesno(
            "Confirmação", "Tem certeza que deseja excluir o usuário selecionado?")

        if confirmacao:
            try:
                self.cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
                self.conn.commit()
                self.tree.delete(item_selecionado)
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível excluir o usuário: {e}")

    def carregar_usuarios(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            self.cursor.execute("SELECT id, nome, cpf, email FROM usuarios")
            for usuario in self.cursor.fetchall():
                self.tree.insert('', END, values=usuario)
        except Exception as e:
            messagebox.showerror("Erro no Banco de Dados",
                                 f"Não foi possível carregar os usuários: {e}")

    def centraliza(self, master):
        master.update_idletasks()
        width = master.winfo_width()
        height = master.winfo_height()
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry(f'{width}x{height}+{x}+{y}')

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

        frm_botoes = ttk.Frame(self.janela)
        frm_botoes.grid(column=1, row=2, sticky=E, padx=10, pady=10)
        self.btn_login = ttk.Button(frm_botoes, text="Entrar", bootstyle="primary", command=self.login)
        self.btn_login.pack(side=LEFT, padx=5)
        self.btn_cadastrar = ttk.Button(frm_botoes, text="Cadastrar", bootstyle="success-outline", command=self.cadastrar)
        self.btn_cadastrar.pack(side=LEFT)

        self.janela.bind("<Return>", self.login)
        self.centraliza(self.janela)

    def conectar_db(self):
        self.conn = sqlite3.connect("usuarios.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON;') # Habilitar chaves estrangeiras
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
        # --- TABELA DE PEDIDOS COM STATUS ---
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS pedidos ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'usuario_id INTEGER NOT NULL,'
            'produtos TEXT NOT NULL,'
            'total REAL NOT NULL,'
            'data_pedido TEXT NOT NULL,'
            "status TEXT NOT NULL DEFAULT 'Recebido'," # Novo campo status
            'FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE)' # Deletar pedidos se usuário for deletado
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

        ttk.Label(self.top_cadastrar, text='NOME:').grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.ent_nome = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(self.top_cadastrar, text='CPF:').grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.ent_cpf = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_cpf.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(self.top_cadastrar, text='EMAIL:').grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.ent_email = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_email.grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(self.top_cadastrar, text='SENHA:').grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.ent_senha_cad = ttk.Entry(self.top_cadastrar, show="*", width=30)
        self.ent_senha_cad.grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(self.top_cadastrar, text='Confirmar Cadastro', bootstyle="success", command=self.confirmar_cadastro).grid(row=4, column=0, columnspan=2, sticky='we', padx=5, pady=10)
        self.centraliza(self.top_cadastrar)

    def confirmar_cadastro(self):
        nome = self.ent_nome.get()
        cpf = self.ent_cpf.get()
        email = self.ent_email.get()
        senha = self.ent_senha_cad.get()

        if not all([nome, cpf, email, senha]):
            messagebox.showwarning('Aviso', 'Todos os campos são obrigatórios.', parent=self.top_cadastrar)
            return
        try:
            sql_novo_usuario = "INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)"
            self.cursor.execute(sql_novo_usuario, [nome, cpf, email, senha])
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Cadastro realizado com sucesso!', parent=self.top_cadastrar)
            self.top_cadastrar.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "CPF ou Email já cadastrados!", parent=self.top_cadastrar)

    def abrir_tela_admin(self):
        self.janela.withdraw()
        top_admin = ttk.Toplevel(self.janela)
        TelaAdmin(top_admin, self.conn, self.cursor)
        top_admin.protocol("WM_DELETE_WINDOW", lambda: self.fechar_janela_top(top_admin))

    def abrir_tela_cardapio(self, usuario_id, usuario_nome):
        self.janela.withdraw()
        top_cardapio = ttk.Toplevel(self.janela)
        self.tela_cardapio_instancia = TelaCardapio(top_cardapio, self.conn, self.cursor, usuario_id, usuario_nome, lambda: self.fechar_tela_cliente(top_cardapio))

    def fechar_janela_top(self, janela_top):
        janela_top.destroy()
        self.janela.deiconify()

    def fechar_tela_cliente(self, top_cardapio):
        if hasattr(self, 'tela_cardapio_instancia') and self.tela_cardapio_instancia.carrinho:
            carrinho = self.tela_cardapio_instancia.carrinho
            for prod_id, qtd in carrinho.items():
                self.cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?", (qtd, prod_id))
            self.conn.commit()
        self.fechar_janela_top(top_cardapio)

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
            self.abrir_tela_cardapio(usuario[0], usuario[1])
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def centraliza(self, master):
        master.update_idletasks()
        width = master.winfo_width()
        height = master.winfo_height()
        x = (master.winfo_screenwidth() // 2) - (width // 2)
        y = (master.winfo_screenheight() // 2) - (height // 2)
        master.geometry(f'{width}x{height}+{x}+{y}')

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

        frm_topo = ttk.Frame(self.janela)
        frm_topo.pack(fill=X, padx=10, pady=10)
        ttk.Label(frm_topo, text="Nosso Cardápio", font=("Arial", 16, "bold")).pack(side=LEFT)
        
        self.btn_ver_carrinho = ttk.Button(frm_topo, text="Ver Carrinho", command=self.abrir_carrinho, bootstyle="info")
        self.btn_ver_carrinho.pack(side=RIGHT, padx=5)
        ttk.Button(frm_topo, text="Histórico de Pedidos", command=self.abrir_historico, bootstyle="primary-outline").pack(side=RIGHT, padx=5)
        ttk.Button(frm_topo, text="Logout", command=self.on_close_callback, bootstyle="danger-outline").pack(side=RIGHT, padx=5)

        container = ttk.Frame(self.janela)
        container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.janela.protocol("WM_DELETE_WINDOW", self.on_close_callback)
        self.carregar_produtos()
        self.atualizar_contador_carrinho()

    def carregar_produtos(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        try:
            self.cursor.execute("SELECT * FROM produtos")
            for produto in self.cursor.fetchall():
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
            ttk.Label(frm_produto, image=self.imagens_produtos[produto_id]).pack(side=LEFT, padx=10, pady=10)
        except:
            ttk.Label(frm_produto, text="Imagem\nIndisponível", width=12, anchor=CENTER).pack(side=LEFT, padx=10, pady=10)

        frm_info = ttk.Frame(frm_produto)
        frm_info.pack(side=LEFT, fill=X, expand=True, padx=10)
        ttk.Label(frm_info, text=desc, wraplength=400, justify=LEFT, font=("Arial", 9)).pack(anchor=W)
        ttk.Label(frm_info, text=f"R$ {preco:.2f}", font=("Arial", 12, "bold")).pack(anchor=W, pady=5)
        
        if estoque <= 0:
            ttk.Label(frm_info, text="ESGOTADO", bootstyle="danger", font=("Arial", 10, "bold")).pack(anchor=W, pady=5)

        frm_controles = ttk.Frame(frm_produto)
        frm_controles.pack(side=RIGHT, padx=10)
        
        btn_mais = ttk.Button(frm_controles, text="+", bootstyle="success", command=lambda p_id=produto_id: self.adicionar_ao_carrinho(p_id))
        btn_mais.pack(pady=5)
        btn_menos = ttk.Button(frm_controles, text="-", bootstyle="danger", command=lambda p_id=produto_id: self.remover_do_carrinho(p_id))
        btn_menos.pack()

        if estoque <= 0:
            btn_mais.config(state=DISABLED)

    def adicionar_ao_carrinho(self, produto_id):
        self.cursor.execute("SELECT estoque FROM produtos WHERE id=?", (produto_id,))
        if self.cursor.fetchone()[0] > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque - 1 WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carrinho[produto_id] = self.carrinho.get(produto_id, 0) + 1
            self.carregar_produtos()
            self.atualizar_contador_carrinho()
        else:
            messagebox.showwarning("Estoque", "Produto esgotado!")

    def remover_do_carrinho(self, produto_id):
        if self.carrinho.get(produto_id, 0) > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque + 1 WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carrinho[produto_id] -= 1
            if self.carrinho[produto_id] == 0:
                del self.carrinho[produto_id]
            self.carregar_produtos()
            self.atualizar_contador_carrinho()

    def atualizar_contador_carrinho(self):
        total_itens = sum(self.carrinho.values())
        self.btn_ver_carrinho.config(text=f"Ver Carrinho ({total_itens})" if total_itens > 0 else "Ver Carrinho")

    def abrir_carrinho(self):
        if not self.carrinho:
            messagebox.showinfo("Carrinho Vazio", "Seu carrinho está vazio.")
            return
        top_carrinho = ttk.Toplevel(self.janela)
        TelaCarrinho(top_carrinho, self.conn, self.cursor, self.carrinho, self.usuario_id, self.carregar_produtos, self.atualizar_contador_carrinho)
    
    def abrir_historico(self):
        top_historico = ttk.Toplevel(self.janela)
        TelaHistorico(top_historico, self.conn, self.cursor, self.usuario_id)

class TelaCarrinho:
    def __init__(self, master, conn, cursor, carrinho_ref, usuario_id, refresh_cardapio_cb, refresh_counter_cb):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.carrinho = carrinho_ref
        self.usuario_id = usuario_id
        self.refresh_cardapio = refresh_cardapio_cb
        self.refresh_counter = refresh_counter_cb
        self.janela.title("Meu Carrinho")
        self.janela.geometry("550x600")
        self.janela.grab_set()

        ttk.Label(self.janela, text="Resumo do Pedido", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Container para os itens, para poder limpar e recarregar
        self.container_itens = ttk.Frame(self.janela)
        self.container_itens.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        self.lbl_total = ttk.Label(self.janela, text="", font=("Arial", 14, "bold"))
        self.lbl_total.pack(pady=10)

        frm_botoes = ttk.Frame(self.janela)
        frm_botoes.pack(pady=10)
        ttk.Button(frm_botoes, text="Realizar Pedido", bootstyle="success", command=self.finalizar_pedido).pack(side=LEFT, padx=5)
        ttk.Button(frm_botoes, text="Voltar", bootstyle="secondary-outline", command=self.janela.destroy).pack(side=LEFT, padx=5)

        self.atualizar_visualizacao_carrinho()

    def atualizar_visualizacao_carrinho(self):
        for widget in self.container_itens.winfo_children():
            widget.destroy()

        total_pedido = 0
        if not self.carrinho:
            self.janela.destroy()
            return
        
        for produto_id, quantidade in self.carrinho.items():
            self.cursor.execute("SELECT nome, preco FROM produtos WHERE id=?", (produto_id,))
            nome, preco = self.cursor.fetchone()
            subtotal = preco * quantidade
            total_pedido += subtotal
            self.criar_bloco_item_carrinho(produto_id, nome, quantidade, subtotal)
        
        self.lbl_total.config(text=f"Total: R$ {total_pedido:.2f}")
        self.refresh_counter()

    def criar_bloco_item_carrinho(self, p_id, nome, qtd, subtotal):
        frm_item = ttk.Frame(self.container_itens, relief=SOLID, borderwidth=1)
        frm_item.pack(fill=X, padx=10, pady=5)

        info_txt = f"{nome}\nSubtotal: R$ {subtotal:.2f}"
        ttk.Label(frm_item, text=info_txt, justify=LEFT).pack(side=LEFT, expand=True, fill=X, padx=10)

        frm_controles = ttk.Frame(frm_item)
        frm_controles.pack(side=RIGHT, padx=10, pady=5)

        ttk.Button(frm_controles, text="-", width=2, bootstyle="danger", command=lambda: self.diminuir_quantidade(p_id)).pack(side=LEFT, padx=2)
        ttk.Label(frm_controles, text=str(qtd), width=3, anchor=CENTER).pack(side=LEFT)
        ttk.Button(frm_controles, text="+", width=2, bootstyle="success", command=lambda: self.aumentar_quantidade(p_id)).pack(side=LEFT, padx=2)
        ttk.Button(frm_controles, text="🗑️", width=2, bootstyle="danger-outline", command=lambda: self.remover_totalmente(p_id)).pack(side=LEFT, padx=(10, 2))

    def aumentar_quantidade(self, p_id):
        self.cursor.execute("SELECT estoque FROM produtos WHERE id=?", (p_id,))
        if self.cursor.fetchone()[0] > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque - 1 WHERE id=?", (p_id,))
            self.conn.commit()
            self.carrinho[p_id] += 1
            self.atualizar_visualizacao_carrinho()
            self.refresh_cardapio()
        else:
            messagebox.showwarning("Estoque", "Não há mais estoque para este produto.", parent=self.janela)

    def diminuir_quantidade(self, p_id):
        self.cursor.execute("UPDATE produtos SET estoque = estoque + 1 WHERE id=?", (p_id,))
        self.conn.commit()
        self.carrinho[p_id] -= 1
        if self.carrinho[p_id] == 0:
            del self.carrinho[p_id]
        self.atualizar_visualizacao_carrinho()
        self.refresh_cardapio()

    def remover_totalmente(self, p_id):
        self.cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id=?", (self.carrinho[p_id], p_id))
        self.conn.commit()
        del self.carrinho[p_id]
        self.atualizar_visualizacao_carrinho()
        self.refresh_cardapio()
        
    def finalizar_pedido(self):
        total_final = 0
        produtos_detalhes = {}
        for prod_id, qtd in self.carrinho.items():
            self.cursor.execute("SELECT nome, preco FROM produtos WHERE id=?", (prod_id,))
            nome, preco = self.cursor.fetchone()
            total_final += preco * qtd
            produtos_detalhes[prod_id] = {'nome': nome, 'qtd': qtd}

        produtos_json = json.dumps(produtos_detalhes)
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        try:
            self.cursor.execute(
                "INSERT INTO pedidos (usuario_id, produtos, total, data_pedido) VALUES (?, ?, ?, ?)",
                (self.usuario_id, produtos_json, total_final, data_atual)
            )
            self.conn.commit()
            messagebox.showinfo("Pedido Finalizado", "Seu pedido foi realizado com sucesso!", parent=self.janela)
            self.carrinho.clear()
            self.refresh_cardapio()
            self.refresh_counter()
            self.janela.destroy()
        except Exception as e:
            messagebox.showerror("Erro ao Salvar Pedido", f"Ocorreu um erro: {e}", parent=self.janela)

class TelaHistorico:
    def __init__(self, master, conn, cursor, usuario_id):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.usuario_id = usuario_id
        self.janela.title("Meus Pedidos")
        self.janela.geometry("700x500")
        self.janela.grab_set()

        main_frame = ttk.Frame(self.janela)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        frm_lista = ttk.Labelframe(main_frame, text="Pedidos Realizados")
        frm_lista.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        self.frm_detalhes = ttk.Labelframe(main_frame, text="Detalhes do Pedido")
        self.frm_detalhes.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
        
        # --- Treeview COM STATUS ---
        self.tree = ttk.Treeview(frm_lista, columns=('ID', 'Data', 'Total', 'Status'), show='headings', bootstyle="primary")
        self.tree.heading('ID', text='Pedido ID')
        self.tree.heading('Data', text='Data')
        self.tree.heading('Total', text='Total (R$)')
        self.tree.heading('Status', text='Status')

        self.tree.column('ID', width=80, anchor=CENTER)
        self.tree.column('Data', width=150)
        self.tree.column('Total', width=100, anchor=E)
        self.tree.column('Status', width=120)
        
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.mostrar_detalhes)
        self.carregar_pedidos()

    def carregar_pedidos(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            self.cursor.execute("SELECT id, data_pedido, total, status FROM pedidos WHERE usuario_id=? ORDER BY id DESC", (self.usuario_id,))
            for p in self.cursor.fetchall():
                self.tree.insert('', END, values=(p[0], p[1], f"{p[2]:.2f}", p[3]))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o histórico: {e}", parent=self.janela)
    
    def mostrar_detalhes(self, event):
        for widget in self.frm_detalhes.winfo_children(): widget.destroy()
        item_selecionado = self.tree.selection()
        if not item_selecionado: return

        pedido_id = self.tree.item(item_selecionado, 'values')[0]
        try:
            self.cursor.execute("SELECT produtos FROM pedidos WHERE id=?", (pedido_id,))
            produtos_json = self.cursor.fetchone()[0]
            produtos_dict = json.loads(produtos_json)

            if not produtos_dict:
                ttk.Label(self.frm_detalhes, text="Não há itens neste pedido.").pack(padx=10, pady=10)
                return

            frm_cabecalho = ttk.Frame(self.frm_detalhes)
            frm_cabecalho.pack(fill=X, padx=10, pady=(5,0))
            ttk.Label(frm_cabecalho, text="Produto", font=('bold')).pack(side=LEFT)
            ttk.Label(frm_cabecalho, text="Qtd", font=('bold')).pack(side=RIGHT)
            ttk.Separator(self.frm_detalhes, orient=HORIZONTAL).pack(fill=X, padx=10, pady=5)

            for prod_id, detalhes in produtos_dict.items():
                nome_produto = detalhes.get('nome', 'Produto Indisponível')
                qtd = detalhes.get('qtd', '?')
                frm_item = ttk.Frame(self.frm_detalhes)
                frm_item.pack(fill=X, padx=10, pady=2)
                ttk.Label(frm_item, text=nome_produto).pack(side=LEFT)
                ttk.Label(frm_item, text=str(qtd)).pack(side=RIGHT)
        except Exception as e:
            ttk.Label(self.frm_detalhes, text=f"Erro ao carregar detalhes:\n{e}").pack(padx=10, pady=10)


class TelaAdminPedidos:
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Gerenciamento de Pedidos")
        self.janela.geometry("900x600")
        self.janela.grab_set()

        main_frame = ttk.Frame(self.janela)
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        frm_lista = ttk.Labelframe(main_frame, text="Pedidos Ativos")
        frm_lista.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        self.frm_detalhes = ttk.Labelframe(main_frame, text="Detalhes e Ações")
        self.frm_detalhes.pack(side=RIGHT, fill=BOTH, expand=True, padx=(5, 0))
        
        self.tree = ttk.Treeview(frm_lista, columns=('ID', 'Cliente', 'Data', 'Total', 'Status'), show='headings', bootstyle="info")
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
        
        self.tree.pack(fill=BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.mostrar_detalhes)
        
        self.criar_widgets_detalhes()
        self.carregar_pedidos()

    def criar_widgets_detalhes(self):
        self.detalhes_texto = tk.Text(self.frm_detalhes, height=10, state=DISABLED, font=("Courier", 9))
        self.detalhes_texto.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        frm_acoes = ttk.Frame(self.frm_detalhes)
        frm_acoes.pack(fill=X, padx=10, pady=10)

        ttk.Label(frm_acoes, text="Mudar status para:").pack(side=LEFT)
        self.status_var = tk.StringVar()
        self.combobox_status = ttk.Combobox(frm_acoes, textvariable=self.status_var, state='readonly',
                                            values=["Recebido", "Em preparo", "Em rota de entrega", "Finalizado"])
        self.combobox_status.pack(side=LEFT, padx=5)
        
        self.btn_atualizar = ttk.Button(frm_acoes, text="Atualizar", bootstyle="success", command=self.atualizar_status, state=DISABLED)
        self.btn_atualizar.pack(side=LEFT)

    def carregar_pedidos(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            # Seleciona pedidos que NÃO estão finalizados, juntando com o nome do usuário
            sql = """
                SELECT p.id, u.nome, p.data_pedido, p.total, p.status
                FROM pedidos p
                JOIN usuarios u ON p.usuario_id = u.id
                WHERE p.status != 'Finalizado'
                ORDER BY p.id ASC
            """
            self.cursor.execute(sql)
            for p in self.cursor.fetchall():
                self.tree.insert('', END, values=(p[0], p[1], p[2], f"{p[3]:.2f}", p[4]))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os pedidos: {e}", parent=self.janela)
    
    def mostrar_detalhes(self, event):
        item_selecionado = self.tree.selection()
        if not item_selecionado: 
            self.btn_atualizar.config(state=DISABLED)
            self.status_var.set('')
            return

        self.btn_atualizar.config(state=NORMAL)
        valores = self.tree.item(item_selecionado, 'values')
        pedido_id = valores[0]
        status_atual = valores[4]
        self.status_var.set(status_atual)
        
        self.detalhes_texto.config(state=NORMAL)
        self.detalhes_texto.delete('1.0', END)
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
        self.detalhes_texto.config(state=DISABLED)

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
            # Recarrega a lista, o que fará o pedido "Finalizado" desaparecer
            self.carregar_pedidos()
            # Limpa a seleção e os detalhes
            self.detalhes_texto.config(state=NORMAL)
            self.detalhes_texto.delete('1.0', END)
            self.detalhes_texto.config(state=DISABLED)
            self.status_var.set('')
            self.btn_atualizar.config(state=DISABLED)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível atualizar o status: {e}", parent=self.janela)

if __name__ == "__main__":
    app = ttk.Window(themename='darkly')
    Tela(app)
    app.mainloop()

