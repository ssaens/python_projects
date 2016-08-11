import time
import os

def generate_page(resource):
    if os.path.exists(resource.url):
        if os.path.isfile(resource.url):
            return generate_file_html(resource).encode()
        elif os.path.isdir(resource.url):
            return generate_dir_html(resource).encode()

def generate_dir_html(resource):
    directory = resource.resource
    if directory.endswith('/'):
        directory = directory[:-1]

    with open('./temps/dir_template.html') as fh:
        html = fh.read()
    with open('./temps/table_row.html') as fh:
        row_template = fh.read()

    links = ''
    subdirs = os.listdir(resource.url)

    for subdir in subdirs:
        fullpath = os.path.join(resource.parent, subdir)
        relpath = os.path.join(directory, subdir)
        is_file = os.path.isfile(fullpath)

        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(fullpath)
        link = row_template.replace('MTIME', time.ctime(mtime))
        link = link.replace('SIZE', str(size))
        link = link.replace('ITEM', subdir)
        link = link.replace('PATH', os.path.join(relpath))

        if is_file:
            link = link.replace('<!--FILESTART', '')
            link = link.replace('RAWTARGET', relpath)
            link = link.replace('FILEEND-->','')
        else:
            link = link.replace('<!--DIRSTART', '')
            link = link.replace('DIREND-->', '')
        links += link + '\n'

    path = 'Root' if not directory else path

    # html = html.replace('<SERVER_DIR>', '../')
    html = html.replace('<!--ITEMS-->', links)
    html = html.replace('<!--DIRECTORY-->', path)

    return html

def generate_file_html(resource):
    with open('./temps/file_template.html') as fh:
        file_template = fh.read()
    file_text = ''
    with open(fullpath) as fh:
        for line in fh:
            file_text += ''


    return
