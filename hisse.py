import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore,QtGui
import requests
from PyQt5.QtGui import *
from bs4 import BeautifulSoup
import pandas as pd
import winreg as wr

url = "https://uzmanpara.milliyet.com.tr/canli-borsa/bist-TUM-hisseleri/"
response = requests.get(url)
html_icerigi = response.content
soup = BeautifulSoup(html_icerigi,"html.parser")


def get_data_for_one(kod):
    fiyat = soup.find_all("tr",{"id":"h_tr_id_"+kod})
    dizi = []

    dizi.append(str(fiyat).split("</td>")[2].split(">")[1]+"₺")
    dizi.append(str(fiyat).split("</td>")[3].split(">")[1]+"%")
    dizi.append(str(fiyat).split("</td>")[4].split(">")[1])
    return dizi

def get_data_for_all():
    fiyat = soup.find_all("tr",{"class":"zebra"})
    dizi = []
    for i in fiyat:
        dizi.append(str(i).split("\"")[3].split("_")[3])
    return dizi

def refresh(tableWidget):
    tableWidget.update()

def get_kodlar():
    key_location = r'Software\\'
    key = wr.OpenKey(wr.HKEY_CURRENT_USER, key_location, 0, wr.KEY_ALL_ACCESS)
    value = wr.QueryValueEx(key, 'value One')
    return str(value[0]).split(",")
def set_kodlar(dizi):
    write_this=''
    for i in dizi:
        if(len(write_this)==0):
            write_this = i
        else:
            write_this = write_this+","+i

    key_location = r'Software\\'
    key = wr.OpenKey(wr.HKEY_CURRENT_USER, key_location, 0, wr.KEY_ALL_ACCESS)
    value = wr.SetValueEx(key, "value One", 0, wr.REG_SZ,write_this)

kodlar=get_kodlar()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = QWidget()
    screen.setWindowTitle("Hisse Senedi Takip")
    tableWidget = QTableWidget(len(kodlar)+1,5,screen)
    screen.setGeometry(1000,50,800,500)
    total_button_count = 0
    
    def on_click_for_delete(index):
        global total_button_count 
        total_button_count = 0
        if len(kodlar)>=1:
            kodlar.remove(index)
        screen.hide()
        show_table()
        screen.show()
    
    def on_click_for_add(kod):
        global total_button_count
        total_button_count = 0 
        kodlar.append(kod)
        screen.hide()
        show_table()
        screen.show()

    def create_button(text):
        global total_button_count 
        
        buton = QPushButton("X",screen)
        buton.move(500,27+total_button_count*30)
        buton.clicked.connect(lambda:on_click_for_delete(text))
        total_button_count += 1
        return buton

    def show_table():
        items = get_data_for_all()
        for i in kodlar:
            items.remove(i)
        tableWidget = QTableWidget(len(kodlar),5,screen)
        tableWidget.setWindowTitle("Hisse Takip Uygulaması")
        tableWidget.verticalHeader().hide()
        tableWidget.setHorizontalHeaderItem(0,QTableWidgetItem("Hisse Kodu"))
        tableWidget.setHorizontalHeaderItem(1,QTableWidgetItem("Hisse Fiyatı"))
        tableWidget.setHorizontalHeaderItem(2,QTableWidgetItem("Değişim"))
        tableWidget.setHorizontalHeaderItem(3,QTableWidgetItem("Son Güncelleme"))
        tableWidget.setHorizontalHeaderItem(4,QTableWidgetItem(""))
        for j in range(0,len(kodlar)):
            dizi = get_data_for_one(kodlar[j])
            tableWidget.setItem(j,0,QTableWidgetItem(kodlar[j]))
            for i in range(1,len(dizi)+1):
                
                if i == 2:
                    if(float(dizi[i-1].replace('%', '').replace(",","."))>0):
                        tableWidget.setItem(j,i,QTableWidgetItem(dizi[i-1]))
                        tableWidget.item(j,i).setBackground(QtGui.QColor("#235846"))
                        tableWidget.item(j,i).setForeground(QBrush(QColor(255, 255, 255)))
                    elif(float(dizi[i-1].replace('%', '').replace(",","."))==0):
                        tableWidget.setItem(j,i,QTableWidgetItem(dizi[i-1]))
                    else:
                        tableWidget.setItem(j,i,QTableWidgetItem(dizi[i-1]))
                        tableWidget.item(j,i).setBackground(QtGui.QColor("#E40511"))
                        tableWidget.item(j,i).setForeground(QBrush(QColor(255, 255, 255)))
                else:
                    tableWidget.setItem(j,i,QTableWidgetItem(dizi[i-1]))
        tableWidget.horizontalHeader().setStretchLastSection(True)
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableWidget.setMinimumWidth(screen.width()-200)
        tableWidget.setMinimumHeight(screen.height())
        
        butonlar = []
        for i in kodlar:
            create_button(i).show()

        komboBoxWidget = QComboBox(screen)
        komboBoxWidget.move(615,57)
        komboBoxWidget.addItems(items)
        label = QLabel(screen)
        label.setText("Hisse Ekle")
        label.move(620,35)
        save_label = QLabel(screen)
        buton = QPushButton("Ekle",screen)
        buton.move(685,55)
        buton.clicked.connect(lambda:on_click_for_add(komboBoxWidget.currentText()))
        buton.show()
    
    
        save_buton = QPushButton("Kaydet",screen)
        save_buton.move(650,350)
        save_buton.clicked.connect(lambda:for_save_button())
        save_buton.show()
        
        
        
        def for_save_button():
            global total_button_count
            total_button_count = 0 
            set_kodlar(kodlar)
            save_label.setText("Kaydedildi")
            save_label.setGeometry(665,375,50,15)
            screen.hide()
            show_table()
            screen.show()
    
    
    
    
    
    show_table()
    screen.show()
    
    sys.exit(app.exec_())