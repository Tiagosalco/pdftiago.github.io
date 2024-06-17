from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge')
def merge():
    subprocess.call(['python', 'pdfmerger.py'])
    return redirect(url_for('index'))

@app.route('/crop')
def crop():
    subprocess.call(['python', 'recortarpdf.py'])
    return redirect(url_for('index'))

@app.route('/convert-to-images')
def convert_to_images():
    subprocess.call(['python', 'pdf_a_tres_fotos.py'])
    return redirect(url_for('index'))

@app.route('/convert-to-pdf')
def convert_to_pdf():
    subprocess.call(['python', 'imagestopdf.py'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
