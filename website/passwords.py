valid_characters = {
    'alphabet_lower': 'abcdefghijklmnopqrstuvwxyz',
    'alphabet_higher': 'ABCDEFGHIJKKLMNOPQRSTUVWXYZ',
    'integers': '0123456789',
    'symbols': '_.,/?-+=*^%'
}

def check_password(current_password: str, new_password=""):
    if len(current_password) <= 9:
        response = "Your password should be longer than 9 characters"
    elif new_password != "" and current_password != new_password:
        response = "Passwords do not match"
    else:
        lowercase, uppercase, integers, symbols, misc = (0, 0, 0, 0, 0)
        for character in current_password:
            if character in valid_characters['alphabet_lower']:
                lowercase += 1
            elif character in valid_characters['alphabet_higher']:
                uppercase += 1
            elif character in valid_characters['integers']:
                integers += 1
            elif character in valid_characters['symbols']:
                symbols += 1
            else:
                misc += 1
        if 0 in (lowercase, uppercase, integers, symbols):
            response = "Your password must contain a mix of lowercase and uppercase letters, numbers and symbols (.,/?-+=*^%)"
        else:
            return None
        
    return response