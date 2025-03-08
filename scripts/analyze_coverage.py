#!/usr/bin/env python3
"""
Coverage Analysis Tool

This script analyzes pytest coverage output to identify testing priorities and produce
a detailed report of which modules and specific lines need testing attention.

Usage:
    python scripts/analyze_coverage.py [--output coverage_report.json] [--run-tests]

Options:
    --output FILE    Output JSON file for the report (default: coverage_report.json)
    --run-tests      Run pytest with coverage before analysis (default: use existing .coverage)
    --html           Generate HTML report in addition to JSON
    --threshold PCT  Fail if coverage is below this percentage (default: none)
"""

import os
import re
import sys
import json
import argparse
import subprocess
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime


# ANSI color codes for terminal output
COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "reset": "\033[0m",
    "bold": "\033[1m",
}


@dataclass
class ModuleCoverage:
    """Coverage information for a module."""
    name: str
    statements: int
    missing: int
    branches: int
    branch_missing: int 
    coverage: float
    missing_lines: str
    
    # Additional processed fields
    missing_line_ranges: List[str] = field(default_factory=list)
    parsed_missing_lines: Set[int] = field(default_factory=set)
    
    @property
    def priority(self) -> str:
        """Determine testing priority based on coverage."""
        if self.coverage < 70:
            return "High"
        elif self.coverage < 85: 
            return "Medium"
        else:
            return "Low"
    
    @property
    def priority_color(self) -> str:
        """Get color for priority level."""
        if self.priority == "High":
            return COLORS["red"]
        elif self.priority == "Medium":
            return COLORS["yellow"]
        else:
            return COLORS["green"]
    
    def parse_missing_lines(self) -> None:
        """Parse missing lines string into a set of individual line numbers and ranges."""
        if not self.missing_lines:
            self.parsed_missing_lines = set()
            return
            
        parts = self.missing_lines.split(", ")
        line_set = set()
        range_list = []
        
        for part in parts:
            # Handle ranges like "10-20"
            if "->" in part:
                # Handle branch coverage notation "10->12"
                start, end = part.split("->")
                line_set.add(int(start))
                range_list.append(f"{start} (branch)")
            elif "-" in part:
                # Handle line ranges "10-20"
                start, end = part.split("-")
                line_set.update(range(int(start), int(end) + 1))
                range_list.append(f"{start}-{end}")
            else:
                # Handle individual lines
                try:
                    line_set.add(int(part))
                except ValueError:
                    # Skip any non-integer parts
                    pass
        
        self.parsed_missing_lines = line_set
        self.missing_line_ranges = range_list


@dataclass
class ModulePriority:
    """Priority group for modules."""
    name: str
    modules: List[ModuleCoverage] = field(default_factory=list)
    
    @property
    def count(self) -> int:
        return len(self.modules)
    
    @property 
    def total_missing_lines(self) -> int:
        return sum(m.missing for m in self.modules)


