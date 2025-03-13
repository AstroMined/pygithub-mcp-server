#!/usr/bin/env python
"""
Test Coverage Analyzer

This script runs coverage analysis on specified test modules and generates
detailed reports to aid in the migration from unit tests to integration tests.

Usage:
    python -m scripts.coverage.test_coverage_analyzer --unit-tests tests/unit/operations/test_repositories_ops.py
    python -m scripts.coverage.test_coverage_analyzer --compare-unit-integration

"""

import argparse
import os
import sys
import subprocess
import json
from pathlib import Path

def run_coverage(test_paths, output_dir="htmlcov", name="coverage"):
    """Run pytest with coverage on specified test paths."""
    cmd = [
        "pytest",
        "--cov=src/pygithub_mcp_server",
        f"--cov-report=html:{output_dir}/{name}",
        f"--cov-report=json:{output_dir}/{name}.json",
        "-v"
    ]
    cmd.extend(test_paths)
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error running tests:")
        print(result.stderr)
        return False
    
    print(result.stdout)
    return True

def analyze_coverage(coverage_json_path):
    """Analyze coverage data from a JSON file."""
    if not os.path.exists(coverage_json_path):
        print(f"Coverage file not found: {coverage_json_path}")
        return None
    
    with open(coverage_json_path, 'r') as f:
        coverage_data = json.load(f)
    
    total_statements = 0
    covered_statements = 0
    results = {}
    
    for file_path, file_data in coverage_data['files'].items():
        if file_path.startswith('src/pygithub_mcp_server'):
            total_statements += file_data['summary']['num_statements']
            covered_statements += file_data['summary']['covered_statements']
            
            results[file_path] = {
                'total_lines': file_data['summary']['num_statements'],
                'covered_lines': file_data['summary']['covered_statements'],
                'coverage_percent': file_data['summary']['percent_covered'],
                'missing_lines': file_data['missing_lines']
            }
    
    overall_coverage = 0
    if total_statements > 0:
        overall_coverage = (covered_statements / total_statements) * 100
    
    return {
        'overall_coverage': overall_coverage,
        'total_statements': total_statements,
        'covered_statements': covered_statements,
        'file_coverage': results
    }

def compare_coverage(unit_json_path, integration_json_path, output_file="coverage_comparison.md"):
    """Compare coverage between unit tests and integration tests."""
    unit_coverage = analyze_coverage(unit_json_path)
    integration_coverage = analyze_coverage(integration_json_path)
    
    if not unit_coverage or not integration_coverage:
        print("Unable to compare coverage - missing data")
        return
    
    output_path = os.path.join("htmlcov", output_file)
    
    with open(output_path, 'w') as f:
        f.write("# Test Coverage Comparison: Unit vs Integration\n\n")
        
        f.write("## Overall Coverage\n\n")
        f.write("| Test Type | Coverage % | Covered Statements | Total Statements |\n")
        f.write("|-----------|------------|--------------------|-----------------|\n")
        f.write(f"| Unit Tests | {unit_coverage['overall_coverage']:.2f}% | {unit_coverage['covered_statements']} | {unit_coverage['total_statements']} |\n")
        f.write(f"| Integration Tests | {integration_coverage['overall_coverage']:.2f}% | {integration_coverage['covered_statements']} | {integration_coverage['total_statements']} |\n\n")
        
        f.write("## Coverage Gaps\n\n")
        f.write("Files and lines covered by unit tests but not by integration tests:\n\n")
        
        for file_path, unit_data in unit_coverage['file_coverage'].items():
            integration_data = integration_coverage['file_coverage'].get(file_path, {})
            integration_missing = integration_data.get('missing_lines', [])
            unit_missing = unit_data.get('missing_lines', [])
            
            # Find lines covered by unit tests but not by integration tests
            coverage_gaps = [line for line in unit_missing if line not in integration_missing]
            
            if coverage_gaps:
                f.write(f"### {file_path}\n\n")
                f.write(f"Unit test coverage: {unit_data['coverage_percent']:.2f}%\n\n")
                f.write(f"Integration test coverage: {integration_data.get('coverage_percent', 0):.2f}%\n\n")
                f.write("Missing lines in integration tests: " + ", ".join(map(str, coverage_gaps)) + "\n\n")
    
    print(f"Coverage comparison written to {output_path}")

