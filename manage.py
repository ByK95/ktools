from flask import Flask, render_template, request, send_from_directory, send_file
import os
import zipfile
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)


def unzip_to_folder(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        root_names = {name.split('/')[0] for name in zip_ref.namelist()}
        
        if len(root_names) > 1:
            extract_to = os.path.join(extract_to, list(root_names)[0])
        
        zip_ref.extractall(extract_to)
        if len(root_names) > 1:
            return extract_to
        return os.path.join(extract_to, list(root_names)[0])

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        zip_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(zip_path)
        
        folder_path = unzip_to_folder(zip_path, UPLOAD_FOLDER)
        folder = os.path.basename(folder_path)
        
        anim_bin_path = os.path.join(folder_path, 'anim.bin')
        atlas_tex_path = os.path.join(folder_path, 'atlas-0.tex')
        
        if os.path.exists(anim_bin_path):
            subprocess.run(["./krane", anim_bin_path, f"{folder_path}/build.bin", f"./{OUTPUT_FOLDER}/{folder}"])
        else:
            return 'anim.bin file not found.'

        if os.path.exists(atlas_tex_path):
            subprocess.run(["./ktech", atlas_tex_path, f"./{OUTPUT_FOLDER}/{folder}"])
        else:
            return 'atlas-0.tex file not found.'
        
        return 'File uploaded and processed.'
    return 'No file uploaded.'


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    # Create a ZIP file
    zipf = zipfile.ZipFile(f"{OUTPUT_FOLDER}/{filename}.zip", 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(f"{OUTPUT_FOLDER}/{filename}"):
        for file in files:
            zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), f"{OUTPUT_FOLDER}/{filename}"))
    zipf.close()

    return send_file(f"{OUTPUT_FOLDER}/{filename}.zip", as_attachment=True)

@app.route('/list_files', methods=['GET'])
def list_files():
    files = os.listdir(OUTPUT_FOLDER)
    return render_template('list_files.html', files=files)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)

