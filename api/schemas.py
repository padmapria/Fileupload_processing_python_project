from typing import Dict, Any

class ApiResponse:
    """Standard API response format."""
    
    @staticmethod
    def success(data: Dict[str, Any] = None, message: str = None) -> Dict[str, Any]:
        response = {'status': 'success'}
        if data:
            response['data'] = data
        if message:
            response['message'] = message
        return response
    
    @staticmethod
    def error(message: str, error_code: str = None) -> Dict[str, Any]:
        response = {
            'status': 'error',
            'message': message
        }
        if error_code:
            response['error_code'] = error_code
        return response