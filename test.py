import pickle

with open(r'C:\Users\dlgpd\Desktop\20-1\oss\term-project\Learn_for_yourself\chat_system\wordList.txt','rb') as f:
    data = pickle.load(f)
    print(data)  # hello
