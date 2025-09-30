import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
from tkinter.scrolledtext import ScrolledText

from PIL import Image, ImageTk
import os

ADMIN_EMAIL = "admin@"
ADMIN_SENHA = "admin123"
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

        self.centraliza(self.janela)

    def conectar_db(self):
        self.conn = sqlite3.connect("usuarios.db")
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
        self.conn.commit()
        self.popular_produtos_se_vazio()

    def popular_produtos_se_vazio(self):
        self.cursor.execute("SELECT COUNT(*) FROM produtos")
        if self.cursor.fetchone()[0] == 0:
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

        self.lbl_nome = ttk.Label(self.top_cadastrar, text='NOME:')
        self.lbl_nome.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.ent_nome = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_cpf = ttk.Label(self.top_cadastrar, text='CPF:')
        self.lbl_cpf.grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.ent_cpf = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_cpf.grid(row=1, column=1, padx=5, pady=5)

        
        self.lbl_email = tk.Label(self.top_cadastrar, text='EMAIL:')
        self.lbl_email.grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.ent_email = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_email.grid(row=2, column=1, padx=5, pady=5)

        self.lbl_senha = ttk.Label(self.top_cadastrar, text='SENHA:')
        self.lbl_senha.grid(row=3, column=0, padx=5, pady=5, sticky=W)
        self.ent_senha_cad = ttk.Entry(self.top_cadastrar, show="*", width=30)
        self.ent_senha_cad.grid(row=3, column=1, padx=5, pady=5)

        self.btn_confirmar_cadastro = ttk.Button(self.top_cadastrar, text='Confirmar Cadastro', bootstyle="success", command=self.confirmar_cadastro)
        self.btn_confirmar_cadastro.grid(row=4, column=0, columnspan=2, sticky='we', padx=5, pady=10)
        self.centraliza(self.top_cadastrar)

    def confirmar_cadastro(self):
        nome = self.ent_nome.get()
        cpf = self.ent_cpf.get()
        email = self.ent_email.get()
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
        TelaAdmin(top_admin, self.conn, self.cursor)
        top_admin.protocol("WM_DELETE_WINDOW", lambda: self.fechar_admin(top_admin))
    
    def abrir_tela_cardapio(self, usuario_nome):
        self.janela.withdraw()
        top_cardapio = ttk.Toplevel(self.janela)
        self.tela_cardapio_inst = TelaCardapio(top_cardapio, self.conn, self.cursor, usuario_nome, lambda: self.fechar_tela_cliente(top_cardapio))

    def fechar_admin(self, top_admin):
        top_admin.destroy()
        self.janela.deiconify()
    
    def fechar_tela_cliente(self, top_cardapio):
        if hasattr(self, 'tela_cardapio_inst') and hasattr(self.tela_cardapio_inst, 'carrinho'):
            carrinho = self.tela_cardapio_inst.carrinho
            for prod_id, qtd in carrinho.items():
                if qtd > 0:
                    self.cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id = ?", (qtd, prod_id))
            self.conn.commit()
        top_cardapio.destroy()
        self.janela.deiconify()

    def login(self):
        email = self.ent_usuario.get()
        senha = self.ent_senha.get()

        if email == ADMIN_EMAIL and senha == ADMIN_SENHA:
            messagebox.showinfo("Login", "Bem-vindo, Administrador!")
            self.abrir_tela_admin()
            return

        self.cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        usuario = self.cursor.fetchone()

        if usuario:
            messagebox.showinfo("Login", f"Bem-vindo, {usuario[1]}!")
            self.abrir_tela_cardapio(usuario[1]) 
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

