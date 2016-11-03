#!/usr/bin/env python
#-*-coding=utf-8-*-

# içe aktarmalar
from Tkinter import *
from threading import Thread
from time import sleep
import socket as sock





# oyunun yöneticisi olan "Oyun" sınıfını tanımlama
class Oyun(object):
    def __init__(self):
        self.nesneOlustur()
        self.tusBaglaAnaPencere()
        self.basla()
        self.anaPencere.mainloop()
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self):
        # ana pencereyi oluştur
        self.anaPencere = AnaPencere(320, 320)
        
        # ÜST KISIM
        # üst duvarı oluştur ve yerleştir
        duvarUst = Duvar(self.anaPencere, 32, 1, "#00FF00")
        duvarUst.pack()
        # ORTA KISIM
        cerceveOrta = Frame(self.anaPencere)
        cerceveOrta.pack()
        # sol duvarı oluştur ve yerleştir
        duvarSol = Duvar(cerceveOrta, 1, 30, "#00FF00")
        duvarSol.pack(side = "left")
        # sahayı oluştur ve yerleştir
        self.saha = Saha(cerceveOrta, 30, 30, "#FF0000")
        self.saha.pack(side = "left")
        # sağ duvarı oluştur ve yerleştir
        duvarSag = Duvar(cerceveOrta, 1, 30, "#00FF00")
        duvarSag.pack(side = "left")
        # ALT KISIM
        # alt duvarı oluştur ve yerleştir
        duvarAlt = Duvar(self.anaPencere, 32, 1, "#00FF00")
        duvarAlt.pack()
        
        # YEMİ OLUŞTUR
        self.yem = Yem(self.saha, 5, 5, "#0000FF")
        
        # DİĞER YILANI OLUŞTUR
        self.digerYilan = DigerYilan(self.saha, "#00FFFF")
        
        # ANA YILANI OLUŞTUR
        self.anaYilan = AnaYilan(self.saha, self.yem, "#FFFF00", 0.1)
        
        # sunucu ve istemci IP ve portlarını isteyen pencereyi oluştur
        self.pencereNet = PencereNet(self.anaPencere, self.anaYilan, self.digerYilan,
                                     self.yem, 160, 160)
    
    
    
    # ana pencerede kullanılacak tuşları ve basıldıklarında çalışacak fonksiyonları ayarla
    def tusBaglaAnaPencere(self):
        self.anaPencere.bind("<Return>", self.anaYilan.DuraklatHareketlendir)
        self.anaPencere.bind("<Right>", self.anaYilan.sagaDon)
        self.anaPencere.bind("<Down>", self.anaYilan.asagiDon)
        self.anaPencere.bind("<Left>", self.anaYilan.solaDon)
        self.anaPencere.bind("<Up>", self.anaYilan.yukariDon)
        self.anaPencere.bind("<Control-q>", self.cik)
    
    
    
    # başla...
    def basla(self):
        self.anaYilan.start()
    
    
    
    # programdan çık
    def cik(self, event = None):
        self.pencereNet.soket.close()
        self.anaYilan.ol()
        self.digerYilan.ol()
        self.anaPencere.destroy()
        exit()





# ana pencerenin sınıfı
class AnaPencere(Tk):
    def __init__(self, gen, yuk):
        Tk.__init__(self)
        self.nesneOlustur(gen, yuk)
        self.boyutlaOrtala()
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, gen, yuk):
        self.gen = gen
        self.yuk = yuk
    
    
    
    # pencereyi belirtilen boyutlara göre boyutlandır ve ekranda ortala
    def boyutlaOrtala(self):
        # ekran genisligi
        ekranGen = self.winfo_screenwidth()
        # ekran yuksekligi
        ekranYuk = self.winfo_screenheight()
        # pencere genisligi
        gen = self.gen
        # pencere yuksekligi
        yuk = self.yuk
        # pencereyi ortalamaya yarayacak x degeri
        x = (ekranGen - gen) / 2
        # pencereyi ortalamaya yarayacak y degeri
        y = (ekranYuk - yuk) / 2
        # pencerenin büyüklüğünü ayarlama ve pencereyi ortalama
        self.geometry("%dx%d+%d+%d" %(gen, yuk, x, y))





