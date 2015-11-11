import os

directory = "/Users/traveler/Dropbox/school stuff/378/geocomputing/topic 11 - system access/rename_test"
file_list = os.listdir("/Users/traveler/Dropbox/school stuff/378/geocomputing/topic 11 - system access/rename_test")

for myfile in file_list:
    path = os.path.join(directory, myfile)
    target = os.path.join(directory, "new_" + myfile)
    os.rename(path, target)