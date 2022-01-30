from fileinput import filename
from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import transcribe_mp3
import midxml
import xmlpdf

app = Flask(__name__)
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/download_files', methods=['POST'])
def upload_file():
    directory = "Temporary"
    mp3_file = request.files['mp3_file']
    if mp3_file:
        mp3_file.save(os.path.join(directory, mp3_file.filename))
    print(os.path.join(directory, mp3_file.filename))
    transcribe_mp3.transcribe(os.path.join(directory, mp3_file.filename))
    midxml.midTOXML()
    xmlpdf.xmlToPdf()
    return render_template('midAndXml.html', 
                           mid_file_path="output.mid",
                           pdf_file_path="output1.pdf")

@app.route('/download_files/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)