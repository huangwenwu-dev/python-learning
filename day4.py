contacts = {"老王": "12300000000", "老六": "32100000000"}
print(contacts)

contacts = {"老王": "12300000000", "老六": "32100000000"}
print(contacts.get("老刘"))

contacts = {"老王": "12300000000", "老六": "32100000000"}
print("老刘" in contacts)


contacts = {"老王": "12300000000"}
contacts["老六"] = "32100000000"
print(contacts)

contacts["老王"] = "11100000000"
print(contacts)


contacts = {"老王": "12300000000", "老六": "32100000000"}
del contacts["老六"]
print(contacts)

contacts = {"老王": "12300000000", "老六": "32100000000"}
contacts.pop("老王")
print(contacts)


contacts = {"老王": "12300000000", "老六": "32100000000"}
for name, phone in contacts.items():
    print(f"{name} 的电话是 {phone}")