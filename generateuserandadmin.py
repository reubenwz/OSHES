import random
import json

first_name_male = ["John", "Nick", "Charles", "Jay", "Andy"]
last_name_male = ["Jagger", "Tennessee", "Raymond", "Mathers","Tiger", "Roger"]

first_name_female = ["Aline", "Lisa", "Yui", "Jessica", "Veronica"]
last_name_female = ["Stewart","Tennessee", "Alba", "Brown", "Garcia"]
email = ["gmail", "hotmail"]
street = ["Upper Serangoon", "Kent Ridge", "Sembawang", "Jurong West", "Lower Seletar", "Tampines", "Tanjong Katong", "Ang Mo Kio", "Bishan", "Pasir Ris", "Woodleigh", "River Valley"]

def generate_phone_number():
    return '0' + random_number(3) + '-' + random_number(3) + '-' + random_number(4) 

def random_number(digits):
    sample = ['0','1','2','3','4','5','6','7','8','9']
    return ''.join(random.sample(sample, digits))

#customer
CUSTOMER_N = 20
with open('customers.json', 'w+') as f:
    customers = []
    for i in range(CUSTOMER_N):
        id = i + 1
        male = i % 2 == 0
        if male:
            name = random.choice(first_name_male) + ' ' + random.choice(last_name_male)
            gender = 'Male'
        else:
            name = random.choice(first_name_female) + ' ' + random.choice(last_name_female)
            gender = 'Female'
        
        email_address = '.'.join(name.lower().split(' ')) + '@' + random.choice(email) + '.com'
        phone_number = generate_phone_number()
        address = f'{random.randint(1,50)} {random.choice(street)} S{random_number(6)}' 
        password = 'password' + str(id)
        customers.append({'CustomerID':id, 'Name': name, 'Gender': gender, 'EmailAddress': email_address, 'PhoneNumber': phone_number, \
            'Address': address, 'Password': password})
    output = json.dumps(customers)
    f.write(output)

#admin
ADMIN_N = 5
with open('administrators.json', 'w+') as f:
    admins = []
    for i in range(ADMIN_N):
        id = i + 1
        male = i % 2 == 0
        if male:
            name = random.choice(first_name_male)
            gender = 'Male'
        else:
            name = random.choice(first_name_female)
            gender = 'Female'
        
        phone_number = generate_phone_number()
        password = 'password' + str(id)
        admins.append({'AdminID':id, 'Name': name, 'Gender': gender, 'PhoneNumber': phone_number, \
            'Password': password})
    output = json.dumps(admins)
    f.write(output)



