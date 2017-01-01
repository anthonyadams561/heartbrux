#!/usr/bin/env python

import os
import uuid
import numpy as np
import pandas as pd
from jinja2 import Template
from distutils.dir_util import copy_tree

# The width of the charts, in pixels
MAX_POINTS = 500

script_dir = os.path.dirname(os.path.abspath(__file__))


def create_page(page_name, plots):
    template = Template(get_file_contents(script_dir + '/templates/page.html'))
    return template.render(page_name=page_name, plots=plots)


def add_report_element(template_name, data, options):
    div_id = "element-" + str(uuid.uuid4()).replace("-", "")
    template = Template(get_file_contents(script_dir + '/templates/' + template_name + ".html"))
    return template.render(options=options, data=data, div_id=div_id)

def add_section_break():
    return "<hr>"


def write_file(path, contents):
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

    # Resample the data at various intervals
    resampled_by_minute = data.copy(deep=True).resample('1T').mean()

    resampled_by_quarter_hour = data.copy(deep=True).resample('15T').mean()
    resampled_by_quarter_hour.index = resampled_by_quarter_hour.index.strftime("%H:%M")

    resampled_by_hour = data.copy(deep=True).resample('1H').mean()
    resampled_by_hour.index = resampled_by_hour.index.hour

    # How many hours of data do we have
    time_delta = data.index[data.size - 1] - data.index[0]
    total_hours = time_delta / np.timedelta64(1, 'h')

    # Calculate the summary statistics
    summary_statistics = {}
    summary_statistics["headings"] = [
        "Hours", "Mean", "Median", "StDev"
    ]
    summary_statistics["rows"] = [
        [
            np.round(total_hours, 1),
            np.round(data.mean(), 1),
            np.round(data.median(), 1),
            np.round(data.std(), 1)
        ]
    ]

    # Create the plots
    plots = [
        add_report_element("simple_line", resampled_by_minute, {'report_element_name': 'All Data'}),
        add_report_element("table", summary_statistics, {'report_element_name': 'Summary Statistics'}),
        add_report_element("simple_bar", resampled_by_hour, {
            'report_element_name': 'Mean Heart Rate by Hour',
            'data_element_name': 'Heart Rate',
            'x_axis_label': 'Hour of the Day',
            'y_axis_label': 'Heart Rate (BPM)',
            'y_axis_max': resampled_by_hour.max(),
            'y_axis_min': resampled_by_hour.min() * 0.8
        }),
        add_report_element("simple_bar", resampled_by_quarter_hour, {
            'report_element_name': 'Mean Heart Rate every 15 Minutes',
            'data_element_name': 'Heart Rate',
            'x_axis_label': 'Time',
            'y_axis_label': 'Heart Rate (BPM)',
            'y_axis_max': resampled_by_quarter_hour.max(),
            'y_axis_min': resampled_by_quarter_hour.min() * 0.8
        })
    ]

    # Create the page
    report_date = data.index[0].to_pydatetime().strftime("%A, %B %-d, %Y")
    html = create_page(report_date, plots)
    write_file(output_dir + "/index.html", html)
