#!/usr/bin/env python3
# run_tests.py
import unittest
import sys
from utils.logger import BaseLogging

# Importing test cases
from tests.unit.test_file_processing_service import TestFileProcessingService
from tests.unit.test_file_upload_controller import TestFileUploadController
from tests.integration.test_file_processor_app import TestFileProcessorApp

def run_tests():
    
    # Create an instance to initialize logging
    base_logger = BaseLogging()
    
    # Use the logger directly
    base_logger.log_info("Starting tests")
    
    # Or get the underlying logger
    logger = base_logger.logger
    logger.info("Direct logger usage")
    
    # Create test suites
    unit_test_suite = unittest.TestSuite()
    unit_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFileProcessingService))
    unit_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFileUploadController))

    integration_test_suite = unittest.TestSuite()
    integration_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestFileProcessorApp))

    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    unit_test_result = runner.run(unit_test_suite)
    integration_test_result = runner.run(integration_test_suite)

    # Check the test results
    if unit_test_result.wasSuccessful() and integration_test_result.wasSuccessful():
        print("All tests passed.")
        sys.exit(0)
    else:
        print("Tests failed.")
        sys.exit(1)


if __name__ == '__main__':
    run_tests()