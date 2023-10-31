# Function to parse an uploaded text file and convert it to a List[str]
def parse_text_file(upload_file):
    lines = upload_file.file.read().decode().splitlines()
    return lines