from winreg import *

registry_list = ["key", "sub_key", "value", "data_type", "active/passive"]
usb_list = ["HKEY_LOCAL_MACHINE", r"SYSTEM\CurrentControlSet\Services\USBSTOR", "Start", "REG_DWORD", "3", "4"]
dict_string_winreg = {"HKEY_LOCAL_MACHINE": HKEY_LOCAL_MACHINE}
#key, sub_key, value,data_type, active/passive
#HKEY_CURRENT_USER\Software\Policies\Microsoft\Internet Explorer
#DWORD NoBrowserOptions 1/0


def edit_permission(reg_list, active):
    key = dict_string_winreg[usb_list[0]]
    connect = ConnectRegistry(None, key)
    opened_key = OpenKey(connect, usb_list[1], 0, KEY_ALL_ACCESS)
    if active:
        SetValueEx(opened_key, usb_list[2], 0, usb_list[3], usb_list[4])
    else:
        SetValueEx(opened_key, usb_list[2], 0, usb_list[3], usb_list[5])


edit_permission(usb_list, True)