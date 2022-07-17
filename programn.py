import numpy as np
import math


text_input = input("Nội dung đầu vào: ")
key = input("Key sử dụng: ")
print(text_input)

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
    print(char)
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

print(array_a)
print("\n")
print(array_x)
matrixB = np.dot(array_a,array_x) ## Chắc chắn là int
print(matrixB)


##Decoding
print("\n")
inverse_x = np.linalg.inv(array_x)
print("Inverse matrix x: \n")
print(inverse_x)
print(" ")
decoding_matrix = np.dot(matrixB,inverse_x)
print(decoding_matrix)
m = decoding_matrix.shape[0]
n = decoding_matrix.shape[1]
ans = ""
for i in range(0,m):
    for j in range(0,n):
        ascii = round(decoding_matrix[i,j])
        ans += chr(ascii)

print(ans)
