def log_message(message):
    with open("application.log", "a") as log_file:
        log_file.write(f"{message}\n")

def format_output(text):
    return f"[OUTPUT] {text}"

def handle_error(error):
    log_message(f"Error: {error}")
    return f"An error occurred: {error}"