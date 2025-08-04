def hash_password(password: str) -> str:
    # Hash the password using SHA-256 (or a stronger hashing function like bcrypt)
    return hashlib.sha256(password.encode()).hexdigest()
  

 def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return hash_password(plain_password) == hashed_password


    
def mask_email(email):
    try:
        name, domain = email.split("@")
        # Mask part of the name (e.g., jo***)
        if len(name) >= 3:
            name_masked = name[:2] + "***"
        else:
            name_masked = name[0] + "***"
        return f"{name_masked}@{domain}"
    except:
        return None
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email)
