import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
import os

ADMIN_EMAIL = "admin@"
ADMIN_SENHA = "admin123"


class TelaAdmin:
    # (mantive sua TelaAdmin praticamente igual, com opção de excluir)
    def __init__(self, master, conn, cursor):
        self.janela = master
        self.conn = conn
        self.cursor = cursor
        self.janela.title("Área Administrativa - Usuários Cadastrados")
        self.janela.geometry("600x400")

        ttk.Label(self.janela, text="Usuários Cadastrados",
                  font=("Arial", 16, "bold")).pack(pady=10)

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

        btn_excluir = ttk.Button(frm_botoes_admin, text="Excluir Selecionado",
                                 bootstyle="danger", command=self.excluir_usuario)
        btn_excluir.pack(side=LEFT, padx=5)

        self.carregar_usuarios()
        self.centraliza(self.janela)

    def excluir_usuario(self):
        item_selecionado = self.tree.selection()
        if len(item_selecionado) > 0:
            usuario_id = self.tree.item(item_selecionado, 'values')[0]
            confirmacao = messagebox.askyesno(
                "Confirmação", "Tem certeza que deseja excluir o usuário selecionado?")
            if confirmacao:
                self.cursor.execute(
                    "DELETE FROM usuarios WHERE id=?", (usuario_id,))
                self.conn.commit()
                self.tree.delete(item_selecionado)
                messagebox.showinfo("Sucesso", "Usuário excluído com sucesso.")
        else:
            messagebox.showwarning('Aviso', 'Selecione um usuário.')

    def carregar_usuarios(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            self.cursor.execute("SELECT id, nome, cpf, email FROM usuarios")
            usuarios = self.cursor.fetchall()
            for i in usuarios:
                self.tree.insert('', END, values=i)
        except Exception as erro:
            messagebox.showerror("Erro no Banco de Dados",
                                 f"Não foi possível carregar os usuários: {erro}")

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

        # elementos de login
        self.lbl_usuario = ttk.Label(self.janela, text="Email:")
        self.lbl_usuario.grid(column=0, row=0, sticky=W, padx=5, pady=5)

        self.ent_usuario = ttk.Entry(self.janela)
        self.ent_usuario.grid(column=1, row=0, sticky=E, padx=5, pady=5)

        self.lbl_senha = ttk.Label(self.janela, text="Senha:")
        self.lbl_senha.grid(column=0, row=1, sticky=W, padx=5, pady=5)

        self.ent_senha = ttk.Entry(self.janela, show="*")
        self.ent_senha.grid(column=1, row=1, sticky=E, padx=5, pady=5)

        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.grid(column=1, row=2, columnspan=2, pady=5)

        self.btn_login = ttk.Button(
            self.frm_botoes, text="Entrar", bootstyle="primary", command=self.login)
        self.btn_login.pack(side=LEFT, padx=5)

        self.btn_cadastrar = ttk.Button(
            self.frm_botoes, text="Cadastrar", bootstyle="success", command=self.cadastrar)
        self.btn_cadastrar.pack(side=LEFT)

        self.centraliza(self.janela)
        self.conectar_db()

        # estado do cardápio / carrinho
        self.cardapio_win = None
        self.cart = {}  # {produto_id: quantidade}
        self.product_widgets = {}  # {produto_id: {'stock_label':..., 'sel_label':...}}
        self.product_images = {}  # mantém referências PhotoImage

    def conectar_db(self):
        self.conn = sqlite3.connect("usuarios.db")
        self.cursor = self.conn.cursor()

        # tabela usuarios (com UNIQUE)
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS usuarios'
            '('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'nome TEXT NOT NULL,'
            'cpf TEXT NOT NULL UNIQUE,'
            'email TEXT NOT NULL UNIQUE,'
            'senha TEXT NOT NULL'
            ')'
        )
        # tabela produtos
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS produtos ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'nome TEXT NOT NULL,'
            'estoque INTEGER NOT NULL DEFAULT 0,'
            'descricao TEXT,'
            'imagem TEXT'
            ')'
        )
        self.conn.commit()

        # inserir produtos de exemplo se tabela vazia (apenas para teste)
        self.cursor.execute("SELECT COUNT(*) FROM produtos")
        if self.cursor.fetchone()[0] == 0:
            exemplos = [
                ("Combo Maki Mix", 10,
                 "8 peças: variados makis clássicos.", "images/combo1.png"),
                ("Combo Sashimi Premium", 6,
                 "12 fatias de sashimi fresco.", "images/combo2.png"),
                ("Combo Temaki Família", 5,
                 "4 temakis grandes, perfeito para compartilhar.", "images/combo3.png"),
                ("Combo Rolls Especial", 8,
                 "8 peças de rolls especiais com molho.", None)
            ]
            for nome, estoque, desc, img in exemplos:
                self.cursor.execute("INSERT INTO produtos (nome, estoque, descricao, imagem) VALUES (?, ?, ?, ?)",
                                    (nome, estoque, desc, img))
            self.conn.commit()

        # garante admin existe
        self.cursor.execute(
            "SELECT * FROM usuarios WHERE email=?", (ADMIN_EMAIL,))
        if not self.cursor.fetchone():
            try:
                sql_admin = "INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)"
                self.cursor.execute(
                    sql_admin, ["Admin Master", "00000000000", ADMIN_EMAIL, ADMIN_SENHA])
                self.conn.commit()
            except Exception:
                pass

    # ---------- telas de cadastro de usuário (mantidas) ----------
    def cadastrar(self):
        self.top_cadastrar = ttk.Toplevel(self.janela)
        self.top_cadastrar.grab_set()
        self.top_cadastrar.title("Cadastro de Usuário")

        ttk.Label(self.top_cadastrar, text='NOME:').grid(
            row=0, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='CPF:').grid(
            row=1, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='EMAIL:').grid(
            row=2, column=0, padx=5, pady=5, sticky=W)
        ttk.Label(self.top_cadastrar, text='SENHA:').grid(
            row=3, column=0, padx=5, pady=5, sticky=W)

        self.ent_nome = ttk.Entry(self.top_cadastrar)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5)

        self.ent_cpf = ttk.Entry(self.top_cadastrar)
        self.ent_cpf.grid(row=1, column=1, padx=5, pady=5)

        self.ent_email = ttk.Entry(self.top_cadastrar)
        self.ent_email.grid(row=2, column=1, padx=5, pady=5)

        self.ent_senha_cad = ttk.Entry(self.top_cadastrar, show="*")
        self.ent_senha_cad.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(self.top_cadastrar, text='Confirmar Cadastro', bootstyle="success",
                   command=self.confirmar_cadastro).grid(row=4, column=0, columnspan=2, sticky='we', padx=5, pady=10)
        self.centraliza(self.top_cadastrar)

    def confirmar_cadastro(self):
        nome = self.ent_nome.get().strip()
        cpf = self.ent_cpf.get().strip()
        email = self.ent_email.get().strip()
        senha = self.ent_senha_cad.get().strip()

        if nome == '' or cpf == '' or email == '' or senha == '':
            messagebox.showwarning(
                'Aviso', 'Todos os campos são obrigatórios.', parent=self.top_cadastrar)
            return
        try:
            sql_novo_usuario = "INSERT INTO usuarios (nome, cpf, email, senha) VALUES (?, ?, ?, ?)"
            self.cursor.execute(sql_novo_usuario, [nome, cpf, email, senha])
            self.conn.commit()
            messagebox.showinfo(
                'Sucesso', f'Cadastro realizado com sucesso!\n\nNome: {nome}\nEmail: {email}')
            self.top_cadastrar.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Erro", "CPF ou Email já cadastrados!", parent=self.top_cadastrar)

    # ---------- login ----------
    def abrir_tela_admin(self):
        self.janela.withdraw()
        top_admin = ttk.Toplevel(self.janela)
        TelaAdmin(top_admin, self.conn, self.cursor)
        top_admin.protocol("WM_DELETE_WINDOW",
                           lambda: self.fechar_admin(top_admin))

    def fechar_admin(self, top_admin):
        top_admin.destroy()
        self.janela.deiconify()

    def login(self):
        email = self.ent_usuario.get().strip()
        senha = self.ent_senha.get().strip()

        # admin
        if email == ADMIN_EMAIL and senha == ADMIN_SENHA:
            messagebox.showinfo("Login", "Bem-vindo, Administrador!")
            self.abrir_tela_admin()
            return

        # usuário comum
        self.cursor.execute(
            "SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        usuario = self.cursor.fetchone()
        if usuario:
            messagebox.showinfo("Login", f"Bem-vindo, {usuario[1]}!")
            # abre cardápio para o cliente
            self.janela.withdraw()  # esconde tela de login
            self.abrir_cardapio()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    # ---------- CARDÁPIO ----------
    def abrir_cardapio(self):
        # cria janela do cardápio
        self.cardapio_win = ttk.Toplevel(self.janela)
        self.cardapio_win.title("Cardápio - Combos")
        self.cardapio_win.geometry("900x600")

        # cabeçalho com botão Carrinho
        header = ttk.Frame(self.cardapio_win)
        header.pack(fill='x', padx=10, pady=6)
        ttk.Label(header, text="Cardápio de Combos",
                  font=("Arial", 16, "bold")).pack(side=LEFT)
        self.btn_carrinho = ttk.Button(
            header, text="Carrinho (0)", bootstyle="info", command=self.abrir_carrinho)
        self.btn_carrinho.pack(side=RIGHT)

        # área rolável para produtos (canvas + scrollbar)
        container = ttk.Frame(self.cardapio_win)
        container.pack(fill='both', expand=True, padx=10, pady=6)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(
            container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame_id = canvas.create_window(
            (0, 0), window=scrollable_frame, anchor="nw")

        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scrollable_frame.bind("<Configure>", _on_frame_configure)

        canvas.pack(side=LEFT, fill='both', expand=True)
        scrollbar.pack(side=RIGHT, fill='y')

        # carrega produtos e monta blocos
        produtos = self.cursor.execute(
            "SELECT id, nome, estoque, descricao, imagem FROM produtos").fetchall()

        cols = 3
        padx = 12
        pady = 12
        for idx, (pid, nome, estoque, descricao, imagem) in enumerate(produtos):
            r = idx // cols
            c = idx % cols
            bloco = ttk.Frame(scrollable_frame, width=260,
                              height=220, relief='ridge', padding=6)
            bloco.grid(row=r, column=c, padx=padx, pady=pady, sticky="n")
            # imagem (tenta carregar)
            img_label = ttk.Label(bloco)
            img_label.pack(anchor='n')
            if imagem and os.path.exists(imagem):
                try:
                    img_obj = tk.PhotoImage(file=imagem)
                    # redimensionamento simples não suportado por PhotoImage; assume imagens em tamanho adequado
                    img_label.config(image=img_obj)
                    self.product_images[pid] = img_obj  # manter referência
                except Exception:
                    img_label.config(text="[imagem inválida]")
            else:
                # placeholder (quadrado)
                placeholder = ttk.Frame(
                    bloco, width=180, height=90, relief='sunken')
                placeholder.pack()
                ttk.Label(placeholder, text="Imagem\n(sem arquivo)", anchor='center').place(
                    relx=0.5, rely=0.5, anchor='center')

            # nome + descrição
            ttk.Label(bloco, text=nome, font=("Arial", 11, "bold")
                      ).pack(anchor='w', pady=(6, 0))
            ttk.Label(bloco, text=descricao or "", font=(
                "Arial", 9), wraplength=240).pack(anchor='w')

            # estoque e seleção
            stock_label = ttk.Label(bloco, text=f"Estoque: {estoque}")
            stock_label.pack(anchor='w', pady=(6, 0))
            sel_label = ttk.Label(bloco, text=str(self.cart.get(pid, 0)))
            sel_label.pack(anchor='w')

            # botões + / -
            btn_frame = ttk.Frame(bloco)
            btn_frame.pack(anchor='center', pady=6)
            btn_add = ttk.Button(btn_frame, text="+", bootstyle="success",
                                 command=lambda pid=pid, sl=stock_label, el=sel_label: self.add_to_cart(pid, sl, el))
            btn_add.pack(side=LEFT, padx=4)
            btn_rem = ttk.Button(btn_frame, text="-", bootstyle="danger",
                                 command=lambda pid=pid, sl=stock_label, el=sel_label: self.remove_from_cart(pid, sl, el))
            btn_rem.pack(side=LEFT, padx=4)

            # guarda widgets para atualizar posteriormente
            self.product_widgets[pid] = {
                'stock_label': stock_label, 'sel_label': sel_label}

        # botão voltar
        footer = ttk.Frame(self.cardapio_win)
        footer.pack(fill='x', padx=10, pady=6)
        ttk.Button(footer, text="Voltar", bootstyle="secondary",
                   command=self.fechar_cardapio).pack(side=LEFT)
        # ajustar scroll inicial
        self.cardapio_win.update_idletasks()
        canvas.yview_moveto(0)

    def fechar_cardapio(self):
        if self.cardapio_win:
            self.cardapio_win.destroy()
            self.cardapio_win = None
        self.janela.deiconify()

    def add_to_cart(self, produto_id, stock_label, sel_label):
        # verifica estoque atual no banco
        self.cursor.execute(
            "SELECT estoque FROM produtos WHERE id=?", (produto_id,))
        row = self.cursor.fetchone()
        if not row:
            return
        estoque_atual = row[0]
        if estoque_atual <= 0:
            messagebox.showwarning(
                "Sem estoque", "Este produto está sem estoque no momento.")
            return
        # atualiza DB: decrementa
        novo_estoque = estoque_atual - 1
        self.cursor.execute(
            "UPDATE produtos SET estoque=? WHERE id=?", (novo_estoque, produto_id))
        self.conn.commit()
        # atualiza cart em memória
        self.cart[produto_id] = self.cart.get(produto_id, 0) + 1
        # atualiza labels
        stock_label.config(text=f"Estoque: {novo_estoque}")
        sel_label.config(text=str(self.cart.get(produto_id, 0)))
        self.update_cart_button()

    def remove_from_cart(self, produto_id, stock_label, sel_label):
        qtd_no_carrinho = self.cart.get(produto_id, 0)
        if qtd_no_carrinho <= 0:
            # nada para remover
            return
        # recupera estoque atual
        self.cursor.execute(
            "SELECT estoque FROM produtos WHERE id=?", (produto_id,))
        row = self.cursor.fetchone()
        estoque_atual = row[0] if row else 0
        novo_estoque = estoque_atual + 1
        # atualiza DB: incrementa
        self.cursor.execute(
            "UPDATE produtos SET estoque=? WHERE id=?", (novo_estoque, produto_id))
        self.conn.commit()
        # atualiza cart
        if self.cart[produto_id] == 1:
            del self.cart[produto_id]
            sel = 0
        else:
            self.cart[produto_id] -= 1
            sel = self.cart[produto_id]
        # atualiza labels
        stock_label.config(text=f"Estoque: {novo_estoque}")
        sel_label.config(text=str(sel))
        self.update_cart_button()

    def update_cart_button(self):
        total_items = sum(self.cart.values())
        if hasattr(self, 'btn_carrinho'):
            self.btn_carrinho.config(text=f"Carrinho ({total_items})")

    # ---------- janela carrinho ----------
    def abrir_carrinho(self):
        top = ttk.Toplevel(self.cardapio_win)
        top.title("Carrinho")
        top.geometry("500x400")

        cols = ('Produto', 'Quantidade')
        tree = ttk.Treeview(top, columns=cols, show='headings')
        for c in cols:
            tree.heading(c, text=c)
        tree.pack(fill='both', expand=True, padx=8, pady=8)

        # preencher tree com cart
        for pid, qty in self.cart.items():
            self.cursor.execute("SELECT nome FROM produtos WHERE id=?", (pid,))
            nome = self.cursor.fetchone()[0]
            tree.insert('', END, iid=str(pid), values=(nome, qty))

        frm_botoes = ttk.Frame(top)
        frm_botoes.pack(fill='x', padx=8, pady=6)
        btn_remover = ttk.Button(frm_botoes, text="Remover Selecionado", bootstyle="danger",
                                 command=lambda: self.remover_selecionado_do_carrinho(tree, top))
        btn_remover.pack(side=LEFT, padx=4)

        btn_fechar = ttk.Button(frm_botoes, text="Fechar",
                                bootstyle="secondary", command=top.destroy)
        btn_fechar.pack(side=RIGHT, padx=4)

    def remover_selecionado_do_carrinho(self, tree, top_cart):
        selecionados = tree.selection()
        if not selecionados:
            messagebox.showwarning(
                "Aviso", "Selecione um item para remover.", parent=top_cart)
            return
        confirm = messagebox.askyesno(
            "Remover", "Remover os itens selecionados do carrinho? (Isso devolverá o estoque)")
        if not confirm:
            return
        for iid in selecionados:
            pid = int(iid)
            qty = self.cart.get(pid, 0)
            # atualiza estoque no DB somando qty
            self.cursor.execute(
                "SELECT estoque FROM produtos WHERE id=?", (pid,))
            row = self.cursor.fetchone()
            estoque_atual = row[0] if row else 0
            novo_estoque = estoque_atual + qty
            self.cursor.execute(
                "UPDATE produtos SET estoque=? WHERE id=?", (novo_estoque, pid))
            self.conn.commit()
            # remove do cart
            if pid in self.cart:
                del self.cart[pid]
        # atualiza interface do cardápio (rótulos)
        for pid, widgets in self.product_widgets.items():
            self.cursor.execute(
                "SELECT estoque FROM produtos WHERE id=?", (pid,))
            row = self.cursor.fetchone()
            estoque_atual = row[0] if row else 0
            widgets['stock_label'].config(text=f"Estoque: {estoque_atual}")
            widgets['sel_label'].config(text=str(self.cart.get(pid, 0)))
        # re-preenche tree (ou fecha)
        tree_items = tree.get_children()
        for it in tree_items:
            tree.delete(it)
        for pid, qty in self.cart.items():
            self.cursor.execute("SELECT nome FROM produtos WHERE id=?", (pid,))
            nome = self.cursor.fetchone()[0]
            tree.insert('', END, iid=str(pid), values=(nome, qty))
        self.update_cart_button()

    # ---------- util ----------
    def centraliza(self, master):
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')


# ---- EXECUÇÃO ----
app = ttk.Window(themename='darkly')
Tela(app)
app.mainloop()
