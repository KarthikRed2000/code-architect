# email_mock.py - Mock email service for testing
class MockEmailService:
    """Mock email service that simulates sending without actual SMTP"""
    
    @staticmethod
    def send_email(from_email, to_email, message):
        print(f"📧 [MOCK EMAIL] From: {from_email} → To: {to_email}")
        print(f"   Message: {message}")
        return True
