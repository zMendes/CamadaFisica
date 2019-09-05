
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


t1 =1
TIPO2 = t1.to_bytes(1, 'little')

t2 =2
TIPO2 = t2.to_bytes(1, 'little')

t3 =3
TIPO3 = t3.to_bytes(1, 'little')

t4 =4
TIPO4 = t4.to_bytes(1, 'little')

t5 =5
TIPO5 = t5.to_bytes(1, 'little')

t6 =6
TIPO6 = t6.to_bytes(1, 'little')

PC_ID = 2






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

    ocioso = True  
    
    while ocioso:
        rxBuffer, nRx = com.getData(5)
        id = int.from_bytes(rxBuffer[1:2], byteorder='little')
        tipo = int.from_bytes(rxBuffer[0:1], byteorder='little')
        tamanho = int.from_bytes(rxBuffer[2:3], byteorder='little')
        if   tipo ==t1:
            if id == PC_ID:
                time.sleep(1)
                rxBuffer, nRx = com.getData(tamanho)
                total = int.from_bytes(rxBuffer, byteorder='little')
                com.sendData(TIPO2)
                ocioso = False
                
        else: time.sleep(1)
            
    

    index = 1
    
    lista = list()
          
    
    while index <=total and ocioso==False:
        timer = time.time()
        reset = True

        
        rxBuffer, nRx = com.getData(5)
        tipo = int.from_bytes(rxBuffer[0], byteorder='little')
        while reset:
            reset = False
            if tipo == t3:
                tamanho = int.from_bytes(rxBuffer[2], byteorder='little')
                i_pacote = int.from_bytes(rxBuffer[3:], byteorder='little')    
                if index == i_pacote:
                    com.sendData(TIPO4)
                    index +=1
                    rxBuffer2, nRx = com.getData(tamanho)
                    #Converte o rxBuffer para bytearray para podermos alterá-lo
                    rxBuffer_bytearray = bytearray(rxBuffer2)
                    #Remove o End Of Package
                    rxBuffer_eop = removeEOP(rxBuffer_bytearray)
                    #Remove Stuffing
                    rxBuffer_stuff = removeStuffing(rxBuffer_eop)
                    #Converte de bytearray para uma lista em byte (Para poder salvar a imagem)
                    rxBuffer = toByte(rxBuffer_stuff, lista)

                else:
                    placeholder = 0
                    place = placeholder.to_bytes(2, byteorder='little')
                    index_esperado = index.to_bytes(2, byteorder='little')
                    com.sendData(TIPO6+place+index_esperado)
            else:
                time.sleep(1)
                timer2 = time.time() - timer
                if timer2 >20:
                    com.sendData(TIPO5)
                    ocioso = True
                    print(":(")
                else:
                    timer1 = time.time() - timer
                    if timer1 > 2:
                        com.sendData(TIPO4)
                        timer = time.time()
                        reset = True
                
        
                
  




    
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
