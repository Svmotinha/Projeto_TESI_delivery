import tkinter as tk
from tkinter import messagebox, ttk
import random
import datetime
# É necessário ter a biblioteca Pillow instalada: pip install Pillow
from PIL import Image, ImageTk

# --- 1. CLASSES DE DADOS (Baseado no Diagrama de Classes) ---
# Estas classes servem para armazenar os dados da aplicação de forma organizada.

class Cliente:
    def __init__(self, email, senha, nome, localizacao, cpf):
        self.email = email
        self.senha = senha
        self.nome = nome
        self.localizacao = localizacao
        self.cpf = cpf

class Funcionario:
    def __init__(self, usuario, senha, nome, cargo):
        self.usuario = usuario
        self.senha = senha
        self.nome = nome
        self.cargo = cargo

class Produto:
    def __init__(self, id_produto, nome, preco, descricao, categoria, tempo_preparo_base):
        self.id_cardapio = id_produto
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
        self.categoria = categoria
        self.tempo_preparo_base = tempo_preparo_base # Tempo em segundos

class Pedido:
    def __init__(self, cliente, itens, valor_total, endereco_entrega):
        self.id_pedido = random.randint(1000, 9999)
        self.cliente = cliente
        self.itens = itens # Dicionário {produto: quantidade}
        self.valor_total = valor_total
        self.endereco_entrega = endereco_entrega
        self.status = "Em preparo" # Status inicial do pedido
        self.data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

# --- 2. CLASSE PRINCIPAL DA APLICAÇÃO (CONTROLADOR) ---
# Esta classe gerencia todas as telas e os dados compartilhados.

class SistemaDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()

        # --- DADOS MOCADOS (Simulando um banco de dados) ---
        self.clientes_cadastrados = [
            Cliente("cliente@email.com", "123", "João Silva", "Rua das Flores, 123", "111.222.333-44")
        ]
        self.funcionarios_cadastrados = [
            Funcionario("admin", "admin", "Akira", "Gerente")
        ]
        self.cardapio = [
            # Hot Roll (Tempo: 10-12 min)
            Produto("C01", "Combo Hot Philadelphia", 45.90, "10 Hot Rolls Philadelphia + 1 Refri Lata", "Hot Roll", 600),
            Produto("C07", "Combo Hot Salmão Grelhado", 48.90, "10 Hot Rolls com salmão grelhado e tarê", "Hot Roll", 660),

            # Temakis (Tempo: 8-9 min)
            Produto("C02", "Combo Super Temaki", 55.00, "2 Temakis Salmão completo + 1 porção de sunomono", "Temakis", 480),
            Produto("C08", "Combo Temaki Misto", 57.00, "1 Temaki Salmão + 1 Temaki Califórnia", "Temakis", 500),

            # Yakisobas (Tempo: 15-17 min)
            Produto("C03", "Combo Yakisoba Casal", 65.50, "2 Yakisobas (Frango ou Carne) + 2 Rolinhos Primavera", "Yakisobas", 900),
            Produto("C09", "Combo Yakisoba Família", 110.00, "4 Yakisobas (Frango ou Carne)", "Yakisobas", 1000),

            # Sashimis (Tempo: 5-6 min)
            Produto("C04", "Combo Sashimi Mix", 75.00, "15 fatias de sashimi (Salmão, Atum, Peixe Branco)", "Sashimis", 300),
            Produto("C10", "Combo Sashimi Salmão", 80.00, "20 fatias de sashimi de Salmão premium", "Sashimis", 320),

            # Uramakis (Tempo: 12-13 min)
            Produto("C05", "Combo Uramaki Especial", 49.90, "10 Uramakis Califórnia + 10 Uramakis Skin", "Uramakis", 720),
            Produto("C11", "Combo Uramaki Philadelphia", 52.90, "20 Uramakis Philadelphia", "Uramakis", 750),

            # Pokes (Tempo: 7-8 min)
            Produto("C06", "Combo Poke Fit", 42.00, "1 Poke de Salmão com base de arroz + 1 Suco Natural", "Pokes", 420),
            Produto("C12", "Combo Poke Atum", 44.00, "1 Poke de Atum com molho especial + 1 Refri Lata", "Pokes", 450),
        ]
        
        self.cliente_logado = None
        self.carrinho_atual = {} 
        self.pedidos_registrados = []
        
        # Cores
        self.cor_fundo = "#BFBFBF"
        self.cor_botao = "#F2884B"
        
        # Carregar a imagem do logo
        self.logo_image = None
        try:
            # Caminho absoluto para a imagem do logo
            caminho_logo = r"C:\Users\Samuel Mota\OneDrive\Documentos\UFAC\materias_BSI\TESI.py\imagem_sushi.jpg"
            img = Image.open(caminho_logo)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print(f"Aviso: Arquivo de logo não encontrado no caminho: {caminho_logo}. O logo não será exibido.")
        except Exception as e:
            print(f"Erro ao carregar o logo: {e}. Verifique se a biblioteca Pillow está instalada.")
        
        # Carregar a imagem do cardápio
        self.cardapio_image = None
        try:
            caminho_cardapio_img = "imageem_sushi.png"
            img_cardapio = Image.open(caminho_cardapio_img)
            img_cardapio = img_cardapio.resize((780, 200), Image.Resampling.LANCZOS) 
            self.cardapio_image = ImageTk.PhotoImage(img_cardapio)
        except FileNotFoundError:
            print(f"Aviso: Arquivo '{caminho_cardapio_img}' não encontrado. A imagem do cardápio não será exibida.")
        except Exception as e:
            print(f"Erro ao carregar a imagem do cardápio: {e}.")

        self.mostrar_tela_login()

    def centralizar_janela(self, janela, largura, altura):
        """Centraliza uma janela na tela do monitor."""
        largura_tela = janela.winfo_screenwidth()
        altura_tela = janela.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        janela.geometry(f'{largura}x{altura}+{x}+{y}')

    def mostrar_tela_login(self):
        self.root.withdraw()
        TelaLogin(self)
    
    def mostrar_tela_cadastro(self):
        TelaCadastro(self)

    def login_cliente_sucesso(self, cliente):
        self.cliente_logado = cliente
        self.tela_principal_cliente = TelaPrincipalCliente(self)

    def login_funcionario_sucesso(self, funcionario):
        TelaFuncionario(self)
        
    def logout(self):
        self.cliente_logado = None
        self.carrinho_atual = {}
        if hasattr(self, 'tela_principal_cliente') and self.tela_principal_cliente.janela.winfo_exists():
            self.tela_principal_cliente.janela.destroy()
        self.mostrar_tela_login()
        
    def adicionar_ao_carrinho(self, produto):
        if produto in self.carrinho_atual:
            self.carrinho_atual[produto] += 1
        else:
            self.carrinho_atual[produto] = 1
        messagebox.showinfo("Sucesso", f"'{produto.nome}' adicionado ao carrinho!")
        
    def registrar_novo_pedido(self, endereco, metodo_pagamento):
        valor_total = sum(p.preco * q for p, q in self.carrinho_atual.items())
        novo_pedido = Pedido(self.cliente_logado, self.carrinho_atual.copy(), valor_total, endereco)
        self.pedidos_registrados.append(novo_pedido)
        
        self.carrinho_atual.clear()
        return novo_pedido

    def calcular_tempo_preparo_total(self, itens_carrinho):
        if not itens_carrinho:
            return 0

        tarefas_preparo = []
        for produto, quantidade in itens_carrinho.items():
            num_grupos = (quantidade + 4) // 5
            for _ in range(num_grupos):
                tarefas_preparo.append(produto.tempo_preparo_base)

        tarefas_preparo.sort(reverse=True)

        tempo_total = 0
        for i in range(0, len(tarefas_preparo), 3):
            grupo_tarefas = tarefas_preparo[i:i+3]
            if grupo_tarefas:
                tempo_total += grupo_tarefas[0]
        
        return tempo_total

# --- 3. CLASSES DAS TELAS (INTERFACES GRÁFICAS) ---

