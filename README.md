# Python AutoComplete Tkinter

Um sistema de **auto-completar para Python** simples, leve e poderoso para editores Tkinter — construído com [Jedi](https://github.com/davidhalter/jedi), a melhor biblioteca de análise de código Python.

## Por que usar?

Fazer um auto-complete funcional para Python pode ser complicado — lidar com análise de código, contexto, sugestões e interface não é trivial.  
Este projeto resolve tudo isso para você! Basta importar a classe, passar seu editor Tkinter e pronto: auto-complete inteligente **funcionando com apenas uma linha de código**.

---

## Recursos

- Completa variáveis, funções, classes e módulos Python com alta precisão usando Jedi
- Popup elegante com sugestões em tempo real que não atrapalham sua digitação
- Navegação intuitiva com teclado (setas, Tab, Enter, Esc)
- Personalize as cores do popup facilmente
- Funciona em qualquer widget Text do Tkinter

---

## Como usar

```python
from autocomplete import PythonAutoComplete
import tkinter as tk

root = tk.Tk()
code_editor = tk.Text(root)
code_editor.pack()

# Inicializa o auto-complete com uma linha!
autocomplete = PythonAutoComplete(root, code_editor, color="#282c34")

root.mainloop()

## Instalação

pip install autocomplete  # quando disponível no PyPI
