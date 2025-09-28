import unittest
from unittest.mock import Mock
from flask import Flask
from io import BytesIO

from api.controllers.file_upload_controller import FileUploadController

class TestFileUploadController(unittest.TestCase):
    
    def setUp(self):
        self.app = Flask(__name__)
        self.controller = FileUploadController()
        
        # Mock the service
        self.mock_service = Mock()
        self.controller.file_service = self.mock_service
    
    def test_upload_file_success(self):
        """Testing successful file upload."""
        self.mock_service.is_allowed_file.return_value = True
        self.mock_service.process_file_content.return_value = {
            'record_id': '123', 'filename': 'test.txt', 'results': {'line_count': 1, 'word_count': 2}
        }
        
        file_data = {'file': (BytesIO(b"Hello"), 'test.txt')}
        
        with self.app.test_request_context('/upload', method='POST', data=file_data):
            response = self.controller.upload_file()
            self.assertEqual(response[1], 200)
    
    def test_upload_file_invalid_type(self):
        """Testing upload with wrong file type."""
        self.mock_service.is_allowed_file.return_value = False
        self.mock_service.get_allowed_extensions.return_value = "Only .txt, .csv files are permitted."
        
        file_data = {'file': (BytesIO(b"content"), 'test.jpg')}
        
        with self.app.test_request_context('/upload', method='POST', data=file_data):
            response = self.controller.upload_file()
            self.assertEqual(response[1], 400)
    
    def test_upload_file_no_file(self):
        """Testing upload with no file."""
        with self.app.test_request_context('/upload', method='POST', data={}):
            response = self.controller.upload_file()
            self.assertEqual(response[1], 400)
    
    def test_get_processing_record_by_id_found(self):
        """Testing retrieving existing record."""
        self.mock_service.get_processing_record_by_id.return_value = {
            'id': '123', 'filename': 'test.txt', 'line_count': 5, 'word_count': 10, 'timestamp': '2024-01-01T12:00:00'
        }
        
        # Adding application context for jsonify
        with self.app.app_context():
            with self.app.test_request_context():
                response = self.controller.get_processing_record_by_id('123')
                self.assertEqual(response[1], 200)
    
    def test_get_processing_record_by_id_not_found(self):
        """Testing retrieving non-existent record."""
        self.mock_service.get_processing_record_by_id.return_value = None
        
        # Adding application context for jsonify
        with self.app.app_context():
            with self.app.test_request_context():
                response = self.controller.get_processing_record_by_id('999')
                self.assertEqual(response[1], 404)

if __name__ == '__main__':
    unittest.main()