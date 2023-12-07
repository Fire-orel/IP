import sys
from ip_view import Ui_Form
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication
import json


class window(Ui_Form,QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUi()
    def initUi(self):
        self.info_ou.setReadOnly(True)
        self.btn.clicked.connect(self.proces)
    def proces(self):
        with open("masiv.json","r") as f:
            self.masiv=json.load(f)
        ip_in=self.ip_in.text()
        mask_in=self.maska_in.text()
        ip_in_prov=self.proverka_ip(ip_in)
        maska_ou=self.proverka_maski(mask_in)
        if ip_in_prov =="ip адрес указон не коректно!!" and maska_ou=="Маска указан не коректо!!!! ":
            ou=ou=ip_in_prov+'\n'+maska_ou
            self.info_ou.setText(ou)
        elif ip_in_prov =="ip адрес указон не коректно!!"  :
            ou=ip_in_prov
            self.info_ou.setText(ou)
        elif maska_ou=="Маска указан не коректо!!!! ":
            ou=maska_ou
            self.info_ou.setText(ou)
        else:
            ip_in=ip_in.split(".")
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
            for klass in self.masiv["klass"]:
                if int(ip_in[0])>=self.masiv["klass"][klass][0] and int(ip_in[0])<=self.masiv["klass"][klass][1]:
                    klass_ip=klass


            #узнаём тип ip адреса
            tip_ip=""
            if ip_in[0]=="127" or ip_in[0]=="0"or ip_in[0]=="255":
                tip_ip="Специальный"
            elif ip_in[0]=="10" or ip_in[0]=="127" or (ip_in[0]=="172" and (int(ip_in[1])>16 and int(ip_in[1])<=32)) or (ip_in[0]=='192' and ip_in[1]=='168'):
                tip_ip="Локальный"
            else:
                tip_ip="Глобальный"

            ip_ou_seti=".".join([str(int(i,2)) for i in ip_ou_seti_bin])
            ip_ou_shir=".".join([str(int(i,2)) for i in ip_ou_shir_bin])
            ou=f"ip адрес: {'.'.join(ip_in)}"+"\n"+f"Маска сети: {maska_ou}"+"\n"+f"ip адрес сети: {ip_ou_seti}"+"\n"+f"ip адрес широковещание: {ip_ou_shir}"+"\n"+f"Количество узлов: {2**(32-int(mask_in))-2}"+"\n"+f"Класс ip адреса: {klass_ip}"+"\n"+f"Тип ip адреса: {tip_ip}"
            self.info_ou.setText(ou)




    def proverka_ip(self,ip):
        try:
            ip=ip.split(".")
            for i in ip:
                if int(i)>255:
                    return "ip адрес указон не коректно!!"
                    exit()
            return 0
        except:
            return "ip адрес указон не коректно!!"
    def proverka_maski(self, maska_in):
        if maska_in in self.masiv["maski"]:
            maska_ou=self.masiv["maski"][maska_in]
            return maska_ou
        else:
            return "Маска указан не коректо!!!! "




if __name__=="__main__":
    app=QApplication(sys.argv)
    ex=window()
    ex.show()
    sys.exit(app.exec_())
