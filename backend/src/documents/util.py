import magic

def determine_file_type(file_path):
    # Create a Magic object
    mime = magic.Magic(mime=True)
    
    # Use the Magic object to determine the file type based on content
    file_type = mime.from_file(file_path)
    
    return file_type


