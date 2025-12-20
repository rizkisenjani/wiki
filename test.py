def search(input):
    files = ['python', 'django', 'css']
    found = False
    for file in files:
        if str(input) in file:
            print(file)
            found = True
    if not found:
        print('File Not Found')

s = str(input())

search(s)