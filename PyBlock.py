#Developer: Curly60e
#PyBLOCK its a clock of the Bitcoin blockchain.

import os
import os.path
import time as t
import pickle
import psutil
import qrcode
import random
import xmltodict
import sys
import subprocess
import requests
import json
import simplejson as json
import numpy as np
from cfonts import render, say
from clone import *
from donation import *
from feed import *
from art import *
from logos import *
from sysinf import *
from pblogo import *
from apisnd import *
from ppi import *
from termcolor import colored, cprint
from nodeconnection import *


version = "0.9.2"

def rpc(method, params=[]):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": "minebet",
        "method": method,
        "params": params
    })
    path = {"ip_port":"", "rpcuser":"", "rpcpass":"", "bitcoincli":""}
    if os.path.isfile('bclock.conf'): # Check if the file 'bclock.conf' is in the same folder
        pathv = pickle.load(open("bclock.conf", "rb")) # Load the file 'bclock.conf'
        path = pathv # Copy the variable pathv to 'path'
    return requests.post(path['ip_port'], auth=(path['rpcuser'], path['rpcpass']), data=payload).json()['result']

def getblockcount(): # get access to bitcoin-cli with the command getblockcount
    bitcoincli = " getblockcount"
    os.system(path['bitcoincli'] + bitcoincli)

def clear(): # clear the screen
    os.system('cls' if os.name=='nt' else 'clear')

def getgenesis(): # get and decode Genesis block
    bitcoincli = " getblock 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f 0 | xxd -r -p | hexyl -n 256"
    os.system(path['bitcoincli'] + bitcoincli)

def close():
    print("<<< Back to the Main Menu Press Control + C.\n\n")

def tmp():
    t.sleep(15)

def screensv():
    try:
        doit()
    except (KeyboardInterrupt, SystemExit):
        matrix.close()
        clear()
        ptr()
        menu()

def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.25)

def countdownblockConn():
    b = rpc('getblockcount')
    c = str(b)
    try:
        a = int(input("Insert your block target: "))
        clear()
        blogo()
        print("""
        --------------------- BLOCK {} COUNTDOWN ---------------------

         """.format(a))
        print("\nCountDown:", int(c))
        n = int(c)
        q = int(a) - int(c)
        print("Remaining: " + str(q) + " Blocks\n")
        while a > int(c):
            try:
                b = rpc('getblockcount')
                c = str(b)
                if a == c:
                    break
                elif n != int(c):
                    print("CountDown: ", c)
                    q = int(a) - int(c)
                    print("Remaining: " + str(q) + " Blocks\n")
                    n = int(c)
            except:
                break
        print("#RunTheNumbers " + str(a) + " PyBLOCK")
        input("\nContinue...")
    except:
        menuSelection()

#--------------------------------- End Hex Block Decoder Functions -------------------------------------

#--------------------------------- Menu section -----------------------------------

