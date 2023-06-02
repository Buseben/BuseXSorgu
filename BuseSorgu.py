import os
import time

def BagimlilikKur(packet_name:str):
    print(">>> Gerekli Paketler Kuruluyor Beklemede Kalınız <<<\n\n")
    time.sleep(1)
    if os.name == "nt":
        os.system(f"pip install {packet_name}")
    else:
        try:
            os.system(f"pip3 install {packet_name}")
        except Exception:
            os.system(f"python3 -m pip install {packet_name}")

try:
    import json
except ImportError:
    BagimlilikKur("json")
    import json


try:
    import requests
except ImportError:
    BagimlilikKur("requests")
    import requests


try:
    from colorama import *
except ImportError:
    BagimlilikKur("colorama")
    from colorama import *


red = Fore.RED
blue = Fore.BLUE
reset = Fore.RESET
green = Fore.GREEN


STATTIK_AILE_URL = "http://45.95.65.175/api/aile/api.php"
STATIC_ADSOYAD_URL = "http://45.95.65.175/api/adsoyad/api.php"
STATIC_USERAGENT = "illegalXteam sorgu sistemi"


def ToolHakkında():
    str_data = f"""
{red}>> HAKKINDA:
Bu tool @Buseben Tarafından yazılmıştır sorumluluk kabul etmiyorum 

Telegram Kanalımız:https://t.me/Busetermux.
{reset}"""
    print(str_data)


def ClearScreen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def WaitUserKeys():
    input(f"\n--[ ENTER İLE DEVAM ET ]--")


def PrintBanner():
    str_data = f"""{red}
▀▀▀▀▀▀▀▀▀▀▀▀▀▀
▀ ▀
▀ B U S E   ▀
▀ ▀
▀▀▀▀▀▀▀▀▀▀▀▀▀▀         
                                          
            {blue}Saygılarla iyi sorgular @Buseben.
        {reset}"""
    print(str_data)


def EroorPrinter(err_msg:str):
    err_msg = str(err_msg)
    print(f"\n{red}[ HATA ]: {err_msg}! {reset}")


def InfoPrinter(informat_msg:str):
    info_msg = str(informat_msg)
    print(f"\n{green}[ BİLGİ ]:{blue} {info_msg} {reset}")


def AileSorgulama(target_tc:str):
    tc_num = str(target_tc)        
    req_headers = {
        "User-agent": STATIC_USERAGENT
        }
    req_data = {
        "tc": tc_num
        }
    
    RawResponse = requests.post(STATTIK_AILE_URL, headers=req_headers, data=req_data)

    if RawResponse.status_code == 200:
        return RawResponse.text
    else:
        return {"success": False, "messages":"işlem başarısız"}