def analyze_specific_unit_tests(test_paths, output_dir="htmlcov"):
    """Analyze coverage for specific unit tests."""
    name = "unit_specific"
    if not run_coverage(test_paths, output_dir, name):
        return
    
    coverage_json_path = os.path.join(output_dir, f"{name}.json")
    coverage_data = analyze_coverage(coverage_json_path)
    
    if not coverage_data:
        return
    
    output_path = os.path.join(output_dir, f"{name}_analysis.md")
    
    with open(output_path, 'w') as f:
        test_names = [os.path.basename(path) for path in test_paths]
        f.write(f"# Coverage Analysis for {', '.join(test_names)}\n\n")
        
        f.write(f"Overall coverage: {coverage_data['overall_coverage']:.2f}%\n\n")
        f.write(f"Total statements: {coverage_data['total_statements']}\n")
        f.write(f"Covered statements: {coverage_data['covered_statements']}\n\n")
        
        f.write("## Coverage by File\n\n")
        f.write("| File | Coverage % | Covered Lines | Total Lines | Missing Lines |\n")
        f.write("|------|------------|--------------|-------------|---------------|\n")
        
        # Sort files by coverage percentage (ascending)
        sorted_files = sorted(
            coverage_data['file_coverage'].items(),
            key=lambda x: x[1]['coverage_percent']
        )
        
        for file_path, file_data in sorted_files:
            missing_lines = ', '.join(map(str, file_data['missing_lines'][:20]))
            if len(file_data['missing_lines']) > 20:
                missing_lines += f" ... ({len(file_data['missing_lines'])-20} more)"
                
            f.write(f"| {file_path} | {file_data['coverage_percent']:.2f}% | "
                    f"{file_data['covered_lines']} | {file_data['total_lines']} | "
                    f"{missing_lines} |\n")
    
    print(f"Coverage analysis written to {output_path}")
    
    # Generate test case summary
    generate_test_case_summary(test_paths, output_dir)

def generate_test_case_summary(test_paths, output_dir="htmlcov"):
    """Generate a summary of test cases that need to be replaced."""
    output_path = os.path.join(output_dir, "test_case_summary.md")
    
    with open(output_path, 'w') as f:
        f.write("# Test Cases to Replace with Integration Tests\n\n")
        
        for test_path in test_paths:
            if not os.path.exists(test_path):
                continue
                
            f.write(f"## {os.path.basename(test_path)}\n\n")
            
            with open(test_path, 'r') as test_file:
                content = test_file.read()
            
            # Extract test functions
            lines = content.split('\n')
            test_functions = []
            current_function = None
            function_lines = []
            
            for line in lines:
                if line.startswith("def test_") and "(" in line:
                    if current_function:
                        test_functions.append((current_function, function_lines))
                    current_function = line.split("def ")[1].split("(")[0]
                    function_lines = [line]
                elif current_function and line.strip():
                    function_lines.append(line)
            
            if current_function:
                test_functions.append((current_function, function_lines))
            
            # Write test function summary
            f.write("| Test Function | Description | Key Assertions |\n")
            f.write("|--------------|-------------|----------------|\n")
            
            for func_name, func_lines in test_functions:
                # Extract docstring if present
                description = "No description"
                for i, line in enumerate(func_lines):
                    if '"""' in line or "'''" in line:
                        if i+1 < len(func_lines):
                            description = func_lines[i+1].strip()
                            break
                
                # Extract assertions
                assertions = []
                for line in func_lines:
                    line = line.strip()
                    if line.startswith("assert "):
                        assertions.append(line)
                
                assertion_summary = "<br>".join(assertions[:3])
                if len(assertions) > 3:
                    assertion_summary += f"<br>... ({len(assertions)-3} more)"
                
                f.write(f"| {func_name} | {description} | {assertion_summary} |\n")
            
            f.write("\n")
    
    print(f"Test case summary written to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Test Coverage Analysis Tool")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--unit-tests', nargs='+', help='Analyze specific unit test files')
    group.add_argument('--integration-tests', nargs='+', help='Analyze specific integration test files')
    group.add_argument('--compare-unit-integration', action='store_true', 
                       help='Compare unit test and integration test coverage')
    
    args = parser.parse_args()
    
    # Ensure htmlcov directory exists
    os.makedirs("htmlcov", exist_ok=True)
    
    if args.unit_tests:
        analyze_specific_unit_tests(args.unit_tests)
    elif args.integration_tests:
        test_paths = args.integration_tests
        name = "integration_specific"
        run_coverage(test_paths, "htmlcov", name)
        coverage_json_path = os.path.join("htmlcov", f"{name}.json")
        analyze_coverage(coverage_json_path)
    elif args.compare_unit_integration:
        # Run unit tests with coverage
        run_coverage(['tests/unit/'], "htmlcov", "unit")
        
        # Run integration tests with coverage
        run_coverage(['tests/integration/'], "htmlcov", "integration")
        
        # Compare coverage
        unit_json_path = os.path.join("htmlcov", "unit.json")
        integration_json_path = os.path.join("htmlcov", "integration.json")
        compare_coverage(unit_json_path, integration_json_path)

if __name__ == "__main__":
    main()
