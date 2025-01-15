# Example list
Error_message_list = [False, True, True]

# Assert that all elements in the list are the same
if all(Error_message_list) :
    print("Test passed: Error message is correctly thrown for all inputs.")
else:
   print ("Test failed: Not all inputs triggered the correct error message.")
   AssertionError("User's account was created for an invalid input.")