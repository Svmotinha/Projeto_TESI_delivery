import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("500x300")
        self.janela.title('Tela de Login')

        # Centraliza os widgets na janela
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_columnconfigure(1, weight=1)

        self.lbl_usuario = ttk.Label(self.janela, text="Usuário:")
        self.lbl_usuario.grid(column=0, row=0, sticky=W, padx=10, pady=10)

        self.ent_usuario = ttk.Entry(self.janela, width=30)
        self.ent_usuario.grid(column=1, row=0, sticky=E, padx=10, pady=10)

        self.lbl_senha = ttk.Label(self.janela, text="Senha:")
        self.lbl_senha.grid(column=0, row=1, sticky=W, padx=10, pady=10)

        self.ent_senha = ttk.Entry(self.janela, show="*", width=30)
        self.ent_senha.grid(column=1, row=1, sticky=E, padx=10, pady=10)

        # Cria um Frame para agrupar os botões
        self.frm_botoes = ttk.Frame(self.janela)
        self.frm_botoes.grid(column=1, row=2, sticky=E, pady=10, padx=10)

        # Botão de Login dentro do Frame
        self.btn_login = ttk.Button(self.frm_botoes, text="Entrar", bootstyle="primary")
        self.btn_login.pack(side=LEFT, padx=5)

        # Botão de Cadastrar ao lado do botão de Login
        self.btn_cadastrar = ttk.Button(self.frm_botoes, text="Cadastrar", bootstyle="success-outline", command=self.cadastrar)
        self.btn_cadastrar.pack(side=LEFT)

        self.centraliza(self.janela)

    def centraliza(self, master):
        master.update_idletasks()
        largura_janela = master.winfo_width()
        altura_janela = master.winfo_height()
        largura_monitor = master.winfo_screenwidth()
        altura_monitor = master.winfo_screenheight()
        x = largura_monitor // 2 - largura_janela // 2
        y = altura_monitor // 2 - altura_janela // 2
        master.geometry(f'{largura_janela}x{altura_janela}+{x}+{y}')

    def cadastrar(self):
        # Cria a janela de cadastro como uma Toplevel
        self.top_cadastrar = ttk.Toplevel(self.janela)
        self.top_cadastrar.title('Tela de Cadastro')
        self.top_cadastrar.geometry("400x250")
        self.top_cadastrar.grab_set() # Torna a janela modal

        # --- Widgets da tela de cadastro ---
        # Nome
        lbl_nome = ttk.Label(self.top_cadastrar, text='NOME:')
        lbl_nome.grid(row=0, column=0, sticky=W, padx=10, pady=10)
        self.ent_nome = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_nome.grid(row=0, column=1, padx=10, pady=10)

        # CPF
        lbl_cpf = ttk.Label(self.top_cadastrar, text='CPF:')
        lbl_cpf.grid(row=1, column=0, sticky=W, padx=10, pady=10)
        self.ent_cpf = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_cpf.grid(row=1, column=1, padx=10, pady=10)

        # Email
        lbl_email = ttk.Label(self.top_cadastrar, text='EMAIL:')
        lbl_email.grid(row=2, column=0, sticky=W, padx=10, pady=10)
        self.ent_email = ttk.Entry(self.top_cadastrar, width=30)
        self.ent_email.grid(row=2, column=1, padx=10, pady=10)
        
        # Senha
        lbl_senha_cad = ttk.Label(self.top_cadastrar, text='SENHA:')
        lbl_senha_cad.grid(row=3, column=0, sticky=W, padx=10, pady=10)
        self.ent_senha_cad = ttk.Entry(self.top_cadastrar, show="*", width=30)
        self.ent_senha_cad.grid(row=3, column=1, padx=10, pady=10)

        # Botão de confirmação
        btn_confirmar_cadastro = ttk.Button(
            self.top_cadastrar,
            text='Confirmar Cadastro',
            bootstyle="success",
            command=self.confirmar_cadastro
        )
        btn_confirmar_cadastro.grid(row=4, column=0, columnspan=2, pady=10, padx=10, sticky='we')
        
        self.centraliza(self.top_cadastrar)

    def confirmar_cadastro(self):
        nome = self.ent_nome.get()
        cpf = self.ent_cpf.get()
        email = self.ent_email.get()
        senha = self.ent_senha_cad.get()

        if nome == '' or cpf == '' or email == '' or senha == '':
            messagebox.showwarning(
                'Aviso',
                'Todos os campos são obrigatórios.',
                parent=self.top_cadastrar # Garante que a mensagem apareça sobre a janela de cadastro
            )
        else:
            # Simula o salvamento do usuário
            print("--- NOVO CADASTRO ---")
            print(f"Nome: {nome}")
            print(f"CPF: {cpf}")
            print(f"Email: {email}")
            print(f"Senha: {senha}")
            print("---------------------")

            messagebox.showinfo(
                'Sucesso',
                f'Usuário {nome} cadastrado com sucesso!',
                parent=self.top_cadastrar
            )
            # Fecha a janela de cadastro após o sucesso
            self.top_cadastrar.destroy()

if __name__ == "__main__":
    app = ttk.Window(themename='darkly')
    Tela(app)
    app.mainloop()
