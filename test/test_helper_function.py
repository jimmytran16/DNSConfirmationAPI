import unittest
from api.helpers.helpers import remove_non_numerical_char_from_phone_number

class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        self.testPhoneNumbers = [
            '781 781 1234',
            '7811111111',
            '206/782-8410',
            '(206) 782-8410',
            '9568574141',
            '847 554 3964',
            '847-554-3964',
            '847/554/3964',
            '@#$#@$781---781--111--1',
            'abcdefghijklmnopqrstuvwxyz888-999-8888ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            '(786)859)$%$#-7662',
            '(303))$%$#359-8787',
            '(305)8)$%$#96-4112',
            '360)396-6651)$%$#',
            '(816)668-6350',
            '229)928-7)$%$#788',
            '(559)434-8575',
            '(479)717-7572',
            '(323)9)$%$#74-1095',
            '(229)265-7557',
            '(401)610-8690',
            '(725)244-9344',
            '(570)632-4911',
            '(830)755-6)$%$#974',
            '(330)994-3117',
            '(432)337-3417',
            '(81)$%$#3)732-7230',
            '(251)258-2778',
            '(209)$%$#217-5493',
        ]


    def tearDown(self):
        pass

    # check if the function will return the correct validated phone number string
    # should return back a 10 digit character, since all non numericals from that string is removed
    def test_remove_non_numerical_char_from_phone_number_helper_function_with_correct_resulting_length(self):
        for number in self.testPhoneNumbers:
            validated_number = remove_non_numerical_char_from_phone_number(number)
            self.assertEqual(10,len(validated_number))

    # test if the remove_non_numerical_char_from_phone_number results, will return a string that contains only numbers
    # using the isdecimal() function to check if string contains only numerical chracters
    def test_remove_non_numerical_char_from_phone_number_helper_function_returned_string_containing_only_numbers(self):
        for number in self.testPhoneNumbers:
            validated_number = remove_non_numerical_char_from_phone_number(number)
            self.assertEqual(True,validated_number.isdecimal())
