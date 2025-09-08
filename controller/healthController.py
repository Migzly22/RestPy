def get_health_status():
    """
    Performs a simple health check to ensure the application is running.
    """
    
    return {"status": "ok", "message": "API is healthy!"}

def read_root():
    """
    This is the main screen of the application.
    It returns a welcome message and points to the API documentation.
    """
    return {"message": "Welcome to the DevOps Tools API! Navigate to /docs for the interactive API documentation."}