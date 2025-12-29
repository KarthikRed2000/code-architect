#!/usr/bin/env python3
"""
Master Test Runner for E-Commerce System
Runs all unit tests and generates a comprehensive coverage report
"""

import unittest
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

def run_all_tests():
    """Discover and run all tests"""
    
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover all tests in current directory
    test_suite = loader.discover(os.path.join(os.getcwd(), 'unit-tests'), pattern='test_*.py')
    
    # Create test runner with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    
    # Run tests
    print("=" * 70)
    print("RUNNING ALL UNIT TESTS FOR E-COMMERCE SYSTEM")
    print("=" * 70)
    print()
    
    result = runner.run(test_suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print()
    
    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED!")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        return 1

def run_specific_module(module_name):
    """Run tests for a specific module"""
    
    loader = unittest.TestLoader()
    
    try:
        test_suite = loader.loadTestsFromName(f'test_{module_name}')
        runner = unittest.TextTestRunner(verbosity=2)
        
        print("=" * 70)
        print(f"RUNNING TESTS FOR: {module_name}")
        print("=" * 70)
        print()
        
        result = runner.run(test_suite)
        
        return 0 if result.wasSuccessful() else 1
        
    except Exception as e:
        print(f"Error loading tests for {module_name}: {e}")
        return 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # Run specific module tests
        module = sys.argv[1]
        sys.exit(run_specific_module(module))
    else:
        # Run all tests
        sys.exit(run_all_tests())