# yılanın hareket edeceği alanı sınırlayan duvarın sınıfı
class Duvar(Frame):
    def __init__(self, usta, gen, yuk, renk):
        Frame.__init__(self, usta, width = gen * 10, height = yuk * 10)
        self.nesneOlustur(usta, gen, yuk, renk)
        self.olustur()
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, usta, gen, yuk, renk):
        self.usta = usta
        self.gen = gen
        self.yuk = yuk
        self.renk = renk
    
    
    
    # duvarı oluştur
    def olustur(self):
        x = 0
        y = 0
        for i in range(self.gen):
            for j in range(self.yuk):
                canvas = Canvas(self, width = 10, height = 10,
                                bg = self.renk, highlightthickness = 0)
                canvas.place(x = x, y = y)
                y += 10
            y = 0
            x += 10





# yılanın hareket edeceği sahanın sınıfı
class Saha(Frame):
    def __init__(self, usta, gen, yuk, renk):
        Frame.__init__(self, usta, width = gen * 10, height = yuk * 10)
        self.nesneOlustur(usta, gen, yuk, renk)
        self.olustur()
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, usta, gen, yuk, renk):
        self.usta = usta
        self.gen = gen
        self.yuk = yuk
        self.renk = renk
        self.diziToprak = []
    
    
    
    # sahayı oluştur
    def olustur(self):
        for i in range(self.gen):
            self.diziToprak.append([])
        x = 0
        y = 0
        for i in range(self.gen):
            for j in range(self.yuk):
                self.diziToprak[i].append(Canvas(self, width = 10, height = 10,
                                                 bg = self.renk, highlightthickness = 0))
                self.diziToprak[i][j].place(x = x, y = y)
                y += 10
            y = 0
            x += 10





