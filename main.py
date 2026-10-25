import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


for contact in contacts_list[1:]: 
    fio_string = " ".join(contact[:3])
    fio_parts = fio_string.split()
    
    if len(fio_parts) >= 3:
        contact[0], contact[1], contact[2] = fio_parts[0], fio_parts[1], fio_parts[2]
    elif len(fio_parts) == 2:
        contact[0], contact[1], contact[2] = fio_parts[0], fio_parts[1], ""
    elif len(fio_parts) == 1:
        contact[0], contact[1], contact[2] = fio_parts[0], "", ""


pattern = r"(\+7|8)[\s\(]*(\d{3})[\s\)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s\(]*(?:доб\.?\s*(\d+))?"

for contact in contacts_list[1:]:
    phone = contact[5] 
    
    if phone: 
        match = re.search(pattern, phone)
        if match:
            new_phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
            

            if match.group(6):
                new_phone += f" доб.{match.group(6)}"
            
            contact[5] = new_phone


contacts_dict = {}

for contact in contacts_list[1:]:
    fio_key = (contact[0], contact[1])
    
    if fio_key not in contacts_dict:
        contacts_dict[fio_key] = contact
    else:
        existing_contact = contacts_dict[fio_key]

        for i in range(2, len(contact)):
            if not existing_contact[i] and contact[i]:
                existing_contact[i] = contact[i]
                
final_contacts_list = [contacts_list[0]] + list(contacts_dict.values())
                
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contacts_list)

print("Готово! Данные обработаны и сохранены в phonebook.csv")