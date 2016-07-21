#!/Users/Min/anaconda3/bin/python

import cgi
import cgitb
import shutil

cgitb.enable(display=0, logdir="./logs")

def save_uploaded_file (form_field, upload_dir):
    form = cgi.FieldStorage()
    if not form.has_key(form_field): return
    fileitem = form[form_field]
    if not fileitem.file: return

    outpath = os.path.join(upload_dir, fileitem.filename)

    with open(outpath, 'wb') as fout:
        shutil.copyfileobj(fileitem.file, fout, 100000)
