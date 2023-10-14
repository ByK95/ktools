from flask import Flask, render_template, request, send_from_directory, send_file
import os
import zipfile
import subprocess
import shutil
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def clean_upload_folder(folder_path, zip_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    if os.path.exists(zip_path):
        os.remove(zip_path)


def unzip_to_folder(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        root_names = {name.split('/')[0] for name in zip_ref.namelist() if name.split('/')[0].endswith('.bin')}
        logging.info(f"Unziping: {zip_path}, root_names: {root_names}, extract to: {extract_to}")
        if len(root_names) > 0:
            extract_to = os.path.join(extract_to, os.path.splitext(os.path.basename(zip_path))[0])
        
        zip_ref.extractall(extract_to)
        if len(root_names) > 0:
            return extract_to
        return os.path.join(extract_to, list(root_names)[0])

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        zip_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(zip_path)
        
        folder_path = unzip_to_folder(zip_path, UPLOAD_FOLDER)
        folder = os.path.basename(uploaded_file.filename.replace('.zip', ''))
        logging.info(f"Folder {folder}")
        messages = []
        
        anim_bin_path = os.path.join(folder_path, 'anim.bin')
        build_bin_path = os.path.join(folder_path, 'build.bin')
        atlas_tex_path = os.path.join(folder_path, 'atlas-0.tex')
        
        if os.path.exists(anim_bin_path) and os.path.exists(build_bin_path):
            subprocess.run(["./krane", anim_bin_path, build_bin_path, f"./{OUTPUT_FOLDER}/{folder}"])
        elif os.path.exists(anim_bin_path):
            logging.info(f"Missing {build_bin_path}")
            subprocess.run(["./krane", anim_bin_path, f"./{OUTPUT_FOLDER}/{folder}"])
        else:
            logging.info(f"Missing {anim_bin_path}, {build_bin_path}")
            messages.append('anim.bin file not found.')

        if os.path.exists(atlas_tex_path):
            subprocess.run(["./ktech", atlas_tex_path, f"./{OUTPUT_FOLDER}/{folder}"])
        else:
            logging.info(f"Missing {atlas_tex_path}")
            messages.append('atlas-0.tex file not found.')
        
        clean_upload_folder(folder_path, zip_path)
        if messages:
            return messages
        return 'File uploaded and processed.'
    return 'No file uploaded.'


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
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

