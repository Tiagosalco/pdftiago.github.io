import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def crop_pdf():
    input_pdf_path = input_entry.get()
    output_pdf_path = output_entry.get()
    recorte_superior = 50
    recorte_inferior = 50
    recorte_lateral = 65

    if input_pdf_path and output_pdf_path:
        document = fitz.open(input_pdf_path)

        for page in document:
            rect = page.rect
            new_rect = fitz.Rect(rect.x0 + recorte_lateral, rect.y0 + recorte_superior, rect.x1 - recorte_lateral, rect.y1 - recorte_inferior)
            page.set_cropbox(new_rect)

        document.save(output_pdf_path)
        document.close()
        status_label.config(text="PDF recortado y guardado correctamente.", fg="white")

# Configuración de la interfaz de Tkinter
root = tk.Tk()
root.title("Recortar PDF")
root.configure(bg="#2C2C2C")

tk.Label(root, text="Seleccionar archivo PDF de entrada:", bg="#2C2C2C", fg="white").pack(pady=5)
input_entry = tk.Entry(root, width=50)
input_entry.pack(pady=5)
tk.Button(root, text="Buscar", command=select_input_file, bg="#1E78FF", fg="white").pack(pady=5)

tk.Label(root, text="Seleccionar archivo PDF de salida:", bg="#2C2C2C", fg="white").pack(pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)
tk.Button(root, text="Guardar como", command=select_output_file, bg="#1E78FF", fg="white").pack(pady=5)

tk.Button(root, text="Recortar PDF", command=crop_pdf, bg="#1E78FF", fg="white").pack(pady=20)

status_label = tk.Label(root, text="", bg="#2C2C2C")
status_label.pack(pady=5)

root.mainloop()
