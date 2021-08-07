from pathlib import Path
import tkinter as tk
from tkinter.filedialog import askopenfilename
from dataclasses import dataclass
from functools import partial
global root,username

global registers,run,PC,PCF,instructions
global textbtn
textbtn = "PC:"
import re
filename = ""
PC = 0
PCF = 0

class Breg(object):
  global root
  def __init__(self,name,x,y):
    self.name = name
    self.nameX = name + "X"
    self.nameL = name + "L"
    self.nameH = name + "H"
    self.regH = hex(0)
    self.regL = hex(0)
    self.regX = 0
    self.x = x
    self.y = y
    self.btnH = tk.Button(root, text=self.nameH +": "+ str(self.regH), height = 2,width = 16,activebackground='black',background='black',foreground='white',activeforeground='white')
    self.btnL = tk.Button(root, text=self.nameL +": "+ str(self.regL), height = 2,width = 16,activebackground='black',background='black',foreground='white',activeforeground='white')
    self.btnX = tk.Button(root, text=self.nameX +": "+ str(self.regX), height = 2,width = 16,activebackground='black',background='black',foreground='white',activeforeground='white')
    self.btnH.place(x = self.x,y = self.y)
    self.btnL.place(x = self.x + 120,y = self.y)
    self.btnX.place(x = self.x + 260,y = self.y)
    root.update()
  def setRegXvalue(self,newvalue):
    if abs(newvalue) > int("0xffff",base=16):
       newvalue = newvalue%(int("0xffff",base=16) + 1)
    
    if newvalue == 0:
       self.regH = hex(0)
       self.regL = hex(0)
       self.regX = 0
    
    #######
    elif newvalue > int("0x7fff",base=16) and newvalue <= int("0xffff",base=16):
       self.regH = hex(newvalue >> 8)
       self.regL = hex(newvalue - (int(self.regH,base=16) << 8))
       self.regX =(256*int(self.regH,base=16) + int(self.regL,base=16)) - int("0xffff",base=16) - 1
    elif newvalue > int("0xff",base=16) and newvalue <= int("0x7fff",base=16):
       self.regH = hex(newvalue >> 8)
       self.regL = hex(newvalue - (int(self.regH,base=16) << 8))
       self.regX = newvalue
    elif newvalue > 0 and newvalue <= int("0xff",base=16):
       self.regH = hex(0)
       self.regL = hex(newvalue)
       self.regX = newvalue
    #######
    elif newvalue < 0 and newvalue >= (-int("0xff",base=16)):
       self.regH = hex(int("0xff",base=16))
       self.regL = hex(int("0xff",base=16) + newvalue + 1)
       self.regX = newvalue
    elif newvalue < (-int("0xff",base=16)) and newvalue >= -(int("0x8000",base=16)):
       self.regX = newvalue 
       self.regH = hex((int("0xffff",base=16) + newvalue + 1) >> 8)
       self.regL = hex(self.regX + (int(self.regH,base=16) << 8))
                       
    elif newvalue < (-int("0x8000",base=16)) and newvalue >= (-int("0xffff",base=16)):
       self.regX = int("0xffff",base=16) - abs(newvalue) + 1
       self.regH = hex(self.regX >> 8)
       self.regL = hex(self.regX - (int(self.regH,base=16) << 8))
    string = ": "
    self.btnX.config(text=self.nameX + string + str(self.regX))
    self.btnH.config(text=self.nameH + string + str(self.regH))
    self.btnL.config(text=self.nameL + string + str(self.regL))
    root.update()
  def setRegHvalue(self,inpt):
    self.regH = hex(inpt%(int("0xff",base=16)+1))
    string = ": "
    self.btnH.config(text=self.nameH + string + str(self.regH))
    self.regX = (256*int(self.regH,base=16) + int(self.regL,base=16))
    if self.regX > int("0x7fff",base=16):
      self.regX =(256*int(self.regH,base=16) + int(self.regL,base=16)) - int("0xffff",base=16) - 1
    string = ": "
    self.btnX.config(text=self.nameX + string + str(self.regX))
    root.update()
  def setRegLvalue(self,inpt):
    self.regL = hex(inpt%(int("0xff",base=16)+1))
    string = ": "
    self.btnL.config(text=self.nameL + string + str(self.regL))
    self.regX = 256*int(self.regH,base=16) + int(self.regL,base=16)
    if self.regX > int("0x7fff",base=16):
      self.regX = (256*int(self.regH,base=16) + int(self.regL,base=16)) - int("0xffff",base=16) - 1
    string = ": "
    self.btnX.config(text=self.nameX + string + str(self.regX))
    root.update()
    
root = tk.Tk()
root.title("8088 interpreter")
root.configure(background='black')
root.geometry("450x500")
root.resizable(True,True)