class TelaAdmin:
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Área Administrativa - Usuários Cadastrados")
        self.janela.geometry("700x500")
        
        ttk.Label(self.janela, text="Usuários Cadastrados", font=("Arial", 16, "bold")).pack(pady=10)

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

        frm_botoes_admin = ttk.Frame(self.janela)
        frm_botoes_admin.pack(pady=10)

        btn_excluir = ttk.Button(frm_botoes_admin, text="Excluir Selecionado", bootstyle="danger", command=self.excluir_usuario)
        btn_excluir.pack(side=LEFT, padx=5)

        self.carregar_usuarios()
        self.centraliza(self.janela)

    def excluir_usuario(self):
        item_selecionado = self.tree.selection()
        
        if len(item_selecionado) > 0:
            usuario_id = self.tree.item(item_selecionado, 'values')[0]
            confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir o usuário selecionado?")
            
            if confirmacao:
                self.cursor.execute("DELETE FROM usuarios WHERE id=?", (usuario_id,))
                self.conn.commit()
                self.tree.delete(item_selecionado)
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
        else:
            messagebox.showwarning('Aviso', 'Por favor, selecione um usuário para excluir.')

    def carregar_usuarios(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
            
        try:
            self.cursor.execute("SELECT id, nome, cpf, email FROM usuarios")
            usuarios = self.cursor.fetchall()
            
            for i in usuarios:
                self.tree.insert('', END, values=i)
        except Exception as erro:
            messagebox.showerror("Erro no Banco de Dados", f"Não foi possível carregar os usuários: {erro}")

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
    def __init__(self, master, conn, cursor, usuario_nome, on_close_callback):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.on_close_callback = on_close_callback
        self.janela.title(f"Cardápio - Bem-vindo, {usuario_nome}!")
        self.janela.geometry("800x600")

        self.carrinho = {} 
        self.imagens_produtos = {} 
        
        frm_topo = ttk.Frame(self.janela)
        frm_topo.pack(fill=X, padx=10, pady=10)
        ttk.Label(frm_topo, text="Nosso Cardápio", font=("Arial", 16, "bold")).pack(side=LEFT)
        ttk.Button(frm_topo, text="Ver Carrinho", command=self.abrir_carrinho, bootstyle="info").pack(side=RIGHT)
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
            ttk.Label(frm_produto, image=self.imagens_produtos[produto_id]).pack(side=LEFT, padx=10, pady=10)
        except Exception as e:
            ttk.Label(frm_produto, text="Imagem\nIndisponível", width=12, anchor=CENTER).pack(side=LEFT, padx=10, pady=10)

        frm_info = ttk.Frame(frm_produto)
        frm_info.pack(side=LEFT, fill=X, expand=True, padx=10)
        ttk.Label(frm_info, text=desc, wraplength=400, justify=LEFT).pack(anchor=W)
        ttk.Label(frm_info, text=f"R$ {preco:.2f}").pack(anchor=W, pady=5)
        
        frm_controles = ttk.Frame(frm_produto)
        frm_controles.pack(side=RIGHT, padx=10)
        
        btn_menos = ttk.Button(frm_controles, text="-", bootstyle="danger", command=lambda p=produto_id: self.remover_do_carrinho(p))
        btn_menos.pack()
        
        btn_mais = ttk.Button(frm_controles, text="+", bootstyle="success", command=lambda p=produto_id: self.adicionar_ao_carrinho(p))
        btn_mais.pack(pady=5)
        
        if estoque <= 0:
            btn_mais.config(state=DISABLED)
            ttk.Label(frm_info, text="ESGOTADO", bootstyle="danger").pack(anchor=W, pady=5)

    def adicionar_ao_carrinho(self, produto_id):
        self.cursor.execute("SELECT estoque FROM produtos WHERE id=?", (produto_id,))
        estoque_atual = self.cursor.fetchone()[0]

        if estoque_atual > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque - 1 WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carrinho[produto_id] = self.carrinho.get(produto_id, 0) + 1
            self.carregar_produtos() 
        else:
            messagebox.showwarning("Estoque", "Produto esgotado!")

    def remover_do_carrinho(self, produto_id):
        if produto_id in self.carrinho and self.carrinho[produto_id] > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque + 1 WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carrinho[produto_id] -= 1
            if self.carrinho[produto_id] == 0:
                del self.carrinho[produto_id]
            self.carregar_produtos()
        else:
            messagebox.showwarning("Carrinho", "Este produto não está no seu carrinho.")

    def abrir_carrinho(self):
        if not self.carrinho:
            messagebox.showinfo("Carrinho Vazio", "Seu carrinho está vazio. Adicione produtos primeiro.")
            return
        
        top_carrinho = ttk.Toplevel(self.janela)
        top_carrinho.title("Meu Carrinho")
        TelaCarrinho(top_carrinho, self.conn, self.cursor, self.carrinho, self.carregar_produtos)

class TelaCarrinho:
    def __init__(self, master, conn, cursor, carrinho_ref, refresh_cardapio_callback):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.carrinho = carrinho_ref 
        self.refresh_cardapio = refresh_cardapio_callback
        self.janela.geometry("700x550")
        self.janela.grab_set()

        self.lbl_resumoP = ttk.Label(self.janela, text="Resumo do Pedido", font=("Arial", 16, "bold"))
        self.lbl_resumoP.pack(pady=10)

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
        
        self.lbl_total = ttk.Label(self.janela, text="", font=("Arial", 14, "bold"))
        self.lbl_total.pack(pady=10)
        
        frm_botoes = ttk.Frame(self.janela)
        frm_botoes.pack(pady=10)
        ttk.Button(frm_botoes, text="Realizar Pedido", bootstyle="success", command=self.finalizar_pedido).pack(side=LEFT, padx=5)
        ttk.Button(frm_botoes, text="Voltar", bootstyle="secondary-outline", command=self.janela.destroy).pack(side=LEFT, padx=5)

        self.atualizar_visualizacao_carrinho()

    def atualizar_visualizacao_carrinho(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        total_pedido = 0
        if not self.carrinho:
            ttk.Label(self.scrollable_frame, text="Carrinho Vazio").pack()
        else:
            for produto_id, quantidade in self.carrinho.items():
                self.cursor.execute("SELECT nome, preco FROM produtos WHERE id=?", (produto_id,))
                nome, preco = self.cursor.fetchone()
                subtotal = preco * quantidade
                total_pedido += subtotal
                self.criar_bloco_item_carrinho(produto_id, nome, quantidade, subtotal)
        
        self.lbl_total.config(text=f"Total: R$ {total_pedido:.2f}")

    def criar_bloco_item_carrinho(self, produto_id, nome, quantidade, subtotal):
        frm_item = ttk.Frame(self.scrollable_frame, relief=SOLID, borderwidth=1)
        frm_item.pack(fill=X, padx=5, pady=5)

        info_txt = f"{nome}\nSubtotal: R$ {subtotal:.2f}"
        ttk.Label(frm_item, text=info_txt, justify=LEFT).pack(side=LEFT, expand=True, fill=X, padx=10)
        
        frm_controles = ttk.Frame(frm_item)
        frm_controles.pack(side=RIGHT, padx=10)

        btn_menos = ttk.Button(frm_controles, text="-", width=2, bootstyle="danger", command=lambda: self.diminuir_quantidade(produto_id))
        btn_menos.pack(side=LEFT, padx=2)
        ttk.Label(frm_controles, text=str(quantidade), width=3, anchor=CENTER).pack(side=LEFT)
        btn_mais = ttk.Button(frm_controles, text="+", width=2, bootstyle="success", command=lambda: self.aumentar_quantidade(produto_id))
        btn_mais.pack(side=LEFT, padx=2)
        btn_remover = ttk.Button(frm_controles, text="🗑️", width=2, bootstyle="danger-outline", command=lambda: self.remover_totalmente(produto_id))
        btn_remover.pack(side=LEFT, padx=(10,2))

    def aumentar_quantidade(self, produto_id):
        self.cursor.execute("SELECT estoque FROM produtos WHERE id=?", (produto_id,))
        if self.cursor.fetchone()[0] > 0:
            self.cursor.execute("UPDATE produtos SET estoque = estoque - 1 WHERE id=?", (produto_id,))
            self.conn.commit()
            self.carrinho[produto_id] += 1
            self.atualizar_visualizacao_carrinho()
            self.refresh_cardapio()
        else:
            messagebox.showwarning("Estoque", "Não há mais estoque para este produto.", parent=self.janela)

    def diminuir_quantidade(self, produto_id):
        self.cursor.execute("UPDATE produtos SET estoque = estoque + 1 WHERE id=?", (produto_id,))
        self.conn.commit()
        self.carrinho[produto_id] -= 1
        if self.carrinho[produto_id] == 0:
            del self.carrinho[produto_id]
        self.atualizar_visualizacao_carrinho()
        self.refresh_cardapio()
        if not self.carrinho: 
            self.janela.destroy()

    def remover_totalmente(self, produto_id):
        quantidade_a_devolver = self.carrinho[produto_id]
        self.cursor.execute("UPDATE produtos SET estoque = estoque + ? WHERE id=?", (quantidade_a_devolver, produto_id))
        self.conn.commit()
        del self.carrinho[produto_id]
        self.atualizar_visualizacao_carrinho()
        self.refresh_cardapio()
        if not self.carrinho: self.janela.destroy()

    def finalizar_pedido(self):
        messagebox.showinfo("Pedido Finalizado", "Seu pedido foi realizado com sucesso!")
        self.carrinho.clear()
        self.refresh_cardapio()
        self.janela.destroy()

app = ttk.Window(themename='darkly')
Tela(app)
app.mainloop()