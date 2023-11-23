import json
ip_in=input("Введите ip адрес: ")
maska_in=input("Введите маску сети: ")
with open("masiv.json","r") as f:
    masiv=json.load(f)


#проверка IP адреса
try:
    ip_in=ip_in.split(".")
    for i in ip_in:
        if int(i)>255:
            print("ip адрес указон не коректно!!")
            exit()
except:
    print("ip адрес указон не коректно!!")
    exit()


#проверяем что маска есть в базе
if maska_in in masiv["maski"]:
    maska_ou=masiv["maski"][maska_in]
else:
    print("Маска указан не коректо!!!! ")
    exit()




#переводим IP адрес и маску сети в двоичную систему
ip_in_bin=["{0:08b}".format(int(i)) for i in ip_in]
maska_ou_bin=["{0:08b}".format(int(i)) for i in maska_ou.split(".")]



# узнаём ip адрес сети
ip_ou_seti_bin=[]
for i in range(4):
    ip=ip_in_bin[i]
    mask=maska_ou_bin[i]
    fin=""
    for q in range (8):
        if ip[q]=="1" and mask[q]=="1":
            fin+="1"
        else:
            fin+="0"
    ip_ou_seti_bin.append(fin)
ip_ou_seti=".".join([str(int(i,2)) for i in ip_ou_seti_bin])



#узнаем ip адрес широковещание
maska_ou_bin_revers=[]
ip_ou_shir_bin=[]
for i in maska_ou_bin:
    mask=i
    fin=""
    for q in mask:
        if q=="1":
            fin+="0"
        else:
            fin+="1"
    maska_ou_bin_revers.append(fin)

for i in range(4):
    ip=ip_ou_seti_bin[i]
    mask=maska_ou_bin_revers[i]
    fin=""
    for q in range (8):
        if ip[q]=="1" or mask[q]=="1":
            fin+="1"
        else:
            fin+="0"
    ip_ou_shir_bin.append(fin)
ip_ou_shir=".".join([str(int(i,2)) for i in ip_ou_shir_bin])



#Вывод данных
print(f"ip адрес: {'.'.join(ip_in)}")
print(f"Маска сети: {maska_ou}")
print(f"ip адрес сети: {ip_ou_seti}")
print(f"ip адрес широковещание: {ip_ou_shir}")
print(f"Количество узлов: {2**(32-int(maska_in))-2}")
