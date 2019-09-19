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


serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem14101" # Mac    (variacao de)
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
    size_package = size_package.to_bytes(1, "little")

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
   
    with open("small.png", "rb") as image:
        f = image.read()
        txBuffer = bytearray(f)
    
    txBufferLen = len(txBuffer)

    log = open("log.txt", "w")
    
    for i in range(len(txBuffer)):
        if i > 3:
            if (txBuffer[i] == 122 and txBuffer[i-1] == 122 and txBuffer[i-2] == 122 and txBuffer[i-3] == 122):
                txBuffer.insert(i-1, 0)

    while inicia == False:

        type_1_message = createTypeOneMessage(txBuffer)
        send_message_1 = com.sendData(type_1_message)

        timertimer = time.time()

        log.write("MENSAGEM TIPO 1 - ENVIADA " + str(time.time()) + "- DESTINATÁRIO 2\n")

        time.sleep(2)
        rxBuffer, nRx = com.getData(10)
        
        if rxBuffer[0] == 2:
            log.write("MENSAGEM TIPO 2 - RECEBIDA " + str(time.time()) + "- DESTINATÁRIO 1\n")
            inicia = True
        
    number_of_packages = len(txBuffer) // 128 + 1

    dic = {}
    index = 1

    lista = bytearray()

    for i in txBuffer:
        lista.append(i)

        if len(lista) >= 128:
            dic[index] = lista.copy()
            index = index + 1
            lista.clear()
    
    dic[index] = lista.copy()
    lista.clear()
    
    cont = 1
    stop = False

    while cont < number_of_packages:
        reset = True

        type_3_message = createTypeThreeMessage(dic[cont], cont)
        com.sendData(type_3_message)
        log.write("MENSAGEM TIPO 3 - ENVIADA " + str(time.time()) + "- DESTINATÁRIO 2\n")

        timer1 = time.time()
        timer2 = time.time()

        time.sleep(1)
    
        while reset:

            reset = False
            com.fisica.flush()
            rxBuffer, nRx = com.getDataTimerClient(10, timer1, timer2)
            if rxBuffer[0] == 4:
                log.write("MENSAGEM TIPO 4 - RECEBIDA " + str(time.time()) + "- DESTINATÁRIO 1\n")
                cont = cont + 1
            else:
                if rxBuffer[0] == 222 or rxBuffer[0] == 333:
                    type_5_message = createTypeFiveMessage()
                    com.sendData(type_5_message)
                    log.write("MENSAGEM TIPO 5 - ENVIADA " + str(time.time()) + "- DESTINATÁRIO 2\n")
                    print(":-(")
                    stop = True
                    break
                else:
                    if rxBuffer[0] == 6:
                        index_esperado = int.from_bytes(rxBuffer[3:6], byteorder='little')
                        log.write("MENSAGEM TIPO 6 - RECEBIDA " + str(time.time()) + "- DESTINATÁRIO 1\n")
                        cont = index_esperado
                        log.write("MENSAGEM TIPO 3 - ENVIADA " + str(time.time()) + "- DESTINATÁRIO 2\n")
                        type_3_message = createTypeThreeMessage(dic[cont], cont)
                        com.sendData(type_3_message)
                        timer = time.time()
                        reset = True

                    elif rxBuffer[0] == 111:
                        com.sendData(type_3_message)
                        log.write("MENSAGEM TIPO 3 - ENVIADA " + str(time.time()) + "- DESTINATÁRIO 2\n")
                        timer1 = time.time()
                        reset = True

        if stop:
            break
    
    timetime = time.time() - timertimer
    log.write("Throughput: " + str(txBufferLen/timetime))

    
    log.close()
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()