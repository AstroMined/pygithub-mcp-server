"""
Report generation utilities.

This module contains functions for generating various report formats
from coverage data, including HTML, JSON, and JUnit XML.
"""

import os
import sys
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Any

from .models import CoverageReport, TestFailure, get_color_for_coverage


def generate_html_report(report: CoverageReport, output_file: str, test_failures: Optional[List[TestFailure]] = None) -> None:
    """Generate an HTML report from the coverage data and test failures.
    
    Args:
        report: The coverage report object
        output_file: Path to save the HTML report (usually .html extension)
        test_failures: Optional list of test failures to include
    """
    # Check for Jinja2
    try:
        import jinja2
    except ImportError:
        print("Installing Jinja2...")
        import subprocess
        subprocess.run([sys.executable, "-m", "pip", "install", "jinja2"], 
                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        import jinja2
        
    html_file = output_file.replace('.json', '.html')
    
    # Set up Jinja2 environment
    template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates')
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
        
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    
    try:
        # Get template and render with context
        template = env.get_template('coverage_report.html')
        html_content = template.render(
            report=report,
            test_failures=test_failures or [],
            get_color_for_coverage=get_color_for_coverage
        )
        
        # Write output
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {html_file}")
    except jinja2.exceptions.TemplateNotFound:
        print(f"Error: Could not find template 'coverage_report.html' in {template_dir}")
        print("Please create the template file or check the path.")


def generate_json_report(report: CoverageReport, output_file: str) -> None:
    """Generate a JSON report from the coverage data.
    
    Args:
        report: The coverage report object
        output_file: Path to save the JSON report
    """
    report_dict = report.to_dict()
    
    with open(output_file, 'w') as f:
        json.dump(report_dict, f, indent=2)
    
    print(f"JSON report generated: {output_file}")


def generate_junit_xml(test_failures: List[TestFailure], output_file: str = "junit-report.xml") -> None:
    """Generate JUnit XML report from test failures for CI/CD systems.
    
    Args:
        test_failures: List of test failures to report
        output_file: Path to save the XML report
    """
    root = ET.Element("testsuites")
    testsuite = ET.SubElement(root, "testsuite", 
                             name="PyTest",
                             tests=str(len(test_failures)),
                             failures=str(len([f for f in test_failures if f.outcome == "failed"])),
                             errors=str(len([f for f in test_failures if f.outcome == "error"])),
                             skipped=str(len([f for f in test_failures if f.outcome == "skipped"])))
    
    for failure in test_failures:
        # Extract class and name from test ID
        parts = failure.name.split("::")
        classname = parts[0] if parts else "unknown"
        testname = "::".join(parts[1:]) if len(parts) > 1 else failure.name
        
        testcase = ET.SubElement(testsuite, "testcase", 
                                classname=classname,
                                name=testname,
                                time=str(failure.duration))
        
        if failure.outcome == "failed":
            fail = ET.SubElement(testcase, "failure", message=failure.message[:100])
            fail.text = failure.message
        elif failure.outcome == "error":
            error = ET.SubElement(testcase, "error", message=failure.message[:100])
            error.text = failure.message
        elif failure.outcome == "skipped":
            ET.SubElement(testcase, "skipped")
    
    tree = ET.ElementTree(root)
    tree.write(output_file)
    
    print(f"JUnit XML report generated: {output_file}")


def output_github_actions_annotations(test_failures: List[TestFailure]) -> None:
    """Output test failures as GitHub Actions annotations.
    
    Args:
        test_failures: List of test failures to report
    """
    for failure in test_failures:
        test_name = failure.name
        file_path = failure.file if failure.file else test_name
        line_num = failure.line if failure.line > 0 else 1
        
        # Format message for GitHub Actions
        message = f"::error file={file_path},line={line_num}::{test_name} - {failure.outcome}"
        print(message)
