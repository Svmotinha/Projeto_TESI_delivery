import ttkbootstrap as ttk
from ttkbootstrap.constants import *

janela = ttk.Window(themename='vapor')
janela.geometry("240x110")
janela.title('Tela de Login com layout grid')
janela.resizable(False, False)

lbl_usuario = ttk.Label(janela, text="Usuário:")
lbl_usuario.grid(column=0, row=0, sticky=W, padx=5, pady=5)

ent_usuario = ttk.Entry(janela)
ent_usuario.grid(column=1, row=0, sticky=E, padx=5, pady=5)

lbl_senha = ttk.Label(janela, text="Senha:")
lbl_senha.grid(column=0, row=1, sticky=W, padx=5, pady=5)

ent_senha = ttk.Entry(janela, show="*")
ent_senha.grid(column=1, row=1, sticky=E, padx=5, pady=5)

btn_login = ttk.Button(janela, text="Entrar", bootstyle="primary")
btn_login.grid(column=1, row=2, sticky=W, padx=5, pady=5)

janela.mainloop()