@dataclass
class CoverageReport:
    """Complete coverage analysis report."""
    timestamp: str
    overall_coverage: float
    total_statements: int
    total_missing: int
    modules_count: int
    high_priority: ModulePriority = field(default_factory=lambda: ModulePriority("High"))
    medium_priority: ModulePriority = field(default_factory=lambda: ModulePriority("Medium"))
    low_priority: ModulePriority = field(default_factory=lambda: ModulePriority("Low"))
    
    def add_module(self, module: ModuleCoverage) -> None:
        """Add a module to the appropriate priority group."""
        if module.priority == "High":
            self.high_priority.modules.append(module)
        elif module.priority == "Medium":
            self.medium_priority.modules.append(module)
        else:
            self.low_priority.modules.append(module)
    
    def sort_modules(self) -> None:
        """Sort modules within each priority group by coverage (ascending)."""
        self.high_priority.modules.sort(key=lambda m: (m.coverage, m.name))
        self.medium_priority.modules.sort(key=lambda m: (m.coverage, m.name))
        self.low_priority.modules.sort(key=lambda m: (m.coverage, m.name))
    
    def to_dict(self) -> Dict:
        """Convert the report to a dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "summary": {
                "overall_coverage": self.overall_coverage,
                "total_statements": self.total_statements,
                "total_missing": self.total_missing,
                "modules_count": self.modules_count,
                "high_priority_count": self.high_priority.count,
                "medium_priority_count": self.medium_priority.count,
                "low_priority_count": self.low_priority.count,
            },
            "high_priority_modules": [
                {
                    "name": m.name,
                    "coverage": m.coverage,
                    "statements": m.statements,
                    "missing": m.missing,
                    "missing_lines": m.missing_lines,
                    "parsed_lines": list(m.parsed_missing_lines),
                    "missing_ranges": m.missing_line_ranges
                }
                for m in self.high_priority.modules
            ],
            "medium_priority_modules": [
                {
                    "name": m.name,
                    "coverage": m.coverage,
                    "statements": m.statements,
                    "missing": m.missing,
                    "missing_lines": m.missing_lines,
                    "parsed_lines": list(m.parsed_missing_lines),
                    "missing_ranges": m.missing_line_ranges
                }
                for m in self.medium_priority.modules
            ],
            "low_priority_modules": [
                {
                    "name": m.name,
                    "coverage": m.coverage,
                    "statements": m.statements,
                    "missing": m.missing,
                    "missing_lines": m.missing_lines,
                    "parsed_lines": list(m.parsed_missing_lines),
                    "missing_ranges": m.missing_line_ranges
                }
                for m in self.low_priority.modules
            ]
        }
    
    def print_summary(self) -> None:
        """Print a colorful summary of the coverage report to the console."""
        print(f"\n{COLORS['bold']}=== Coverage Analysis Report ==={COLORS['reset']}")
        print(f"Generated on: {self.timestamp}")
        print(f"Overall coverage: {self.overall_coverage_colored}")
        print(f"Total statements: {self.total_statements}")
        print(f"Missing statements: {self.total_missing}")
        print(f"Total modules: {self.modules_count}")
        print(f"\n{COLORS['bold']}Priority Groups:{COLORS['reset']}")
        print(f"  {COLORS['red']}High Priority{COLORS['reset']}: {self.high_priority.count} modules ({self.high_priority.total_missing_lines} missing lines)")
        print(f"  {COLORS['yellow']}Medium Priority{COLORS['reset']}: {self.medium_priority.count} modules ({self.medium_priority.total_missing_lines} missing lines)")
        print(f"  {COLORS['green']}Low Priority{COLORS['reset']}: {self.low_priority.count} modules ({self.low_priority.total_missing_lines} missing lines)")
        
        if self.high_priority.count > 0:
            print(f"\n{COLORS['bold']}{COLORS['red']}Top High Priority Modules:{COLORS['reset']}")
            for module in self.high_priority.modules[:5]:  # Only show top 5
                print(f"  {module.name}: {module.coverage}% coverage ({module.missing} missing lines)")
                
        if self.medium_priority.count > 0:
            print(f"\n{COLORS['bold']}{COLORS['yellow']}Top Medium Priority Modules:{COLORS['reset']}")
            for module in self.medium_priority.modules[:5]:  # Only show top 5
                print(f"  {module.name}: {module.coverage}% coverage ({module.missing} missing lines)")
    
    @property
    def overall_coverage_colored(self) -> str:
        """Get the overall coverage percentage with appropriate color."""
        if self.overall_coverage < 70:
            return f"{COLORS['red']}{self.overall_coverage:.2f}%{COLORS['reset']}"
        elif self.overall_coverage < 85:
            return f"{COLORS['yellow']}{self.overall_coverage:.2f}%{COLORS['reset']}"
        else:
            return f"{COLORS['green']}{self.overall_coverage:.2f}%{COLORS['reset']}"


def run_coverage(package_path: str = "src/pygithub_mcp_server", include_integration: bool = False) -> str:
    """
    Run pytest with coverage and return the output.
    
    Args:
        package_path: Path to the package to measure coverage for
        include_integration: Whether to run integration tests
        
    Returns:
        The combined stdout and stderr from the coverage run
    """
    if include_integration:
        print("Running unit AND integration tests with coverage... This may take a moment.")
    else:
        print("Running unit tests with coverage... This may take a moment.")
    
    # First, make sure we're using the latest pytest and coverage
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "pytest", "pytest-cov"], 
                  stdout=subprocess.PIPE, 
                  stderr=subprocess.PIPE)
    
    # Build command with optional integration tests flag
    command = ["python", "-m", "pytest", f"--cov={package_path}", "--cov-report=term-missing"]
    if include_integration:
        command.append("--run-integration")
    
    # Run pytest with coverage
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # If tests fail, we still want to analyze coverage
    if result.returncode != 0:
        print(f"Warning: Tests completed with exit code {result.returncode}")
    
    # Combine stdout and stderr to catch all coverage output
    output = result.stdout + result.stderr
    return output


def parse_coverage_output(output: str) -> Tuple[List[ModuleCoverage], float, int, int]:
    """Parse coverage output into structured data."""
    modules = []
    total_statements = 0
    total_missing = 0
    overall_coverage = 0.0
    
    # Look for the TOTAL line to get overall stats
    total_pattern = r"TOTAL\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+%)"
    total_match = re.search(total_pattern, output)
    
    if total_match:
        total_statements = int(total_match.group(1))
        total_missing = int(total_match.group(2))
        coverage_str = total_match.group(5).strip('%')
        overall_coverage = float(coverage_str)
    
    # Extract module lines
    module_pattern = r"(src/pygithub_mcp_server/[^\s]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+%)\s*(.*)"
    
    for line in output.split('\n'):
        match = re.match(module_pattern, line)
        if match:
            name, stmts, miss, branch, bpart, cover, missing = match.groups()
            coverage = int(cover.strip('%'))
            
            module = ModuleCoverage(
                name=name,
                statements=int(stmts),
                missing=int(miss),
                branches=int(branch),
                branch_missing=int(bpart),
                coverage=coverage,
                missing_lines=missing.strip() if missing else ""
            )
            
            # Parse missing lines for easier processing
            module.parse_missing_lines()
            
            modules.append(module)
    
    return modules, overall_coverage, total_statements, total_missing


def generate_report(modules: List[ModuleCoverage], overall_coverage: float, 
                   total_statements: int, total_missing: int) -> CoverageReport:
    """Generate a comprehensive coverage report."""
    # Create the base report
    report = CoverageReport(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        overall_coverage=overall_coverage,
        total_statements=total_statements,
        total_missing=total_missing,
        modules_count=len(modules)
    )
    
    # Add modules to appropriate priority groups
    for module in modules:
        report.add_module(module)
    
    # Sort modules in each priority group
    report.sort_modules()
    
    return report


def generate_html_report(report: CoverageReport, output_file: str) -> None:
    """Generate an HTML report from the coverage data."""
    html_file = output_file.replace('.json', '.html')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Coverage Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .summary {{ display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 30px; }}
        .summary-item {{ background: #f5f5f5; padding: 15px; border-radius: 5px; flex: 1; min-width: 200px; }}
        .high {{ color: #d9534f; }}
        .medium {{ color: #f0ad4e; }}
        .low {{ color: #5cb85c; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #f5f5f5; }}
        .progress-bar {{
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 5px;
        }}
        .progress-value {{
            height: 100%;
            border-radius: 10px;
        }}
        .priority-high {{ background-color: #ffeeed; }}
        .priority-medium {{ background-color: #fff8ee; }}
        .priority-low {{ background-color: #efffee; }}
        .module-details {{ display: none; padding: 10px; background: #f9f9f9; border-left: 5px solid #ddd; margin: 10px 0; }}
        .toggle-details {{ cursor: pointer; color: #0066cc; user-select: none; }}
        .toggle-details:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Coverage Analysis Report</h1>
        <p>Generated on: {report.timestamp}</p>
        
        <div class="summary">
            <div class="summary-item">
                <h3>Overall Coverage</h3>
                <div class="progress-bar">
                    <div class="progress-value" style="width: {report.overall_coverage}%; background-color: {get_color_for_coverage(report.overall_coverage)};"></div>
                </div>
                <p>{report.overall_coverage:.2f}%</p>
            </div>
            
            <div class="summary-item">
                <h3>Statements</h3>
                <p>{report.total_statements} total / {report.total_missing} missing</p>
            </div>
            
            <div class="summary-item">
                <h3>Priority Distribution</h3>
                <p><span class="high">■</span> High: {report.high_priority.count} modules</p>
                <p><span class="medium">■</span> Medium: {report.medium_priority.count} modules</p>
                <p><span class="low">■</span> Low: {report.low_priority.count} modules</p>
            </div>
        </div>
"""

    # Add High Priority Modules section
    if report.high_priority.count > 0:
        html_content += f"""
        <h2 class="high">High Priority Modules</h2>
        <table>
            <tr>
                <th>Module</th>
                <th>Coverage</th>
                <th>Missing / Total</th>
                <th>Details</th>
            </tr>
"""
        for i, module in enumerate(report.high_priority.modules):
            html_content += f"""
            <tr class="priority-high">
                <td>{module.name}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-value" style="width: {module.coverage}%; background-color: {get_color_for_coverage(module.coverage)};"></div>
                    </div>
                    {module.coverage}%
                </td>
                <td>{module.missing} / {module.statements}</td>
                <td><span class="toggle-details" onclick="toggleDetails('high-{i}')">Show Details</span></td>
            </tr>
            <tr>
                <td colspan="4">
                    <div id="high-{i}" class="module-details">
                        <p><strong>Missing Lines:</strong> {module.missing_lines}</p>
                        <p><strong>Ranges:</strong> {', '.join(module.missing_line_ranges) if module.missing_line_ranges else 'None'}</p>
                    </div>
                </td>
            </tr>
"""
        html_content += "</table>"

    # Add Medium Priority Modules section
    if report.medium_priority.count > 0:
        html_content += f"""
        <h2 class="medium">Medium Priority Modules</h2>
        <table>
            <tr>
                <th>Module</th>
                <th>Coverage</th>
                <th>Missing / Total</th>
                <th>Details</th>
            </tr>
"""
        for i, module in enumerate(report.medium_priority.modules):
            html_content += f"""
            <tr class="priority-medium">
                <td>{module.name}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-value" style="width: {module.coverage}%; background-color: {get_color_for_coverage(module.coverage)};"></div>
                    </div>
                    {module.coverage}%
                </td>
                <td>{module.missing} / {module.statements}</td>
                <td><span class="toggle-details" onclick="toggleDetails('medium-{i}')">Show Details</span></td>
            </tr>
            <tr>
                <td colspan="4">
                    <div id="medium-{i}" class="module-details">
                        <p><strong>Missing Lines:</strong> {module.missing_lines}</p>
                        <p><strong>Ranges:</strong> {', '.join(module.missing_line_ranges) if module.missing_line_ranges else 'None'}</p>
                    </div>
                </td>
            </tr>
"""
        html_content += "</table>"

    # Add Low Priority Modules section (collapsed by default)
    if report.low_priority.count > 0:
        html_content += f"""
        <h2 class="low">Low Priority Modules <span class="toggle-details" onclick="toggleLowPriority()">Show</span></h2>
        <div id="low-priority-section" style="display: none;">
        <table>
            <tr>
                <th>Module</th>
                <th>Coverage</th>
                <th>Missing / Total</th>
                <th>Details</th>
            </tr>
"""
        for i, module in enumerate(report.low_priority.modules):
            html_content += f"""
            <tr class="priority-low">
                <td>{module.name}</td>
                <td>
                    <div class="progress-bar">
                        <div class="progress-value" style="width: {module.coverage}%; background-color: {get_color_for_coverage(module.coverage)};"></div>
                    </div>
                    {module.coverage}%
                </td>
                <td>{module.missing} / {module.statements}</td>
                <td><span class="toggle-details" onclick="toggleDetails('low-{i}')">Show Details</span></td>
            </tr>
            <tr>
                <td colspan="4">
                    <div id="low-{i}" class="module-details">
                        <p><strong>Missing Lines:</strong> {module.missing_lines}</p>
                        <p><strong>Ranges:</strong> {', '.join(module.missing_line_ranges) if module.missing_line_ranges else 'None'}</p>
                    </div>
                </td>
            </tr>
"""
        html_content += """
        </table>
        </div>
"""

    # Add JavaScript and close HTML
    html_content += """
        <script>
            function toggleDetails(id) {
                const element = document.getElementById(id);
                if (element.style.display === 'none' || !element.style.display) {
                    element.style.display = 'block';
                } else {
                    element.style.display = 'none';
                }
            }
            
            function toggleLowPriority() {
                const section = document.getElementById('low-priority-section');
                const button = document.querySelector('h2.low .toggle-details');
                if (section.style.display === 'none') {
                    section.style.display = 'block';
                    button.textContent = 'Hide';
                } else {
                    section.style.display = 'none';
                    button.textContent = 'Show';
                }
            }
        </script>
    </div>
</body>
</html>
"""

    with open(html_file, 'w') as f:
        f.write(html_content)
    
    print(f"HTML report generated: {html_file}")


