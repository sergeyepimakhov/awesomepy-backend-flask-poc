import json
import os
import re

import jinja2
from flask import Flask, render_template

import nbconvert.filters as filters

import uuid

app = Flask(__name__, template_folder="templates")


# filters
# https://nbconvert.readthedocs.io/en/latest/api/filters.html#filters
@app.template_filter()
def highlight_code(lst, metadata):
    source = ''.join(lst)
    highlighter = filters.Highlight2HTML()
    return highlighter(source=source, metadata=metadata)


@app.template_filter()
def strip_files_prefix(lst):
    text = ''.join(lst)
    return filters.strip_files_prefix(text)


@app.template_filter()
def markdown2html(lst):
    text = ''.join(lst)
    return filters.markdown2html(text)


@app.template_filter()
def ansi2html(lst):
    text = ''.join(lst)
    return filters.ansi2html(text)


@app.template_filter()
def posix_path(text):
    return filters.posix_path(text)


@app.template_filter()
def get_metadata(output, key, mimetype=None):
    return filters.get_metadata(output, key, mimetype)


@app.template_filter()
def filter_data_type(text):
    data_type_filter = filters.DataTypeFilter()
    return data_type_filter(text)


@app.template_filter()
def json_dumps(text):
    return json.dumps(text)


# define language TODO: use guess from pygments
@app.template_filter()
def language(lines):
    if len(lines) > 0:
        first_line = lines[0]

        first_line = first_line.lstrip()  # trim whitespaces from the left
        if (re.search(r'^%%(bash|sh)(.*)\n?$', first_line) or
                re.search(r'^\s*[!]+\s*(.*)$', first_line) or
                re.search(r'^%env\s*(.*)$', first_line) or
                re.search(r'^%(cat|cp|ls|man|mkdir|more|mv|pwd|rm|rmdir)(.*)$', first_line)):
            language = 'shell' # TODO: shell may be?
        elif re.search(r'^%%(html|HTML)\n?$', first_line):
            language = 'html'
        else:
            language = 'python'

        return language

    return None

# functions
@app.context_processor
def set_uuid4():
    return dict(uuid4=uuid.uuid4)

# https://github.com/jupyter/nbconvert/blob/master/nbconvert/exporters/html.py#L109
def resources_include_css(name):
    # <link rel="stylesheet" type="text/css" href="mystyle.css">
    code = """<link rel="stylesheet" type="text/css" href="%s">""" % name
    return jinja2.Markup(code)


def resources_include_js(name):
    # <link rel="stylesheet" type="text/css" href="mystyle.css">
    code = """<script type="module" src="%s"></script>""" % name
    return jinja2.Markup(code)

# TODO include_js

resources = {'metadata': {'name': 'Sample'},
             'inlining': {'css': []}, # additional css files
             # 'include_css': 'include_css'
             }

resources['global_content_filter'] = {
    'include_code': True,
    'include_markdown': True,
    'include_raw': True,
    'include_unknown': True,
    'include_input': True,
    'include_output': True,
    'include_input_prompt': True, # exclude In[]
    'include_output_prompt': True, # exclude Out[]
    'no_prompt': True,
}

resources['include_css'] = resources_include_css
resources['include_js'] = resources_include_js


@app.route('/classic')
def render_classic():
    nb = None
    try:
        nb = json.loads(open(f"{os.path.dirname(__file__)}/sample.ipynb").read())
    except Exception as e:
        exit(1)

    return render_template('/classic/index.html.j2', nb=nb, resources=resources)


@app.route('/lab')
def render_lab():
    nb = None
    try:
        nb = json.loads(open(f"{os.path.dirname(__file__)}/sample.ipynb").read())
    except Exception as e:
        exit(1)

    return render_template('/lab/index.html.j2', nb=nb, resources=resources)

