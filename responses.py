import commands.command_handler as command_handler

def handle_response(message) -> str:
    p_message = message.lower()
    if len(p_message) < 5:
        return
    command = p_message.split()
    if command[0] != "/leb2":
        return
    
    return command_handler.run_command(command[1:])
