#!/usr/bin/env python3
"""
🌱 Eco Impact Checker for MoodTunes PWA

This script performs a simplified environmental impact assessment
that can be run locally during development.

Usage:
    python scripts/eco_check.py

Exit codes:
    0: Eco check passed
    1: Eco check failed (high environmental impact)
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Tuple


def run_command(cmd: str) -> Tuple[str, str, int]:
    """Run a shell command and return stdout, stderr, and return code."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1


def calculate_bundle_size() -> float:
    """Calculate total bundle size in KB."""
    static_dir = Path("static")
    total_size = 0

    if not static_dir.exists():
        print("⚠️  Static directory not found, assuming minimal bundle size")
        return 50.0  # Default small size

    for file_path in static_dir.rglob("*"):
        if file_path.is_file():
            total_size += file_path.stat().st_size

    return total_size / 1024  # Convert to KB


def analyze_code_efficiency() -> Dict[str, float]:
    """Analyze code for efficiency metrics."""
    metrics = {"unused_imports": 0, "long_lines": 0, "complex_functions": 0, "total_lines": 0}

    for py_file in Path(".").rglob("*.py"):
        if any(skip in str(py_file) for skip in ["__pycache__", ".git", "venv", "env"]):
            continue

        try:
            with open(py_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                metrics["total_lines"] += len(lines)

                for line in lines:
                    stripped = line.strip()
                    if len(line.rstrip()) > 120:  # Long lines
                        metrics["long_lines"] += 1
                    if stripped.startswith("import ") or stripped.startswith("from "):
                        # Simplified unused import detection
                        # In a real implementation, you'd use ast or similar
                        pass

        except Exception as e:
            print(f"⚠️  Error analyzing {py_file}: {e}")
            continue

    return metrics


def get_complexity_metrics() -> float:
    """Analyze code complexity using radon.

    Returns:
        float: Average cyclomatic complexity across all functions
    """
    complexity_output, _, complexity_rc = run_command("radon cc . -a -nc --json")
    avg_complexity = 5.0  # Default assumption

    try:
        if complexity_rc == 0 and complexity_output.strip():
            complexity_data = json.loads(complexity_output)
            total_complexity = 0
            total_functions = 0

            for file_data in complexity_data.values():
                if isinstance(file_data, list):
                    for item in file_data:
                        if "complexity" in item:
                            total_complexity += item["complexity"]
                            total_functions += 1

            if total_functions > 0:
                avg_complexity = total_complexity / total_functions

    except Exception as e:
        print(f"⚠️  Complexity analysis failed: {e}")

    return avg_complexity


def calculate_bundle_factor(bundle_size_kb: float) -> float:
    """Calculate bundle size eco factor score.

    Args:
        bundle_size_kb: Bundle size in kilobytes

    Returns:
        float: Score from 0-100 (higher is better)
    """
    if bundle_size_kb <= 200:  # Under 200KB is excellent
        return 100
    elif bundle_size_kb <= 500:  # Under 500KB is good
        return 80 - ((bundle_size_kb - 200) / 300) * 30
    elif bundle_size_kb <= 1000:  # Under 1MB is acceptable
        return 50 - ((bundle_size_kb - 500) / 500) * 30
    else:  # Over 1MB is poor
        return max(0, 20 - ((bundle_size_kb - 1000) / 500) * 10)


def calculate_complexity_factor(avg_complexity: float) -> float:
    """Calculate complexity eco factor score.

    Args:
        avg_complexity: Average cyclomatic complexity

    Returns:
        float: Score from 0-100 (higher is better)
    """
    if avg_complexity <= 3:
        return 100
    elif avg_complexity <= 5:
        return 80 - ((avg_complexity - 3) / 2) * 30
    elif avg_complexity <= 10:
        return 50 - ((avg_complexity - 5) / 5) * 30
    else:
        return max(0, 20 - ((avg_complexity - 10) / 5) * 10)


def calculate_efficiency_factor(total_lines: int, bundle_size_kb: float) -> float:
    """Calculate code efficiency factor score.

    Args:
        total_lines: Total lines of code
        bundle_size_kb: Bundle size in kilobytes

    Returns:
        float: Score from 0-100 (higher is better)
    """
    lines_per_kb = total_lines / max(bundle_size_kb, 1)
    if lines_per_kb >= 50:  # Dense, efficient code
        return 100
    elif lines_per_kb >= 30:
        return 80
    else:
        return 60


def calculate_eco_score() -> Dict[str, any]:
    """Calculate comprehensive environmental impact score for the application.

    Analyzes multiple factors that contribute to environmental impact:
    - Bundle size (affects download time and bandwidth usage)
    - Code complexity (affects CPU processing requirements)
    - Code efficiency (lines of code per KB of bundle size)

    Returns:
        Dict[str, any]: Dictionary containing eco metrics and overall score
    """
    print("🌱 Calculating environmental impact...")

    # Gather core metrics
    bundle_size_kb = calculate_bundle_size()
    code_metrics = analyze_code_efficiency()
    avg_complexity = get_complexity_metrics()

    print(f"📦 Total bundle size: {bundle_size_kb:.1f} KB")
    print(f"📄 Total code lines: {code_metrics['total_lines']}")
    print(f"🔄 Average complexity: {avg_complexity:.1f}")

    # Calculate individual eco factors
    bundle_factor = calculate_bundle_factor(bundle_size_kb)
    complexity_factor = calculate_complexity_factor(avg_complexity)
    efficiency_factor = calculate_efficiency_factor(code_metrics["total_lines"], bundle_size_kb)

    # Calculate weighted eco score (bundle size has highest impact)
    eco_score = (
        bundle_factor * 0.4
        + complexity_factor * 0.3  # Bundle size affects download/bandwidth
        + efficiency_factor * 0.3  # Complexity affects CPU processing  # Efficiency affects overall resource usage
    )

    # Estimate environmental impact
    # Simplified calculation based on bundle size and complexity
    base_energy = (bundle_size_kb / 1000) * 0.5 + 2.0  # kWh per 1000 visits
    complexity_multiplier = 1 + (avg_complexity - 5) * 0.1
    energy_per_1000_visits = max(0.1, base_energy * complexity_multiplier)
    co2_per_1000_visits = energy_per_1000_visits * 0.5  # Assume green hosting

    return {
        "eco_score": eco_score,
        "bundle_size_kb": bundle_size_kb,
        "avg_complexity": avg_complexity,
        "energy_per_1000_visits": energy_per_1000_visits,
        "co2_per_1000_visits": co2_per_1000_visits,
        "factors": {
            "bundle_factor": bundle_factor,
            "complexity_factor": complexity_factor,
            "efficiency_factor": efficiency_factor,
        },
    }


def display_eco_report(eco_data: Dict[str, any]) -> None:
    """Display formatted eco impact report.

    Args:
        eco_data: Dictionary containing eco metrics and scores
    """
    print("\n📊 ECO IMPACT REPORT")
    print("=" * 25)
    print(f"🌱 Eco Score:           {eco_data['eco_score']:.1f}/100")
    print(f"📦 Bundle Size:         {eco_data['bundle_size_kb']:.1f} KB")
    print(f"🔄 Avg Complexity:      {eco_data['avg_complexity']:.1f}")
    print(f"⚡ Energy (per 1K visits): {eco_data['energy_per_1000_visits']:.3f} kWh")
    print(f"🌍 CO2 (per 1K visits):   {eco_data['co2_per_1000_visits']:.3f} g")

    print(f"\n📈 Factor Breakdown:")
    print(f"  📦 Bundle Factor:     {eco_data['factors']['bundle_factor']:.1f}/100")
    print(f"  🔄 Complexity Factor: {eco_data['factors']['complexity_factor']:.1f}/100")
    print(f"  ⚡ Efficiency Factor: {eco_data['factors']['efficiency_factor']:.1f}/100")


def assess_eco_quality_gate(score: float) -> int:
    """Assess eco score against quality gates and display results.

    Args:
        score: Eco score from 0-100

    Returns:
        int: Exit code (0 for pass, 1 for fail)
    """
    if score >= 80:
        print(f"\n✅ ECO CHECK PASSED (Excellent - {score:.1f}/100)")
        print("🌱 Your app has minimal environmental impact!")
        return 0
    elif score >= 70:
        print(f"\n✅ ECO CHECK PASSED (Good - {score:.1f}/100)")
        print("🌱 Good environmental impact with room for optimization.")
        return 0
    elif score >= 60:
        print(f"\n⚠️  ECO CHECK WARNING (Moderate - {score:.1f}/100)")
        print("🌱 Environmental impact is acceptable but could be improved.")
        return 0  # Warning, but don't fail
    else:
        print(f"\n❌ ECO CHECK FAILED (Poor - {score:.1f}/100)")
        print("🌱 High environmental impact detected!")
        return 1


def main():
    """Main eco check function that orchestrates the environmental impact assessment.

    Validates environment, calculates eco metrics, displays results,
    and provides optimization recommendations.
    """
    print("🌱 MoodTunes PWA - Eco Impact Check")
    print("=" * 40)

    # Validate execution environment
    if not Path("app.py").exists():
        print("❌ Error: app.py not found. Run from project root directory.")
        sys.exit(1)

    try:
        # Calculate and display eco metrics
        eco_data = calculate_eco_score()
        display_eco_report(eco_data)

        # Assess quality gates and get exit code
        exit_code = assess_eco_quality_gate(eco_data["eco_score"])

        # Provide optimization recommendations
        if score < 80:
            print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
            if eco_data["bundle_size_kb"] > 500:
                print("  📦 Reduce bundle size - optimize images, remove unused code")
            if eco_data["avg_complexity"] > 7:
                print("  🔄 Reduce code complexity - break down complex functions")
            if eco_data["factors"]["efficiency_factor"] < 80:
                print("  ⚡ Improve code efficiency - optimize algorithms")

        # Save report for CI/CD if needed
        if os.getenv("CI"):
            with open("eco-check-report.json", "w") as f:
                json.dump(eco_data, f, indent=2)
            print(f"\n📁 Report saved to eco-check-report.json")

        sys.exit(exit_code)

    except Exception as e:
        print(f"❌ Eco check failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
