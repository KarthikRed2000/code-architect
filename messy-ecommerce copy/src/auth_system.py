# Violates: Security Best Practices, Deep Nesting
class AuthSystem:
    def __init__(self):
        self.sessions = {}
        self.failed_attempts = {}
        
    def login(self, username, password):
        if username:
            if password:
                if username not in self.failed_attempts:
                    self.failed_attempts[username] = 0
                    
                if self.failed_attempts[username] < 5:
                    # Check credentials (hardcoded for demo)
                    if username == "admin" and password == "admin123":
                        session_token = f"session_{username}_12345"
                        self.sessions[session_token] = username
                        self.failed_attempts[username] = 0
                        return session_token
                    else:
                        self.failed_attempts[username] += 1
                        if self.failed_attempts[username] >= 5:
                            # Send alert
                            import smtplib
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login("admin@shop.com", "password123")
                            message = f"Account locked for {username}"
                            server.sendmail("admin@shop.com", "security@shop.com", message)
                            server.quit()
                        return None
                else:
                    return "ACCOUNT_LOCKED"
        return None
    
    def logout(self, session_token):
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
