from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")


@app.route('/')
def hello_world():
    return render_template('/lab/index.html.j2', nb={})


@app.template_filter()
def highlight_code(text):
    return None

@app.template_filter()
def strip_files_prefix(text):
    return None

@app.template_filter()
def markdown2html(text):
    return None

@app.template_filter()
def ansi2html(text):
    return None

@app.template_filter()
def posix_path(text):
    return None

@app.template_filter()
def get_metadata(text):
    return None

@app.template_filter()
def filter_data_type(text):
    return None

@app.template_filter()
def json_dumps(text):
    return None