btnok = tk.Button(root, text=textbtn+str(0), height = 1,width = 32,activebackground='black',background='black',foreground='cyan',activeforeground='cyan')
btnok.place(x = 40,y = 350)
btnPC0 = tk.Button(root,highlightthickness = 0, bd = 0, text="", height = 1,width = 32,activebackground='black',background='black',foreground='white',activeforeground='white')
btnPC0.place(x = 40,y = 330)
btnPC1 = tk.Button(root,highlightthickness = 0, bd = 0, text="", height = 1,width = 32,activebackground='black',background='black',foreground='white',activeforeground='white')
btnPC1.place(x = 40,y = 310)
btnPC2 = tk.Button(root,highlightthickness = 0, bd = 0, text="", height = 1,width = 32,activebackground='black',background='black',foreground='white',activeforeground='white')
btnPC2.place(x = 40,y = 375)
btnPC3 = tk.Button(root,highlightthickness = 0, bd = 0, text="", height = 1,width = 32,activebackground='black',background='black',foreground='white',activeforeground='white')
btnPC3.place(x = 40,y = 395)
btnindicator = tk.Button(root,highlightthickness = 0, bd = 0, text="->", height = 1,width = 1,activebackground='black',background='black',foreground='white',activeforeground='white')
btnindicator.place(x = 20,y = 350)
btnPC = tk.Button(root,highlightthickness = 0, bd = 0, text=textbtn, height = 1,width = 5,activebackground='black',background='black',foreground='white',activeforeground='white')
btnPC.place(x = 300,y = 350)
AX = Breg("A",20,80)
BX = Breg("B",20,120)
CX = Breg("C",20,160)
DX = Breg("D",20,200)

root.update()
registers = [AX,BX,CX,DX]

def MOVER (Reg,Reg2):
    global registers
    for x in registers:
        if Reg == x.nameH:
           for y in registers:
               if Reg2 == y.nameH:
                   x.setRegHvalue(int(y.regH,base=16))
                   return
               elif Reg2 == y.nameL:
                   x.setRegHvalue(int(y.regL,base=16))
                   return
               elif Reg2 == y.nameX:
                   print("REGISTER ERROR")
                   return
           x.setRegHvalue(int(Reg2))
           return
        elif Reg == x.nameL:
            for y in registers:
               if Reg2 == y.nameH:
                   x.setRegLvalue(int(y.regH,base=16))
                   return
               elif Reg2 == y.nameL:
                   x.setRegLvalue(int(y.regL,base=16))
                   return
               elif Reg2 == y.nameX:
                   print("REGISTER ERROR")
                   return
            x.setRegLvalue(int(Reg2))
            return
        elif Reg == x.nameX:
            for y in registers:
               if Reg2 == y.nameH:
                   x.setRegXvalue(int(y.regH,base=16))
                   return
               elif Reg2 == y.nameL:
                   x.setRegXvalue(int(y.regL,base=16))
                   return
               elif Reg2 == y.nameX:
                   x.setRegXvalue(y.regX)
                   return
            x.setRegXvalue(int(Reg2))
            return
          
def MOV (Reg,Reg2):
    global PC
    MOVER(Reg,Reg2)
    root.update()
    return object
  
def ADDER (Reg,Reg2):
    global registers
    for x in registers:
        if Reg == x.nameH:
           for y in registers:
               if Reg2 == y.nameH:
                   x.setRegHvalue(int(y.regH,base=16) + int(x.regH,base=16))
                   return
               elif Reg2 == y.nameL:
                   x.setRegHvalue(int(y.regL,base=16) + int(x.regH,base=16))
                   return
               elif Reg2 == y.nameX:
                   print("REGISTER ERROR")
                   return
           x.setRegHvalue(int(Reg2) + int(x.regH,base=16))
           return
        elif Reg == x.nameL:
            for y in registers:
               if Reg2 == y.nameH:
                   x.setRegLvalue(int(y.regH,base=16) + int(x.regL,base=16))
                   return
               elif Reg2 == y.nameL:
                   x.setRegLvalue(int(y.regL,base=16) + int(x.regL,base=16))
                   return
               elif Reg2 == y.nameX:
                   print("REGISTER ERROR")
                   return
            x.setRegLvalue(int(Reg2) + int(x.regL,base=16))
            return
        elif Reg == x.nameX:
            for y in registers:
               if Reg2 == y.nameH:
                   x.setRegXvalue(int(y.regH,base=16) + x.regX)
                   return
               elif Reg2 == y.nameL:
                   x.setRegXvalue(int(y.regL,base=16) + x.regX)
                   return
               elif Reg2 == y.nameX:
                   x.setRegXvalue(y.regX + x.regX)
                   return
            x.setRegXvalue(int(Reg2) + x.regX)
            return
          
