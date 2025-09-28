# tests/unit/test_file_processing_service.p
import unittest
from api.service.file_processing_service import FileProcessingService

class TestFileProcessingService(unittest.TestCase):
    
    def setUp(self):
        self.service = FileProcessingService()
    
    def test_is_allowed_file_valid(self):
        """Testing valid file extensions are allowed."""
        self.assertTrue(self.service.is_allowed_file("test.txt"))
        self.assertTrue(self.service.is_allowed_file("data.csv"))
    
    def test_is_allowed_file_invalid(self):
        """Testing invalid file extensions are rejected."""
        self.assertFalse(self.service.is_allowed_file("image.jpg"))
        self.assertFalse(self.service.is_allowed_file("document.pdf"))
    
    def test_process_file_content_success(self):
        """Testing successful file processing."""
        content = b"Hello World\nThis is a test"
        result = self.service.process_file_content(content, "test.txt")
        
        self.assertEqual(result['results']['line_count'], 2)
        self.assertEqual(result['results']['word_count'], 6)
        self.assertIn('record_id', result)
    
    def test_get_processing_record_by_id(self):
        """Test retrieving record by ID."""
        # Creating a record first
        result = self.service.process_file_content(b"Test content", "test.txt")
        record_id = result['record_id']
        
        # Retrieving it
        record = self.service.get_processing_record_by_id(record_id)
        self.assertEqual(record['filename'], "test.txt")

if __name__ == '__main__':
    unittest.main()