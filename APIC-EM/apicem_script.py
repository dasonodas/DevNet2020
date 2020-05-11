#!/usr/bin/env python3
__author__  = "Diego Pellitero Fernández"

import json
import requests
from pprint import pprint
from tabulate import *

requests.packages.urllib3.disable_warnings()

base_url = "https://devnetsbx-netacad-apicem-3.cisco.com/api/"
api_version = "1"
api_url = base_url + "v" + api_version + "/"


def get_ticket():
    ticket_endpoint = "ticket"
    user = "devnetuser"
    passwd = "Xj3BDqbU"

    headers = {
        "content-type": "application/json"
    }
    body = {
        "username":  user,
        "password": passwd
    }

    resp = requests.post(api_url + ticket_endpoint, json.dumps(body), headers = headers, verify = False)
    if resp.status_code != 200:
        return -1
    else:
        return resp.json()["response"]["serviceTicket"]
        

def get_host_number():
    host_endpoint = "host/count"

    try:
        ticket = get_ticket()
        if ticket == -1:
            raise Exception("There was an error getting the ServiceTicket")
        headers = {
            "content-type": "application/json",
            "X-Auth-Token": ticket
        }
        resp = requests.get(api_url + host_endpoint, headers = headers, verify = False)
        if resp.status_code != 200:
            raise Exception("The status code is not 200. Response text: " + resp.text)
        resp_json = resp.json()
        return resp_json["response"]
    except Exception as e:
        print(e.args[0])


def get_host_inventory():
    host_endpoint = "host"

    try:
        ticket = get_ticket()
        if ticket == -1:
            raise Exception("There was an error getting the ServiceTicket")
        headers = {
            "content-type": "application/json",
            "X-Auth-Token": ticket
        }
        resp = requests.get(api_url + host_endpoint, headers = headers, verify = False)
        if resp.status_code != 200:
            raise Exception("The status code is not 200. Response text: " + resp.text)
        resp_json = resp.json()
        i = 0
        host_list = []
        for host in resp_json["response"]:
            i += 1
            host_list.append([i, host["hostType"], host["hostIp"]])
        return host_list
    except Exception as e:
        print(e.args[0])



def get_device_inventory():
    device_endpoint = "network-device"

    try:
        ticket = get_ticket()
        if ticket == -1:
            raise Exception("There was an error getting the ServiceTicket")
        headers = {
            "content-type": "application/json",
            "X-Auth-Token": ticket
        }
        resp = requests.get(api_url + device_endpoint, headers = headers, verify = False)
        if resp.status_code != 200:
            raise Exception("The status code is not 200. Response text: " + resp.text)
        resp_json = resp.json()
        i = 0
        device_list = []
        for device in resp_json["response"]:
            i += 1
            device_list.append([i, device["family"], device["managementIpAddress"]])
        return device_list
    except Exception as e:
        print(e.args[0])


def get_hosts_and_devices():
    devices_list = get_host_inventory()
    devices_list += get_device_inventory()
    i = 0
    for item in devices_list:
        i += 1
        item[0] = i
    return devices_list


#not available at the moment of coding
def path_trace_analysis(path_data):
    path_trace_endpoint = "flow-analysis"
    try:
        ticket = get_ticket()
        if ticket == -1:
            raise Exception("There was an error getting the ServiceTicket")
        headers = {
            "content-type": "application/json",
            "X-Auth-Token": ticket
        }
        print(api_url + path_trace_endpoint)
        resp = requests.post(api_url + path_trace_endpoint, path_data, headers = headers, verify = False)
        if resp.status_code != 200:
            raise Exception("The status code is not 200. Response text: " + resp.text)
        resp_json = resp.json()
        return resp_json["response"]["flowAnalysisId"]
        
    except Exception as e:
        print(e.args[0])


if __name__ == "__main__":
    while True:
        print("""
----------- Bienvenido a la consola de APIC-EM ------------

Elige una de las siguientes opciones:
    1) Obtener ticket de servicio
    2) Obtener el numero de host conectados a la red
    3) Obtener detalle de hosts conectados a la red
    4) Obtener listado de dispositivos de red
    5) Obtener todos dispoitivos conectados (hosts + disp. de red)
    0) Salir
        """)
        while True:
            try:
                opt = int(input("Introduce una opcion: "))
                if opt < 0 or opt > 5:
                    raise Exception
                break  
            except Exception:
                print("Introduce un numero entre 1 y 5")
        if opt == 0:
            print("Espero volver a verte!!!")
            break
        elif opt == 1:
            print("\nSu ticket de servicio es: " + get_ticket())
        elif opt == 2:
            print("\nEl numero de host en la red es " + str(get_host_number()))
        elif opt == 3:
            print(tabulate(get_host_inventory(), ["Number", "Type", "IP Address"]))
        elif opt == 4:
            print(tabulate(get_device_inventory(), ["Number", "Type", "IP Address"]))
        elif opt == 5:
            print(tabulate(get_hosts_and_devices(), ["Number", "Type", "IP Address"]))
        input("\nPulsa enter para continuar")

