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



#узнаём ip адрес сети
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

#узнаем класс ip адреса
klass_ip=""
for klass in masiv["klass"]:
    if int(ip_in[0])>=masiv["klass"][klass][0] and int(ip_in[0])<=masiv["klass"][klass][1]:
        klass_ip=klass


#узнаём тип ip адреса
tip_ip=""
if ip_in[0]=="127" or ip_in[0]=="0"or ip_in[0]=="255":
    tip_ip="Специальный"
elif ip_in[0]=="10"  or (ip_in[0]=="172" and (int(ip_in[1])>16 and int(ip_in[1])<=32)) or (ip_in[0]=='192' and ip_in[1]=='168'):
    tip_ip="Локальный"
else:
    tip_ip="Глобальный"



#Вывод данных
print()
print(f"ip адрес: {'.'.join(ip_in)}")

print(f"Маска сети: {maska_ou}")

ip_ou_seti=".".join([str(int(i,2)) for i in ip_ou_seti_bin])
print(f"ip адрес сети: {ip_ou_seti}")

ip_ou_shir=".".join([str(int(i,2)) for i in ip_ou_shir_bin])
print(f"ip адрес широковещание: {ip_ou_shir}")

print(f"Количество узлов: {2**(32-int(maska_in))-2}")

print(f"Класс ip адреса: {klass_ip}")

print(f"Тип ip адреса: {tip_ip}")