# ana yılanın sınıfı
class AnaYilan(Thread):
    def __init__(self, saha, yem, renk, sureBekleme):
        Thread.__init__(self)
        self.nesneOlustur(saha, yem, renk, sureBekleme)
        self.goster()
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, saha, yem, renk, sureBekleme):
        self.saha = saha
        self.yem = yem
        self.renk = renk
        self.sureBekleme = sureBekleme
        self.canliMi = True
        self.hareketliMi = False
        # yılanın güncel koordinatları
        # yılanın başı en başta olacak şekilde belirlenir
        self.koorlar = [[3, 0], [2, 0], [1, 0]]
        # yılanın bir önceki koordinatları
        # yılanın başı en başta olacak şekilde belirlenir
        self.koorlarOnceki = [[2, 0], [1, 0], [0, 0]]
        # öntanımlı yön
        self.yon = "sag"
    
    
    
    # sağa dön
    def sagaDon(self, event = None):
        if self.yon == "yukari":
            self.yon = "sag"
        if self.yon == "asagi":
            self.yon = "sag"
    
    # aşağı dön
    def asagiDon(self, event = None):
        if self.yon == "sag":
            self.yon = "asagi"
        if self.yon == "sol":
            self.yon = "asagi"
    
    # sola dön
    def solaDon(self, event = None):
        if self.yon == "yukari":
            self.yon = "sol"
        if self.yon == "asagi":
            self.yon = "sol"
    
    # yukarı dön
    def yukariDon(self, event = None):
        if self.yon == "sag":
            self.yon = "yukari"
        if self.yon == "sol":
            self.yon = "yukari"
    
    
    
    # yılan hareketliyse duraklat, duraklatıldıysa hareketlendir
    def DuraklatHareketlendir(self, event = None):
        self.hareketliMi = True if self.hareketliMi == False else False
    
    
    
    # run...
    def run(self):
        while True:
            # yılanı göster
            self.goster()
            # yılanı hareket ettir
            self.hareketEt()
    
    
    
    # yılanı göster
    def goster(self):
        # eğer yılan canlıysa...
        if self.canliMi == True:
            # önce kuyruktan bir birim sil
            sonParcaX = self.koorlarOnceki[-1][0]
            sonParcaY = self.koorlarOnceki[-1][1]
            self.saha.diziToprak[sonParcaX][sonParcaY].configure(bg = self.saha.renk)
            # sonra yılanı çiz
            for koor in self.koorlar:
                self.saha.diziToprak[koor[0]][koor[1]].configure(bg = self.renk)
    
    
    
    # yılanı hareket ettir
    def hareketEt(self):
        # belirli bir süre bekle
        sleep(self.sureBekleme)
        
        # eğer yılan canlı ve hareketliyse...
        if self.canliMi == True and self.hareketliMi == True:
            # önceki koordinatları belirle
            for i in range(len(self.koorlar)):
                for j in range(len(self.koorlar[i])):
                    self.koorlarOnceki[i][j] = self.koorlar[i][j]
            
            # yılanın başını güncel yönde bir adım götür
            if self.yon == "sag":
                self.koorlar[0][0] += 1    # x i 1 artır
            if self.yon == "asagi":
                self.koorlar[0][1] += 1    # y yi 1 artır
            if self.yon == "sol":
                self.koorlar[0][0] -= 1    # x i 1 azalt
            if self.yon == "yukari":
                self.koorlar[0][1] -= 1    # y yi 1 azalt
            # diğer parçaları bir sonraki parçanın önceki yerine koy
            for i in range(1, len(self.koorlar)):
                for j in range(len(self.koorlar[i])):
                    self.koorlar[i][j] = self.koorlarOnceki[i - 1][j]
            
            # olası durumlara bak
            durum = self.durumaBak()
            # durumu değerlendir
            self.durumDegerlendir(durum)
    
    
    
    # çarpışma varsa "carp", yem yenmişse "ye", diğer durumlarda "hic" döndürür
    def durumaBak(self):
        if self.carpismaVarMi() == True:
            return "carp"
        elif self.yemYenmisMi() == True:
            return "ye"
        else:
            return "hic"
    
    
    
    # çarpışma var mı diye bak
    def carpismaVarMi(self):
        # eğer yılan sırasıyla sol, üst, sağ veya alt duvara çarpmışsa...
        if self.koorlar[0][0] == -1 or \
           self.koorlar[0][1] == -1 or \
           self.koorlar[0][0] == self.saha.gen or \
           self.koorlar[0][1] == self.saha.yuk:
            return True    # ...True döndür
        # eger yilan herhangi bir sekilde kendine carpmissa...
        for liste in self.koorlar[3:]:
            if liste == self.koorlar[0]:
                return True    # True döndür
        # buraya gelindiyse çarpma yoktur
        return False    # False döndür
    
    
    
    # yem yenmiş mi diye bak
    def yemYenmisMi(self):
        # yem yenmişse...
        if self.koorlar[0] == [self.yem.x, self.yem.y]:
            return True    # ...True döndür
        # buraya gelindiyse yem yenmemiştir
        return False    # False döndür
    
    
    
    # durumu değerlendir
    def durumDegerlendir(self, durum):
        # eğer çarpma varsa...
        if durum == "carp":
            self.ol()    # yılanı öldür
        # eğer yem yenmişse...
        elif durum == "ye":
            self.beslen()    # yılanı besle
        # eğer hiçbir şey yoksa...
        else:
            pass    # hiçbir şey yapma
    
    
    
    # yılanı öldür
    def ol(self):
        self.canliMi = False
    
    
    
    # yılanı besle
    def beslen(self):
        # yılanın önceki pozisyonundaki en son birimini yılanın yeni pozisyonuna ekle
        # böylece yılan bir birim büyümüş olur
        x = self.koorlarOnceki[-1][0]
        y = self.koorlarOnceki[-1][1]
        self.koorlar.append([x, y])
        # "koorlar" listesinin büyümesine paralel olarak
        # "koorlarOnceki" listesini de büyüt
        self.koorlarOnceki.append([0, 0])





# diğer yılanın sınıfı
class DigerYilan(object):
    def __init__(self, saha, renk):
        self.nesneOlustur(saha, renk)
        self.goster()
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, saha, renk):
        self.saha = saha
        self.renk = renk
        self.canliMi = True
        # yılanın güncel koordinatları
        # yılanın başı en başta olacak şekilde belirlenir
        self.koorlar = [[3, 0], [2, 0], [1, 0]]
        # yılanın bir önceki koordinatları
        # yılanın başı en başta olacak şekilde belirlenir
        self.koorlarOnceki = [[2, 0], [1, 0], [0, 0]]
    
    
    
    # yılanı göster
    def goster(self):
        # eğer yılanın boyu büyümüşse...
        if len(self.koorlar) > len(self.koorlarOnceki):
            # önceki koordinatların sonuna bir parça daha ekle
            self.koorlarOnceki.append([0, 0])
        # eğer yılan canlıysa...
        if self.canliMi == True:
            # eğer yılanın güncel koordinatlarında bir değişiklik varsa
            if self.koorlarOnceki[0] != self.koorlar[1]:
                # önceki koordinatların son parcasini sil
                self.koorlarOnceki.pop()
                # önceki koordinatların başına şimdiki koordinatların baştan ikinci öğesini ekle
                self.koorlarOnceki.insert(0, self.koorlar[1])
            # önce kuyruktan bir birim sil
            sonParcaX = self.koorlarOnceki[-1][0]
            sonParcaY = self.koorlarOnceki[-1][1]
            self.saha.diziToprak[sonParcaX][sonParcaY].configure(bg = self.saha.renk)
            # sonra yılanı çiz
            for koor in self.koorlar:
                self.saha.diziToprak[koor[0]][koor[1]].configure(bg = self.renk)
    
    
    
    # öldür
    def ol(self):
        self.canliMi = False





