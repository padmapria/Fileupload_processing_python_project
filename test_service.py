# Test the service layer independently
from api.service.file_processing_service import FileProcessingService
import sys
import os

service = FileProcessingService()
result = service.process_file_content(b"Hello world\nThis is a test", "test.txt")
print(result)


print("\nsearching with record id")
record = service.get_processing_record_by_id(result['record_id'])
print(record)


print("\nsearching with record id, failed case")
record = service.get_processing_record_by_id()
print(record)