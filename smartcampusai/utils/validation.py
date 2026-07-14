import re

from typing import Tuple

def validate_email(email: str) -> bool:
    """
    Validates the format of an email address using standard regex.
    """
    if not email:
        return False
    # Standard email regex pattern
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email.strip()))

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validates that the password meets security constraints:
    - Minimum 8 characters.
    - Contains at least one digit and one letter.
    """
    if not password:
        return False, "Password cannot be empty."
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
        
    if not any(char.isalpha() for char in password):
        return False, "Password must contain at least one letter."
        
    return True, "Password is valid."
