from utils.logger import BaseLogging
from flask import request, jsonify
from werkzeug.utils import secure_filename

from api.service.file_processing_service import FileProcessingService
from api.schemas import ApiResponse

class FileUploadController(BaseLogging):
    """
    API controller handling HTTP requests and responses.
    This class contains only web-specific logic.
    """
    
    def __init__(self):   
        super().__init__()    # Auto-logs initialization
        self.file_service = FileProcessingService()
        self.log_info("Controller initialized")  
    
    def upload_file(self):
        """
        Handles file upload requests.
        
        Returns:
            Flask response with processing results or error
        """
        try:
            # Check if file is uploaded 
            if 'file' not in request.files:
                self.log_warning("No file in the request")  
                return jsonify(ApiResponse.error('No file uploaded')), 400
            
            file = request.files['file']
            
            # Check if filename is present
            if file.filename == '':
                self.log_warning("Missing filename")  
                return jsonify(ApiResponse.error('Filename empty')), 400
                
            # Additional safety check for string type
            if not isinstance(file.filename, str):
                self.log_warning(f"Filename is not a string: {type(file.filename)}")  
                return jsonify(ApiResponse.error('Invalid filename format!! Allowed format are ')), 400
            
            # check if file type is valid using service layer
            if not self.file_service.is_allowed_file(file.filename):
                self.log_warning(f"Invalid file type: {file.filename}")  
                return jsonify(ApiResponse.error(
                    'Wrong file type! Only .txt and .csv files are permitted.'
                )), 400
            
            # Secure the filename
            filename = secure_filename(file.filename)
            self.log_info(f"Processing file: {filename}")  
            
            # Read file content
            file_content = file.read()
            
            if not file_content:
                self.log_warning("Uploaded file is empty") 
                return jsonify(ApiResponse.error('File is empty')), 400
            
            # Process the file content using service layer
            result = self.file_service.process_file_content(file_content, filename)
            self.log_info(f"File processed successfully: {result}") 
            
            # Return success response
            response_data = {
                'record_id': result['record_id'],
                'filename': result['filename'],
                'results': result['results']
            }
            
            self.log_info(f"File upload completed for record: {result['record_id']}")  
            return jsonify(ApiResponse.success(
                data=response_data, 
                message='File processed successfully'
            )), 200
            
        except ValueError as e:
            self.log_error(f"Value error during file processing: {e}")  
            return jsonify(ApiResponse.error(str(e))), 400
        except Exception as e:
            self.log_error(f"Unexpected error during file upload: {e}")  
            return jsonify(ApiResponse.error('An internal server error occurred')), 500
    
    def get_processing_record(self, record_id: str):
        """
        Retrieve file processing results corresponding to the record ID.
        
        Args:
            record_id: The record ID to retrieve
            
        Returns:
            record data or error
        """
        try:
            record = self.file_service.get_processing_record(record_id)
            if not record:
                self.log_warning(f"Record not found: {record_id}")  
                return jsonify(ApiResponse.error('Record not found')), 404
            
            self.log_info(f"Record retrieved successfully: {record_id}")  
            return jsonify(ApiResponse.success(data=record)), 200
            
        except Exception as e:
            self.log_error(f"Error retrieving record {record_id}: {e}")  
            return jsonify(ApiResponse.error('An internal server error occurred')), 500