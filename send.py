#!/usr/bin/env python3
# -- coding: utf-8 --
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################

print("comecou")

from enlace import *
import time

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports

# im = input("Digite o nome da imagem a ser transmitida: ")


# serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/tty.usbmodem14101" # Mac    (variacao de)
# serialName = "COM11"                  # Windows(variacao de)
print("abriu com")

def createTypeOneMessage(payloadLen):

    payload = len(payloadLen) // 128 + 1
    payload = payload.to_bytes(10, "little")

    eop =  "zzzz"
    eop = eop.encode()

    payload_eop = payload + eop

    len_payload = len(payload_eop)
    len_payload = len_payload.to_bytes(1, "little")

    type_message_1 = 1
    type_message_1 = type_message_1.to_bytes(1, "little")

    id_server = 2
    id_server = id_server.to_bytes(1,"little")

    index = 0
    index = index.to_bytes(2,"little")

    return (type_message_1 + id_server + len_payload + index + payload_eop)

def createTypeThreeMessage(payload, index):
    
    type_message_3 = 3
    type_message_3 = type_message_3.to_bytes(1, "little")

    id_server = 2
    id_server = id_server.to_bytes(1,"little")

    eop =  "zzzz"
    eop = eop.encode()

    size_package = 132
    size_package = size_package.to_bytes(2, "little")

    index = index.to_bytes(2, "little")

    return (type_message_3 + id_server + size_package + index + payload + eop)

def createTypeFiveMessage():

    type_message_5 = 5
    type_message_5 = type_message_5.to_bytes(1, "little")

    id_server = 2
    id_server = id_server.to_bytes(1,"little")

    size_payload = 0
    size_payload = size_payload.to_bytes(1,"little")

    eop =  "zzzz"
    eop = eop.encode()

    index = 0
    index = index.to_bytes(2,"little")

    return (type_message_5 + id_server + size_payload + index + eop)




def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao

    inicia = False

    com.enable()

    time.sleep(2)
    
    com.fisica.flush()
   
    with open("logo.png", "rb") as image:
        f = image.read()
        txBuffer = bytearray(f)
    
    for i in range(len(txBuffer)):
        if i > 3:
            if (txBuffer[i] == 122 and txBuffer[i-1] == 122 and txBuffer[i-2] == 122 and txBuffer[i-3] == 122):
                txBuffer.insert(i-1, 0)

    while inicia == False:

        type_1_message = createTypeOneMessage(txBuffer)
        com.sendData(type_1_message)
        time.sleep(5)
        rxBuffer, nRx = com.getData(5)
        tipo = int.from_bytes(rxBuffer[0], byteorder='little')
        if tipo == 2:
            inicia = True

    number_of_packages = len(txBuffer) // 128 + 1

    # eop = "zzzz"
    # e = eop.encode()

    # t = 132
    # tpkg = t.to_bytes(2, "little")

    # com.fisica.flush()

    dic = {}
    index = 1

    lista = bytearray()

    com.fisica.flush()

    for i in txBuffer:
        lista.append(i)

        if len(lista) >= 128:
            dic[index] = lista
            index = index + 1
            lista.clear()

    cont = 1

    while cont <= number_of_packages:
        reset = True
        com.fisica.flush()
        type_3_message = createTypeThreeMessage(dic[cont], cont)
        com.sendData(type_3_message)
        timer = time.time()
    
        time.sleep(1)

        while reset:
            reset= False
            rxBuffer, nRx = com.getData(5)
            tipo = int.from_bytes(rxBuffer[0], byteorder='little')
            if tipo == 4:
                cont = cont + 1
            else:
                timer1 = time.time() - timer
                if timer1 > 5:
                    com.sendData(type_3_message)
                else:
                    timer2 = time.time() - timer
                    if timer2 > 20:
                        type_5_message = createTypeFiveMessage()
                        com.sendData(type_5_message)
                        print(":-(")
                        break
                    else:
                        if tipo == 6:
                            index_esperado = int.from_bytes(rxBuffer[3:], byteorder='little')
                            cont = index_esperado
                            com.sendData(dic[cont])
                            timer = time.time()]
                            reset = True


    com.fisica.flush()
    headpkg = 1 + headpkg
    hpbyte = headpkg.to_bytes(2, "little")
    tpkg = len(listay).to_bytes(2, "little")
    stuff = head + hpbyte + tpkg + listay + e
    com.sendData(stuff)
    listay.clear()

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()