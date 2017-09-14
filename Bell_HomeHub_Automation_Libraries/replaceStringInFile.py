import re


def replaceStringInFile(file, pattern, subst):
    # Read contents from file as a single string
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()

    # Use RE package to allow for replacement (also allowing for (multiline) REGEX)
    file_string = (re.sub(pattern, subst, file_string))

    # Write contents to file.
    # Using mode 'w' truncates the file.
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()
	
if __name__=='__main__':
	file = "TPValues.txt"
	pattern = "N-TP-2.4G-40MHz-1ss-1c 0.9"
	subst = "N-TP-2.4G-40MHz-1ss-1c 0.9 4"
	replaceStringInFile(file, pattern, subst)