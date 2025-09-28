# api/service/file_upload_service.py
import uuid
from datetime import datetime
from typing import Dict, Optional
from utils.logger import BaseLogging

class FileProcessingService(BaseLogging):
    """
    Service class handling file processing business logic.
    This class contains all the core business rules and operations.
    """
    
    def __init__(self):
        super().__init__()  # Auto-logs initialization
        
        # Service data
        self.file_records = {}
        self.allowed_extensions = {'txt', 'csv'}
    
    def get_allowed_extensions(self) -> set:
        """Get the list of allowed file extensions."""
        
        allowed_extensions_list = ", ".join([f".{ext}" for ext in allowed_extensions])
        return f"Only {allowed_extensions_list} files are permitted." 
    
    def is_allowed_file(self, filename: str) -> bool:
        """
        Validate if the uploaded file has an allowed extension.
        
        Args:
            filename: The name of the file to validate
            
        Returns:
            bool: True if file extension is allowed, False otherwise
        """
        
        self.log_debug(f"Validating file extension: {filename}")  
            
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        is_allowed = extension in self.allowed_extensions
        
        if not is_allowed:
            self.log_warning(f"File type not allowed: {filename}")  
        else:
            self.log_debug(f"File type allowed: {filename}")  
            
        return is_allowed
       
    
    def process_file_content(self, file_content: bytes, filename: str) -> Dict:
        
        """
        Main function to process file content and return results.
        
        Args:
            file_content: The content of the file as bytes
            filename: Original filename
            
        Returns:
            Dict containing processing results and record ID
            
        Raises:
            ValueError: If file content is invalid
        """
        
        self.log_info(f"Starting file processing: {filename}")  
        
        # Validate input
        if not file_content:
            self.log_error("File content is empty")  
            raise ValueError("File content is empty")
        
        if not filename:
            self.log_error("Filename is required")  
            raise ValueError("Filename is required")
        
        # Process file content
        processing_results = self._count_lines_and_words(file_content)
        self.log_info(f"File processing completed: {processing_results}")  
        
        # Save to db
        record_id = self._save_to_db(filename, processing_results)
        
        return {
            'record_id': record_id,
            'filename': filename,
            'results': processing_results
        }
        
    
    def _count_lines_and_words(self, file_content: bytes) -> Dict[str, int]:
        """
        Process the file content to count lines and words.
        
        Args:
            file_content: The content of the file as bytes
            
        Returns:
            Dict containing line_count and word_count
        """
        self.log_debug("Counting lines and words")  
        
        try:
            content = file_content.decode('utf-8')
            lines = content.splitlines()
            line_count = len(lines)
            
            word_count = 0
            for line in lines:
                words = line.split()
                word_count += len(words)
            
            result = {'line_count': line_count, 'word_count': word_count}
            self.log_debug(f"Count results: {result}")  
            return result
            
        except UnicodeDecodeError as e:
            self.log_error(f"Error decoding file: {e}")  
            raise ValueError("File content is not valid UTF-8 text")
        except Exception as e:
            self.log_error(f"Unexpected error: {e}") 
            raise ValueError(f"Error processing file: {str(e)}")
    
    def _save_to_db(self, filename: str, processing_results: Dict[str, int]) -> str:
        """
        Saving processed data to an in-memory database.
        
        Args:
            filename: The original filename
            processing_results: Dictionary containing processing results
            
        Returns:
            str: Record ID for the saved data
        """
        try:
            record_id = str(uuid.uuid4())
            record = {
                'id': record_id,
                'filename': filename,
                'line_count': processing_results['line_count'],
                'word_count': processing_results['word_count'],
                'timestamp': datetime.now().isoformat()
            }
            
            self.file_records[record_id] = record
            self.log_info(f"Saved record: {record_id} for file: {filename}")  
            return record_id
            
        except Exception as e:
            self.log_error(f"Error saving to database: {e}")  
            raise
    
    def get_processing_record_by_id(self, record_id: str) -> Optional[Dict]:
        """
        Retrieve a record from the in-memory database for the passed record_id.
        
        Args:
            record_id: The ID of the record to retrieve
            
        Returns:
            Dict containing the record data or None if not found
        """
        self.log_debug(f"Retrieving record: {record_id}")  
        
        if not record_id:
            self.log_error("Record id is empty")  
            raise ValueError("Record id is empty")
            
        record = self.file_records.get(record_id)
        
        if record:
            self.log_debug(f"Record found: {record_id}")  
        else:
            self.log_warning(f"Record not found: {record_id}")  
        return record