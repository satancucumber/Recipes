import requests
url = "http://127.0.0.1:5000/api/v1/recipe"
request = {"ingredients" : "2;6;1;2;1" ,"name" : "Тост с огурцом", "inf" : "Хрустящий хлеб с огурцом", "cuisineid" : 1, "countsteps" : 2, "steps" : "Пожарить хлеб с двух сторон до хрустящей корочки;Положить на хлеб порезанный огурец"}

r = requests.post(url, json=request)

#r = requests.get(url, type_id = 1)

print(r.content.decode())
print(r)
#a = ['1', '2', '3', '4']
#cnt = int(a.pop(0))
#print(cnt, a)
#a = ";".join(a)


'''
cnt = 10
data = "5;5;68;3;40;1;9;4;30;8;45"
input = data.split(";")
print(input)
cnt_id = int(input.pop(0))
print(input)
new = ['0']*cnt
print(new)
for i in range(cnt_id):
    new[int(input[i*2])-1] = int(input[i*2+1])
print(new)
'''