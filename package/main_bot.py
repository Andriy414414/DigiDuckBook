import typing as t
from prompt_toolkit import prompt


from contacts.contacts_handlers import main_contacts
from sort_folder.sort_module import main_sort
from goose_game.game import main_game
from utils.tool_kit import RainbowLexer, get_completer



def bot_unk() -> str:
    return'Unknown command'

def bot_help() -> str:
    return 'Here could be your advertisement'

def bot_exit() -> str:
    return "Good bye!"

COMMANDS_MAIN_BOT : dict[t.Callable, list[str] ] = {
    main_contacts : ["1", "ab", "contacts", "adress book"],
    # main_notes : ["2", "notes", "note book"],
    main_sort : ["3", "sort", "folder", "dir", "sort folder"],
    main_game : ["4", "game", "fun", "goose",],
    bot_help : ["help", "?", "start"],
    bot_exit : ["good bye", "close", "exit"],
}

def bot_cm_parser(input_str :str) -> t.Callable :
    """
    Parse user input and return the corresponding callable function.

    Args:
        input_str (str): The user's input string.
    Returns:
        t.Callable: A callable function corresponding to the input command.
    TODO: Add more detailed documentation here.
    """
    for func, commands in COMMANDS_MAIN_BOT.items():
        if input_str.strip().lower() in commands:
            return func
    return bot_unk

Completer = get_completer(COMMANDS_MAIN_BOT.values())

def main_digi_duck() -> None:
    """
    Main function for the Digi Duck menu.

    TODO: Add more detailed documentation here.
    """
    while True:
        # user_input = input("Digi Duck menu >>>")
        user_input = prompt(
            message="\nDigi Duck menu >>>",
            completer=Completer,                
            lexer=RainbowLexer("#008000")               
            )
        if not user_input or user_input.isspace():
            continue
       
        module_func = bot_cm_parser(user_input)

        if module_func.__name__.startswith("bot"):
            print(module_func())
            if module_func == bot_exit:
                break
            continue

        module_func()

        

if __name__ == "__main__":
    main_digi_duck()