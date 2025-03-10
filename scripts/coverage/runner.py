"""
Test collection and execution with coverage.

This module handles collecting pytest tests and running them with coverage.
"""

import os
import re
import sys
import json
import subprocess
from typing import List, Dict, Tuple, Any
from datetime import datetime

from .models import TestFailure

def get_file_from_nodeid(nodeid: str) -> str:
    """Extract file path from pytest nodeid."""
    return nodeid.split("::")[0] if "::" in nodeid else nodeid

def get_line_from_location(location: str) -> int:
    """Extract line number from pytest location string."""
    try:
        return int(location.split(":")[-1]) if ":" in location else 0
    except ValueError:
        return 0

def collect_tests(include_integration: bool = False) -> List[str]:
    """
    Collect all test nodeids.
    
    Args:
        include_integration: Whether to include integration tests
        
    Returns:
        List of test nodeids
    """
    print("Collecting tests... ")
    
    # First collect all tests to get a count
    collect_cmd = ["python", "-m", "pytest", "tests", "--collect-only", "-q"]
    if include_integration:
        collect_cmd.append("--run-integration")
    else:
        collect_cmd.extend(["-m", "not integration"])
    
    # print(f"Debug: Collection command: {' '.join(collect_cmd)}")
    
    try:
        result = subprocess.run(collect_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Show collection output for debugging
        print(f"Collection output: {result.stdout.strip()}")
        if result.stderr:
            print(f"Collection stderr: {result.stderr.strip()}")
        
        # Each line in the output should be a test ID in the quiet mode
        test_list = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        
        # Count total tests
        total_tests = len(test_list)
        
        # Print the test count for info
        print(f"Collected {total_tests} Tests")
        
        return test_list
    
    except Exception as e:
        print(f"Error during test collection: {e}")
        return []

def group_tests_by_module(test_list: List[str]) -> Dict[str, Dict]:
    """
    Group a list of tests by their module.
    
    Args:
        test_list: List of test nodeids
        
    Returns:
        Dictionary mapping module names to test information
    """
    modules = {}
    ungrouped_tests = []
    
    for test_path in test_list:
        if not test_path:
            continue
            
        # Extract the module part of the test path
        parts = test_path.split('::')
        
        if len(parts) > 0:
            # Get module path - categorize by directory and file
            test_path = parts[0]
            
            # Extract the category from path
            if '/' in test_path:
                path_parts = test_path.split('/')
                if len(path_parts) >= 3 and path_parts[0] == "tests":
                    # Create a key based on the full path excluding "tests/" and the filename
                    # E.g., "unit/schemas/repositories" or "integration/operations/issues"
                    module_key = '/'.join(path_parts[1:-1])  # Exclude filename
                    module_name = ' '.join(part.capitalize() for part in path_parts[1:-1])
                    
                    # Add to modules dictionary with count
                    if module_key not in modules:
                        modules[module_key] = {
                            "name": module_name,
                            "tests": [],
                        }
                    
                    modules[module_key]["tests"].append(test_path)
                else:
                    # Keep track of tests that don't fit the expected structure
                    ungrouped_tests.append(test_path)
            else:
                # Keep track of tests without path separators (unlikely but possible)
                ungrouped_tests.append(test_path)
    
    # Add ungrouped tests as a separate module if there are any
    if ungrouped_tests:
        modules["other"] = {
            "name": "Other Tests",
            "tests": ungrouped_tests,
        }
    
    # Add counts to each module
    for key in modules:
        modules[key]["count"] = len(modules[key]["tests"])
        
    return modules

def run_module_tests(module_name: str, test_files: List[str], package_path: str, include_integration: bool) -> Tuple[str, List[TestFailure], int]:
    """
    Run tests for a specific module with coverage.
    
    Args:
        module_name: Human-readable name of the module
        test_files: List of test files to run
        package_path: Path to the package to measure coverage for
        include_integration: Whether to run integration tests
        
    Returns:
        Tuple of (output, failures, test_count)
    """
    print(f"Running {module_name} Tests ({len(test_files)})")
    
    # Build the test command for this module
    module_cmd = [
        "python", "-m", "pytest",
        f"--cov={package_path}",
        "--cov-append",  # Append to coverage data for each module
        "--json-report",
        f"--json-report-file=test_results.json",
    ]
    
    # Add test files to the command
    module_cmd.extend(test_files)
    
    if include_integration:
        module_cmd.append("--run-integration")
        
    # print(f"Debug: Running module command: {' '.join(module_cmd)}")
    
    # Run tests for this module
    start_time = datetime.now()
    result = subprocess.run(
        module_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    end_time = datetime.now()
    elapsed = (end_time - start_time).total_seconds()
    
    return_code = result.returncode
    print(f"Module tests completed in {elapsed:.1f} seconds (Return code: {return_code})")
    
    # If output is too long, truncate it
    output_sample = (result.stdout + result.stderr)
    if len(output_sample) > 500:
        output_sample = output_sample[:500] + "... [truncated]"
        
    if return_code != 0 and return_code != 5:  # 5 is test failures
        print(f"Warning: Module tests returned non-zero exit code. Output sample:\n{output_sample}")
    
    # Parse failures for this module
    failures = []
    try:
        if os.path.exists("test_results.json"):
            with open("test_results.json") as f:
                test_results = json.load(f)
            
            for test in test_results.get("tests", []):
                if test.get("outcome") != "passed":
                    # Create failure record
                    failure = TestFailure(
                        name=test.get("nodeid", "Unknown"),
                        outcome=test.get("outcome", "error"),
                        message=test.get("call", {}).get("longrepr", "No details available"),
                        duration=test.get("duration", 0.0),
                        file=get_file_from_nodeid(test.get("nodeid", "")),
                        line=get_line_from_location(test.get("location", ""))
                    )
                    failures.append(failure)
            
            if failures:
                print(f"Found {len(failures)} test failures in this module")
    except Exception as e:
        print(f"Error parsing test failures for module {module_name}: {e}")
        
    return output_sample, failures, len(test_files)

def run_coverage(package_path: str = "src/pygithub_mcp_server", include_integration: bool = False) -> Tuple[str, List[TestFailure]]:
    """
    Run pytest with coverage and return the output and test failures.
    
    Args:
        package_path: Path to the package to measure coverage for
        include_integration: Whether to run integration tests
        
    Returns:
        Tuple of (coverage_output, test_failures)
    """
    # Install required dependencies if needed
    subprocess.run(["python", "-m", "pip", "install", "--quiet", "--upgrade", 
                   "pytest", "pytest-cov", "pytest-json-report"],
                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Clear any existing coverage data
    if os.path.exists(".coverage"):
        os.remove(".coverage")
        
    # Collect tests
    test_list = collect_tests(include_integration)
    
    if not test_list:
        print("No tests found or test collection failed!")
        return "", []
    
    total_tests = len(test_list)
    print(f"Collected {total_tests} Tests")
    
    # Group tests by module
    modules = group_tests_by_module(test_list)
    
    # Debug: Print grouping information
    print("\nTest grouping debug info:")
    print(f"Total tests collected: {total_tests}")
    grouped_tests = sum(module_info["count"] for module_info in modules.values())
    print(f"Tests assigned to groups: {grouped_tests}")
    print(f"Number of test groups: {len(modules)}")
    if grouped_tests < total_tests:
        print(f"Warning: {total_tests - grouped_tests} tests were not assigned to any group!")
    print("Groups created:")
    for key in sorted(modules.keys()):
        print(f"  {key}: {modules[key]['count']} tests")
    print("")
    
    if not modules:
        print("Warning: Could not group tests by module. Running all tests at once.")
        # Fallback to running all tests at once
        all_cmd = [
            "python", "-m", "pytest",
            "tests/",
            f"--cov={package_path}",
            "--cov-report=term",  # Don't use term-missing to avoid stdout clutter
            "--json-report",
            f"--json-report-file=test_results.json",
        ]
        
        if include_integration:
            all_cmd.append("--run-integration")
            
        # print(f"Debug: Running fallback command: {' '.join(all_cmd)}")
        
        result = subprocess.run(
            all_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Print return code to help debug issues
        print(f"Return code: {result.returncode}")
        
        # If there's an error, show a sample of the output to help diagnose
        if result.returncode != 0:
            output_sample = result.stdout + result.stderr
            if len(output_sample) > 500:
                output_sample = output_sample[:500] + "... [truncated]"
            print(f"Command output sample:\n{output_sample}")
        
        # Generate coverage report
        cov_report = subprocess.run(
            ["python", "-m", "coverage", "report", f"--include={package_path}/*"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Parse failures
        failures = []
        try:
            if os.path.exists("test_results.json"):
                with open("test_results.json") as f:
                    test_results = json.load(f)
                
                for test in test_results.get("tests", []):
                    if test.get("outcome") != "passed":
                        # Create failure record
                        failure = TestFailure(
                            name=test.get("nodeid", "Unknown"),
                            outcome=test.get("outcome", "error"),
                            message=test.get("call", {}).get("longrepr", "No details available"),
                            duration=test.get("duration", 0.0),
                            file=get_file_from_nodeid(test.get("nodeid", "")),
                            line=get_line_from_location(test.get("location", ""))
                        )
                        failures.append(failure)
                
                if failures:
                    print(f"Found {len(failures)} test failures")
        except Exception as e:
            print(f"Error parsing test failures: {e}")
            
        return cov_report.stdout, failures
    
    # Run tests module by module with coverage
    all_output = ""
    all_failures = []
    tests_completed = 0
    
    for module_key, module_info in modules.items():
        module_name = module_info["name"]
        test_list = module_info["tests"]
        
        # Run tests for this module
        output, failures, test_count = run_module_tests(
            module_name,
            test_list,
            package_path,
            include_integration
        )
        
        # Add failures to the list
        all_failures.extend(failures)
        
        # Update progress
        tests_completed += test_count
        print(f"{tests_completed} of {total_tests} Tests Complete")
    
    # Generate a final coverage report
    print("Generating final coverage report...")
    cov_report_cmd = [
        "python", "-m", "coverage", "report",
        f"--include={package_path}/*"
    ]
    
    final_result = subprocess.run(
        cov_report_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    all_output = final_result.stdout
    
    print(f"All tests completed. Total failures: {len(all_failures)}")
    return all_output, all_failures