def get_color_for_coverage(coverage: float) -> str:
    """Return an appropriate color for the given coverage percentage."""
    if coverage < 70:
        return "#d9534f"  # Red
    elif coverage < 85:
        return "#f0ad4e"  # Yellow
    else:
        return "#5cb85c"  # Green


def main() -> int:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Analyze pytest coverage and identify priority areas.")
    parser.add_argument("--output", default="coverage_report.json", help="Output JSON file for the report")
    parser.add_argument("--run-tests", action="store_true", help="Run pytest with coverage before analysis")
    parser.add_argument("--include-integration", action="store_true", help="Include integration tests in coverage analysis")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    parser.add_argument("--threshold", type=float, help="Fail if coverage is below this percentage")
    
    args = parser.parse_args()
    
    # Get coverage data
    if args.run_tests:
        output = run_coverage(include_integration=args.include_integration)
    else:
        # Check if .coverage file exists
        if not os.path.exists(".coverage"):
            print("No .coverage file found. Run with --run-tests to generate one.")
            return 1
        
        # Convert .coverage to terminal output format
        print("Using existing .coverage file...")
        output = subprocess.run(
            ["python", "-m", "coverage", "report", "--include=src/pygithub_mcp_server/*"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        ).stdout
    
    # Parse the coverage output
    modules, overall_coverage, total_statements, total_missing = parse_coverage_output(output)
    
    if not modules:
        print("No coverage data found. Make sure tests are running correctly.")
        return 1
    
    # Generate the report
    report = generate_report(modules, overall_coverage, total_statements, total_missing)
    
    # Save the report to JSON
    with open(args.output, "w") as f:
        json.dump(report.to_dict(), f, indent=2)
    
    print(f"Coverage report saved to {args.output}")
    
    # Generate HTML report if requested
    if args.html:
        generate_html_report(report, args.output)
    
    # Print a summary to the console
    report.print_summary()
    
    # Check threshold if specified
    if args.threshold is not None and overall_coverage < args.threshold:
        print(f"\n{COLORS['red']}Error: Coverage {overall_coverage:.2f}% is below threshold {args.threshold}%{COLORS['reset']}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