def menuUserConn(): #Menu before connection over ssh
    clear()
    blogo()
    a = "Local" if path['bitcoincli'] else "Remote"
    blk = rpc('getblockchaininfo')
    d = blk

    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    alias = r.json()

    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}


    \u001b[31;1mA.\033[0;37;40m PyBLOCK
    \u001b[38;5;202mB.\033[0;37;40m Bitcoin Core
    \u001b[33;1mL.\033[0;37;40m Lightning Network
    \u001b[38;5;40mP.\033[0;37;40m Platforms
    \u001b[38;5;15mX.\033[0;37;40m Donate
    \u001b[38;5;93mQ.\033[0;37;40m Exit
    \n\n""".format(a, alias['alias'], d['blocks'], version, checkupdate()))
    mainmenuREMOTEcontrol(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def bitcoincoremenuREMOTE():
    clear()
    blogo()
    a = "Local" if path['bitcoincli'] else "Remote"
    blk = rpc('getblockchaininfo')
    d = blk

    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    alias = r.json()

    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \u001b[38;5;202mA.\033[0;37;40m Bitcoin-cli Console
    \u001b[38;5;202mB.\033[0;37;40m Show Blockchain Information
    \u001b[38;5;202mC.\033[0;37;40m Run the Numbers
    \u001b[38;5;202mD.\033[0;37;40m Show QR from a Bitcoin Address
    \u001b[38;5;202mE.\033[0;37;40m Miscellaneous
    \u001b[33;1mR.\033[0;37;40m Return
    \n\n""".format(a, alias['alias'], d['blocks'], version, checkupdate()))
    bitcoincoremenuREMOTEcontrol(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def lightningnetworkREMOTE():
    clear()
    blogo()
    a = "Local" if path['bitcoincli'] else "Remote"
    blk = rpc('getblockchaininfo')
    d = blk

    cert_path = lndconnectload["tls"]
    macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
    r = requests.get(url, headers=headers, verify=cert_path)
    alias = r.json()

    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \u001b[33;1mA.\033[0;37;40m New Invoice
    \u001b[33;1mB.\033[0;37;40m Pay Invoice
    \u001b[33;1mC.\033[0;37;40m New Bitcoin Address
    \u001b[33;1mD.\033[0;37;40m List Invoices
    \u001b[33;1mE.\033[0;37;40m Channel Balance
    \u001b[33;1mF.\033[0;37;40m Show Channels
    \u001b[33;1mG.\033[0;37;40m Onchain Balance
    \u001b[33;1mH.\033[0;37;40m List Onchain Transactions
    \u001b[33;1mI.\033[0;37;40m Get Node Info
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(a, alias['alias'], d['blocks'], version, checkupdate()))
    lightningnetworkREMOTEcontrol(input("\033[1;32;40mSelect option: \033[0;37;40m"))


def runTheNumbersMenuConn():
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \033[1;32;40mA.\033[0;37;40m Countdown Block
    \033[1;32;40mB.\033[0;37;40m Countdown Halving
    \033[1;32;40mC.\033[0;37;40m Audit
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate()))
    runTheNumbersControlConn(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def weatherMenu():
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \033[1;32;40mA.\033[0;37;40m Version 1
    \033[1;32;40mB.\033[0;37;40m Version 2
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate()))
    menuWeather(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def dnt(): # Donation selection menu
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \u001b[38;5;15mA.\033[0;37;40m Developers Donation
    \u001b[38;5;15mB.\033[0;37;40m Testers Donation
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate()))
    menuC(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def dntDev(): # Dev Donation Menu
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \u001b[38;5;202mA.\033[0;37;40m Bitcoin Address
    \u001b[33;1mB.\033[0;37;40m Lightning Network
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate()))
    menuE(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def dntTst(): # Tester Donation Menu
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \u001b[38;5;202mA.\033[0;37;40m Bitcoin Address
    \u001b[33;1mB.\033[0;37;40m Lightning Network
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate()))
    menuF(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def APIMenuLOCAL():
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \033[1;32;40mA.\033[0;37;40m TippinMe   FREE
    \033[1;32;40mB.\033[0;37;40m Tallycoin  FREE
    \033[1;32;40mC.\033[0;37;40m Mempool    FREE
    \033[1;32;40mD.\033[0;37;40m CoinGecko  FREE
    \033[1;32;40mE.\033[0;37;40m Rate.sx    FREE
    \033[1;32;40mF.\033[0;37;40m BWT        FREE
    \033[1;32;40mG.\033[0;37;40m LNBits     \033[3;35;40m{lnbitspaid}\033[0;37;40m
    \033[1;32;40mH.\033[0;37;40m LNPay      \033[3;35;40m{lnpaypaid}\033[0;37;40m
    \033[1;32;40mI.\033[0;37;40m OpenNode   \033[3;35;40m{opennodepaid}\033[0;37;40m
    \033[1;32;40mJ.\033[0;37;40m SatNode    FREE
    \033[1;32;40mK.\033[0;37;40m Weather    FREE
    \033[1;32;40mL.\033[0;37;40m Arcade     FREE
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate(),lnbitspaid = "PAID" if os.path.isfile("lnbitSN.conf") else "PREMIUM", lnpaypaid = "PAID" if os.path.isfile("lnpaySN.conf") else "PREMIUM", opennodepaid = "PAID" if os.path.isfile("opennodeSN.conf") else "PREMIUM"))
    platfformsLOCALcontrol(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def satnodeMenu(): # Satnode Menu
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \033[1;32;40mA.\033[0;37;40m Start SatNode
    \033[1;32;40mB.\033[0;37;40m Feed
    \033[1;32;40mC.\033[0;37;40m Setup
    \033[1;34;40mS.\033[0;37;40m Send a Message to Space
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate()))
    menuD(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def rateSX():
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \033[1;32;40mA.\033[0;37;40m Rate
    \033[1;32;40mB.\033[0;37;40m Chart
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate()))
    rateSXMenu(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def mempoolmenu():
    clear()
    blogo()
    if path['bitcoincli']:
        n = "Local" if path['bitcoincli'] else "Remote"
        bitcoincli = " getblockchaininfo"
        a = os.popen(path['bitcoincli'] + bitcoincli).read()
        b = json.loads(a)
        d = b

        lncli = " getinfo"
        lsd = os.popen(lndconnectload['ln'] + lncli).read()
        lsd0 = str(lsd)
        alias = json.loads(lsd0)
    else:
        a = "Local" if path['bitcoincli'] else "Remote"
        blk = rpc('getblockchaininfo')
        d = blk

        cert_path = lndconnectload["tls"]
        macaroon = codecs.encode(open(lndconnectload["macaroon"], 'rb').read(), 'hex')
        headers = {'Grpc-Metadata-macaroon': macaroon}
        url = 'https://{}/v1/getinfo'.format(lndconnectload["ip_port"])
        r = requests.get(url, headers=headers, verify=cert_path)
        alias = r.json()
    print("""\t\t
    \033[1;37;40m{}\033[0;37;40m: \033[1;31;40mPyBLOCK\033[0;37;40m
    \033[1;37;40mNode\033[0;37;40m: \033[1;33;40m{}\033[0;37;40m
    \033[1;37;40mBlock\033[0;37;40m: \033[1;32;40m{}\033[0;37;40m
    \033[1;37;40mVersion\033[0;37;40m: {}

    \033[1;32;40mA.\033[0;37;40m Blocks
    \033[1;32;40mB.\033[0;37;40m Recommended Fee
    \u001b[31;1mR.\033[0;37;40m Return
    \n\n""".format(n if path['bitcoincli'] else a , alias['alias'], d['blocks'], version, checkupdate()))
    mempoolmenuS(input("\033[1;32;40mSelect option: \033[0;37;40m"))

def menuSelection():
    path = {"ip_port":"", "rpcuser":"", "rpcpass":"", "bitcoincli":""}
    pathv = pickle.load(open("bclock.conf", "rb")) # Load the file 'bclock.conf'
    path = pathv # Copy the variable pathv to 'path'
    if path['bitcoincli']:
        menu()
    else:
        menuUserConn()

def menuSelectionLN():
    lndconnectload = {"ip_port":"", "tls":"", "macaroon":"", "lncli":""}
    lndconnectData = pickle.load(open("blndconnect.conf", "rb")) # Load the file 'bclock.conf'
    lndconnectload = lndconnectData # Copy the variable pathv to 'path'
    if lndconnectload['ln']:
        menuLNDLOCAL()
    else:
        menuLND()

def aaccPPiLNBits():
    try:
        bitLN = {"NN":"","pd":""}
        if os.path.isfile('lnbitSN.conf'):
            bitData= pickle.load(open("lnbitSN.conf", "rb"))
            bitLN = bitData
            APILnbit()
        else:
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            bitLN['NN'] = randrange(10000000)
            curl = 'curl -X POST https://lnbits.com/api/v1/payments -d ' + "'{" + """"out": false, "amount": 100000, "memo": "LNBits on PyBLOCK {}" """.format(bitLN['NN']) + "}'" + """ -H "X-Api-Key: 1d646820055e4e2da218e801eaacfc94 " -H "Content-type: application/json" """
            sh = os.popen(curl).read()
            clear()
            prt()
            n = str(sh)
            d = json.loads(n)
            q = d['payment_request']
            c = q.lower()
            while True:
                print("\033[1;30;47m")
                qr.add_data(c)
                qr.print_ascii()
                print("\033[0;37;40m")
                qr.clear()
                print("Lightning Invoice: " + c)
                dn = str(d['checking_id'])
                t.sleep(10)
                checkcurl = 'curl -X GET https://lnbits.com/api/v1/payments/' + dn + """ -H "X-Api-Key: 1d646820055e4e2da218e801eaacfc94" -H "Content-type: application/json" """
                rsh = os.popen(checkcurl).read()
                clear()
                blogo()
                nn = str(rsh)
                dd = json.loads(nn)
                db = dd['paid']
                if db is True:
                    clear()
                    blogo()
                    tick()
                    bitLN['pd'] = "PAID"
                    pickle.dump(bitLN, open("lnbitSN.conf", "wb"))
                    createFileConnLNBits()
                    break
                else:
                    continue

    except:
        clear()
        blogo()
        print("\n\tSERIAL NUMBER NOT FOUND\n")
        input("Continue...")

def aaccPPiLNPay():
    try:
        bitLN = {"NN":"","pd":""}
        if os.path.isfile('lnpaySN.conf'): # Check if the file 'bclock.conf' is in the same folder
            bitData= pickle.load(open("lnpaySN.conf", "rb")) # Load the file 'bclock.conf'
            bitLN = bitData # Copy the variable pathv to 'path'
            APILnPay()
        else:
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            bitLN['NN'] = randrange(10000000)
            curl = 'curl -X POST https://lnbits.com/api/v1/payments -d ' + "'{" + """"out": false, "amount": 100000, "memo": "LNPay on PyBLOCK {}" """.format(bitLN['NN']) + "}'" + """ -H "X-Api-Key: 1d646820055e4e2da218e801eaacfc94 " -H "Content-type: application/json" """
            sh = os.popen(curl).read()
            clear()
            prt()
            n = str(sh)
            d = json.loads(n)
            q = d['payment_request']
            c = q.lower()
            while True:
                print("\033[1;30;47m")
                qr.add_data(c)
                qr.print_ascii()
                print("\033[0;37;40m")
                qr.clear()
                print("Lightning Invoice: " + c)
                dn = str(d['checking_id'])
                t.sleep(10)
                checkcurl = 'curl -X GET https://lnbits.com/api/v1/payments/' + dn + """ -H "X-Api-Key: 1d646820055e4e2da218e801eaacfc94" -H "Content-type: application/json" """
                rsh = os.popen(checkcurl).read()
                clear()
                blogo()
                nn = str(rsh)
                dd = json.loads(nn)
                db = dd['paid']
                if db is True:
                    clear()
                    blogo()
                    tick()
                    bitLN['pd'] = "PAID"
                    pickle.dump(bitLN, open("lnpaySN.conf", "wb"))
                    createFileConnLNPay()
                    break
                else:
                    continue

    except:
        clear()
        blogo()
        print("\n\tSERIAL NUMBER NOT FOUND\n")
        input("Continue...")

def aaccPPiOpenNode():
    try:
        bitLN = {"NN":"","pd":""}
        if os.path.isfile('opennodeSN.conf'): # Check if the file 'bclock.conf' is in the same folder
            bitData= pickle.load(open("opennodeSN.conf", "rb")) # Load the file 'bclock.conf'
            bitLN = bitData # Copy the variable pathv to 'path'
            APIOpenNode()
        else:
            qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            bitLN['NN'] = randrange(10000000)
            curl = 'curl -X POST https://lnbits.com/api/v1/payments -d ' + "'{" + """"out": false, "amount": 100000, "memo": "OpenNode on PyBLOCK {}" """.format(bitLN['NN']) + "}'" + """ -H "X-Api-Key: 1d646820055e4e2da218e801eaacfc94 " -H "Content-type: application/json" """
            sh = os.popen(curl).read()
            clear()
            prt()
            n = str(sh)
            d = json.loads(n)
            q = d['payment_request']
            c = q.lower()
            while True:
                print("\033[1;30;47m")
                qr.add_data(c)
                qr.print_ascii()
                print("\033[0;37;40m")
                qr.clear()
                print("Lightning Invoice: " + c)
                dn = str(d['checking_id'])
                t.sleep(10)
                checkcurl = 'curl -X GET https://lnbits.com/api/v1/payments/' + dn + """ -H "X-Api-Key: 1d646820055e4e2da218e801eaacfc94" -H "Content-type: application/json" """
                rsh = os.popen(checkcurl).read()
                clear()
                blogo()
                nn = str(rsh)
                dd = json.loads(nn)
                db = dd['paid']
                if db is True:
                    clear()
                    blogo()
                    tick()
                    bitLN['pd'] = "PAID"
                    pickle.dump(bitLN, open("opennodeSN.conf", "wb"))
                    createFileConnOpenNode()
                    break
                else:
                    continue

    except:
        clear()
        blogo()
        print("\n\tSERIAL NUMBER NOT FOUND\n")
        input("Continue...")

def aaccPPiTippinMe():
    if os.path.isfile('tippinme.conf'): # Check if the file 'bclock.conf' is in the same folder
        APITippinMe()
    else:
        createFileTippinMe()

def aaccPPiTallyCo():
    if os.path.isfile('tallyco.conf'): # Check if the file 'bclock.conf' is in the same folder
        APITallyCo()
    else:
        createFileConnTallyCo()

def checkupdate():
    r = requests.get('https://raw.githubusercontent.com/curly60e/PyBLOCK-Termux-Mobile/master/ver.txt')
    r.headers['Content-Type']
    n = r.text
    di = json.loads(n)
    if di['version'] == version:
        q = print(" ")
    else:
        print("\n---------------------------------------------------")
        q = print("\n    \033[1;31;40mNew version available\033[0;37;40m > Press U to Upgrade\n")
        print("---------------------------------------------------")

def upgrade():
    gitfetch = "git fetch"
    gitchekcout = "git checkout origin/master -- PyBlock.py ppi.py pblogo.py sysinf.py apisnd.py clone.py donation.py feed.py logos.py nodeconnection.py requirements.txt"
    clear()
    blogo()
    b = os.popen(gitfetch).read()
    a = os.popen(gitchekcout).read()
    print(b)
    print(a)
    print("\n---------------------------------------------------")
    print("\n\t\033[1;31;40mYou'll need to restart PyBLOCK\033[0;37;40m\n")
    print("---------------------------------------------------\n")
    input("Continue...")

#--------------------------------- End Menu section -----------------------------------
#--------------------------------- Main Menu execution --------------------------------

def runTheNumbersControlConn(menuNumbersconn):
    if menuNumbersconn in ["A", "a"]:
        clear()
        blogo()
        countdownblockConn()
    elif menuNumbersconn in ["B", "b"]:
        clear()
        blogo()
        remoteHalving()
    elif menuNumbersconn in ["C", "c"]:
        clear()
        blogo()
        calc = """
                    ----------------------------
                             PROCESSING
                            THE  NUMBERS
                    ----------------------------
         """
        comeback = """
                    ----------------------------
                       MAKE YOURSELF A COFFEE
                         AND COME BACK IN A
                               MOMENT
                    ----------------------------
        """
        cprint(comeback, 'yellow')
        cprint(calc, 'red', attrs=['blink'])
        runthenumbersConn()

def menuPI(menuWN):
    if menuWN in ["A", "a"]:
        aaccPPiTippinMe()
    elif menuWN in ["B", "b"]:
        aaccPPiTallyCo()
    elif menuWN in ["C", "c"]:
        aaccPPiLNBits()
    elif menuWN in ["D", "d"]:
        aaccPPiLNPay()
    elif menuWN in ["E", "e"]:
        aaccPPiOpenNode()

def menuTallyCo(menuTLC):
    if menuTLC in ["A", "a"]:
        tallycoGetPayment()
    elif menuTLC in ["B", "b"]:
        tallycoDonateid()
    elif menuTLC in ["R", "r"]:
        APIMenu()

def menuTippinMe(menuTM):
    if menuTM in ["A", "a"]:
        tippinmeGetInvoice()
    elif menuTM in ["R", "r"]:
        APIMenu()

def menuOpenNode(menuOP):
    if menuOP in ["A", "a"]:
        clear()
        prt()
        OpenNodecreatecharge()
    elif menuOP in ["B", "b"]:
        clear()
        prt()
        OpenNodeiniciatewithdrawal()
    elif menuOP in ["C", "c"]:
        clear()
        prt()
        OpenNodelistfunds()
    elif menuOP in ["D", "d"]:
        clear()
        prt()
        OpenNodeListPayments()
    elif menuOP in ["S", "s"]:
        clear()
        prt()
        OpenNodeCheckStatus()
    elif menuOP in ["R", "r"]:
        APIMenu()

def menuLNPAY(menuNW):
    if menuNW in ["A", "a"]:
        clear()
        prt()
        lnpayCreateInvoice()
    elif menuNW in ["B", "b"]:
        clear()
        prt()
        lnpayPayInvoice()
    elif menuNW in ["C", "c"]:
        clear()
        prt()
        lnpayGetBalance()
    elif menuNW in ["D", "d"]:
        clear()
        prt()
        lnpayGetTransactions()
    elif menuNW in ["E", "e"]:
        clear()
        prt()
        lnpayTransBWallets()
    elif menuNW in ["R", "r"]:
        APIMenu()

def menuLNBPI(menuLNQ):
    if menuLNQ in ["A", "a"]:
        clear()
        prt()
        lnbitCreateNewInvoice()
    elif menuLNQ in ["B", "b"]:
        clear()
        prt()
        lnbitPayInvoice()
    elif menuLNQ in ["C", "c"]:
        clear()
        prt()
        lnbitCreatePayWall()
    elif menuLNQ in ["D", "d"]:
        clear()
        prt()
        lnbitDeletePayWall()
    elif menuLNQ in ["E", "e"]:
        clear()
        prt()
        lnbitListPawWall()
    elif menuLNQ in ["R", "r"]:
        APIMenu()

def mainmenuREMOTEcontrol(menuS): #Execution of the Main Menu options
    if menuS in ["A", "a"]:
        while True:
            try:
                clear()
                close()
                remotegetblock()
                tmp()
            except:
                break
    elif menuS in ["B", "b"]:
        bitcoincoremenuREMOTE()
    elif menuS in ["L", "l"]:
        lightningnetworkREMOTE()
    elif menuS in ["P", "p"]:
        APIMenuLOCAL()
    elif menuS in ["X", "x"]:
        dnt()
    elif menuS in ["U", "u"]:
        upgrade()
    elif menuS in ["S", "s"]:
        settings4Remote()
    elif menuS in ["Q", "q"]:
        os._exit(0)
        apisnd.close()
        donation.close()
        clone.close()
        logos.close()
        feed.close()
        sysinf.close()
        nodeconnection.close()
        exit()
    elif menuS in ["T", "t"]: #Test feature fast access
        clear()
        delay_print("\033[1;32;40mWake up, Neo...")
        t.sleep(2)
        clear()
        delay_print("The Matrix has you...")
        t.sleep(2)
        clear()
        delay_print("Follow the white rabbit.")
        t.sleep(3)
        clear()
        print("Knock, knock, Neo.\033[0;37;40m\n")
        t.sleep(2)
        clear()
        t.sleep(3)
        screensv()
    elif menuS in ["nym", "Nym", "NYM", "nYm", "nyM", "NYm", "NyM", "nYM"]:
        clear()
        blogo()
        robotNym()
    elif menuS in ["wt", "WT", "Wt", "wT"]:
        clear()
        blogo()
        callGitWardenTerminal()

def bitcoincoremenuREMOTEcontrol(bcore):
    if bcore in ["A", "a"]:
        while True:
            try:
                clear()
                blogo()
                sysinfo()
                close()
                remoteconsole()
                t.sleep(5)
            except:
                break
    elif bcore in ["B", "b"]:
        remotegetblockcount()
    elif bcore in ["C", "c"]:
        runTheNumbersMenuConn()
    elif bcore in ["D", "d"]:
        try:
            clear()
            blogo()
            sysinfo()
            close()
            decodeQR()
            input("Continue...")
        except:
            pass
    elif bcore in ["E", "e"]:
        miscellaneousLOCAL()

def lightningnetworkREMOTEcontrol(lncore):
    if lncore in ["A", "a"]:
        clear()
        blogo()
        getnewinvoice()
    elif lncore in ["B", "b"]:
        clear()
        blogo()
        payinvoice()
    elif lncore in ["C", "c"]:
        clear()
        blogo()
        getnewaddress()
    elif lncore in ["D", "d"]:
        clear()
        blogo()
        listinvoice()
    elif lncore in ["E", "e"]:
        clear()
        blogo()
        channelbalance()
    elif lncore in ["F", "f"]:
        clear()
        blogo()
        channels()
    elif lncore in ["G", "g"]:
        clear()
        blogo()
        balanceOC()
    elif lncore in ["H", "h"]:
        clear()
        blogo()
        listonchaintxs()
    elif lncore in ["I", "i"]:
        clear()
        blogo()
        getinfo()
    elif lncore in ["R", "r"]:
        menuSelection()

def menuC(menuO): # Donation access Menu
    if menuO in ["A", "a"]:
        dntDev()
    elif menuO in ["B", "b"]:
        dntTst()
    elif menuO in ["R", "r"]:
        menuSelection()

def menuD(menuN): # Satnode access Menu
    if menuN in ["A", "a"]:
        satnode()
    elif menuN in ["B", "b"]:
        readFile()
    elif menuN in ["S", "s"]:
        try:
            clear()
            blogo()
            close()
            message = input("\n\033[0;37;40mYour message it's a \033[1;34;40mF\033[0;37;40mile or a plain \033[1;32;40mT\033[0;37;40mext? \033[1;34;40mF\033[0;37;40m/\033[1;32;40mT\033[0;37;40m: ")
            if message in ["F", "f"]:
                try:
                    clear()
                    blogo()
                    close()
                    apisenderFile()
                    t.sleep(30)
                    menuSelection()
                except:
                    menuSelection()
            elif message in ["T", "t"]:
                try:
                    clear()
                    blogo()
                    close()
                    apisender()
                    t.sleep(30)
                    menuSelection()
                except:
                    menuSelection()
        except:
            menuSelection()
    elif menuN in ["C", "c"]:
        try:
            print("\n\t This only will work on Linux or Unix systems.\n")
            a = input("Do we continue? Y/n: ")
            if a in ["Y", "y"]:
                gitclone()
            else:
                menuSelection()
        except:
            pass
    elif menuN in ["R", "r"]:
        menuSelection()

def menuE(menuQ): # Dev Donation access Menu
    if menuQ in ["A", "a"]:
        try:
            clear()
            blogo()
            close()
            donationAddr()
            t.sleep(50)
            menuSelection()
        except:
            menuSelection()
    elif menuQ in ["B", "b"]:
        try:
            clear()
            blogo()
            close()
            donationLN()
            t.sleep(50)
            menuSelection()
        except:
            menuSelection()
    elif menuQ in ["R", "r"]:
        menuSelection()

def menuF(menuV): # Tester Donation access Menu
    if menuV in ["A", "a"]:
        try:
            clear()
            blogo()
            close()
            donationAddrTst()
            t.sleep(50)
            menuSelection()
        except:
            menuSelection()
    elif menuV in ["B", "b"]:
        try:
            clear()
            blogo()
            close()
            donationLNTst()
            t.sleep(50)
            menuSelection()
        except:
            menuSelection()
    elif menuV in ["R", "r"]:
        menuSelection()

def platfformsLOCALcontrol(platf):
    if platf in ["A", "a"]:
        aaccPPiTippinMe()
    elif platf in ["B", "b"]:
        aaccPPiTallyCo()
    elif platf in ["C", "c"]:
        mempoolmenu()
    elif platf in ["D", "d"]:
        clear()
        blogo()
        CoingeckoPP()
    elif platf in ["E", "e"]:
        rateSX()
    elif platf in ["F", "f"]:
        bwtConn()
    elif platf in ["G", "g"]:
        aaccPPiLNBits()
    elif platf in ["H", "h"]:
        aaccPPiLNPay()
    elif platf in ["I", "i"]:
        aaccPPiOpenNode()
    elif platf in ["J", "j"]:
        satnodeMenu()
    elif platf in ["K", "k"]:
        weatherMenu()
    elif platf in ["L", "l"]:
        gameroom()
    elif platf in ["R", "r"]:
        menuSelection()

def rateSXMenu(menuSX):
    if menuSX in ["A", "a"]:
        clear()
        blogo()
        rateSXList()
    elif menuSX in ["B", "b"]:
        clear()
        blogo()
        rateSXGraph()
    elif menuSX in ["R", "r"]:
        menuSelection()

#--------------------------------- End Main Menu execution --------------------------------

settings = {"gradient":"", "design":"block", "colorA":"green", "colorB":"yellow"}
settingsClock = {"gradient":"", "colorA":"green", "colorB":"yellow"}
while True: # Loop
    try:
        clear()
        path = {"ip_port":"", "rpcuser":"", "rpcpass":"", "bitcoincli":""}

        if os.path.isfile('bclock.conf') or os.path.isfile('blnclock.conf'): # Check if the file 'bclock.conf' is in the same folder
            pathv = pickle.load(open("bclock.conf", "rb")) # Load the file 'bclock.conf'
            path = pathv # Copy the variable pathv to 'path'
        else:
            blogo()
            print("Welcome to \033[1;31;40mPyBLOCK\033[0;37;40m\n\n")
            print("\n\tIf you are going to use your local node leave IP:PORT/USER/PASSWORD in blank.\n")
            path['ip_port'] = "http://{}".format(input("Insert IP:PORT to access your remote Bitcoin-Cli node: "))
            path['rpcuser'] = input("RPC User: ")
            path['rpcpass'] = input("RPC Password: ")
            print("\n\tLocal Bitcoin Core Node connection.\n")
            path['bitcoincli']= input("Insert the Path to Bitcoin-Cli: ")
            pickle.dump(path, open("bclock.conf", "wb"))

        menuSelection()


    except:
        print("\n")
        sys.exit(101)
