import os
import multiprocessing
import logging

logging.basicConfig(level=logging.DEBUG)

parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
notebooks_directory = os.path.abspath(parent_directory + '/notebooks')
notebooks_html_directory = os.path.abspath(parent_directory + '/notebooks/html_output')

def runipy(notebook):
    """thread worker function"""
    logging.info('Running notebook: {}'.format(notebook))
    os.system('runipy -o "{dir}/{file}"'.format(dir=notebooks_directory, file=notebook))
    logging.info('Converting notebook to html: {}'.format(notebook))
    os.system('ipython nbconvert "{dir}/{file}" --to=html --output="{html_dir}/{file}"'.format(dir=notebooks_directory,
                                                                                               html_dir=notebooks_html_directory,
                                                                                               file=notebook))
    return


if __name__ == '__main__':
    multiprocessing.freeze_support()

    if not os.path.exists(notebooks_html_directory):
        os.makedirs(notebooks_html_directory)

    notebooks = set()
    for file in os.listdir(notebooks_directory):
        if file.endswith(".ipynb"):
            notebooks.add(file)

    for notebook in notebooks:
        p = multiprocessing.Process(target=runipy, args=(notebook,))
        p.start()

    # open html file
    html_index = open('{dir}/index.html'.format(dir=notebooks_html_directory), 'w')

    # write beginning of html file
    html_index.write('''<!DOCTYPE html>
    <html>
    <head lang="en">
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <ul>
    ''')

    for notebook in notebooks:
        notebook_link = notebook + '.html'

        # write link to html list
        html_index.write('<li><a href="{notebook_link}">{notebook_link}</a></li>\n'.format(notebook_link=notebook_link))

    # close html
    html_index.write('''</ul></body>
    </html>''')

    # close the file
    html_index.close()
