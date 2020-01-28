import json
import os

import jinja2
from flask import Flask, render_template

import nbconvert.filters as filters

import uuid

app = Flask(__name__, template_folder="templates")

# filters

# https://nbconvert.readthedocs.io/en/latest/api/filters.html#filters
@app.template_filter()
def highlight_code(lst, metadata):
    # text = ''.join(lst)
    return lst


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

# functions
@app.context_processor
def set_uuid4():
    return dict(uuid4=uuid.uuid4)


@app.route('/')
def hello_world():
    nb = None
    try:
        nb = json.loads(open(f"{os.path.dirname(__file__)}/sample.ipynb").read())
    except Exception as e:
        exit(1)

    # https://github.com/jupyter/nbconvert/blob/master/nbconvert/exporters/html.py#L109
    def resources_include_css(name):
        # <link rel="stylesheet" type="text/css" href="mystyle.css">
        code = """<link rel="stylesheet" type="text/css" href="%s">""" % name
        return jinja2.Markup(code)

    # TODO include_js

    resources = {'metadata': {'name': 'name'}, # ???
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
        'include_input_prompt': True,
        'include_output_prompt': True,
        'no_prompt': False,
    }

    resources['include_css'] = resources_include_css

    return render_template('/lab/index.html.j2', nb=nb, resources=resources)

