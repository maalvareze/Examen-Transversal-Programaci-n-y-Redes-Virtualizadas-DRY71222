# vlan_check.py
def check_vlan(vlan_id):
    if 1 <= vlan_id <= 1005:
        return "VLAN en el rango normal"
    elif 1006 <= vlan_id <= 4094:
        return "VLAN en el rango extendido"
    else:
        return "VLAN fuera del rango permitido"

vlan_id = int(input("Ingrese el número de VLAN: "))
print(check_vlan(vlan_id))
