import time
import os

root = '/Users/dillon/projects/'
app_root = '/Users/dillon/projects/python/yaolink/'

def gen_home(resource, req, res):
    print('home')

def gen_page(resource, req, res):
    print('gen_page:', path_to(resource))
    resource = path_to(resource)
    if os.path.exists(resource):
        if os.path.isfile(resource):
            generate_file_page(resource, req, res)
        elif os.path.isdir(resource):
            if not resource.endswith('/'):
                resource += '/'
            generate_dir_page(resource, req, res)
        res.set_code(201)
    else:
        res.set_code(404)

def get_raw(resource, req, res):
    resource = path_to(resource)
    print('get_raw:', resource)
    if os.path.exists(resource):
        if os.path.isfile(resource):
            with open(resource, 'rb') as fh:
                content = fh.read()
                res.set_body(resource, content)
                res.set_code(200)
        elif os.path.isdir(resource):
            print('Cannot get raw for dir')
            res.set_code(400)
    else:
        res.set_code(404)

def get_icon(resource, req, res):
    resource = rpath_to('favicon.ico')
    get_raw(resource, req, res)

def get_download(resource, req, res):
    print('get_download:', path_to(resource))
    resource = path_to(resource)
    with open(resource, 'rb') as fh:
        requested = fh.read()
    res.set_body(resource, requested)
    res.set_code(200)

def get_prof(resource, req, res):
    print('prof')

def generate_dir_page(resource, req, res):
    rel_path = resource[len(root):]

    with open('/Users/dillon/projects/python/yaolink/temps/dir_template.html') as fh:
        html = fh.read()
    with open('/Users/dillon/projects/python/yaolink/temps/table_row.html') as fh:
        row_template = fh.read()

    links = ''

    if rel_path:
        links = row_template.replace('MTIME', '')
        links = links.replace('SIZE', '')
        links = links.replace('ITEM', '..')
        links = links.replace('PATH', '/p/' + os.path.dirname(rel_path[:-1]))
        links = links.replace('<!--DIRSTART', '')
        links = links.replace('DIREND-->', '')

    subdirs = os.listdir(resource)

    for subdir in subdirs:
        path = os.path.join(resource, subdir)

        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(path)
        link = row_template.replace('MTIME', time.ctime(mtime))
        link = link.replace('SIZE', str(size))
        link = link.replace('ITEM', subdir)

        link_path = (rel_path + subdir).replace(' ', '%20')

        if os.path.isfile(path):
            link = link.replace('PATH', '/p/' + link_path)
            link = link.replace('<!--FILESTART', '')
            link = link.replace('RAWTARGET', '/r/' + link_path)
            link = link.replace('FILEEND-->','')
        else:
            link = link.replace('PATH', '/p/' + link_path + '/')
            link = link.replace('<!--DIRSTART', '')
            link = link.replace('DIREND-->', '')
        links += link + '\n'

    html = html.replace('<!--ITEMS-->', links)
    html = html.replace('<!--DIRECTORY-->', resource)

    res.set_body('page.html', html)

def generate_file_page(resource, req, res):
    with open('/Users/dillon/projects/python/yaolink/temps/file_template.html') as fh:
        html = fh.read()
    lines = ''
    with open(resource) as fh:
        for ind, line in enumerate(fh):
            lines += '<tr><td>{0}</td><td><pre>{1}</pre></td></tr>\n'.format(ind+1, line)
    html = html.replace('<!--FILE-->', os.path.basename(resource))
    html = html.replace('<!--LINES-->', lines)
    html = html.replace('PARENT', '/p/' +  os.path.dirname(resource[len(root):]))
    res.set_body('.html', html)
    res.set_code(201)

def path_to(relpath):
    return os.path.join(root, relpath)

def rpath_to(relpath):
    return os.path.join(app_root, relpath)
