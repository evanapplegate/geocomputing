telephone_number_list = list(raw_input('Enter telephone number >'))
good_telephone_number = []

for i in range(len(telephone_number_list)):
    if telephone_number_list[i].isdigit():
        good_telephone_number.append(telephone_number_list[i])
        
final_number = "".join(good_telephone_number)

print "the phone number stripped of non-digits is:", final_number