"""
Coverage analysis tool main entry point.

This module provides the main entry point and CLI argument handling
for the coverage analysis tool. Run using:

    python -m scripts.coverage [options]
"""

import os
import sys
import argparse
import subprocess
from typing import List, Optional, Dict, Any

from .runner import run_coverage
from .parser import parse_coverage_output, generate_report
from .reports import (
    generate_html_report,
    generate_json_report,
    generate_junit_xml,
    output_github_actions_annotations
)


def main() -> int:
    """Main entry point for the coverage analysis tool."""
    parser = argparse.ArgumentParser(description="Analyze pytest coverage data and generate reports")
    parser.add_argument("--output", default="coverage_report.json", 
                        help="Output JSON file for the report (default: coverage_report.json)")
    parser.add_argument("--run-tests", action="store_true", 
                        help="Run pytest with coverage before analysis")
    parser.add_argument("--html", action="store_true", 
                        help="Generate HTML report in addition to JSON")
    parser.add_argument("--include-integration", action="store_true", 
                        help="Include integration tests in the coverage analysis")
    parser.add_argument("--threshold", type=float, 
                        help="Fail if coverage is below this percentage")
    parser.add_argument("--junit-xml", 
                        help="Generate JUnit XML report for CI/CD integration")
    parser.add_argument("--package-path", default="src/pygithub_mcp_server",
                        help="Path to the package to measure coverage for")
    
    args = parser.parse_args()
    
    # Collect and run tests if requested
    coverage_output = ""
    test_failures = []
    
    if args.run_tests:
        print(f"Running tests with coverage for {args.package_path}")
        coverage_output, test_failures = run_coverage(
            package_path=args.package_path,
            include_integration=args.include_integration
        )
    else:
        # Just generate coverage report from existing .coverage data
        if os.path.exists(".coverage"):
            result = subprocess.run(
                ["python", "-m", "coverage", "report", f"--include={args.package_path}/*"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            coverage_output = result.stdout
        else:
            print("No .coverage data found. Please run with --run-tests or run pytest with coverage first.")
            return 1
    
    # Parse the coverage output
    modules, overall_coverage, total_statements, total_missing = parse_coverage_output(coverage_output)
    
    if not modules:
        print("No modules found in coverage output. Make sure tests are running correctly.")
        return 1
    
    # Generate the report
    report = generate_report(modules, overall_coverage, total_statements, total_missing)
    
    # Print a summary to the console
    report.print_summary()
    
    # Generate JSON report
    generate_json_report(report, args.output)
    
    # Generate HTML report if requested
    if args.html:
        generate_html_report(report, args.output, test_failures)
    
    # Generate JUnit XML report if requested
    if args.junit_xml and test_failures:
        generate_junit_xml(test_failures, args.junit_xml)
    
    # Generate GitHub Actions annotations for failures
    if os.environ.get("GITHUB_ACTIONS") == "true" and test_failures:
        output_github_actions_annotations(test_failures)
    
    # Check coverage threshold if specified
    if args.threshold is not None and overall_coverage < args.threshold:
        print(f"❌ Coverage ({overall_coverage:.2f}%) is below the threshold ({args.threshold}%)")
        return 2
    
    print(f"✅ Analysis completed successfully. Overall coverage: {overall_coverage:.2f}%")
    return 0


if __name__ == "__main__":
    sys.exit(main())
