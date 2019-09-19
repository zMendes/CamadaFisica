
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação 
####################################################


print("Iniciou")

from enlace import *
import time

t1 = 1
t2 = 2
t3 = 3
t4 = 4






t5 =5 
t6 = 6
PC_ID =2

def typeTwo():
    type_message = 2
    type_message = type_message.to_bytes(1, "little")
    
    id_server = 1
    id_server = id_server.to_bytes(1,"little")
    
    len_playload = 0
    len_playload = len_playload.to_bytes(1,"little")
    
    index = 0
    index = index.to_bytes(3,"little")
    
    eop =  "zzzz"
    eop = eop.encode()
    
    return (type_message + id_server + len_playload + index + eop)

def typeFour():
    type_message = 4
    type_message = type_message.to_bytes(1, "little")
    
    id_server = 1
    id_server = id_server.to_bytes(1,"little")
    
    len_playload = 0
    len_playload = len_playload.to_bytes(1,"little")
    
    index = 0
    index = index.to_bytes(3,"little")
    
    eop =  "zzzz"
    eop = eop.encode()
    
    return (type_message + id_server + len_playload + index + eop)

def typeFive():
    type_message = 5
    type_message = type_message.to_bytes(1, "little")
    
    id_server = 1
    id_server = id_server.to_bytes(1,"little")
    
    len_playload = 0
    len_playload = len_playload.to_bytes(1,"little")
    
    index = 0
    index = index.to_bytes(3,"little")
    
    eop =  "zzzz"
    eop = eop.encode()
    
    return (type_message + id_server + len_playload + index + eop)

def typeSix(index):
    type_message = 6
    type_message = type_message.to_bytes(1, "little")
    
    id_server = 1
    id_server = id_server.to_bytes(1,"little")
    
    len_playload = 0
    len_playload = len_playload.to_bytes(1,"little")
    
    index = index.to_bytes(3,"little")
    
    eop =  "zzzz"
    eop = eop.encode()
    
    return (type_message + id_server + len_playload + index + eop)









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
print("abriu com")

def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName) # repare que o metodo construtor recebe um string (nome)
    # Ativa comunicacao
    com.enable()
    time.sleep(2)

    file = open("log.txt", "w")

    # Log
    print("-------------------------")
    print("Comunicação inicializada")
    print("  porta : {}".format(com.fisica.name))
    print("-------------------------")
    
    ocioso = True  
    #com.fisica.flush()
    while ocioso:
        rxBuffer, nRx = com.getData(5)
        print("Depois do get Data")
        id = int.from_bytes(rxBuffer[1:2], byteorder='little')
        tipo = int.from_bytes(rxBuffer[0:1], byteorder='little')
        tamanho = int.from_bytes(rxBuffer[2:3], byteorder='little')
        print("Tipo da mensagem recebida: ", tipo)
        if   tipo == t1:
            if id == 2:
                file.write("Mensagem: Tipo 1 - recebida: " + str(round(time.time())) + " - destinatário: 2 \n")
                time.sleep(1)
                rxBuffer, nRx = com.getData(tamanho)
                rxBuffer = bytearray(rxBuffer)
                rxBuffer2 = removeEOP(rxBuffer)
                total = int.from_bytes(rxBuffer, byteorder='little')
                print("Enviando Mensagem TIPO2")
                type2 = typeTwo()
                com.sendData(type2)
                file.write("Mensagem: Tipo 2 - enviada: " + str(round(time.time())) + " - destinatário: 1 \n")
                ocioso = False
                print("Saindo do ocioso")
                
        else: time.sleep(1)
            
    

    index = 1
    
    lista = list()
          
        
    
    while index <total and ocioso==False:
        timer1 = time.time()
        timer2 = time.time()
        reset = True    
        while reset:
            reset = False
            
            rxBuffer, nRx = com.getDataTimerServer(5, timer1, timer2)
            tipo = int.from_bytes(rxBuffer[0:1], byteorder='little')
                    
            if tipo == t3:
                file.write("Mensagem: Tipo 3 - recebida: " + str(round(time.time())) + " - destinatário: 2 \n")
                print("Mensagem T3 recebida")
                tamanho = int.from_bytes(rxBuffer[2:3], byteorder='little')
                i_pacote = int.from_bytes(rxBuffer[3:5], byteorder='little')    
                if index == i_pacote:
                    print("Pacote de número {0} veio corretamente.".format(index))
                    com.sendData(typeFour())
                    print(typeFour())
                    file.write("Mensagem: Tipo 4 - enviada: " + str(round(time.time())) +  " - destinatário: 1 \n")
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
                    print("Index recebido e esperado não batem")    
                    print("Enviando mensagem T6")
                    file.write("Mensagem: Tipo 6 - enviada: " + str(round(time.time())) + " - destinatário: 1 \n")
                    com.sendData(typeSix(index))
                    
            else:   
                print("Mensagem recebida não é T3")
                print(rxBuffer, "RXXXXXXXXXXXXXXXXXXXxx")
                time.sleep(1)
                a = rxBuffer[0]
                if a ==222:
                    com.sendData(typeFive())
                    file.write("Mensagem: Tipo 5 - enviada: " + str(round(time.time())) + " - destinatário: 1 \n")
                    ocioso = True
                    print(":(")
                elif a==111:
                    reset = True
                    com.sendData(typeFour())
                    file.write("Mensagem: Tipo 4 - enviada: " + str(round(time.time())) + " - destinatário: 1 \n")
                    timer1 = time.time()
                else:
                    com.fisica.flush()
                    print("deu o flsuhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
                
            time.sleep(0.2)
                
        
                
  




    file.close()
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
