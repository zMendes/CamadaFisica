
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

    # Carrega dados
    print ("gerando dados para transmissao :")
  
      #no exemplo estamos gerando uma lista de bytes ou dois bytes concatenados
    
    #exemplo 1
    #ListTxBuffer =list()
    #for x in range(1,10):
    #    ListTxBuffer.append(x)
    #txBuffer = bytes(ListTxBuffer)
    
    #txBuffer = bytes([2]) + bytes([3])+ bytes("teste", 'utf-8')
    
    
    #txBuffer = open("cloud9.jpg", "rb").read()
    
    # Transmite dado
    #print("tentado transmitir .... {} bytes".format(txLen))
    
    
    #com.sendData(txBuffer)

    # espera o fim da transmissão
    #while(com.tx.getIsBussy()):
      #    pass
    
    
    # Atualiza dados da transmissão
    

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")

    lista_buffer =bytearray()
    rxBuffer, nRx = com.getData(6)
    #print(rxBuffer)
    #print(rxBuffer[-2:])
    print("Primeiro RXXXXXXXX", rxBuffer)
    tamanho = int.from_bytes(rxBuffer[4:], byteorder='little')
    index = int.from_bytes(rxBuffer[2:4 ], byteorder='little')
    total = int.from_bytes(rxBuffer[:2], byteorder='little')
    print(index, "indexxxxxxxx")
    print("Totalllllllllllllllllll", total)
    print(rxBuffer[-3:-5])
    print("Primeiro tamanho", tamanho)
    print(total)
    while index <=total:
        if index ==1:
            rxBuffer2, nRx = com.getData(tamanho)
            print(rxBuffer2)
            print("PRIMEIROOOOOOOO")
            print(tamanho, "aaaaaaaaaaaaa")
            index +=1

        else:
            rxBuffer2, nRx = com.getData(6)
            print(index, "indexxxxxxxxxxxxx")
            print(tamanho, "aaaaaaaaaaaaa")
            tamanho = int.from_bytes(rxBuffer2[4:], byteorder='little')
            index = int.from_bytes(rxBuffer2[2:4], byteorder='little')
            rxBuffer2, nRx = com.getData(tamanho)
            print(rxBuffer2)

        rxBuffer2 = bytearray(rxBuffer2)
        z = 0
        for i in range(len(rxBuffer2)):
            if i >4:
                if (rxBuffer2[i] == 122 and rxBuffer2[i-1] == 122 and rxBuffer2[i-2]==0  and rxBuffer2[i-3] == 122 and rxBuffer2[i-4] == 122):
                    z+=1

        for i in range (len(rxBuffer2)-z):
            if i >4:
                if (rxBuffer2[i] == 122 and rxBuffer2[i-1] == 122 and rxBuffer2[i-2]==0  and rxBuffer2[i-3] == 122 and rxBuffer2[i-4] == 122):
                     del rxBuffer2[i-2]
        lista_buffer.append(rxBuffer2)                 

    #print(rxBuffer)

    #print(nRx)
    
    #print("Len da imagem recebida",tamanho ) 
    
    #com.fisica.flush()
    #com.sendData(rxBuffer)
    #txSize = com.tx.getStatus()
    #print("Transmitido:", txSize)
  
    
    



    
    #print(rxBuffer2)

    print ("Lido              {} bytes ".format(nRx))

    
    open("logo.png", "wb").write(lista_buffer)
    print("Imagem salva")
    #print(rxBuffer2[:EOPstart-2].decode("utf-8"))
    print("------------------------------------------")


    # log
        
    #print (rxBuffer)
    #time.sleep(5)
    #print("Enviando o len de volta")
    #com.sendData(rxBuffer)
    #print("Enviado")
    
         
    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()  