# yılanın yediği yemin sınıfı
class Yem(object):
    def __init__(self, saha, x, y, renk):
        self.nesneOlustur(saha, x, y, renk)
        self.goster()
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, saha, x, y, renk):
        self.saha = saha
        self.x = x
        self.y = y
        self.xEski = self.x
        self.yEski = self.y
        self.renk = renk
    
    
    
    # yemi göster
    def goster(self):
        if self.x != self.xEski and self.y != self.yEski:
            # önceki yemi sil
            self.saha.diziToprak[self.xEski][self.yEski].configure(bg = self.saha.renk)
            self.xEski = self.x
            self.yEski = self.y
        
        # yeni yemi koy
        self.saha.diziToprak[self.x][self.y].configure(bg = self.renk)





# sunucunun ve istemcinin IP ve port larının istendiği pencerenin sınıfı
class PencereNet(Toplevel):
    def __init__(self, anaPencere, anaYilan, digerYilan, yem, gen, yuk):
        Toplevel.__init__(self)
        self.nesneOlustur(anaPencere, anaYilan, digerYilan, yem, gen, yuk)
        self.ortala()
        self.aracYerlestir()
        self.transient(self.anaPencere)    # pencereyi ana pencerenin üstüne getir
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, anaPencere, anaYilan, digerYilan, yem, gen, yuk):
        self.anaPencere = anaPencere
        self.anaYilan = anaYilan
        self.digerYilan = digerYilan
        self.yem = yem
        self.gen = gen
        self.yuk = yuk
        self.IPSunucu = None
        self.IPIstemci = None
        self.portSunucu = None
        self.portIstemci = None
        self.soket = None
        self.gonderici = None
        self.alici = None
    
    
    
    # pencereyi ekranda ortala
    def ortala(self):
        # ekran genisligi
        ekranGen = self.winfo_screenwidth()
        # ekran yuksekligi
        ekranYuk = self.winfo_screenheight()
        # pencere genisligi
        gen = self.gen
        # pencere yuksekligi
        yuk = self.yuk
        # pencereyi ortalamaya yarayacak x degeri
        x = (ekranGen - gen) / 2
        # pencereyi ortalamaya yarayacak y degeri
        y = (ekranYuk - yuk) / 2
        # pencerenin büyüklüğünü ayarlama ve pencereyi ortalama
        self.geometry("%dx%d+%d+%d" %(gen, yuk, x, y))
    
    
    
    # pencereye araçları yerleştir
    def aracYerlestir(self):
        # çerçeveleri yerleştir
        cerceve1 = Frame(self)
        cerceve1.pack()
        cerceve2 = Frame(self)
        cerceve2.pack()
        cerceve3 = Frame(self)
        cerceve3.pack()
        cerceve4 = Frame(self)
        cerceve4.pack()
        # etiketleri yerleştir
        Label(cerceve1, text = "Istemci IP: ").pack(side = LEFT)
        Label(cerceve2, text = "Istemci port: ").pack(side = LEFT)
        Label(cerceve3, text = "Sunucu IP: ").pack(side = LEFT)
        Label(cerceve4, text = "Sunucu port: ").pack(side = LEFT)
        # girişleri yerleştir
        self.girisIPIstemci = Entry(cerceve1)
        self.girisIPIstemci.insert(END, "127.0.0.1")
        self.girisIPIstemci.pack(side = LEFT)
        self.girisPortIstemci = Entry(cerceve2)
        self.girisPortIstemci.pack(side = LEFT)
        self.girisIPSunucu = Entry(cerceve3)
        self.girisIPSunucu.insert(END, "127.0.0.1")
        self.girisIPSunucu.pack(side = LEFT)
        self.girisPortSunucu = Entry(cerceve4)
        self.girisPortSunucu.pack(side = LEFT)
        # tamam tuşunu yerleştir
        Button(self, text = "Tamam", command = self.bilgiAlIsle).pack()
    
    
    
    # penceredeki girişlere girilen bilgileri al ve işle
    def bilgiAlIsle(self):
        # IP ve port ları ilişkili değişkenlere kaydet
        self.IPIstemci = self.girisIPIstemci.get()
        self.IPSunucu = self.girisIPSunucu.get()
        self.portIstemci = int(self.girisPortIstemci.get())
        self.portSunucu = int(self.girisPortSunucu.get())
        
        # bir soket aç
        self.soket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM, sock.IPPROTO_UDP)
        # soketi açarken bir hata oluşup oluşmadığını kontrol et
        if self.soket < 0:
            print "Soketi acarken bir hata olustu."
            exit()
        # bu soketi istemcinin IP ve port una bağla
        self.soket.bind((self.IPIstemci, self.portIstemci))
        
        # gönderici ve alıcıyı oluştur
        self.gonderici = Gonderici(self.soket, self.IPSunucu, self.portSunucu,
                                   self.anaYilan)
        self.alici = Alici(self.soket, self.digerYilan, self.yem)
        # gönderici ve alıcıyı başlat
        self.gonderici.start()
        self.alici.start()
        
        # en son bu pencereyi kapat
        self.destroy()





