"""
Data models for coverage analysis.

This module contains the dataclasses that represent coverage data
and test failures for reporting purposes.
"""

from typing import List, Set, Dict, Any
from dataclasses import dataclass, field


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
    
    def to_dict(self) -> Dict[str, Any]:
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


@dataclass
class TestFailure:
    """Information about a test failure."""
    name: str
    outcome: str
    message: str
    duration: float = 0.0
    file: str = ""
    line: int = 0

    @property
    def category(self) -> str:
        """Classify the failure based on the error message."""
        if "SyntaxError" in self.message:
            return "syntax_error"
        elif "AssertionError" in self.message:
            return "assertion_failure"
        elif any(err in self.message for err in ["ImportError", "ModuleNotFoundError"]):
            return "import_error"
        elif "timeout" in self.message.lower():
            return "timeout_error"
        else:
            return "other"

    @property
    def module_name(self) -> str:
        """Extract module name from test path."""
        parts = self.name.split('::')[0].split('/')
        if len(parts) > 1:
            return parts[-1].replace('test_', '').replace('.py', '')
        return ""


def get_color_for_coverage(coverage: float) -> str:
    """Return an appropriate color for the given coverage percentage."""
    if coverage < 70:
        return "#d9534f"  # Red
    elif coverage < 85:
        return "#f0ad4e"  # Yellow
    else:
        return "#5cb85c"  # Green