while True:
    ClearScreen()
    PrintBanner()
    print(f"""
{green}0){blue} Tool hakkında
{green}1){blue} Ad soyad il ile sorgulama
{green}2){blue} Tc den aile sorgu

{green}99){red} Çıkış
{reset}""")

    UserSelections = input("[ işlem seçiniz ]: ")

    if UserSelections == "1":
        ClearScreen()
        print("")
        FirstName = input("[ Adı ] > ")
        LastName = input("[ Soyadı ] > ")
        NufusIl = input("[ Nufus il ] > ")
        
        if len(FirstName) <= 2 and len(LastName) <= 2:
            EroorPrinter("Geçersiz uzunlukta ad soyad")
            WaitUserKeys()
            continue
        
        if len(NufusIl) > 0:
            req_data = {
            "ad": str(FirstName),
            "soyad" : str(LastName),
            "il": str(NufusIl)
            }
        else:
            req_data = {
                "ad" : str(FirstName),
                "soyad" : str(LastName)
                }
    
        req_header = {
            "User-agent" : STATIC_USERAGENT
            }

        
        RawResponse = requests.post(STATIC_ADSOYAD_URL, headers=req_header, data=req_data)

        if RawResponse.status_code == 200:
            ParsedData = json.loads(RawResponse.text)

            #print(ParsedData)
            #exit(0)
            if ParsedData["success"] == True:
                InfoPrinter("İşlem başarılı veriler yazılıyor..\n")
                print(f"{blue}-------------- BİLGİLER --------------{reset}\n")
                time.sleep(1)
                DataDicList = ParsedData["data"]

                for single_element in DataDicList:
                    for dict_key in single_element:
                        if dict_key == "ANNEADI" or dict_key == "ANNETC":
                            continue
                        print(f"{blue}[ {str(dict_key)} ] >>{green} {str(single_element[str(dict_key)])}{reset}") 
                    print(f"{blue}"+"|"+"-"*30+reset)
            
            else:
                err_mesages = ParsedData["message"]
                EroorPrinter(f"İşlem başarısız oldu ")
                print(f"{green}[ SEBEP ]: {red}{err_masg}")

            WaitUserKeys()
            continue
        else:
            EroorPrinter(f"İşlem başarısız oldu http kodu: {str(RawResponse.status_code)}")
            WaitUserKeys()
            continue


    elif UserSelections == "0":
        ClearScreen()
        ToolHakkında()
        WaitUserKeys()
        continue

    elif UserSelections == "2":
        ClearScreen()
        sorgu_tc = input("Tc numarasını giriniz >> ")
        InfoPrinter("İstek işleniyor bekleyiniz..")
        Sonuclar = json.loads(AileSorgulama(sorgu_tc))
        
        if type(Sonuclar) == dict:
            EroorPrinter(f"İşlem başarısız.")
            err_masg = str(Sonuclar["Message"])
            print(f"{green}[SEBEP]: {red}{err_masg}{reset}")
            WaitUserKeys()
            continue
        else:
            InfoPrinter("İşlem başarılı veriler yazılıyor..\n")
            print(f"{blue}-------------- BİLGİLER --------------{reset}\n")
            time.sleep(1)
            for single_element in Sonuclar:
                for dict_key in single_element:
                    if dict_key == "Yakınlık":
                        print(f"{blue}[ YAKINLIK DURUMU ] >{green} {single_element[str(dict_key)]} {reset}")
                    
                    if dict_key == "KimlikNo": 
                        print(f"{blue}[ Tc numarası ] >{green} {single_element[str(dict_key)]} {reset}")

                    if dict_key == "Isim":
                        print(f"{blue}[ İsmi ] >{green} {single_element[str(dict_key)]} {reset}")

                    if dict_key == "Soyisim":
                        print(f"{blue}[ Soyadı ] >{green} {single_element[str(dict_key)]} {reset}")

                    if dict_key == "DogumTarihi":
                        print(f"{blue}[ Doğum Tarihi ] >{green} {single_element[str(dict_key)]} {reset}")

                    if dict_key == "NufusIl":
                        print(f"{blue}[ Nufus il ] >{green} {single_element[str(dict_key)]} {reset}")
                    
                    if dict_key == "NufusIlce":
                        print(f"{blue}[ Nufus ilçe ] >{green} {single_element[str(dict_key)]} {reset}")

                    if dict_key == "AnneIsim":
                        print(f"{blue}[ Anne Adı ] >{green} {single_element[str(dict_key)]} {reset}")

                    if dict_key == "AnneKimlikNo":
                        print(f"{blue}[ Anne Tc ] >{green} {single_element[str(dict_key)]} {reset}")

                    if dict_key == "BabaIsim":
                        print(f"{blue}[ Baba Adı ] >{green} {single_element[str(dict_key)]} {reset}")
                    
                    if dict_key == "BabaKimlikNo":
                        print(f"{blue}[ Baba Tc ] >{green} {single_element[str(dict_key)]} {reset}")

                
                print(f"{blue}"+"|"+"-"*30+reset)

            WaitUserKeys()
            continue
    elif UserSelections == "99":
        InfoPrinter("Sistemden çıktınız.")
        WaitUserKeys()
        break

    else:
        EroorPrinter("Bilinmeyen işlem isteği")
        WaitUserKeys()
        continue
