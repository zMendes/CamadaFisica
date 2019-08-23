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
serialName = "/dev/tty.usbmodem14201" # Mac    (variacao de)
# serialName = "COM11"                  # Windows(variacao de)
print("abriu com")


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao

    com.enable()

    time.sleep(2)
    
    com.fisica.flush()

    a = time.time()

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    # Carrega dados
    print ("Gerando dados para transmissao :")
    
    with open("logo.png", "rb") as image:
        f = image.read()
        txBuffer = bytearray(f)

    # txBuffer.insert(10, 122)
    # txBuffer.insert(10, 122)
    # txBuffer.insert(10, 122)
    # txBuffer.insert(10, 122)

    # txBuffer.insert(30, 122)
    # txBuffer.insert(30, 122)
    # txBuffer.insert(30, 122)
    # txBuffer.insert(30, 122)
    
    # txBuffer.insert(20, 97)
    # txBuffer.insert(20, 97)
    # txBuffer.insert(20, 97)
    # txBuffer.insert(20, 97)

    # txBuffer = "Eae amigão beleza? Aqui vai o aaaa e aqui vai o zzzz "
    # txBuffer = bytearray(txBuffer, "utf-8")

    npkg = len(txBuffer) // 128 + 1
    
    for i in range(len(txBuffer)):
        if i > 3:
            if (txBuffer[i] == 122 and txBuffer[i-1] == 122 and txBuffer[i-2] == 122 and txBuffer[i-3] == 122):
                print("PASSOU EM COLOCAR OS ZEROS")
                print(i)
                txBuffer.insert(i-1, 0)

    for i in range(len(txBuffer)):
        if i > 3:
            if (txBuffer[i] == 97 and txBuffer[i-1] == 97 and txBuffer[i-2] == 97 and txBuffer[i-3] == 97):
                print("PASSOU EM COLOCAR OS ZEROS NO AAAA")
                print(i)
                txBuffer.insert(i-1, 0)

    txLen = len(txBuffer) + 4
    
    head = npkg.to_bytes(2, "little")

    eop = "zzzz"

    e = eop.encode()

    t = 132

    tpkg = t.to_bytes(2, "little")

    com.fisica.flush()

    listay = bytearray()
    headpkg = 0

    com.fisica.flush()

    for i in txBuffer:
        listay.append(i)

        if len(listay) >= 128:
            com.fisica.flush()
            headpkg = 1 + headpkg
            hpbyte = headpkg.to_bytes(2, "little")
            stuff = head + hpbyte + tpkg +  listay + e 
            print("Number of package", headpkg)
            print("Stuff", stuff)
            print("Len package", len(stuff))
            com.sendData(stuff)
            time.sleep(0.05)
            listay.clear()

    com.fisica.flush()
    headpkg = 1 + headpkg
    hpbyte = headpkg.to_bytes(2, "little")
    tpkg = len(listay).to_bytes(2, "little")
    stuff = head + hpbyte + tpkg + listay + e
    print("Number of package", headpkg)
    print("Stuff", stuff)
    print("Len package", len(listay))
    com.sendData(stuff)
    listay.clear()

    # # Transmite dado
    # print("tentado transmitir .... {} bytes".format(len(stuff)))
    # com.sendData(stuff)
    
    # # Atualiza dados da transmissão
    # txSize = com.tx.getStatus()
    # print ("Transmitido       {} bytes ".format(txSize))

    # # Faz a recepção dos dados
    # print ("Recebendo dados .... ")

    # #repare que o tamanho da mensagem a ser lida é conhecida!     
    # rxBuffer, nRx = com.getData(2)

    # # log
    # print ("Lido              {} bytes ".format(nRx))
    
    # print("BUFFER")
    # print (rxBuffer)

    # com.fisica.flush()

    # # Transmite dado
    # print("tentado transmitir .... {} bytes".format(txLen))
    # com.sendData(txBuffer)
    
    # # Atualiza dados da transmissão
    # txSize = com.tx.getStatus()
    # print ("Transmitido       {} bytes ".format(txSize))

    # #repare que o tamanho da mensagem a ser lida é conhecida!     
    # # rxBuffer, nRx = com.getData(2)

    b = time.time() - a

    # print(b)
    # print(txLen)

    print("Troughout: ", txLen/b)

    # print("Overhead: ", overhead)

    # log
    # print ("Lido              {} bytes ".format(nRx))
    
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()