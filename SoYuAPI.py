import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
import json
from datetime import datetime
import threading
import urllib.parse

class SoYuAPI:
    def __init__(self, root):
        self.root = root
        self.root.title("SoYuAPI - Cliente HTTP Completo")
        self.root.geometry("1300x750")
        self.root.configure(bg='#1e1e2e')
        
        # Variáveis
        self.current_method = tk.StringVar(value="POST")
        self.url_var = tk.StringVar(value="http://esp12e.local/api/save")
        self.body_type = tk.StringVar(value="Form-Data")
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar interface
        self.create_menu()
        self.create_toolbar()
        self.create_main_panels()
        
        # Atalhos
        self.root.bind('<Control-Return>', lambda e: self.send_request())
        self.root.bind('<Control-s>', lambda e: self.save_request())
        self.root.bind('<Control-o>', lambda e: self.load_request())
        
        # Pré-configurar dados
        self.body_text.insert('1.0', 'ssid=myrede&pass=mypass&keepap=0')
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        self.colors = {
            'bg': '#1e1e2e',
            'bg2': '#2d2d44',
            'bg3': '#3d3d5c',
            'bg4': '#45475a',
            'text': '#cdd6f4',
            'text2': '#a6adc8',
            'accent': '#89b4fa',
            'accent2': '#74c7ec',
            'success': '#a6e3a1',
            'error': '#f38ba8',
            'warning': '#f9e2af'
        }
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text'])
        style.configure('TButton', background=self.colors['accent'], foreground='#1e1e2e', 
                       borderwidth=0, focuscolor='none', font=('Arial', 10, 'bold'))
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Nova Requisição", command=self.new_request, accelerator="Ctrl+N")
        file_menu.add_command(label="Abrir...", command=self.load_request, accelerator="Ctrl+O")
        file_menu.add_command(label="Salvar", command=self.save_request, accelerator="Ctrl+S")
        file_menu.add_command(label="Salvar Como...", command=self.save_request_as)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit, accelerator="Ctrl+Q")
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Limpar Resposta", command=self.clear_response)
        edit_menu.add_command(label="Limpar Tudo", command=self.clear_all)
        menubar.add_cascade(label="Editar", menu=edit_menu)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self.show_about)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        
        self.root.config(menu=menubar)
        
    def create_toolbar(self):
        toolbar = tk.Frame(self.root, bg=self.colors['bg2'], height=50)
        toolbar.pack(fill=tk.X, pady=(0, 1))
        toolbar.pack_propagate(False)
        
        # Método HTTP
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        self.method_combo = ttk.Combobox(toolbar, values=methods, textvariable=self.current_method,
                                        width=10, state='readonly')
        self.method_combo.pack(side=tk.LEFT, padx=(10, 5))
        
        # URL
        self.url_entry = tk.Entry(toolbar, textvariable=self.url_var, bg=self.colors['bg3'],
                                 fg=self.colors['text'], insertbackground=self.colors['text'],
                                 font=('Arial', 11), relief=tk.FLAT)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Botão Enviar
        send_btn = tk.Button(toolbar, text="🚀 Enviar", command=self.send_request,
                            bg=self.colors['accent'], fg='#1e1e2e',
                            font=('Arial', 10, 'bold'), relief=tk.FLAT,
                            padx=20, pady=5, cursor='hand2')
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Botão Salvar
        save_btn = tk.Button(toolbar, text="💾 Salvar", command=self.save_request,
                            bg=self.colors['bg3'], fg=self.colors['text'],
                            font=('Arial', 10), relief=tk.FLAT,
                            padx=15, pady=5, cursor='hand2')
        save_btn.pack(side=tk.LEFT, padx=2)
        
        # Botão Abrir
        open_btn = tk.Button(toolbar, text="📂 Abrir", command=self.load_request,
                            bg=self.colors['bg3'], fg=self.colors['text'],
                            font=('Arial', 10), relief=tk.FLAT,
                            padx=15, pady=5, cursor='hand2')
        open_btn.pack(side=tk.LEFT, padx=2)
        
        # Botão Limpar
        clear_btn = tk.Button(toolbar, text="🗑️ Limpar", command=self.clear_all,
                             bg=self.colors['bg3'], fg=self.colors['text'],
                             font=('Arial', 10), relief=tk.FLAT,
                             padx=15, pady=5, cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Status da conexão (placeholder)
        self.connection_status = tk.Label(toolbar, text="● Desconectado",
                                         bg=self.colors['bg2'], fg=self.colors['error'],
                                         font=('Arial', 9))
        self.connection_status.pack(side=tk.RIGHT, padx=10)
        
    def create_main_panels(self):
        # Painel principal com PanedWindow
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL,
                                   bg=self.colors['bg'], sashrelief=tk.RAISED,
                                   sashwidth=5)
        self.paned.pack(fill=tk.BOTH, expand=True)
        
        # ===== PAINEL ESQUERDO (Requisição) =====
        left_frame = tk.Frame(self.paned, bg=self.colors['bg'])
        self.paned.add(left_frame, width=550)
        
        # Notebook para abas da requisição
        self.request_notebook = ttk.Notebook(left_frame)
        self.request_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Aba Params (Query String)
        params_frame = tk.Frame(self.request_notebook, bg=self.colors['bg2'])
        self.request_notebook.add(params_frame, text="🔗 Parâmetros")
        self.create_params_tab(params_frame)
        
        # Aba Headers
        headers_frame = tk.Frame(self.request_notebook, bg=self.colors['bg2'])
        self.request_notebook.add(headers_frame, text="📋 Headers")
        self.create_headers_tab(headers_frame)
        
        # Aba Body
        body_frame = tk.Frame(self.request_notebook, bg=self.colors['bg2'])
        self.request_notebook.add(body_frame, text="📦 Body")
        self.create_body_tab(body_frame)
        
        # Aba Auth
        auth_frame = tk.Frame(self.request_notebook, bg=self.colors['bg2'])
        self.request_notebook.add(auth_frame, text="🔐 Autenticação")
        self.create_auth_tab(auth_frame)
        
        # ===== PAINEL DIREITO (Resposta) =====
        right_frame = tk.Frame(self.paned, bg=self.colors['bg'])
        self.paned.add(right_frame, width=750)
        
        # Status e tempo
        status_frame = tk.Frame(right_frame, bg=self.colors['bg2'], height=45)
        status_frame.pack(fill=tk.X, pady=(0, 5))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Status: Aguardando...",
                                    bg=self.colors['bg2'], fg=self.colors['text2'],
                                    font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(status_frame, text="⏱️ Tempo: -",
                                  bg=self.colors['bg2'], fg=self.colors['text2'],
                                  font=('Arial', 10))
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        self.size_label = tk.Label(status_frame, text="📦 Tamanho: -",
                                  bg=self.colors['bg2'], fg=self.colors['text2'],
                                  font=('Arial', 10))
        self.size_label.pack(side=tk.LEFT, padx=10)
        
        # Notebook da resposta
        self.response_notebook = ttk.Notebook(right_frame)
        self.response_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Aba Body da Resposta
        response_body_frame = tk.Frame(self.response_notebook, bg=self.colors['bg2'])
        self.response_notebook.add(response_body_frame, text="📄 Resposta")
        
        self.response_text = scrolledtext.ScrolledText(response_body_frame,
                                                      bg=self.colors['bg3'],
                                                      fg=self.colors['text'],
                                                      insertbackground=self.colors['text'],
                                                      font=('Courier New', 10),
                                                      wrap=tk.WORD)
        self.response_text.pack(fill=tk.BOTH, expand=True)
        
        # Aba Headers da Resposta
        response_headers_frame = tk.Frame(self.response_notebook, bg=self.colors['bg2'])
        self.response_notebook.add(response_headers_frame, text="📋 Headers da Resposta")
        
        self.response_headers_text = scrolledtext.ScrolledText(response_headers_frame,
                                                              bg=self.colors['bg3'],
                                                              fg=self.colors['text'],
                                                              insertbackground=self.colors['text'],
                                                              font=('Courier New', 10),
                                                              wrap=tk.WORD)
        self.response_headers_text.pack(fill=tk.BOTH, expand=True)
        
        # Aba Preview
        preview_frame = tk.Frame(self.response_notebook, bg=self.colors['bg2'])
        self.response_notebook.add(preview_frame, text="👁️ Preview")
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame,
                                                     bg=self.colors['bg3'],
                                                     fg=self.colors['text'],
                                                     insertbackground=self.colors['text'],
                                                     font=('Arial', 11),
                                                     wrap=tk.WORD)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
    def create_params_tab(self, parent):
        """Aba de Parâmetros (Query String)"""
        container = tk.Frame(parent, bg=self.colors['bg2'])
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Treeview para parâmetros
        columns = ('Parâmetro', 'Valor')
        self.params_tree = ttk.Treeview(container, columns=columns, show='headings', height=6)
        self.params_tree.heading('Parâmetro', text='Parâmetro')
        self.params_tree.heading('Valor', text='Valor')
        self.params_tree.column('Parâmetro', width=200)
        self.params_tree.column('Valor', width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.params_tree.yview)
        self.params_tree.configure(yscrollcommand=scrollbar.set)
        
        self.params_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar edição inline
        self.setup_editable_treeview(self.params_tree)
        
        # Botões
        btn_frame = tk.Frame(parent, bg=self.colors['bg2'])
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_btn = tk.Button(btn_frame, text="+ Adicionar Parâmetro",
                           command=lambda: self.params_tree.insert('', 'end', values=('', '')),
                           bg=self.colors['bg3'], fg=self.colors['text'],
                           relief=tk.FLAT, padx=10, cursor='hand2')
        add_btn.pack(side=tk.LEFT, padx=2)
        
        remove_btn = tk.Button(btn_frame, text="✕ Remover Selecionado",
                              command=self.remove_selected_param,
                              bg=self.colors['bg3'], fg=self.colors['text'],
                              relief=tk.FLAT, padx=10, cursor='hand2')
        remove_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = tk.Button(btn_frame, text="🗑️ Limpar Todos",
                             command=self.clear_params,
                             bg=self.colors['bg3'], fg=self.colors['text'],
                             relief=tk.FLAT, padx=10, cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Dica
        tip_label = tk.Label(parent, 
                            text="💡 Parâmetros são adicionados à URL como query string (?key=value)",
                            bg=self.colors['bg2'], fg=self.colors['text2'],
                            font=('Arial', 8))
        tip_label.pack(side=tk.BOTTOM, pady=2)
        
        # Adicionar parâmetros de exemplo
        self.params_tree.insert('', 'end', values=('', ''))
        
    def create_headers_tab(self, parent):
        """Aba de Headers"""
        container = tk.Frame(parent, bg=self.colors['bg2'])
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Headers padrão
        default_headers = [
            ("Content-Type", "application/x-www-form-urlencoded"),
            ("Accept", "*/*"),
            ("User-Agent", "SoYuAPI/1.0")
        ]
        
        # Treeview para headers
        columns = ('Chave', 'Valor')
        self.headers_tree = ttk.Treeview(container, columns=columns, show='headings', height=5)
        self.headers_tree.heading('Chave', text='Chave')
        self.headers_tree.heading('Valor', text='Valor')
        self.headers_tree.column('Chave', width=200)
        self.headers_tree.column('Valor', width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=self.headers_tree.yview)
        self.headers_tree.configure(yscrollcommand=scrollbar.set)
        
        self.headers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configurar edição inline
        self.setup_editable_treeview(self.headers_tree)
        
        # Adicionar headers padrão
        for key, value in default_headers:
            self.headers_tree.insert('', 'end', values=(key, value))
            
        # Botões
        btn_frame = tk.Frame(parent, bg=self.colors['bg2'])
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        add_btn = tk.Button(btn_frame, text="+ Adicionar Header",
                           command=lambda: self.headers_tree.insert('', 'end', values=('', '')),
                           bg=self.colors['bg3'], fg=self.colors['text'],
                           relief=tk.FLAT, padx=10, cursor='hand2')
        add_btn.pack(side=tk.LEFT, padx=2)
        
        remove_btn = tk.Button(btn_frame, text="✕ Remover Selecionado",
                              command=self.remove_selected_header,
                              bg=self.colors['bg3'], fg=self.colors['text'],
                              relief=tk.FLAT, padx=10, cursor='hand2')
        remove_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = tk.Button(btn_frame, text="🗑️ Limpar Todos",
                             command=self.clear_headers,
                             bg=self.colors['bg3'], fg=self.colors['text'],
                             relief=tk.FLAT, padx=10, cursor='hand2')
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Dica
        tip_label = tk.Label(parent, 
                            text="💡 Dica: Dê duplo clique para editar | Enter para confirmar | Esc para cancelar",
                            bg=self.colors['bg2'], fg=self.colors['text2'],
                            font=('Arial', 8))
        tip_label.pack(side=tk.BOTTOM, pady=2)
        
    def create_body_tab(self, parent):
        """Aba de Body"""
        container = tk.Frame(parent, bg=self.colors['bg2'])
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tipo de body
        type_frame = tk.Frame(container, bg=self.colors['bg2'])
        type_frame.pack(fill=tk.X, pady=(0, 5))
        
        tk.Label(type_frame, text="Tipo:", bg=self.colors['bg2'], fg=self.colors['text'],
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        body_types = ["Form-Data", "JSON", "Text", "XML", "GraphQL"]
        self.body_combo = ttk.Combobox(type_frame, values=body_types, textvariable=self.body_type,
                                      width=15, state='readonly')
        self.body_combo.pack(side=tk.LEFT, padx=5)
        self.body_combo.bind('<<ComboboxSelected>>', self.on_body_type_change)
        
        # Botão para formatar JSON
        format_btn = tk.Button(type_frame, text="🔧 Format JSON",
                              command=self.format_json,
                              bg=self.colors['bg3'], fg=self.colors['text'],
                              relief=tk.FLAT, padx=10, cursor='hand2')
        format_btn.pack(side=tk.LEFT, padx=5)
        
        # Área de texto do body
        self.body_text = scrolledtext.ScrolledText(container,
                                                  bg=self.colors['bg3'],
                                                  fg=self.colors['text'],
                                                  insertbackground=self.colors['text'],
                                                  font=('Courier New', 10),
                                                  height=14)
        self.body_text.pack(fill=tk.BOTH, expand=True)
        
        # Dica
        tip_label = tk.Label(container, 
                            text="💡 Form-Data: chave1=valor1&chave2=valor2 | JSON: {\"key\": \"value\"}",
                            bg=self.colors['bg2'], fg=self.colors['text2'],
                            font=('Arial', 8))
        tip_label.pack(side=tk.BOTTOM, pady=2)
        
    def create_auth_tab(self, parent):
        """Aba de Autenticação"""
        container = tk.Frame(parent, bg=self.colors['bg2'])
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tipo de autenticação
        tk.Label(container, text="Tipo de Autenticação:", 
                bg=self.colors['bg2'], fg=self.colors['text'],
                font=('Arial', 10)).pack(anchor=tk.W, pady=(0, 5))
        
        self.auth_type = tk.StringVar(value="None")
        auth_types = ["None", "Basic Auth", "Bearer Token", "API Key"]
        auth_combo = ttk.Combobox(container, values=auth_types, textvariable=self.auth_type,
                                 width=20, state='readonly')
        auth_combo.pack(anchor=tk.W, pady=(0, 10))
        auth_combo.bind('<<ComboboxSelected>>', self.on_auth_change)
        
        # Frame para credenciais
        self.auth_frame = tk.Frame(container, bg=self.colors['bg2'])
        self.auth_frame.pack(fill=tk.X, pady=5)
        
        # Campos serão adicionados dinamicamente
        self.auth_widgets = []
        
        # Configuração inicial
        self.on_auth_change()
        
    def on_auth_change(self, event=None):
        """Muda os campos de autenticação baseado no tipo"""
        # Limpar widgets anteriores
        for widget in self.auth_widgets:
            widget.destroy()
        self.auth_widgets = []
        
        auth_type = self.auth_type.get()
        
        if auth_type == "Basic Auth":
            # Usuário e Senha
            tk.Label(self.auth_frame, text="Usuário:", 
                    bg=self.colors['bg2'], fg=self.colors['text']).pack(anchor=tk.W)
            user_entry = tk.Entry(self.auth_frame, bg=self.colors['bg3'],
                                 fg=self.colors['text'], relief=tk.FLAT, width=40)
            user_entry.pack(anchor=tk.W, pady=(0, 5))
            self.auth_widgets.append(user_entry)
            
            tk.Label(self.auth_frame, text="Senha:", 
                    bg=self.colors['bg2'], fg=self.colors['text']).pack(anchor=tk.W)
            pass_entry = tk.Entry(self.auth_frame, bg=self.colors['bg3'],
                                 fg=self.colors['text'], relief=tk.FLAT, width=40, show="*")
            pass_entry.pack(anchor=tk.W, pady=(0, 5))
            self.auth_widgets.append(pass_entry)
            
        elif auth_type == "Bearer Token":
            tk.Label(self.auth_frame, text="Token:", 
                    bg=self.colors['bg2'], fg=self.colors['text']).pack(anchor=tk.W)
            token_entry = tk.Entry(self.auth_frame, bg=self.colors['bg3'],
                                  fg=self.colors['text'], relief=tk.FLAT, width=40)
            token_entry.pack(anchor=tk.W, pady=(0, 5))
            self.auth_widgets.append(token_entry)
            
        elif auth_type == "API Key":
            tk.Label(self.auth_frame, text="API Key:", 
                    bg=self.colors['bg2'], fg=self.colors['text']).pack(anchor=tk.W)
            key_entry = tk.Entry(self.auth_frame, bg=self.colors['bg3'],
                                fg=self.colors['text'], relief=tk.FLAT, width=40)
            key_entry.pack(anchor=tk.W, pady=(0, 5))
            self.auth_widgets.append(key_entry)
            
            tk.Label(self.auth_frame, text="Chave (ex: X-API-Key):", 
                    bg=self.colors['bg2'], fg=self.colors['text']).pack(anchor=tk.W)
            key_name_entry = tk.Entry(self.auth_frame, bg=self.colors['bg3'],
                                     fg=self.colors['text'], relief=tk.FLAT, width=40)
            key_name_entry.insert(0, "X-API-Key")
            key_name_entry.pack(anchor=tk.W, pady=(0, 5))
            self.auth_widgets.append(key_name_entry)
            
    def setup_editable_treeview(self, treeview):
        """Configura edição inline para Treeview"""
        edit_entry = None
        current_item = None
        current_col = None
        
        def on_double_click(event):
            nonlocal edit_entry, current_item, current_col
            region = treeview.identify_region(event.x, event.y)
            if region != "cell":
                return
                
            column = treeview.identify_column(event.x)
            item = treeview.identify_row(event.y)
            
            if not item:
                return
                
            col_index = int(column[1:]) - 1
            start_editing(item, col_index)
            
        def start_editing(item, col):
            nonlocal edit_entry, current_item, current_col
            if edit_entry:
                finish_editing()
                
            current_item = item
            current_col = col
            
            values = list(treeview.item(item, 'values'))
            current_value = values[col] if col < len(values) else ''
            
            bbox = treeview.bbox(item, column=f"#{col+1}")
            if not bbox:
                return
                
            x, y, width, height = bbox
            
            edit_entry = tk.Entry(treeview, 
                                 font=('Arial', 10),
                                 bg=self.colors['bg3'],
                                 fg=self.colors['text'],
                                 insertbackground=self.colors['text'],
                                 relief=tk.FLAT)
            edit_entry.place(x=x, y=y, width=width, height=height)
            edit_entry.insert(0, current_value)
            edit_entry.select_range(0, tk.END)
            edit_entry.focus_set()
            
            edit_entry.bind('<Return>', lambda e: finish_editing())
            edit_entry.bind('<FocusOut>', lambda e: finish_editing())
            edit_entry.bind('<Escape>', lambda e: cancel_editing())
            
        def finish_editing():
            nonlocal edit_entry, current_item, current_col
            if not edit_entry:
                return
                
            new_value = edit_entry.get()
            edit_entry.destroy()
            edit_entry = None
            
            if current_item is not None:
                values = list(treeview.item(current_item, 'values'))
                if current_col < len(values):
                    values[current_col] = new_value
                    treeview.item(current_item, values=values)
                    
            current_item = None
            current_col = None
            
        def cancel_editing():
            nonlocal edit_entry, current_item, current_col
            if edit_entry:
                edit_entry.destroy()
                edit_entry = None
                current_item = None
                current_col = None
                
        treeview.bind('<Double-Button-1>', on_double_click)
        treeview.bind('<Button-1>', lambda e: finish_editing() if edit_entry else None)
        
        # Teclas de atalho
        def on_key(event):
            if event.keysym in ['Return', 'F2'] and not edit_entry:
                selected = treeview.selection()
                if selected:
                    start_editing(selected[0], 0)
                    
        treeview.bind('<Key>', on_key)
        
    def on_body_type_change(self, event=None):
        """Muda o tipo de body e atualiza o Content-Type"""
        body_type = self.body_type.get()
        
        if body_type == "JSON":
            self.body_text.delete('1.0', tk.END)
            self.body_text.insert('1.0', '{\n  "chave": "valor"\n}')
            self.update_content_type('application/json')
        elif body_type == "Form-Data":
            self.body_text.delete('1.0', tk.END)
            self.body_text.insert('1.0', 'chave1=valor1&chave2=valor2')
            self.update_content_type('application/x-www-form-urlencoded')
        elif body_type == "Text":
            self.body_text.delete('1.0', tk.END)
            self.body_text.insert('1.0', 'texto simples')
            self.update_content_type('text/plain')
        elif body_type == "XML":
            self.body_text.delete('1.0', tk.END)
            self.body_text.insert('1.0', '<?xml version="1.0"?><root>texto</root>')
            self.update_content_type('application/xml')
        elif body_type == "GraphQL":
            self.body_text.delete('1.0', tk.END)
            self.body_text.insert('1.0', '{\n  "query": "query { users { name } }"\n}')
            self.update_content_type('application/graphql')
            
    def update_content_type(self, content_type):
        """Atualiza o header Content-Type"""
        found = False
        for item in self.headers_tree.get_children():
            values = self.headers_tree.item(item, 'values')
            if values and values[0].strip().lower() == 'content-type':
                self.headers_tree.item(item, values=(values[0], content_type))
                found = True
                break
        if not found:
            self.headers_tree.insert('', 'end', values=('Content-Type', content_type))
            
    def remove_selected_header(self):
        selected = self.headers_tree.selection()
        if selected:
            self.headers_tree.delete(selected[0])
            
    def clear_headers(self):
        for item in self.headers_tree.get_children():
            self.headers_tree.delete(item)
        self.headers_tree.insert('', 'end', values=('Content-Type', 'application/x-www-form-urlencoded'))
        
    def remove_selected_param(self):
        selected = self.params_tree.selection()
        if selected:
            self.params_tree.delete(selected[0])
            
    def clear_params(self):
        for item in self.params_tree.get_children():
            self.params_tree.delete(item)
        self.params_tree.insert('', 'end', values=('', ''))
        
    def get_headers_dict(self):
        headers = {}
        for item in self.headers_tree.get_children():
            values = self.headers_tree.item(item, 'values')
            if values and values[0].strip():
                headers[values[0].strip()] = values[1].strip() if len(values) > 1 else ''
        return headers
        
    def get_params_dict(self):
        params = {}
        for item in self.params_tree.get_children():
            values = self.params_tree.item(item, 'values')
            if values and values[0].strip():
                params[values[0].strip()] = values[1].strip() if len(values) > 1 else ''
        return params
        
    def get_auth_headers(self):
        """Retorna headers de autenticação"""
        auth_headers = {}
        auth_type = self.auth_type.get()
        
        if auth_type == "Basic Auth":
            if len(self.auth_widgets) >= 2:
                user = self.auth_widgets[0].get()
                password = self.auth_widgets[1].get()
                if user and password:
                    import base64
                    credentials = f"{user}:{password}"
                    encoded = base64.b64encode(credentials.encode()).decode()
                    auth_headers['Authorization'] = f"Basic {encoded}"
                    
        elif auth_type == "Bearer Token":
            if self.auth_widgets:
                token = self.auth_widgets[0].get()
                if token:
                    auth_headers['Authorization'] = f"Bearer {token}"
                    
        elif auth_type == "API Key":
            if len(self.auth_widgets) >= 2:
                key = self.auth_widgets[0].get()
                key_name = self.auth_widgets[1].get()
                if key and key_name:
                    auth_headers[key_name] = key
                    
        return auth_headers
        
    def format_json(self):
        """Formata o JSON no body"""
        try:
            body = self.body_text.get('1.0', 'end-1c')
            if body.strip():
                json_obj = json.loads(body)
                formatted = json.dumps(json_obj, indent=2, ensure_ascii=False)
                self.body_text.delete('1.0', tk.END)
                self.body_text.insert('1.0', formatted)
                self.update_content_type('application/json')
                self.body_type.set('JSON')
        except json.JSONDecodeError:
            messagebox.showerror("Erro", "JSON inválido! Verifique a sintaxe.")
            
    def build_url_with_params(self):
        """Constrói a URL com os parâmetros"""
        url = self.url_var.get().strip()
        params = self.get_params_dict()
        
        if params:
            # Construir query string
            query_string = urllib.parse.urlencode(params)
            if '?' in url:
                url += '&' + query_string
            else:
                url += '?' + query_string
        return url
        
    def send_request(self):
        # Limpar resposta anterior
        self.response_text.delete('1.0', tk.END)
        self.response_headers_text.delete('1.0', tk.END)
        self.preview_text.delete('1.0', tk.END)
        self.status_label.config(text="Status: Enviando...", fg=self.colors['accent2'])
        self.connection_status.config(text="● Conectando...", fg=self.colors['warning'])
        
        # Executar em thread
        thread = threading.Thread(target=self._make_request)
        thread.daemon = True
        thread.start()
        
    def _make_request(self):
        try:
            # Construir URL com parâmetros
            url = self.build_url_with_params()
            if not url:
                self.root.after(0, lambda: self.status_label.config(
                    text="Status: ⚠️ URL vazia!", fg=self.colors['error']))
                return
                
            method = self.current_method.get()
            headers = self.get_headers_dict()
            
            # Adicionar headers de autenticação
            auth_headers = self.get_auth_headers()
            headers.update(auth_headers)
            
            # Body
            body = self.body_text.get('1.0', 'end-1c').strip()
            body_type = self.body_type.get()
            
            # Preparar dados
            data = None
            json_data = None
            
            if body_type == "Form-Data" and body:
                data = body
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
            elif body_type == "JSON" and body:
                try:
                    json_data = json.loads(body)
                    headers['Content-Type'] = 'application/json'
                except json.JSONDecodeError as e:
                    self.root.after(0, lambda: self.status_label.config(
                        text=f"Status: ❌ JSON inválido!", fg=self.colors['error']))
                    return
            elif body_type == "GraphQL" and body:
                try:
                    json_data = json.loads(body)
                    headers['Content-Type'] = 'application/graphql'
                except:
                    data = body
            else:
                data = body
                
            # Fazer requisição
            start_time = datetime.now()
            
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "POST":
                response = requests.post(url, data=data, json=json_data, headers=headers)
            elif method == "PUT":
                response = requests.put(url, data=data, json=json_data, headers=headers)
            elif method == "PATCH":
                response = requests.patch(url, data=data, json=json_data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, data=data, json=json_data, headers=headers)
            elif method == "HEAD":
                response = requests.head(url, headers=headers)
            elif method == "OPTIONS":
                response = requests.options(url, headers=headers)
            else:
                response = requests.get(url, headers=headers)
                
            end_time = datetime.now()
            elapsed = (end_time - start_time).total_seconds() * 1000
            
            # Atualizar UI
            self.root.after(0, lambda: self.display_response(response, elapsed))
            
        except requests.exceptions.ConnectionError:
            self.root.after(0, lambda: self.status_label.config(
                text="Status: ❌ Erro de conexão!", fg=self.colors['error']))
            self.root.after(0, lambda: self.connection_status.config(
                text="● Desconectado", fg=self.colors['error']))
        except requests.exceptions.Timeout:
            self.root.after(0, lambda: self.status_label.config(
                text="Status: ⏱️ Timeout!", fg=self.colors['error']))
        except Exception as e:
            self.root.after(0, lambda: self.status_label.config(
                text=f"Status: ❌ Erro: {str(e)}", fg=self.colors['error']))
                
    def display_response(self, response, elapsed):
        # Status
        status_color = self.colors['success'] if response.ok else self.colors['error']
        self.status_label.config(
            text=f"Status: {response.status_code} {response.reason}",
            fg=status_color)
        self.time_label.config(text=f"⏱️ Tempo: {elapsed:.0f}ms")
        
        # Tamanho
        size = len(response.content)
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size/1024:.1f} KB"
        else:
            size_str = f"{size/(1024*1024):.1f} MB"
        self.size_label.config(text=f"📦 Tamanho: {size_str}")
        
        # Status da conexão
        self.connection_status.config(
            text="● Conectado" if response.ok else "● Erro",
            fg=self.colors['success'] if response.ok else self.colors['error'])
        
        # Body da resposta
        try:
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                formatted = json.dumps(response.json(), indent=2, ensure_ascii=False)
                self.response_text.delete('1.0', tk.END)
                self.response_text.insert('1.0', formatted)
            else:
                self.response_text.delete('1.0', tk.END)
                self.response_text.insert('1.0', response.text)
        except:
            self.response_text.delete('1.0', tk.END)
            self.response_text.insert('1.0', response.text)
            
        # Headers da resposta
        headers_str = ""
        for key, value in response.headers.items():
            headers_str += f"{key}: {value}\n"
        self.response_headers_text.delete('1.0', tk.END)
        self.response_headers_text.insert('1.0', headers_str)
        
        # Preview (primeiras 500 caracteres)
        preview = response.text[:500]
        if len(response.text) > 500:
            preview += "\n\n... (truncado)"
        self.preview_text.delete('1.0', tk.END)
        self.preview_text.insert('1.0', preview)
        
    def clear_response(self):
        """Limpa apenas a resposta"""
        self.response_text.delete('1.0', tk.END)
        self.response_headers_text.delete('1.0', tk.END)
        self.preview_text.delete('1.0', tk.END)
        self.status_label.config(text="Status: Limpo", fg=self.colors['text2'])
        self.time_label.config(text="⏱️ Tempo: -")
        self.size_label.config(text="📦 Tamanho: -")
        
    def clear_all(self):
        """Limpa tudo"""
        self.clear_response()
        self.url_var.set("")
        self.body_text.delete('1.0', tk.END)
        self.body_text.insert('1.0', '')
        
        # Limpar headers
        for item in self.headers_tree.get_children():
            self.headers_tree.delete(item)
        self.headers_tree.insert('', 'end', values=('Content-Type', 'application/x-www-form-urlencoded'))
        
        # Limpar params
        for item in self.params_tree.get_children():
            self.params_tree.delete(item)
        self.params_tree.insert('', 'end', values=('', ''))
        
    def new_request(self):
        """Nova requisição"""
        self.clear_all()
        self.current_method.set("GET")
        self.url_var.set("")
        self.body_type.set("Form-Data")
        
    def save_request(self):
        """Salva a requisição atual"""
        data = {
            'method': self.current_method.get(),
            'url': self.url_var.get(),
            'headers': self.get_headers_dict(),
            'params': self.get_params_dict(),
            'body_type': self.body_type.get(),
            'body': self.body_text.get('1.0', 'end-1c'),
            'auth_type': self.auth_type.get()
        }
        
        # Salvar credenciais de autenticação
        if self.auth_type.get() == "Basic Auth" and len(self.auth_widgets) >= 2:
            data['auth_user'] = self.auth_widgets[0].get()
            data['auth_password'] = self.auth_widgets[1].get()
        elif self.auth_type.get() == "Bearer Token" and self.auth_widgets:
            data['auth_token'] = self.auth_widgets[0].get()
        elif self.auth_type.get() == "API Key" and len(self.auth_widgets) >= 2:
            data['auth_key'] = self.auth_widgets[0].get()
            data['auth_key_name'] = self.auth_widgets[1].get()
            
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Sucesso", f"Requisição salva em:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
                
    def save_request_as(self):
        """Salvar como..."""
        self.save_request()
                
    def load_request(self):
        """Carrega uma requisição"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.current_method.set(data.get('method', 'GET'))
                self.url_var.set(data.get('url', ''))
                
                # Limpar headers
                for item in self.headers_tree.get_children():
                    self.headers_tree.delete(item)
                for key, value in data.get('headers', {}).items():
                    self.headers_tree.insert('', 'end', values=(key, value))
                    
                # Limpar params
                for item in self.params_tree.get_children():
                    self.params_tree.delete(item)
                for key, value in data.get('params', {}).items():
                    self.params_tree.insert('', 'end', values=(key, value))
                if not data.get('params'):
                    self.params_tree.insert('', 'end', values=('', ''))
                    
                # Body
                self.body_type.set(data.get('body_type', 'Form-Data'))
                self.body_text.delete('1.0', tk.END)
                body = data.get('body', '')
                if body:
                    self.body_text.insert('1.0', body)
                    
                # Auth
                self.auth_type.set(data.get('auth_type', 'None'))
                self.on_auth_change()
                if 'auth_user' in data and len(self.auth_widgets) >= 2:
                    self.auth_widgets[0].insert(0, data.get('auth_user', ''))
                    self.auth_widgets[1].insert(0, data.get('auth_password', ''))
                    
                messagebox.showinfo("Sucesso", f"Requisição carregada de:\n{filename}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar: {str(e)}")
                
    def show_about(self):
        """Mostra informações sobre o programa"""
        about_text = """
        🚀 SoYuAPI
        Versão: 2.0
        
        Um cliente HTTP completo inspirado no SoYuAPI.
        
        Funcionalidades:
        • Métodos HTTP (GET, POST, PUT, DELETE, etc)
        • Parâmetros de URL (Query String)
        • Headers personalizáveis
        • Body com suporte a JSON, Form-Data, XML, GraphQL
        • Autenticação (Basic, Bearer, API Key)
        • Salvar/Carregar requisições
        • Formatação de JSON
        • Preview da resposta
        
        Desenvolvido em Python com Tkinter
        """
        messagebox.showinfo("Sobre", about_text)

def main():
    root = tk.Tk()
    app = SoYuAPI(root)
    root.mainloop()

if __name__ == "__main__":
    main()