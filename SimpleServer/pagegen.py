import time
import os

def generate_page(path, resource):
    if os.path.exists(path):
        if os.path.isfile(path):
            with open(path, 'rb') as fh:
                content = fh.read()
            return content
        elif os.path.isdir(path):
            return generate_dir_html(path, resource).encode()

def generate_dir_html(path, directory):
    if directory.endswith('/'):
        directory = directory[:-1]

    with open('./temps/dir_template.html') as dir_template:
        html_template = dir_template.read()
    html = html_template

    subdirs = os.listdir(path)
    with open('./temps/table_row.html') as row_template:
        template = row_template.read()

    table_rows = []
    for subdir in subdirs:
        fullpath = os.path.join(directory, subdir)
        add_raw = False if os.path.isfile(fullpath) else True
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fullpath)
        link = template.replace('MTIME', time.ctime(mtime))
        link = link.replace('SIZE', str(size))
        link = link.replace('ITEM', subdir)
        link = link.replace('PATH', os.path.join(fullpath))
        if add_raw:
            link = link.replace('<!--rawstart', '')
            link = link.replace('rawend-->','')
        table_rows.append(link)
    links = '\n'.join(table_rows)

    directory = 'Root' if not directory else directory

    html = html.replace('<!--ITEMS-->', links)
    html = html.replace('<!--DIRECTORY-->', directory)

    return html

def generate_file_html():
    return
