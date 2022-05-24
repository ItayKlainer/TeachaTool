from winreg import *

dict_string_winreg = {"HKEY_LOCAL_MACHINE": HKEY_LOCAL_MACHINE, "HKEY_CURRENT_USER": HKEY_CURRENT_USER}
#registry_list = ["is a key", "key", "sub_key", "value", "data_type", "active, passive"]
usb_list = ["HKEY_LOCAL_MACHINE", r"SYSTEM\CurrentControlSet\Services\USBSTOR", "Start", REG_DWORD, 3, 4]
cmd_list = ["HKEY_CURRENT_USER", r"SOFTWARE\Policies\Microsoft\Windows\System", "DisableCMD", REG_DWORD, 0 , 1]
download_list = ["HKEY_CURRENT_USER", r"SOFTWARE\Policies\Google\Chrome", "DownloadRestrictions", REG_DWORD, 4, 3]
internet_list1 = ["HKEY_CURRENT_USER", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "DisallowRun", REG_DWORD, 0, 1]
internet_list2 = ["HKEY_CURRENT_USER", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun", "1", REG_EXPAND_SZ, "", "Chrome.exe"]


'''
test_list1 = ["HKEY_CURRENT_USER", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "RestrictRun", REG_DWORD, 0, 1]
test_list2 = ["HKEY_CURRENT_USER", r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\RestrictRun", "1", REG_EXPAND_SZ, "", "pycharm64.exe"]
'''

permissions_list = [usb_list, cmd_list, download_list, internet_list1, internet_list2]


def apply_permission(i, active):
    key = dict_string_winreg[permissions_list[i][0]]
    connect = ConnectRegistry(None, key)
    opened_key = CreateKeyEx(connect, permissions_list[i][1], 0, KEY_ALL_ACCESS)
    if active == 1:
        SetValueEx(opened_key, permissions_list[i][2], 0, permissions_list[i][3], permissions_list[i][4])
    else:
        SetValueEx(opened_key, permissions_list[i][2], 0, permissions_list[i][3], permissions_list[i][5])





