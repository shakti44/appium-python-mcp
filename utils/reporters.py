"""Test reporters for automation results."""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field


@dataclass
class TestResult:
    """Test result data structure."""
    name: str
    status: str  # passed, failed, skipped
    duration: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None
    logs: List[str] = field(default_factory=list)


@dataclass
class TestSuite:
    """Test suite data structure."""
    name: str
    tests: List[TestResult] = field(default_factory=list)
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    ended_at: Optional[str] = None
    
    @property
    def total_tests(self) -> int:
        """Get total number of tests."""
        return len(self.tests)
    
    @property
    def passed(self) -> int:
        """Get number of passed tests."""
        return sum(1 for t in self.tests if t.status == "passed")
    
    @property
    def failed(self) -> int:
        """Get number of failed tests."""
        return sum(1 for t in self.tests if t.status == "failed")
    
    @property
    def skipped(self) -> int:
        """Get number of skipped tests."""
        return sum(1 for t in self.tests if t.status == "skipped")
    
    @property
    def total_duration(self) -> float:
        """Get total duration of all tests."""
        return sum(t.duration for t in self.tests)


class JSONReporter:
    """JSON test reporter."""
    
    def __init__(self, output_dir: Path):
        """
        Initialize JSON reporter.
        
        Args:
            output_dir: Directory for report output
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, test_suite: TestSuite) -> Path:
        """
        Generate JSON report.
        
        Args:
            test_suite: Test suite to report
            
        Returns:
            Path to generated report
        """
        report_path = self.output_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            "suite": asdict(test_suite),
            "summary": {
                "total": test_suite.total_tests,
                "passed": test_suite.passed,
                "failed": test_suite.failed,
                "skipped": test_suite.skipped,
                "duration": test_suite.total_duration,
                "pass_rate": f"{(test_suite.passed / test_suite.total_tests * 100):.2f}%" if test_suite.total_tests > 0 else "0%"
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return report_path


class HTMLReporter:
    """HTML test reporter."""
    
    def __init__(self, output_dir: Path):
        """
        Initialize HTML reporter.
        
        Args:
            output_dir: Directory for report output
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, test_suite: TestSuite) -> Path:
        """
        Generate HTML report.
        
        Args:
            test_suite: Test suite to report
            
        Returns:
            Path to generated report
        """
        report_path = self.output_dir / f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        html_content = self._generate_html(test_suite)
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        return report_path
    
    def _generate_html(self, test_suite: TestSuite) -> str:
        """Generate HTML content for report."""
        status_color = {
            "passed": "#28a745",
            "failed": "#dc3545",
            "skipped": "#ffc107"
        }
        
        test_rows = ""
        for test in test_suite.tests:
            color = status_color.get(test.status, "#6c757d")
            error_html = f"<div class='error'>{test.error_message}</div>" if test.error_message else ""
            screenshot_html = f"<a href='{test.screenshot_path}'>View Screenshot</a>" if test.screenshot_path else ""
            
            test_rows += f"""
            <tr>
                <td>{test.name}</td>
                <td style='color: {color}; font-weight: bold;'>{test.status.upper()}</td>
                <td>{test.duration:.2f}s</td>
                <td>{test.timestamp}</td>
                <td>{error_html}{screenshot_html}</td>
            </tr>
            """
        
        pass_rate = (test_suite.passed / test_suite.total_tests * 100) if test_suite.total_tests > 0 else 0
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Report - {test_suite.name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
                .summary-item {{ display: inline-block; margin-right: 30px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #007bff; color: white; }}
                tr:hover {{ background-color: #f5f5f5; }}
                .error {{ color: #dc3545; font-size: 0.9em; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <h1>Test Report: {test_suite.name}</h1>
            <div class="summary">
                <div class="summary-item"><strong>Total Tests:</strong> {test_suite.total_tests}</div>
                <div class="summary-item"><strong>Passed:</strong> <span style="color: #28a745;">{test_suite.passed}</span></div>
                <div class="summary-item"><strong>Failed:</strong> <span style="color: #dc3545;">{test_suite.failed}</span></div>
                <div class="summary-item"><strong>Skipped:</strong> <span style="color: #ffc107;">{test_suite.skipped}</span></div>
                <div class="summary-item"><strong>Duration:</strong> {test_suite.total_duration:.2f}s</div>
                <div class="summary-item"><strong>Pass Rate:</strong> {pass_rate:.2f}%</div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Test Name</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Timestamp</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {test_rows}
                </tbody>
            </table>
        </body>
        </html>
        """
        return html
