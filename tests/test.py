from tkinter import *
import AutoComplete.autocomplete.autoComplet as autoComplet

root = Tk()
root.title("test")
root.config(bg="#303030")

codeEdit = Text(root, bg="#303030", fg="white")
codeEdit.pack()

autoComplet.PythonAutoComplete(root, codeEdit, color="#202020")

root.mainloop()