class TelaLogin:
    def __init__(self, app_master):
        self.app = app_master
        self.janela = tk.Toplevel(self.app.root)
        self.janela.title("Login")
        self.janela.config(bg=self.app.cor_fundo)
        self.app.centralizar_janela(self.janela, 350, 400) # Altura ajustada para o logo

        # Exibir o logo se ele foi carregado
        if self.app.logo_image:
            logo_label = tk.Label(self.janela, image=self.app.logo_image, bg=self.app.cor_fundo)
            logo_label.pack(pady=10)

        tk.Label(self.janela, text="Usuário (email ou 'admin'):", bg=self.app.cor_fundo).pack(pady=(10,0))
        self.entry_usuario = tk.Entry(self.janela, width=30)
        self.entry_usuario.pack()

        tk.Label(self.janela, text="Senha:", bg=self.app.cor_fundo).pack(pady=(10,0))
        self.entry_senha = tk.Entry(self.janela, show="*", width=30)
        self.entry_senha.pack()
        
        self.frame_botoes = tk.Frame(self.janela, bg=self.app.cor_fundo)
        self.frame_botoes.pack(pady=20)

        btn_login = tk.Button(self.frame_botoes, text="Login", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2, activebackground=self.app.cor_botao, activeforeground="black")
        btn_login.bind("<Button-1>", self.validar_login)
        btn_login.pack(side=tk.LEFT, padx=5)
        
        self.btn_cadastro = tk.Button(self.frame_botoes, text="Cadastrar-se", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2, activebackground=self.app.cor_botao, activeforeground="black")
        self.btn_cadastro.bind("<Button-1>", self.abrir_cadastro)
        
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_app)
        self.entry_usuario.focus_force()

    def validar_login(self, event):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        for cliente in self.app.clientes_cadastrados:
            if cliente.email == usuario and cliente.senha == senha:
                self.janela.destroy()
                self.app.login_cliente_sucesso(cliente)
                return

        for funcionario in self.app.funcionarios_cadastrados:
            if funcionario.usuario == usuario and funcionario.senha == senha:
                self.janela.destroy()
                self.app.login_funcionario_sucesso(funcionario)
                return
        
        messagebox.showerror("Erro de Login", "Credenciais inválidas. Se não tiver conta, cadastre-se.")
        self.btn_cadastro.pack(side=tk.LEFT, padx=5)
    
    def abrir_cadastro(self, event):
        self.janela.destroy()
        self.app.mostrar_tela_cadastro()

    def fechar_app(self):
        self.app.root.destroy()

