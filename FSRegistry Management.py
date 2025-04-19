import argparse
import os
import shutil
import winreg

parser = argparse.ArgumentParser()

parser.add_argument("--create", help="Create file. The command takes one argument: file name.")
parser.add_argument("--delete", help="Delete file. The command takes one argument: file name.")
parser.add_argument("--write", help="Write in file. The command takes two arguments: file name, text.", nargs=2)
parser.add_argument("--read", help="Read from file. The command takes one argument.")
parser.add_argument("--copy", help="Copy file from one directory to another. The command takes two arguments: first directory, second directory.", nargs=2)
parser.add_argument("--rename", help="Rename file. The command takes two arguments: full path to the file and new full path to the new file.", nargs=2)
parser.add_argument("--keyCreate", help="Create key. The command takes two arguments.", nargs=2)
parser.add_argument("--keyDelete", help="Delete key. The command takes two arguments.", nargs=2)
parser.add_argument("--keyWrite", help="Create key. The command takes four arguments.", nargs=4)

args = parser.parse_args()

def get_hkey(hkey):
    keys = {
        "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
        "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
        "HKEY_USERS": winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
        }
    return keys.get(hkey.upper())
def create_key(hkey_name, sub_key):
    hkey = get_hkey(hkey_name)
    key = winreg.CreateKeyEx(hkey, sub_key, 0, winreg.KEY_ALL_ACCESS)
    winreg.CloseKey(key)
    return
def delete_key(hkey_name, sub_key):
    hkey = get_hkey(hkey_name)
    try:
        winreg.DeleteKey(hkey, sub_key)
    except FileNotFoundError:
        print("Error.")
    return
def write_key(hkey_name, sub_key, name, value):
    hkey = get_hkey(hkey_name)
    try:
        key = winreg.OpenKeyEx(hkey, sub_key, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
    except FileNotFoundError:
        print("Error.")
def create_file(file_name):
    try:
        open(file_name, "w")
        print("File created.")
    except FileExistsError:
        print("Error.")
        return
def delete_file(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("Error.")
        return
    file.close()
    os.remove(file_name)
    print("You have deleted ", file_name)
def write_file(file_name, text):
    try:
        file = open(file_name, "a")
        file.write(text)
        file.close()
        print("Information added to the file.")
    except FileNotFoundError:
        print("Error.")
        return
def read_file(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("Error.")
        return
    print(file.read())
    file.close()
def copy_file(sourse, dest):
    try:
        shutil.copyfile(sourse, dest)
        print("File was copied.")
    except FileNotFoundError:
        print("Error.")
        return
def rename_file(file_name, new_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("Error." "")
        return
    try:
        file = open(new_name, "r")
    except FileNotFoundError:
        file.close()
        os.rename(file_name, new_name)
        print("The name of file was changed from", file_name, "to", new_name)
        return
    print("There is already a file with this name:", new_name)
    return


if args.create:
    create_file(args.create)
elif args.delete:
    delete_file(args.delete)
elif args.write:
    write_file(args.write[0], args.write[1])
elif args.read:
    read_file(args.read)
elif args.copy:
    copy_file(args.copy[0], args.copy[1])
elif args.rename:
    rename_file(args.rename[0], args.rename[1])
elif args.keyCreate:
    create_key(args.keyCreate[0], args.keyCreate[1])
elif args.keyDelete:
    delete_key(args.keyDelete[0], args.keyDelete[1])
elif args.keyWrite:
    write_key(args.keyWrite[0], args.keyWrite[1], args.keyWrite[2], args.keyWrite[3])
