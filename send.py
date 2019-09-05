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

    npkg = len(txBuffer) // 128 + 1
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