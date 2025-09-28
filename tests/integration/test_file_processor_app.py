# tests/integration/test_file_processor_app.py

import unittest
import json
from io import BytesIO
from app import create_app

class TestFileProcessorApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
    
    def test_upload_file_success(self):
        """Testing successful file upload."""
        data = {
            'file': (BytesIO(b"Hello World"), 'test.txt')
        }
        
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
    
    def test_upload_file_invalid_type(self):
        """Test upload with wrong file type."""
        data = {
            'file': (BytesIO(b"content"), 'test.jpg')
        }
        
        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 500)
    
    def test_get_record(self):
        """Test record retrieval."""
        # First upload a file to get a record ID
        upload_data = {'file': (BytesIO(b"Test"), 'test.txt')}
        upload_response = self.client.post('/upload', data=upload_data)
        record_id = upload_response.get_json()['data']['record_id']
        
        # Then retrieve it
        response = self.client.get(f'/records/{record_id}')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()