def ADD (Reg,Reg2):
    global PC
    ADDER(Reg,Reg2)
    root.update()
    return object
  
def SUBBER (Reg,Reg2):
    global registers
    for x in registers:
        if Reg == x.nameH:
           for y in registers:
               if Reg2 == y.nameH:
                   x.setRegHvalue(int(x.regH,base=16) - int(y.regH,base=16))
                   return
               elif Reg2 == y.nameL:
                   x.setRegHvalue(int(x.regH,base=16) - int(y.regL,base=16))
                   return
               elif Reg2 == y.nameX:
                   print("REGISTER ERROR")
                   return
           x.setRegHvalue(int(x.regH,base=16) - int(Reg2))
           return
        elif Reg == x.nameL:
            for y in registers:
               if Reg2 == y.nameH:
                   x.setRegLvalue(int(x.regL,base=16) - int(y.regH,base=16))
                   return
               elif Reg2 == y.nameL:
                   x.setRegLvalue(int(x.regL,base=16) - int(y.regL,base=16))
                   return
               elif Reg2 == y.nameX:
                   print("REGISTER ERROR")
                   return
            x.setRegLvalue(int(x.regL,base=16) - int(Reg2))
            return
        elif Reg == x.nameX:
            for y in registers:
               if Reg2 == y.nameH:
                   x.setRegXvalue(x.regX - int(y.regH,base=16))
                   return 
               elif Reg2 == y.nameL:
                   x.setRegXvalue(x.regX - int(y.regL,base=16))
                   return
               elif Reg2 == y.nameX:
                   x.setRegXvalue(x.regX - y.regX)
                   return
            x.setRegXvalue(x.regX - int(Reg2))
            return
          
def SUB (Reg,Reg2):
    global PC
    SUBBER(Reg,Reg2)
    root.update()
    return object

def GOTO (label):
    global PC
    PC = 0
    for x in instructions:
      if x == label + ":":
         PC = x.index(label + ":") + 1
         return
    print(PC)
    print("ERROR MISSING LABEL " + label)
def NOP ():
    global PC
    root.update()
    return object
#############################################################################
def MULTIPLER (Reg2):
    global registers
    for y in registers:
       if y.nameH == Reg2:
         registers[0].setRegXvalue(int(y.regH,base=16) * int(registers[0].regL,base=16))
         return
       elif y.nameL == Reg2:
         registers[0].setRegXvalue(int(y.regL,base=16) * int(registers[0].regL,base=16))
         return
       elif y.nameX == Reg2:
         k = registers[0].regX * y.regX
         if k <= int("0xffff",base=16):
            registers[0].setRegXvalue(k)
            registers[3].setRegXvalue(0)
         elif k > int("0xffff",base=16):
            registers[3].setRegXvalue(k >> 16)
            registers[0].setRegXvalue(k - ((k >> 16) << 16)) 
           
def MUL (Reg2):
    global PC
    MULTIPLER(Reg2)
    root.update()
    return object
instructions = [
               partial(NOP),
               partial(NOP)
##################compiled test syntax########### 

#################################################          
                ]
instructionsprint = [ " ",
                      " "
################uncompiled test syntax###########               

#################################################
                ]
