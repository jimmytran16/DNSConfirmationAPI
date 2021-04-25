import re

# function using regex to get rid of all non-numerical characters from the string that contains the phone number  
# returned back the phone number string that contains only numerical characters
# for example -- '781 781 7811' will ne returned as '7817817811'
def remove_non_numerical_char_from_phone_number(number):
    pattern = "[^0-9]" 
    replacement = ""
    unvalidated_phone_number = number 
    validated_phone_number = re.sub(pattern,replacement,unvalidated_phone_number)
    return validated_phone_number

if __name__ == '__main__':
    print(remove_non_numerical_char_from_phone_number('@#$#@$781---781--111--1'))
