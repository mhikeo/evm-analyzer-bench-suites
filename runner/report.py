#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
top-level CLI to create an HTML benchmark report
"""

from pathlib import Path
import os, yaml, sys
from jinja2 import select_autoescape, Template

code_root_dir = Path(__file__).parent.resolve()
# Make relative loading work without relative import, which
# doesn't work with main programs
sys.path.insert(0, code_root_dir)

code_dir = Path(__file__).parent.resolve()

RGB_RED    = "rgba(255, 145, 164, .4)"
RGB_GREEN  = "rgba(80, 200, 120, .4)"
RGB_YELLOW = "rgba(253, 195, 83, .4)"
RGB_GREY   = "rgba(128, 128, 128, .4)"

def print_html_report(data, project_root_dir, suite):
    """
    Write an HTML analysis report for `suite`
    """
    eval_colors = {
        # Unsupported("rgba(255, 145, 164, .4)", "Unsupported"),
        'False Positive'     : RGB_RED,
        'False Negative'     : RGB_RED,
        'Errored'            : RGB_RED,
        'Wrong Vulnerability': RGB_RED,
        'True Positive'      : RGB_GREEN,
        'True Negative'      : RGB_GREEN,
        'Analysis Failed'    : RGB_YELLOW,
        'Ignored'            : RGB_YELLOW,
        'Timed Out'          : RGB_YELLOW,
        'Too Long'           : RGB_YELLOW,
        'Unconfigured'       : RGB_GREY,
    }

    html_dir = project_root_dir / 'html'
    suite_path = html_dir / suite
    os.makedirs(suite_path, exist_ok = True)
    jinja2_dir = project_root_dir / 'jinja2'
    template_path = jinja2_dir / 'report_template.html'
    t = Template(open(template_path).read(),
                 autoescape=select_autoescape(['html']),
                 trim_blocks=True)

    # Set up some variables for render
    t.globals = locals()
    html_path = suite_path / "index.html"

    open(html_path, 'w').write(t.render())

import pprint
pp = pprint.PrettyPrinter(indent=4)

analyzer = 'Mythril'
suite = 'Suhabe'
project_root_dir = code_dir.parent
suite_dir = project_root_dir / 'benchdata' / suite

# FIXME: loop over analyzers
yaml_file = suite_dir / (analyzer + ".yaml")
with open(yaml_file, 'r') as fp:
    try:
        data = yaml.load(fp)
        # pp.pprint(data)
    except yaml.YAMLError as exc:
        print(exc)

print_html_report(data, project_root_dir, suite)