from flask import Flask, render_template, request, redirect, url_for, send_file, flash, after_this_request
import PyPDF2
import fitz  # PyMuPDF
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import zipfile
import tempfile

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necesario para usar flash

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['GET', 'POST'])
def merge():
    if request.method == 'POST':
        try:
            files = request.files.getlist('files')
            pdf_merger = PyPDF2.PdfMerger()
            original_names = []

            for file in files:
                pdf_merger.append(file)
                original_names.append(file.filename.rsplit('.', 1)[0])

            output_filename = f"merge_{'_'.join(original_names)}.pdf"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            with open(output_path, 'wb') as f:
                pdf_merger.write(f)

            @after_this_request
            def remove_file(response):
                try:
                    os.remove(output_path)
                except Exception as error:
                    app.logger.error("Error removing or closing downloaded file handle", error)
                return response

            return send_file(output_path, as_attachment=True, download_name=output_filename)
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('merge'))

    return render_template('merge.html')

@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        try:
            file = request.files['file']
            recorte_superior = 50
            recorte_inferior = 50
            recorte_lateral = 65

            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            original_name = file.filename.rsplit('.', 1)[0]
            output_filename = f"crop_{original_name}.pdf"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)

            for page in pdf_document:
                rect = page.rect
                new_rect = fitz.Rect(rect.x0 + recorte_lateral, rect.y0 + recorte_superior, rect.x1 - recorte_lateral, rect.y1 - recorte_inferior)
                page.set_cropbox(new_rect)

            pdf_document.save(output_path)
            pdf_document.close()

            @after_this_request
            def remove_file(response):
                try:
                    os.remove(output_path)
                except Exception as error:
                    app.logger.error("Error removing or closing downloaded file handle", error)
                return response

            return send_file(output_path, as_attachment=True, download_name=output_filename)
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('crop'))

    return render_template('crop.html')

@app.route('/convert-to-images', methods=['GET', 'POST'])
def convert_to_images():
    if request.method == 'POST':
        try:
            file = request.files['file']
            original_name = file.filename.rsplit('.', 1)[0]
            output_folder = tempfile.mkdtemp()

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
            zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for root, dirs, files in os.walk(output_folder):
                    for file in files:
                        zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), output_folder))

            @after_this_request
            def remove_files(response):
                try:
                    os.remove(zip_path)
                    for root, dirs, files in os.walk(output_folder):
                        for file in files:
                            os.remove(os.path.join(root, file))
                    os.rmdir(output_folder)
                except Exception as error:
                    app.logger.error("Error removing or closing downloaded file handle", error)
                return response

            return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('convert_to_images'))

    return render_template('convert_to_images.html')

@app.route('/convert-to-pdf', methods=['GET', 'POST'])
def convert_to_pdf():
    if request.method == 'POST':
        try:
            files = request.files.getlist('files')
            original_names = [file.filename.rsplit('.', 1)[0] for file in files]
            output_filename = f"convert_{'_'.join(original_names)}.pdf"
            output_path = os.path.join(tempfile.gettempdir(), output_filename)
            c = canvas.Canvas(output_path, pagesize=letter)

            for file in files:
                image = Image.open(file.stream)
                img_width, img_height = image.size
                c.setPageSize((img_width, img_height))
                c.drawImage(file, 0, 0, img_width, img_height)
                c.showPage()

            c.save()

            @after_this_request
            def remove_file(response):
                try:
                    os.remove(output_path)
                except Exception as error:
                    app.logger.error("Error removing or closing downloaded file handle", error)
                return response

            return send_file(output_path, as_attachment=True, download_name=output_filename)
        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for('convert_to_pdf'))

    return render_template('convert_to_pdf.html')

if __name__ == '__main__':
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host='0.0.0.0', port=5000)
