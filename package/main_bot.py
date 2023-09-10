from contacts.contacts_handlers import main_contacts
import typing as t




def bot_unk() -> str:
    return'Unknown command'

def bot_help() -> str:
    pass

def bot_exit() -> str:
    return "Good bye!"

COMMANDS_DIGI_DUCK : dict[t.Callable, list[str] ] = {
    main_contacts : ["1", "ab", "contacts", "adress book"],
    # main_notes : ["2", "notes", "note book"],
    # main_sort : ["3","sort","folder", "dir"],
    bot_help : ["help", "?", "start"],
    bot_exit : ["good bye", "close", "exit"],
    
}

def bot_cm_parser(input_str :str) -> t.Callable | None:
    """
    TODO doc
    """
    for func, commands in COMMANDS_DIGI_DUCK.items():
        if input_str.strip().lower() in commands:
            return func
    return bot_unk


def main_digi_duck() -> None:
    while True:
        user_input = input("Hello this is Digi Duck menu >>>")
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