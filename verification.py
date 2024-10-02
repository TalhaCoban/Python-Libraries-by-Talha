import socket
import uuid
import os
import hashlib
import winreg as reg



def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ':'.join([mac[e:e+2] for e in range(0, 12, 2)])


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def encrypt_mac_and_ip(mac, ip):
    # MAC ve IP adreslerini birleştirip SHA256 ile şifrele
    combined_str = mac + ip
    encrypted_str = hashlib.sha256(combined_str.encode()).hexdigest()
    return encrypted_str


def write_to_registry(encrypted_data):
    # Windows'ta regedit'e yazma
    key = reg.HKEY_CURRENT_USER
    sub_key = r"Software\ArcNet"
    try:
        reg.CreateKey(key, sub_key)
        registry_key = reg.OpenKey(key, sub_key, 0, reg.KEY_WRITE)
        reg.SetValueEx(registry_key, "Encrypted_Data", 0, reg.REG_SZ, encrypted_data)
        reg.CloseKey(registry_key)
        return True
    except Exception as e:
        print("Registry yazma hatası:", e)
        return False


def read_from_registry():
    # Windows'tan regedit'ten okuma
    key = reg.HKEY_CURRENT_USER
    sub_key = r"Software\ArcNet"
    try:
        registry_key = reg.OpenKey(key, sub_key, 0, reg.KEY_READ)
        encrypted_data = reg.QueryValueEx(registry_key, "Encrypted_Data")[0]
        reg.CloseKey(registry_key)
        return encrypted_data
    except Exception as e:
        print("Registry okuma hatası:", e)
        return None


def decrypt_and_compare(encrypted_data, mac, ip):
    # Registry'den alınan şifrelenmiş veriyi çöz ve karşılaştır
    expected_encrypted_data = encrypt_mac_and_ip(mac, ip)
    if encrypted_data == expected_encrypted_data:
        return True
    else:
        return False

def registry():
    # Eğer kayıtlı veri yoksa, kullanıcıdan MAC ve IP adreslerini alıp şifrele
    mac_address = get_mac_address()
    ip_address = get_ip_address()
    encrypted_data = encrypt_mac_and_ip(mac_address, ip_address)
    if write_to_registry(encrypted_data):
        print("MAC ve IP adresi başarıyla kaydedildi.")
        return True
    else:
        print("MAC ve IP adresi kaydedilemedi.")
        return False


def verification():
    
    # Registry'den kayıtlı veriyi oku
    encrypted_data = read_from_registry()

    # Kullanıcının MAC ve IP adresini tekrar al
    current_mac_address = get_mac_address()
    current_ip_address = get_ip_address()
    
    # Registry'den alınan veriyi çöz ve karşılaştır
    if decrypt_and_compare(encrypted_data, current_mac_address, current_ip_address):
        return True
    else: 
        return False
    
