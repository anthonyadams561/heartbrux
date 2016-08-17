#!/usr/bin/env python

import os
import uuid
from jinja2 import Template
from distutils.dir_util import copy_tree

# The width of the charts, in pixels
MAX_POINTS = 500

script_dir = os.path.dirname(os.path.abspath(__file__))


def create_page(page_name, plots):
    template = Template(get_file_contents(script_dir + '/templates/page.html'))
    return template.render(page_name=page_name, plots=plots)


def create_plot(template_name, plot_name, data):
    div_id = "plot-" + str(uuid.uuid4()).replace("-", "")
    template = Template(get_file_contents(script_dir + '/templates/' + template_name + ".html"))
    return template.render(plot_name=plot_name, data=data, div_id=div_id)


def write_to_file(path, contents):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    f = open(path, "w")
    f.write(contents)
    f.close()


def get_file_contents(path):
    f = open(path, "r")
    contents = f.read()
    f.close()
    return contents


def generate_report(data, output_dir):
    # If the specified directory doesn't exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Copy dependencies to the build directory
    copy_tree(script_dir + "/templates/dependencies", output_dir)

    # Create the plots
    plots = [
        create_plot("simple_line", "All Data", data),
        create_plot("simple_line", "First 30 Min", data[0:30]),
        create_plot("simple_line", "More Good Stuff", data[30:75])
    ]

    # Create the page
    html = create_page("Today", plots)
    write_to_file(output_dir + "/index.html", html)

