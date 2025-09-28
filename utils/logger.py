# utils/logger.py
import logging
import os
from datetime import datetime

class BaseLogging:
    """Base class for logging with shared handler setup."""
    
    _logging_configured = False  # Class variable to track if logging is setup
    
    def __init__(self):
        class_name = self.__class__.__name__
        
        # Use a consistent logger name (root or module-based)
        self.logger = logging.getLogger("file_processor")  # Consistent name
        
        # Configure logging only once
        if not BaseLogging._logging_configured:
            self._setup_logging()
            BaseLogging._logging_configured = True
        
        self.log_info(f"{class_name} initialized")
    
    def _setup_logging(self):
        """Setup logging configuration (runs only once)."""
        # Create logs directory if it doesn't exist
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Create a unique log file name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"file_processor_{timestamp}.log")
        
        # Console handler
        console_handler = logging.StreamHandler()
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Get root logger and add handlers
        root_logger = logging.getLogger()
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)
        root_logger.setLevel(logging.INFO)
        
        # Log that logging is configured
        root_logger.info(f"Logging configured. Log file: {log_file}")
    
    def log_info(self, message: str):
        """Log info level message."""
        self.logger.info(f"[{self.__class__.__name__}] {message}")
    
    def log_error(self, message: str, exc_info: bool = False):
        """Log error level message."""
        self.logger.error(f"[{self.__class__.__name__}] {message}", exc_info=exc_info)
    
    def log_warning(self, message: str):
        """Log warning level message."""
        self.logger.warning(f"[{self.__class__.__name__}] {message}")
    
    def log_debug(self, message: str):
        """Log debug level message."""
        self.logger.debug(f"[{self.__class__.__name__}] {message}")