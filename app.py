#app.py
import os
import logging
from flask import Flask, request

from utils.logger import BaseLogging
from api.controllers.file_upload_controller import FileUploadController

class FileProcessorApp(BaseLogging):
    """Main application class."""
    
    def __init__(self):
        super().__init__()  # Auto-logs initialization
        self.app = None
        self.controller = None
    
    def create_app(self):
        """Create and configure the Flask application."""
        self.app = Flask(__name__)
        
        # Configuration
        # API-level size limit (1MB)
        self.app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
        self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
        
        # Initialize controller
        self.controller = FileUploadController()
        
        # Upload a file
        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            return self.controller.upload_file()
        
        @self.app.route('/records/<record_id>', methods=['GET'])
        def get_processing_record_by_id(record_id):
            return self.controller.get_processing_record_by_id(record_id)
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            self.log_info("Health check called") 
            return {'status': 'healthy', 'service': 'file-processing'}
        
        # Error handlers
        # Global error handler for oversized files
        @self.app.errorhandler(413)
        def too_large(e):
            self.log_warning("File too large")  
            return {'error': 'File is too large. Maximum size is 1MB.'}, 413
        
        @self.app.errorhandler(404)
        def not_found(e):
            self.log_warning(f"404: {request.path}")  
            return {'error': 'Endpoint not found'}, 404
        
        @self.app.errorhandler(500)
        def internal_error(e):
            self.log_error("Internal server error", exc_info=True)  
            return {'error': 'Internal server error'}, 500
        
        self.log_info("Application setup completed")  
        return self.app
    
    def run(self, debug=True, host='0.0.0.0', port=5000):
        """Run the application."""
        self.log_info(f"Starting app on {host}:{port}")  
        self.app.run(debug=debug, host=host, port=port)

def create_app():
    """Factory function for WSGI."""
    app_instance = FileProcessorApp()
    return app_instance.create_app()

if __name__ == '__main__':
    app_instance = FileProcessorApp()
    app = app_instance.create_app()
    app_instance.run()