with open("test.s",mode="r") as file:
    uncompiled = file.readlines()
    for line in uncompiled:
       count = 0
       for letter in line:
          exad = False
          contatore = 0
          if letter == ":":
            reg1 = ""
            while line[contatore] != ":" and line[contatore] != "\n":
              if line[contatore] != " ":
                reg1 = reg1 + line[contatore]
              contatore = contatore + 1
            instructionsprint.append(reg1 + ":")
            instructions.append(reg1 + ":")
            contatore = 0
            break
            
          if letter == ' ' or letter == '\n':
            count = count + 1
            pass
          elif (line[count] == "M" and line[count+1] == "O" and line[count + 2] == "V" and line[count + 3] == "B"): 
            count = count + 5
            reg1 = ""
            reg2 = ""
            while line[count] != ",":
              reg1 = reg1 + line[count]
              count = count + 1
            count = count + 2
            while line[count] != ' ' and line[count] != '\n':
              reg2 = reg2 + line[count]
              count = count + 1
            tmp = ""
            for letter in reg2:
               tmp = tmp + letter
               if tmp == "0x" or tmp == "-0x":
                 exad = True
                 reg2 = int(reg2,base=16)
            instructions.append(partial(MOV,reg1,reg2))
            if exad == True:
              instructionsprint.append("MOVB "+ reg1 + "," + hex(reg2))
            else:
              instructionsprint.append("MOVB "+ reg1 + "," + reg2)
            exad = False
            break
          elif (line[count] == "M" and line[count+1] == "O" and line[count + 2] == "V" and line[count + 3] == " "): 
            count = count + 4
            reg1 = ""
            reg2 = ""
            while line[count] != ",":
              reg1 = reg1 + line[count]
              count = count + 1
            count = count + 2
            while line[count] != ' ' and line[count] != '\n':
              reg2 = reg2 + line[count]
              count = count + 1
            tmp = ""
            for letter in reg2:
               tmp = tmp + letter
               if tmp == "0x" or tmp == "-0x":
                 exad = True
                 reg2 = int(reg2,base=16)
            instructions.append(partial(MOV,reg1,reg2))
            if exad == True:
              instructionsprint.append("MOV "+ reg1 + "," + hex(reg2))
            else:
              instructionsprint.append("MOV "+ reg1 + "," + reg2)
            exad = False
            break
          elif (line[count] == "A" and line[count+1] == "D" and line[count + 2] == "D" and line[count + 3] == "B"): 
            count = count + 5
            reg1 = ""
            reg2 = ""
            while line[count] != ",":
              reg1 = reg1 + line[count]
              count = count + 1
            count = count + 2
            while line[count] != ' ' and line[count] != '\n':
              reg2 = reg2 + line[count]
              count = count + 1
            tmp = ""
            for letter in reg2:
               tmp = tmp + letter
               if tmp == "0x" or tmp == "-0x":
                 exad = True
                 reg2 = int(reg2,base=16)
            instructions.append(partial(ADD,reg1,reg2))
            if exad == True:
              instructionsprint.append("ADDB "+ reg1 + "," + hex(reg2))
            else:
              instructionsprint.append("ADDB "+ reg1 + "," + reg2)
            exad = False
            break
          elif (line[count] == "A" and line[count+1] == "D" and line[count + 2] == "D" and line[count + 3] == " "): 
            count = count + 4
            reg1 = ""
            reg2 = ""
            while line[count] != ",":
              reg1 = reg1 + line[count]
              count = count + 1
            count = count + 2
            while line[count] != ' ' and line[count] != '\n':
              reg2 = reg2 + line[count]
              count = count + 1
            tmp = ""
            for letter in reg2:
               tmp = tmp + letter
               if tmp == "0x" or tmp == "-0x":
                 exad = True
                 reg2 = int(reg2,base=16)
            instructions.append(partial(ADD,reg1,reg2))
            if exad == True:
              instructionsprint.append("ADD "+ reg1 + "," + hex(reg2))
            else:
              instructionsprint.append("ADD "+ reg1 + "," + reg2)
            exad = False
            break
          elif (line[count] == "G" and line[count+1] == "O" and line[count + 2] == "T" and line[count + 3] == "O") or (line[count] == "J" and line[count+1] == "M" and line[count + 2] == "P"): 
            tmpvar = count
            count = count + 4
            reg1 = ""
            reg2 = ""
            while line[count] != " " and line[count] != "\n":
              reg1 = reg1 + line[count]
              count = count + 1
            
            if (line[tmpvar] == "J" and line[tmpvar+1] == "M" and line[tmpvar + 2] == "P"):
              instructionsprint.append("JMP "+ reg1)
            else:
              instructionsprint.append("GOTO "+ reg1)
            instructions.append("GOTO "+ reg1)
            break
            
           
          
instructionsprint.append("")          
instructions.append(partial(NOP))
instructionsprint.append("")          
instructions.append(partial(NOP))

for x in instructionsprint:
  print(x)

#in compiling those tho variables will be taken from an external file,the first one is "my" compiled code
#the second one is just a string printing to make it readable to the user
for x in range(0,len(instructions),1):
  PCF = PCF + 1
PCF = PCF - 1
PC = 2
while PC <= PCF:
    if type(instructions[PC]) == str:
      btnok.config(text=instructionsprint[PC])
      btnPC.config(text = textbtn + str(PC - 2))
      btnPC0.config(text=instructionsprint[PC - 1])
      btnPC1.config(text=instructionsprint[PC - 2])
      btnPC2.config(text=instructionsprint[PC + 1])
      btnPC3.config(text=instructionsprint[PC + 2])
      root.update()
      input("")
      if instructions[PC][0] == "G" and instructions[PC][1] == "O" and instructions[PC][2] == "T" and instructions[PC][3] == "O":
           tmp = ""
           for x in range(5,len(instructions[PC]),1):
              tmp = tmp + instructions[PC][x]
           GOTO(tmp)
    else:
        btnok.config(text=instructionsprint[PC])
        btnPC.config(text = textbtn + str(PC - 2))
        btnPC0.config(text=instructionsprint[PC - 1])
        btnPC1.config(text=instructionsprint[PC - 2])
        btnPC2.config(text=instructionsprint[PC + 1])
        btnPC3.config(text=instructionsprint[PC + 2])
        root.update()
        input("")       
        instructions[PC]()
    PC = PC + 1

root.mainloop()
       



