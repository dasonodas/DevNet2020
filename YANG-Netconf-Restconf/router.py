#!/usr/bin/env python3

import json, requests, xmltodict
from ncclient import manager
import xml.dom.minidom
from tabulate import *

requests.packages.urllib3.disable_warnings()

router = {
    "address": "10.10.20.48",
    "netconf-port": 830 ,
    "restconf-port": 443,
    "username": "developer",
    "password": "C1sco12345"
}


def print_options():
    print("""
    Elija una de las siguientes opciones:
        1) Obtener una lista de las interfaces del router
        2) Crear una interfaz de loopback
        3) Eliminar una interfaz
        4) Ver la tabla de rutas
        
        0) Salir
    """)
    



def change_router_settings():
    print("Antes de empezar vamos a configurar los parametros de conexion con el router.")
    print("La configuracion por defecto es: ")
    print("\tDireccion: ", router["address"])
    print("\tPuerto de netconf: ", router["netconf-port"])
    print("\tPuerto de restconf: ", router["restconf-port"])
    print("\tNombre de usuario: ", router["username"])
    print("\tContraseña de usuario: ", router["password"])

    aux = input("\n¿Quiere continuar con esta configuración? (s/n): ").lower()
    if aux == "s":
        print("Perfecto")
        return
    else:
        while True:
            try:
                router["address"] = input("Introduce la direccion del router")
                router["netconf-port"] = int(input("Introduce el puerto de netconf"))
                router["restconf-port"] = int(input("Introduce el puerto de restconf"))
                router["username"] = input("Introduce el numbre de usuario")
                router["password"] = input("Introduce la contraseña de usuario")
            except ValueError:
                print("Ha habido un error, vuelva a introducir los valores")
            print("\n\tSe han salvado los parametros.")
            break


# Build the restconf base url, append the port in case of not using 443
def get_restconf_base_url():
    return ("https://{}:{}/restconf/data/".format(router["address"], router["restconf-port"]))


def get_interfaces_netconf():
    # Definimos la conexion
    con = manager.connect(host = router["address"], port = router["netconf-port"],
                    username = router["username"],
                    password = router["password"],
                    hostkey_verify = False)

    # Filtro para netconf
    netconf_filter = """
    <filter>
        <interfaces	xmlns="http://openconfig.net/yang/interfaces">
        </interfaces>
    </filter>
    """

    netconf_reply = con.get_config(source="running", filter = netconf_filter)

    reply_dict = xmltodict.parse(netconf_reply.xml)
    interface_lists = []
    i = 0
    for interface in reply_dict["rpc-reply"]["data"]['interfaces']["interface"]:
        int_status = interface["config"]["enabled"]
        if  "ipv4" in interface["subinterfaces"]["subinterface"]:
            ip_addr = interface["subinterfaces"]["subinterface"]["ipv4"]["addresses"]["address"]["ip"]
        else:
            ip_addr = "None"

        if "ethernet" in interface:
            mac_addr = interface["ethernet"]["config"]["mac-address"]
        else:
            mac_addr = "None"
        
        interface_lists.append([interface["name"], ip_addr, int_status, mac_addr])
    return interface_lists


def create_loopback_interface_restconf(name, description, ip_addr, netmask):
    #Into to send
    base_url = get_restconf_base_url()
    final_url = base_url + "ietf-interfaces:interfaces/interface=" + name

    auth = (router["username"], router["password"])

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }


    yang_config = {
        "ietf-interfaces:interface": {
            "name": name,
            "description": description,
            "type": "iana-if-type:softwareLoopback",
            "enabled": True,
            "ietf-ip:ipv4": {
                "address": [
                    {
                        "ip": ip_addr,
                        "netmask": netmask
                    }
                ]
            },
            "ietf-ip:ipv6": {}
        }
    }
    resp = requests.put(final_url, data = json.dumps(yang_config), auth=auth, headers = headers, verify = False)

    return resp
    if resp.status_code >= 200 and resp.status_code <= 299:
        print("Status OK: {}".format(resp.status_code))
    else:
        print("Error code: {}, reply {}".format(resp.status_code, resp.json()))


def delete_interface_restconf(name):
    base_url = get_restconf_base_url()
    final_url = base_url + "ietf-interfaces:interfaces/interface=" + name

    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json"
    }

    auth = (router["username"], router["password"])

    resp = requests.delete(final_url, auth=auth, headers = headers, verify = False)

    return resp


def get_routing_table():
    # Definimos la conexion
    con = manager.connect(host = router["address"], port = router["netconf-port"],
                    username = router["username"],
                    password = router["password"],
                    hostkey_verify = False)

    # Filtro para netconf
    netconf_filter = """
    <filter>
        <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing" />
    </filter>
    """

    netconf_reply = con.get_config(source="running", filter = netconf_filter)

    return xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()


if __name__ == "__main__":
    
    change_router_settings()
    
    opt = 1
    while True:
        print_options()

        while True:
            try:
                opt = int(input("Elige una opcion: "))
                assert opt >= 0 and opt < 6
                break
            except ValueError:
                print("Introduce un numero valido.")
            except AssertionError:
                print("Opcion no valida, vuelva a intentarlo.")
        print("")
        if opt == 1:
            interface_lists = get_interfaces_netconf()
            
            print(tabulate(interface_lists, ["Name", "IPv4 Address", "Status", "MAC-Address"]))
        
        elif opt == 2:
            name = input("Escribe el nombre de la interfaz que quieres crear: ")
            description = input("Introduce la descripcion de la interfaz: ")
            ip_addr = input("Introduce la direccion IPv4 de la interfaz: ")
            netmask = input("Introduce la mascara de red de la interfaz: ") 
            resp = create_loopback_interface_restconf(name, description, ip_addr, netmask)
            if resp.status_code >= 200 and resp.status_code <= 299:
                print("Status OK: {}".format(resp.status_code))
            else:
                print("Error code: {}, reply {}".format(resp.status_code, resp.json()))

        elif opt == 3:
            name = input("Escribe el nombre de la interfaz que quieres eliminar: ")
            resp = delete_interface_restconf(name)
            if resp.status_code >= 200 and resp.status_code <= 299:
                print("Status OK: {}".format(resp.status_code))
            elif resp.status_code == 404:
                print("The resource does not exist. Error code: {}".format(resp.status_code))
            elif resp.status_code > 404:
                print("There was an error. Error code: {}".format(resp.status_code))

        elif opt == 4:
            print(get_routing_table())

        elif opt == 0:
            print("Un placer, nos vemos!")
            break
        print("")
        input("Pulse enter para continuar")

