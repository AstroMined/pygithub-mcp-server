"""
Coverage output parsing utilities.

This module contains functions for parsing coverage output
and converting it into structured data models.
"""

import re
from typing import List, Tuple

from .models import ModuleCoverage, CoverageReport


def parse_coverage_output(output: str) -> Tuple[List[ModuleCoverage], float, int, int]:
    """Parse coverage output into structured data.
    
    Args:
        output: The raw coverage output as text
        
    Returns:
        Tuple of (modules, overall_coverage, total_statements, total_missing)
    """
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
    """Generate a comprehensive coverage report from parsed data.
    
    Args:
        modules: List of module coverage data
        overall_coverage: Overall coverage percentage
        total_statements: Total statements in the codebase
        total_missing: Total missing statements
        
    Returns:
        A structured CoverageReport object
    """
    from datetime import datetime
    
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
