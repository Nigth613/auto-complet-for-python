import tkinter as tk
from tkinter import ttk
import jedi
import re

class PythonAutoComplete:
    def __init__(self, root, code_editor, color="#2d2d2d"):
        """
        Inicializa o sistema de autocompletar para Python
        
        Args:
            root: A janela principal do Tkinter
            code_editor: O widget Text onde o código será editado
            color: Cor de fundo do popup de autocompletar (padrão: #2d2d2d)
        """
        self.root = root
        self.code_editor = code_editor
        self.color = color
        
        # Popup para mostrar sugestões
        self.popup = None
        self.listbox = None
        self.current_completions = []
        
        # Configurar eventos
        self.setup_events()
        
        # Configurar estilo do popup
        self.setup_styles()
    
    def setup_styles(self):
        """Configura os estilos visuais do popup"""
        self.popup_bg = self.color
        self.popup_fg = "#ffffff"
        self.popup_select_bg = "#404040"
        self.popup_select_fg = "#ffffff"
    
    def setup_events(self):
        """Configura os eventos do editor de código"""
        # Evento para detectar digitação
        self.code_editor.bind('<KeyRelease>', self.on_key_release)
        self.code_editor.bind('<Button-1>', self.hide_popup)
        self.code_editor.bind('<FocusOut>', self.hide_popup)
        
        # Eventos para navegação no popup
        self.code_editor.bind('<Up>', self.on_up_key)
        self.code_editor.bind('<Down>', self.on_down_key)
        self.code_editor.bind('<Return>', self.on_enter_key)
        self.code_editor.bind('<Tab>', self.on_tab_key)
        self.code_editor.bind('<Escape>', self.on_escape_key)
    
    def get_current_word(self):
        """Obtém a palavra atual sendo digitada"""
        try:
            # Posição atual do cursor
            current_pos = self.code_editor.index(tk.INSERT)
            line_start = current_pos.split('.')[0] + '.0'
            line_text = self.code_editor.get(line_start, current_pos)
            
            # Encontrar a palavra atual
            words = re.findall(r'\b\w+\b', line_text)
            if words:
                return words[-1]
            return ""
        except:
            return ""
    
    def get_code_context(self):
        """Obtém todo o código do editor para análise do Jedi"""
        try:
            return self.code_editor.get('1.0', tk.END)
        except:
            return ""
    
    def get_cursor_position(self):
        try:
            current_pos = self.code_editor.index(tk.INSERT)
            line, col = map(int, current_pos.split('.'))
            return line, col
        except:
            return 1, 0

    
    def get_completions(self):
        try:
            code = self.get_code_context()
            line, col = self.get_cursor_position()

            # Criar script Jedi com o código atual
            script = jedi.Script(code)

            # Obter as sugestões usando o método correto para Jedi 0.19+
            completions = script.complete(line, col)

            suggestions = []
            for completion in completions:
                completion_type = getattr(completion, 'type', 'unknown')
                name = getattr(completion, 'name', str(completion))
                complete_text = getattr(completion, 'complete', name)
                description = getattr(completion, 'description', '')
                display_text = f"{name} ({completion_type})" if completion_type else name

                suggestions.append({
                    'name': name,
                    'complete': complete_text,
                    'type': completion_type,
                    'description': description,
                    'display': display_text
                })

            return suggestions[:20]  # Limita a 20 sugestões
        except Exception as e:
            print(f"Erro ao obter completions: {e}")
            return []

    
    def show_popup(self, completions):
        """Mostra o popup com as sugestões"""
        if not completions:
            self.hide_popup()
            return
        
        self.current_completions = completions
        
        # Destruir popup anterior se existir
        if self.popup:
            self.popup.destroy()
        
        # Criar novo popup
        self.popup = tk.Toplevel(self.root)
        self.popup.wm_overrideredirect(True)
        self.popup.configure(bg=self.popup_bg)
        
        # Criar listbox para sugestões
        self.listbox = tk.Listbox(
            self.popup,
            height=min(10, len(completions)),
            width=40,
            bg=self.popup_bg,
            fg=self.popup_fg,
            selectbackground=self.popup_select_bg,
            selectforeground=self.popup_select_fg,
            font=('Consolas', 9),
            relief=tk.FLAT,
            borderwidth=1,
            highlightthickness=0,
            activestyle='dotbox'
        )
        
        # Adicionar sugestões à listbox
        for completion in completions:
            self.listbox.insert(tk.END, completion['display'])
        
        # Selecionar primeira opção
        if completions:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
        
        self.listbox.pack(fill=tk.BOTH, expand=True)
        
        # Posicionar popup próximo ao cursor
        self.position_popup()
        
        # Configurar eventos da listbox
        self.listbox.bind('<Double-Button-1>', self.on_listbox_select)
        self.listbox.bind('<Return>', self.on_listbox_select)
    
    def position_popup(self):
        """Posiciona o popup próximo ao cursor"""
        try:
            # Obter posição do cursor no editor
            cursor_pos = self.code_editor.index(tk.INSERT)
            x, y, _, _ = self.code_editor.bbox(cursor_pos)
            
            # Obter posição da janela principal
            root_x = self.root.winfo_rootx()
            root_y = self.root.winfo_rooty()
            
            # Obter posição do editor na janela
            editor_x = self.code_editor.winfo_x()
            editor_y = self.code_editor.winfo_y()
            
            # Calcular posição final
            popup_x = root_x + editor_x + x
            popup_y = root_y + editor_y + y + 20  # 20 pixels abaixo do cursor
            
            self.popup.geometry(f"+{popup_x}+{popup_y}")
        except:
            # Fallback para posição padrão
            self.popup.geometry("+100+100")
    
    def hide_popup(self, event=None):
        """Esconde o popup"""
        if self.popup:
            self.popup.destroy()
            self.popup = None
            self.listbox = None
            self.current_completions = []
    
    def insert_completion(self, completion):
        """Insere a completion selecionada no editor"""
        try:
            # Obter palavra atual
            current_word = self.get_current_word()
            
            # Obter posição atual
            current_pos = self.code_editor.index(tk.INSERT)
            line, col = map(int, current_pos.split('.'))
            
            # Calcular posição de início da palavra
            start_pos = f"{line}.{col - len(current_word)}"
            
            # Remover palavra atual e inserir completion
            self.code_editor.delete(start_pos, current_pos)
            self.code_editor.insert(start_pos, completion['name'])
            
            self.hide_popup()
        except Exception as e:
            print(f"Erro ao inserir completion: {e}")
    
    def on_key_release(self, event):
        """Evento chamado quando uma tecla é liberada"""
        # Ignorar teclas especiais
        if event.keysym in ['Up', 'Down', 'Left', 'Right', 'Return', 'Tab', 'Escape']:
            return
        
        # Verificar se devemos mostrar autocompletar
        current_word = self.get_current_word()
        
        if len(current_word) >= 2:  # Mostrar após 2 caracteres
            completions = self.get_completions()
            if completions:
                self.show_popup(completions)
            else:
                self.hide_popup()
        else:
            self.hide_popup()
    
    def on_up_key(self, event):
        """Navegar para cima no popup"""
        if self.popup and self.listbox:
            current = self.listbox.curselection()
            if current:
                index = current[0]
                if index > 0:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(index - 1)
                    self.listbox.activate(index - 1)
            return 'break'
    
    def on_down_key(self, event):
        """Navegar para baixo no popup"""
        if self.popup and self.listbox:
            current = self.listbox.curselection()
            if current:
                index = current[0]
                if index < self.listbox.size() - 1:
                    self.listbox.selection_clear(0, tk.END)
                    self.listbox.selection_set(index + 1)
                    self.listbox.activate(index + 1)
            return 'break'
    
    def on_enter_key(self, event):
        """Aceitar sugestão com Enter"""
        if self.popup and self.listbox:
            current = self.listbox.curselection()
            if current and self.current_completions:
                completion = self.current_completions[current[0]]
                self.insert_completion(completion)
                return 'break'
    
    def on_tab_key(self, event):
        """Aceitar sugestão com Tab"""
        if self.popup and self.listbox:
            current = self.listbox.curselection()
            if current and self.current_completions:
                completion = self.current_completions[current[0]]
                self.insert_completion(completion)
                return 'break'
    
    def on_escape_key(self, event):
        """Esconder popup com Escape"""
        if self.popup:
            self.hide_popup()
            return 'break'
    
    def on_listbox_select(self, event):
        """Evento quando item da listbox é selecionado"""
        if self.listbox and self.current_completions:
            selection = self.listbox.curselection()
            if selection:
                completion = self.current_completions[selection[0]]
                self.insert_completion(completion)