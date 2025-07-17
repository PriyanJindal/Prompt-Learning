#!/usr/bin/env python3
"""
Script to diagnose and fix import issues with Phoenix and other dependencies.
Run this if you're having import conflicts.
"""

import sys
import os
import subprocess

def check_python_path():
    """Check for conflicting python paths."""
    print("🔍 Checking Python path for conflicts...")
    
    phoenix_paths = [p for p in sys.path if 'phoenix' in p.lower()]
    if phoenix_paths:
        print("Found Phoenix-related paths:")
        for path in phoenix_paths:
            print(f"  - {path}")
        print()
    
    return phoenix_paths

def install_missing_packages():
    """Install missing packages."""
    print("📦 Installing missing packages...")
    
    required_packages = [
        "email-validator",
        "arize-phoenix-evals",
        "arize-phoenix-client",
        "arize-toolkit"
    ]
    
    for package in required_packages:
        try:
            print(f"Installing {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ Successfully installed {package}")
            else:
                print(f"✗ Failed to install {package}: {result.stderr}")
        except Exception as e:
            print(f"✗ Error installing {package}: {e}")

def test_imports():
    """Test critical imports."""
    print("🧪 Testing imports...")
    
    # Test basic imports
    try:
        import pandas as pd
        print("✓ pandas")
    except ImportError as e:
        print(f"✗ pandas: {e}")
    
    try:
        import requests
        print("✓ requests")
    except ImportError as e:
        print(f"✗ requests: {e}")
    
    try:
        import email_validator
        print("✓ email_validator")
    except ImportError as e:
        print(f"✗ email_validator: {e}")
        print("  Run: pip install email-validator")
    
    # Test Phoenix imports with path manipulation
    original_path = sys.path.copy()
    
    # Remove local phoenix paths temporarily
    phoenix_paths_to_remove = [p for p in sys.path if 'phoenix' in p.lower() and 'src' in p]
    for path in phoenix_paths_to_remove:
        if path in sys.path:
            sys.path.remove(path)
    
    try:
        from phoenix.evals import llm_generate, OpenAIModel
        print("✓ phoenix.evals (with path cleanup)")
    except ImportError as e:
        print(f"✗ phoenix.evals: {e}")
        
        # Try with original path
        sys.path = original_path
        try:
            from phoenix.evals import llm_generate, OpenAIModel
            print("✓ phoenix.evals (with original path)")
        except ImportError as e2:
            print(f"✗ phoenix.evals (original path): {e2}")
    
    # Restore original path
    sys.path = original_path
    
    try:
        from arize_toolkit.extensions.prompt_optimizer import PromptLearningOptimizer
        print("✓ PromptLearningOptimizer")
    except ImportError as e:
        print(f"✗ PromptLearningOptimizer: {e}")

def main():
    """Main diagnostic function."""
    print("🔧 BigBench Hard Import Diagnostic Tool")
    print("=" * 50)
    
    # Check for conflicts
    phoenix_paths = check_python_path()
    
    if phoenix_paths:
        print("⚠️  Found local Phoenix installation that may conflict.")
        print("   This script will try to work around it.")
        print()
    
    # Install missing packages
    install_missing_packages()
    print()
    
    # Test imports
    test_imports()
    print()
    
    print("🎯 Recommendations:")
    if phoenix_paths:
        print("1. Consider removing or renaming local phoenix directory")
        print("2. Or use virtual environment to isolate dependencies")
    print("3. Make sure all packages are installed: pip install -r requirements.txt")
    print("4. Try running test_import.py after this")

if __name__ == "__main__":
    main() 