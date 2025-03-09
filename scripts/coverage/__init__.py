"""
Coverage analysis package for pytest-based test suites.

This package provides utilities for running tests with coverage analysis,
parsing coverage output, and generating reports in various formats.

Usage:
    # Run the tool directly
    python -m scripts.coverage [options]

    # Import and use programmatically
    from scripts.coverage.runner import run_coverage
    from scripts.coverage.parser import parse_coverage_output, generate_report
    from scripts.coverage.reports import generate_html_report, generate_json_report
"""

from .models import ModuleCoverage, ModulePriority, CoverageReport, TestFailure
from .runner import run_coverage, collect_tests, group_tests_by_module, run_module_tests
from .parser import parse_coverage_output, generate_report 
from .reports import generate_html_report, generate_json_report, generate_junit_xml, output_github_actions_annotations

__all__ = [
    'ModuleCoverage', 'ModulePriority', 'CoverageReport', 'TestFailure',
    'run_coverage', 'collect_tests', 'group_tests_by_module', 'run_module_tests',
    'parse_coverage_output', 'generate_report',
    'generate_html_report', 'generate_json_report', 'generate_junit_xml', 'output_github_actions_annotations',
]
