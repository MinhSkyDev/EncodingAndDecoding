from tkinter import *
import numpy as np
import math
import pyperclip


tk = Tk()
tk.title('Encoding and Decoding')
tk.geometry("650x450")

input_str = StringVar()
input_key_str = StringVar()
textOutput = StringVar()
checkButton = False
textOutput_label = Label(tk,textvariable = textOutput)
textOutput_label_check = False
text_clipboard = ""


def addToClipBoard():
    global text_clipboard
    pyperclip.copy(text_clipboard)

copy_clipboard_button = Button(tk,text = "Copy to clipboard !")

def encode():
    global textOutput_label_check
    global text_clipboard
    output_str = ""
    text_input = input_str.get()
    key = input_key_str.get()

    ## Xử lý đầu vào đưa text_input về một ma trận
    row_array = np.zeros(4)
    array_a = np.zeros(shape=(1,4))
    countRow = 0

    ##Matrix A processing
    for char in text_input:
        if countRow == 4:
            array_a = np.append(array_a,[row_array], axis = 0)
            countRow = 0
            row_array = np.zeros(4)
        row_array[countRow] = ord(char)
        countRow += 1

    if countRow <= 4:
        array_a = np.append(array_a,[row_array], axis = 0)
    ##Delete first [0,0,0,0] row
    array_a = np.delete(array_a,0,0)
    array_a = array_a.astype(int) ## ép kiểu về int

    ##Matrix X Processing
    array_x = np.zeros(shape=(4,1))
    column_array = []
    countColumn =1
    countChar =0
    for char in key:
        if countChar > 16:
            break
        if len(column_array) == 4:
            array_x = np.insert(array_x,countColumn,column_array,axis = 1)
            column_array = []
            countColumn +=1
        column_array.append(ord(char))
        countChar +=1

    if len(column_array) <= 4 and countChar <16:
        for i in range(len(column_array)-1,3):
            column_array.append(0)
        array_x = np.insert(array_x,countColumn,column_array,axis = 1)
        countColumn += 1
    ##Đưa ma trận về đúng 4x4
    if countColumn <5:
        for i in range(countColumn,5):
            column_array = [0,0,0,0]
            array_x = np.insert(array_x,i,column_array,axis = 1)
    array_x = np.delete(array_x,0,1)

    ##Tránh để ma trận là một ma trận không nghịch đảo được
    for i in range(0,4):
        if array_x[i][i] == 0:
            array_x[i][i] = 1
    array_x = array_x.astype(int)
    matrixB = np.dot(array_a,array_x)
    m = matrixB.shape[0]
    n = matrixB.shape[1]
    for i in range(0,m):
        for j in range(0,n):
            output_str += str(matrixB[i,j]) +" "
    textOutput.set(output_str)
    text_clipboard = output_str


def decode():
    global text_clipboard
    try:
        global textOutput_label_check
        text_encoded = input_str.get()
        key = input_key_str.get()

        ##input processing
        text_encoded_list = text_encoded.split()
        map_object = map(int,text_encoded_list)
        arrayB = list(map_object)
        m = int(len(arrayB)/4) ## vì ma trận được mã hóa là mxn
        n =4
        matrixB = np.array(arrayB).reshape(m,n)

        ##Matrix X Processing
        array_x = np.zeros(shape=(4,1))
        column_array = []
        countColumn =1
        countChar =0
        for char in key:
            if countChar > 16:
                break
            if len(column_array) == 4:
                array_x = np.insert(array_x,countColumn,column_array,axis = 1)
                column_array = []
                countColumn +=1
            column_array.append(ord(char))
            countChar +=1

        if len(column_array) <= 4 and countChar <16:
            for i in range(len(column_array)-1,3):
                column_array.append(0)
            array_x = np.insert(array_x,countColumn,column_array,axis = 1)
            countColumn += 1

        if countColumn <5:
            for i in range(countColumn,5):
                column_array = [0,0,0,0]
                array_x = np.insert(array_x,i,column_array,axis = 1)
        array_x = np.delete(array_x,0,1)

        ##Tránh để ma trận là một ma trận không nghịch đảo được
        for i in range(0,4):
            if array_x[i][i] == 0:
                array_x[i][i] = 1
        array_x = array_x.astype(int)


        ##Bắt đầu giải mã
        inverse_x = np.linalg.inv(array_x)
        decoding_matrix = np.dot(matrixB,inverse_x)
        ans = ""
        for i in range(0,m):
            for j in range(0,n):
                ascii = round(decoding_matrix[i,j])
                ans += chr(ascii)
        textOutput.set(ans)
        text_clipboard = textOutput.get()
        text_clipboard = str(text_clipboard)
    except:
        textOutput.set("Không hợp lệ")

## key : ???
## 20223 105 116 99 20790 110 109 101 20412 111 116 104 19719 116 100 97 9702 33 0 0
def main():
    main_title = Label(tk,text = "Chương trình mã hóa và giải mã thông tin")
    main_title.pack()
    input_label = Label(tk,text = "Nội dung nhập")
    input_label.pack()
    input_box = Entry(tk,bd = 5,textvariable = input_str, width = 50, font = ('Helvetica',30))
    input_box.pack(padx =10, pady =10)
    input_key_label = Label(tk,text = "Key nhập vào: ")
    input_key_label.pack()
    input_key_button = Entry(tk, textvariable = input_key_str, width = 50, font = ('Helvetica',30))
    input_key_button.pack(padx = 10)
    function_choose_label = Label(tk,text = "Chọn chức năng muốn sử dụng")
    function_choose_label.pack()
    encode_button = Button(tk, text = "Mã hóa",command = encode)
    decode_button = Button(tk, text = "Giải mã", command = decode)
    copy_button = Button(tk,text = "Copy to clipboard",command = addToClipBoard)
    textOutput_label.pack()
    encode_button.pack(side = LEFT, padx = 100)
    decode_button.pack(side = RIGHT, padx = 100)
    copy_button.pack(side = TOP)
    ##output_textbox = TextBox(tk,)
    tk.mainloop()



if __name__ == "__main__":
    main()
