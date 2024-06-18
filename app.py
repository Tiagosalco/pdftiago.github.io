from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import zipfile

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        files = request.files.getlist('files')
        pdf_merger = PyPDF2.PdfMerger()
        original_names = []

        for file in files:
            pdf_merger.append(file)
            original_names.append(file.filename.rsplit('.', 1)[0])

        output_filename = f"merge_{'_'.join(original_names)}.pdf"
        with open(output_filename, 'wb') as f:
            pdf_merger.write(f)

        return send_file(output_filename, as_attachment=True, download_name=output_filename)

    return render_template('merge.html')

@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        file = request.files['file']
        recorte_superior = 50
        recorte_inferior = 50
        recorte_lateral = 65

        pdf_document = fitz.open(stream=file.read(), filetype="pdf")
        original_name = file.filename.rsplit('.', 1)[0]
        output_filename = f"crop_{original_name}.pdf"

        for page in pdf_document:
            rect = page.rect
            new_rect = fitz.Rect(rect.x0 + recorte_lateral, rect.y0 + recorte_superior, rect.x1 - recorte_lateral, rect.y1 - recorte_inferior)
            page.set_cropbox(new_rect)

        pdf_document.save(output_filename)
        pdf_document.close()

        return send_file(output_filename, as_attachment=True, download_name=output_filename)

    return render_template('crop.html')

@app.route('/convert-to-images', methods=['GET', 'POST'])
def convert_to_images():
    if request.method == 'POST':
        file = request.files['file']
        output_folder = request.form.get('output_folder')
        original_name = file.filename.rsplit('.', 1)[0]
        os.makedirs(output_folder, exist_ok=True)

        pdf_document = fitz.open(stream=file.read(), filetype="pdf")

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pixmap = page.get_pixmap()

            img = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
            img_width, img_height = img.size
            img_height //= 3

            for i in range(3):
                cropped_image = img.crop((0, i * img_height, img_width, (i + 1) * img_height))
                image_path = os.path.join(output_folder, f"{original_name}_page_{page_number + 1}_part_{i + 1}.png")
                cropped_image.save(image_path)

        pdf_document.close()

        zip_filename = f"images_{original_name}.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for root, dirs, files in os.walk(output_folder):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_folder))

        if os.path.exists(zip_filename):
            return send_file(zip_filename, as_attachment=True, download_name=zip_filename)
        else:
            flash('Error al crear el archivo ZIP.', 'error')
            return redirect(url_for('convert_to_images'))

    return render_template('convert_to_images.html')

@app.route('/convert-to-pdf', methods=['GET', 'POST'])
def convert_to_pdf():
    if request.method == 'POST':
        files = request.files.getlist('files')
        original_names = [file.filename.rsplit('.', 1)[0] for file in files]
        output_filename = f"convert_{'_'.join(original_names)}.pdf"
        c = canvas.Canvas(output_filename, pagesize=letter)

        for file in files:
            image = Image.open(file.stream)
            img_width, img_height = image.size
            c.setPageSize((img_width, img_height))
            c.drawImage(file, 0, 0, img_width, img_height)
            c.showPage()

        c.save()

        return send_file(output_filename, as_attachment=True, download_name=output_filename)

    return render_template('convert_to_pdf.html')

if __name__ == '__main__':
    app.run(debug=True)
