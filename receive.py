
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################


print("comecou")

from enlace import *
import time

def removeEOP(rxBuffer2):
    print(rxBuffer2)
    for i in range (len(rxBuffer2)):
        
    
            if i >3 :

                if (rxBuffer2[i] == 122 and rxBuffer2[i-1] == 122 and rxBuffer2[i-2]==122  and rxBuffer2[i-3] == 122):
                    if i ==len(rxBuffer2)-1:
                        del rxBuffer2[i]
                        del rxBuffer2[i-1]
                        del rxBuffer2[i-2]
                        del rxBuffer2[i-3]
                    else:
                        print(rxBuffer2[i-3])
                        print(rxBuffer2[-4])
                        print("EOP está num lugar inesperado.")
                        

    return rxBuffer2


def removeStuffing(rxBuffer2):
    z = 0
    for i in range(len(rxBuffer2)):
        if i >4:
            if (rxBuffer2[i] == 122 and rxBuffer2[i-1] == 122 and rxBuffer2[i-2]==0  and rxBuffer2[i-3] == 122 and rxBuffer2[i-4] == 122):
                z+=1
                    
    for i in range (len(rxBuffer2)-z):
        if i >4:
            if (rxBuffer2[i] == 122 and rxBuffer2[i-1] == 122 and rxBuffer2[i-2]==0  and rxBuffer2[i-3] == 122 and rxBuffer2[i-4] == 122):
                del rxBuffer2[i-2]
    return rxBuffer2

def toByte(rxBuffer2, lista):
    for x in rxBuffer2:
        lista.append(x)
        rxBuffer2 = bytes(lista)
    return rxBuffer2

# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python3 -m serial.tools.list_ports

serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
#serialName = "/dev/cu.usbmodem142101"
#serialName = "COM4"                  # Windows(variacao de)
print("abriu com")

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()

    

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")

    ocioso = True;  
    rxBuffer, nRx = com.getData(6)
    


    
    

    tamanho = int.from_bytes(rxBuffer[4:], byteorder='little')
    index = int.from_bytes(rxBuffer[2:4 ], byteorder='little')
    total = int.from_bytes(rxBuffer[:2], byteorder='little')
    lista = list()
          
    
    while index <total:
        if index ==1:
            rxBuffer2, nRx = com.getData(tamanho)
         

            index +=1
                

        else:
            rxBuffer, nRx = com.getData(6)
            tamanho = int.from_bytes(rxBuffer[4:], byteorder='little')
            index = int.from_bytes(rxBuffer[2:4], byteorder='little')
            print("Index atual: ", index)
            print("Tamanho do próximo pacote: ", tamanho)
            rxBuffer2, nRx = com.getData(tamanho)
            

        #Converte o rxBuffer para bytearray para podermos alterá-lo
        rxBuffer_bytearray = bytearray(rxBuffer2)
        #Remove o End Of Package
        rxBuffer_eop = removeEOP(rxBuffer_bytearray)
        #Remove Stuffing
        rxBuffer_stuff = removeStuffing(rxBuffer_eop)
        #Converte de bytearray para uma lista em byte (Para poder salvar a imagem)
        rxBuffer = toByte(rxBuffer_stuff, lista)
        
  




    
    #print(rxBuffer2)

    print ("Lido              {} bytes ".format(nRx))

    
    open("logo.png", "wb").write(rxBuffer)
    print("Imagem salva")
    #print(rxBuffer2[:EOPstart-2].decode("utf-8"))
    print("------------------------------------------")
    
         
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()




    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()  