class TelaCadastro:
    def __init__(self, app_master):
        self.app = app_master
        self.janela = tk.Toplevel(self.app.root)
        self.janela.title("Cadastro de Novo Cliente")
        self.janela.config(bg=self.app.cor_fundo)
        self.app.centralizar_janela(self.janela, 400, 300)

        frame_form = tk.Frame(self.janela, bg=self.app.cor_fundo)
        frame_form.pack(pady=15, padx=15)

        labels = ["Nome Completo:", "Email:", "Senha:", "Endereço:", "CPF:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(frame_form, text=label_text, bg=self.app.cor_fundo)
            label.grid(row=i, column=0, sticky="w", pady=2, padx=5)
            entry = tk.Entry(frame_form, width=40, show="*" if label_text == "Senha:" else "")
            entry.grid(row=i, column=1, pady=2, padx=5)
            self.entries[label_text] = entry
        
        btn_confirmar = tk.Button(self.janela, text="Confirmar Cadastro", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2)
        btn_confirmar.bind("<Button-1>", self.realizar_cadastro)
        btn_confirmar.pack(pady=10)

        btn_voltar = tk.Button(self.janela, text="Voltar para Login", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2)
        btn_voltar.bind("<Button-1>", self.voltar_login)
        btn_voltar.pack(pady=5)

    def realizar_cadastro(self, event):
        nome = self.entries["Nome Completo:"].get()
        email = self.entries["Email:"].get()
        senha = self.entries["Senha:"].get()
        localizacao = self.entries["Endereço:"].get()
        cpf = self.entries["CPF:"].get()

        if not all([nome, email, senha, localizacao, cpf]):
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios.")
            return
        
        novo_cliente = Cliente(email, senha, nome, localizacao, cpf)
        self.app.clientes_cadastrados.append(novo_cliente)
        
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso! Faça o login agora.")
        self.voltar_login(None)

    def voltar_login(self, event):
        self.janela.destroy()
        self.app.mostrar_tela_login()

class TelaPrincipalCliente:
    def __init__(self, app_master):
        self.app = app_master
        self.janela = tk.Toplevel(self.app.root)
        self.janela.title(f"Cardápio - Bem-vindo, {self.app.cliente_logado.nome}!")
        self.janela.config(bg=self.app.cor_fundo)
        self.app.centralizar_janela(self.janela, 800, 850) # Altura aumentada

        # Adicionar a imagem do cardápio se ela existir
        if self.app.cardapio_image:
            cardapio_img_label = tk.Label(self.janela, image=self.app.cardapio_image, bg=self.app.cor_fundo)
            cardapio_img_label.pack(pady=(10, 0))

        frame_acoes = tk.Frame(self.janela, bg=self.app.cor_fundo)
        frame_acoes.pack(pady=10, fill=tk.X, padx=10)
        
        btn_carrinho = tk.Button(frame_acoes, text="Ver Carrinho", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2)
        btn_carrinho.bind("<Button-1>", self.mostrar_carrinho)
        btn_carrinho.pack(side=tk.LEFT)

        btn_logout = tk.Button(frame_acoes, text="Logout", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2)
        btn_logout.bind("<Button-1>", self.fazer_logout)
        btn_logout.pack(side=tk.RIGHT)

        frame_principal_cardapio = tk.Frame(self.janela, bg=self.app.cor_fundo)
        frame_principal_cardapio.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        categorias = sorted(list(set(p.categoria for p in self.app.cardapio)))
        
        col, row = 0, 0
        for i, categoria in enumerate(categorias):
            frame_categoria = tk.LabelFrame(frame_principal_cardapio, text=categoria, font=("Arial", 12, "bold"), padx=10, pady=10, bg=self.app.cor_fundo, borderwidth=1, relief=tk.SOLID)
            frame_categoria.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

            frame_principal_cardapio.grid_columnconfigure(col, weight=1)
            frame_principal_cardapio.grid_rowconfigure(row, weight=1)

            produtos_da_categoria = [p for p in self.app.cardapio if p.categoria == categoria]
            
            for produto in produtos_da_categoria:
                frame_produto = tk.Frame(frame_categoria, bg=self.app.cor_fundo)
                info = f"{produto.nome}\nR$ {produto.preco:.2f}"
                tk.Label(frame_produto, text=info, justify=tk.LEFT, bg=self.app.cor_fundo).pack(anchor="w")
                
                btn_add = tk.Button(frame_produto, text="Adicionar", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2)
                btn_add.bind("<Button-1>", lambda event, p=produto: self.app.adicionar_ao_carrinho(p))
                btn_add.pack(anchor="e", pady=5)
                frame_produto.pack(fill=tk.X, pady=5)
            
            col += 1
            if col > 1: # 2 colunas
                col = 0
                row += 1

        self.janela.protocol("WM_DELETE_WINDOW", self.fazer_logout)
    
    def mostrar_carrinho(self, event):
        TelaCarrinho(self.app)

    def fazer_logout(self, event):
        self.janela.destroy()
        self.app.logout()

class TelaCarrinho:
    def __init__(self, app_master):
        self.app = app_master
        self.janela = tk.Toplevel(self.app.root)
        self.janela.title("Meu Carrinho de Compras")
        self.janela.config(bg=self.app.cor_fundo)
        self.app.centralizar_janela(self.janela, 550, 450)
        
        # --- Estrutura com Canvas para Scroll ---
        container = tk.Frame(self.janela, bg=self.app.cor_fundo)
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(container, bg=self.app.cor_fundo, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=self.app.cor_fundo)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Fim da Estrutura com Scroll ---

        self.label_total = tk.Label(self.janela, text="", font=("Arial", 12, "bold"), bg=self.app.cor_fundo)
        self.label_total.pack(pady=10)

        frame_botoes = tk.Frame(self.janela, bg=self.app.cor_fundo)
        frame_botoes.pack(pady=(0, 10))
        
        self.btn_concluir = tk.Button(frame_botoes, text="Concluir Pedido", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2)
        self.btn_concluir.bind("<Button-1>", self.concluir_pedido)
        self.btn_concluir.pack(side=tk.LEFT, padx=5)
        
        self.atualizar_lista_carrinho()
        
    def atualizar_lista_carrinho(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.app.carrinho_atual:
            tk.Label(self.scrollable_frame, text="Seu carrinho está vazio.", bg=self.app.cor_fundo, font=("Arial", 12)).pack(pady=20)
            self.valor_total = 0.0
            self.btn_concluir.config(state=tk.DISABLED)
        else:
            self.valor_total = 0.0
            for produto, quantidade in self.app.carrinho_atual.items():
                self.criar_bloco_item(produto, quantidade)
                self.valor_total += produto.preco * quantidade
            
            self.btn_concluir.config(state=tk.NORMAL)
        
        self.label_total.config(text=f"Total do Pedido: R$ {self.valor_total:.2f}")

    def criar_bloco_item(self, produto, quantidade):
        item_frame = tk.Frame(self.scrollable_frame, bg=self.app.cor_fundo, relief=tk.SOLID, borderwidth=1)
        item_frame.pack(fill=tk.X, pady=5, padx=5)

        # Informações do produto
        info_frame = tk.Frame(item_frame, bg=self.app.cor_fundo)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        nome_produto = tk.Label(info_frame, text=produto.nome, font=("Arial", 10, "bold"), bg=self.app.cor_fundo, wraplength=250, justify=tk.LEFT)
        nome_produto.pack(anchor="w")
        
        subtotal = produto.preco * quantidade
        preco_info = tk.Label(info_frame, text=f"Subtotal: R$ {subtotal:.2f}", bg=self.app.cor_fundo)
        preco_info.pack(anchor="w")

        # Controles de quantidade
        controles_frame = tk.Frame(item_frame, bg=self.app.cor_fundo)
        controles_frame.pack(side=tk.RIGHT, padx=5, pady=5)
        
        btn_menos = tk.Button(controles_frame, text="-", width=2, bg=self.app.cor_botao, fg="black", relief=tk.RAISED)
        btn_menos.bind("<Button-1>", lambda e, p=produto: self.diminuir_quantidade(p))
        btn_menos.pack(side=tk.LEFT)

        label_qtd = tk.Label(controles_frame, text=str(quantidade), font=("Arial", 10, "bold"), width=4, bg=self.app.cor_fundo)
        label_qtd.pack(side=tk.LEFT, padx=5)
        
        btn_mais = tk.Button(controles_frame, text="+", width=2, bg=self.app.cor_botao, fg="black", relief=tk.RAISED)
        btn_mais.bind("<Button-1>", lambda e, p=produto: self.aumentar_quantidade(p))
        btn_mais.pack(side=tk.LEFT)

        btn_remover_item = tk.Button(controles_frame, text="Remover", bg="#ff6666", fg="black", relief=tk.RAISED, borderwidth=1)
        btn_remover_item.bind("<Button-1>", lambda e, p=produto: self.remover_item_total(p))
        btn_remover_item.pack(side=tk.LEFT, padx=(10, 0))

    def aumentar_quantidade(self, produto):
        self.app.carrinho_atual[produto] += 1
        self.atualizar_lista_carrinho()

    def diminuir_quantidade(self, produto):
        if self.app.carrinho_atual[produto] > 1:
            self.app.carrinho_atual[produto] -= 1
        else:
            del self.app.carrinho_atual[produto]
        self.atualizar_lista_carrinho()
    
    def remover_item_total(self, produto):
        del self.app.carrinho_atual[produto]
        self.atualizar_lista_carrinho()

    def concluir_pedido(self, event):
        if not self.app.carrinho_atual:
            messagebox.showwarning("Carrinho Vazio", "Adicione itens ao carrinho.")
            return
        
        self.janela.destroy()
        TelaPagamento(self.app, self.valor_total)

class TelaPagamento:
    def __init__(self, app_master, valor_total):
        self.app = app_master
        self.valor_total = valor_total
        
        self.janela = tk.Toplevel(self.app.root)
        self.janela.title("Finalizar Pedido")
        self.janela.config(bg=self.app.cor_fundo)
        self.app.centralizar_janela(self.janela, 400, 300)
        
        tk.Label(self.janela, text="Resumo do Pedido", font=("Arial", 14, "bold"), bg=self.app.cor_fundo).pack(pady=10)
        tk.Label(self.janela, text=f"Valor Total: R$ {self.valor_total:.2f}", bg=self.app.cor_fundo).pack()
        
        tk.Label(self.janela, text="Endereço de Entrega:", font=("Arial", 10, "bold"), bg=self.app.cor_fundo).pack(pady=(20, 0))
        self.entry_endereco = tk.Entry(self.janela, width=50)
        self.entry_endereco.pack()
        self.entry_endereco.insert(0, self.app.cliente_logado.localizacao)

        tk.Label(self.janela, text="Método de Pagamento:", font=("Arial", 10, "bold"), bg=self.app.cor_fundo).pack(pady=(20, 0))
        
        self.metodo_pagamento = tk.StringVar(value="Cartão de Crédito")
        style_radio = {"bg": self.app.cor_fundo, "activebackground": self.app.cor_fundo, "highlightthickness": 0}
        tk.Radiobutton(self.janela, text="Cartão de Crédito", variable=self.metodo_pagamento, value="Cartão de Crédito", **style_radio).pack(anchor="w", padx=50)
        tk.Radiobutton(self.janela, text="PIX", variable=self.metodo_pagamento, value="PIX", **style_radio).pack(anchor="w", padx=50)
        tk.Radiobutton(self.janela, text="Dinheiro", variable=self.metodo_pagamento, value="Dinheiro", **style_radio).pack(anchor="w", padx=50)

        btn_confirmar = tk.Button(self.janela, text="Confirmar Pedido", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2)
        btn_confirmar.bind("<Button-1>", self.confirmar)
        btn_confirmar.pack(pady=20)

    def confirmar(self, event):
        endereco = self.entry_endereco.get()
        if not endereco:
            messagebox.showerror("Erro", "O endereço de entrega é obrigatório.")
            return
        
        metodo = self.metodo_pagamento.get()
        novo_pedido = self.app.registrar_novo_pedido(endereco, metodo)
        tempo_preparo_calculado = self.app.calcular_tempo_preparo_total(novo_pedido.itens)

        self.janela.destroy()
        TelaStatusPedido(self.app, novo_pedido, tempo_preparo_calculado)

class TelaStatusPedido:
    def __init__(self, app_master, pedido, tempo_preparo_calculado):
        self.app = app_master
        self.pedido = pedido
        self.janela = tk.Toplevel(self.app.root)
        self.janela.title(f"Status do Pedido #{pedido.id_pedido}")
        self.janela.config(bg=self.app.cor_fundo)
        self.app.centralizar_janela(self.janela, 400, 300)
        
        self.tempo_preparo = tempo_preparo_calculado
        self.tempo_entrega = 600 # 10 minutos para demonstração

        tk.Label(self.janela, text=f"Pedido #{pedido.id_pedido}", font=("Arial", 14, "bold"), bg=self.app.cor_fundo).pack(pady=10)
        
        self.label_status = tk.Label(self.janela, text=f"Status: {pedido.status}", font=("Arial", 12), bg=self.app.cor_fundo)
        self.label_status.pack(pady=5)

        self.label_timer_desc = tk.Label(self.janela, text="Tempo restante para preparo:", font=("Arial", 10), bg=self.app.cor_fundo)
        self.label_timer_desc.pack()
        self.label_timer = tk.Label(self.janela, text="", font=("Arial", 18, "bold"), bg=self.app.cor_fundo)
        self.label_timer.pack()
        
        btn_voltar = tk.Button(self.janela, text="Voltar ao Cardápio", bg=self.app.cor_botao, fg="black", relief=tk.RAISED, borderwidth=2)
        btn_voltar.bind("<Button-1>", self.voltar_cardapio)
        btn_voltar.pack(pady=20)
        
        self.janela.protocol("WM_DELETE_WINDOW", lambda: self.voltar_cardapio(None))
        self.atualizar_timer_preparo()

    def atualizar_timer_preparo(self):
        if self.tempo_preparo > 0:
            mins, secs = divmod(self.tempo_preparo, 60)
            self.label_timer.config(text=f"{mins:02d}:{secs:02d}")
            self.tempo_preparo -= 1
            self.janela.after(1000, self.atualizar_timer_preparo)
        else:
            self.pedido.status = "Pronto para entrega"
            if self.janela.winfo_exists():
                self.label_status.config(text=f"Status: {self.pedido.status}")
                self.label_timer_desc.config(text="Tempo estimado de entrega:")
                self.atualizar_timer_entrega()

    def atualizar_timer_entrega(self):
        if self.tempo_entrega > 0:
            mins, secs = divmod(self.tempo_entrega, 60)
            if self.janela.winfo_exists():
                self.label_timer.config(text=f"{mins:02d}:{secs:02d}")
            self.tempo_entrega -= 1
            self.janela.after(1000, self.atualizar_timer_entrega)
        else:
            self.pedido.status = "Entregue"
            if self.janela.winfo_exists():
                self.label_status.config(text=f"Status: {self.pedido.status}")
                self.label_timer_desc.config(text="")
                self.label_timer.config(text="Pedido Entregue!")

    def voltar_cardapio(self, event):
        self.janela.destroy()

class TelaFuncionario:
    def __init__(self, app_master):
        self.app = app_master
        self.janela = tk.Toplevel(self.app.root)
        self.janela.title("Painel do Funcionário - Gerenciar Pedidos")
        self.janela.config(bg=self.app.cor_fundo)
        self.app.centralizar_janela(self.janela, 850, 500)

        tk.Label(self.janela, text="Pedidos Recebidos", font=("Arial", 16, "bold"), bg=self.app.cor_fundo).pack(pady=10)

        style = ttk.Style(self.janela)
        style.theme_use("default")
        style.configure("Treeview", background="white", fieldbackground="white", foreground="black")
        style.map('Treeview', background=[('selected', self.app.cor_botao)])

        colunas = ("id", "cliente", "valor", "endereco", "status", "data")
        self.tree = ttk.Treeview(self.janela, columns=colunas, show='headings')
        self.tree.heading("id", text="Pedido #"); self.tree.heading("cliente", text="Cliente")
        self.tree.heading("valor", text="Valor Total"); self.tree.heading("endereco", text="Endereço")
        self.tree.heading("status", text="Status"); self.tree.heading("data", text="Data/Hora")
        self.tree.column("id", width=80, anchor=tk.CENTER); self.tree.column("valor", width=100, anchor=tk.E)
        self.tree.column("status", width=140, anchor=tk.CENTER); self.tree.column("endereco", width=200)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        frame_botoes = tk.Frame(self.janela, bg=self.app.cor_fundo)
        frame_botoes.pack(pady=10)
        
        btn_style = {"bg": self.app.cor_botao, "fg": "black", "relief": tk.RAISED, "borderwidth": 2}
        btn_update = tk.Button(frame_botoes, text="Atualizar Lista", **btn_style)
        btn_update.bind("<Button-1>", self.atualizar_pedidos)
        btn_update.pack(side=tk.LEFT, padx=5)

        btn_pronto = tk.Button(frame_botoes, text="Marcar como 'Pronto p/ Entrega'", **btn_style)
        btn_pronto.bind("<Button-1>", lambda e: self.mudar_status("Pronto para entrega"))
        btn_pronto.pack(side=tk.LEFT, padx=5)
        
        btn_entregue = tk.Button(frame_botoes, text="Marcar como 'Entregue'", **btn_style)
        btn_entregue.bind("<Button-1>", lambda e: self.mudar_status("Entregue"))
        btn_entregue.pack(side=tk.LEFT, padx=5)
        
        btn_logout = tk.Button(frame_botoes, text="Logout", **btn_style)
        btn_logout.bind("<Button-1>", self.fazer_logout)
        btn_logout.pack(side=tk.RIGHT, padx=20)

        self.atualizar_pedidos(None)
        self.janela.protocol("WM_DELETE_WINDOW", lambda: self.fazer_logout(None))

    def atualizar_pedidos(self, event):
        self.tree.delete(*self.tree.get_children())
        for pedido in self.app.pedidos_registrados:
            valor_str = f"R$ {pedido.valor_total:.2f}"
            self.tree.insert("", tk.END, iid=pedido.id_pedido, values=(
                pedido.id_pedido, pedido.cliente.nome, valor_str,
                pedido.endereco_entrega, pedido.status, pedido.data_hora
            ))
            
    def mudar_status(self, novo_status):
        selecionado = self.tree.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para alterar o status.")
            return
        
        id_pedido = int(selecionado)
        for pedido in self.app.pedidos_registrados:
            if pedido.id_pedido == id_pedido:
                pedido.status = novo_status
                break
        self.atualizar_pedidos(None)

    def fazer_logout(self, event):
        self.janela.destroy()
        self.app.mostrar_tela_login()

# --- 4. INICIALIZAÇÃO DA APLICAÇÃO ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaDeliveryApp(root)
    root.mainloop()