# göndericinin sınıfı
class Gonderici(Thread):
    def __init__(self, soket, IP, port, anaYilan):
        Thread.__init__(self)
        self.nesneOlustur(soket, IP, port, anaYilan)
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, soket, IP, port, anaYilan):
        self.soket = soket
        self.IP = IP
        self.port = port
        self.anaYilan = anaYilan
    
    
    
    # run...
    def run(self):
        while True:
            # gönderilecek veriyi hazırla
            # ana yılanın koordinatlarını içerir
            strGonder = "yilan:" + str(self.anaYilan.koorlar)
            # ana yılanın koordinatlarını sunucuya gönder
            sonuc = self.soket.sendto(strGonder, (self.IP, self.port))
            # veri gönderilirken bir hata oluşup oluşmadığını kontrol et
            if sonuc < 0:
                print "Veri gonderilirken bir hata olustu."
                self.soket.close()
                exit()





# alıcının sınıfı
class Alici(Thread):
    def __init__(self, soket, digerYilan, yem):
        Thread.__init__(self)
        self.nesneOlustur(soket, digerYilan, yem)
    
    
    
    # sınıfın nesnelerini oluştur
    def nesneOlustur(self, soket, digerYilan, yem):
        self.soket = soket
        self.digerYilan = digerYilan
        self.yem = yem
    
    
    
    # run...
    def run(self):
        while True:
            # VERİYİ AL
            # kaç byte veri alınacağını belirle
            kacByte = 40000
            # veriyi al
            # bu veri sunucudan geldiğine göre oradaki ana yılanın ve yemin
            # koordinatlarını belirtecek
            veri, address = self.soket.recvfrom(kacByte)
            # veri alınırken bir hata oluşup oluşmadığını kontrol et
            if veri < 0:
                print "Veri alinirken bir hata olustu."
                self.soket.close()
                exit()
            
            # VERİYİ İŞLE
            # veriyi yılana ait olanlar ve yeme ait olanlar olmak üzere ikiye ayır
            indis = veri.find("yem")
            # aranan bulunabildi mi bulunamadı mı diye kontrol et
            if indis < 0:
                print "'yem' karakter dizisi bulunamadı."
            veriYilan = veri[:indis]
            veriYem = veri[indis:]
            # yılana ait veriden "yilan:" ön ekini çıkar
            veriYilan = veriYilan[6:]
            # yeme ait veriden "yem:" ön ekini çıkar
            veriYem = veriYem[4:]
            # yılanın yeni koordinatlarını liste haline getir
            koorlarYilan = eval(veriYilan)
            # yemin yeni koordinatlarını liste haline getir
            koorlarYem = eval(veriYem)
            # buradaki diğer yılanın koordinatlarını yeni koordinatlar haline getir
            self.digerYilan.koorlar = koorlarYilan
            # diğer yılanı göster
            self.digerYilan.goster()
            # buradaki yemin koordinatlarını yeni koordinatlar haline getir
            [self.yem.x, self.yem.y] = koorlarYem
            # yemi göster
            self.yem.goster()





if __name__ == "__main__":
    Oyun()
