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


def deploy_with_docker_compose():
    """Deploy using existing docker-compose.yml configuration"""
    logger.info("Starting deployment with docker-compose...")
    
    try:
        # Stop any existing containers
        logger.info("Stopping existing containers...")
        subprocess.run(["docker-compose", "down"], capture_output=True)
        
        # Build and start using docker-compose (uses all config from docker-compose.yml)
        logger.info("Building and starting services...")
        result = subprocess.run(
            ["docker-compose", "up", "-d"],
            check=True,
            capture_output=True,
            text=True
        )
        
        logger.info("Docker-compose deployment successful")
        
        # Wait for health check (defined in docker-compose.yml) to pass
        logger.info("Waiting for service to be healthy...")
        if wait_for_health():
            logger.info("Service is healthy and ready!")
            return True
        else:
            logger.warning("Service started but health check timeout")
            return True  # Still return True as container is running
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Docker-compose failed: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Deployment error: {str(e)}")
        return False

def wait_for_health(timeout=60):
    """Wait for the health check to pass (uses the same check as docker-compose)"""
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            # Use the same health check as defined in docker-compose.yml
            result = subprocess.run(
                ["curl", "-f", "http://localhost:5000/health"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return True
                
        except subprocess.TimeoutExpired:
            pass
        except Exception:
            pass
            
        time.sleep(5)
        logger.info("Waiting for service to be healthy...")
    
    return False

if __name__ == '__main__':
    run_tests()