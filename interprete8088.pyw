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
    if newvalue > int("0xffff",base=16):
       print("ERRORE OVERFLOW")
       self.regX = -1
       self.regL = hex(-1)
       self.regH = hex(-1)
    elif newvalue > int("0xff",base=16) and newvalue <= int("0xffff",base=16):
       self.regH = hex(newvalue >> 8)
       self.regL = hex(newvalue - (int(self.regH,base=16) << 8))
       self.regX = newvalue
    else:
       self.regH = hex(0)
       self.regL = hex(newvalue)
       self.regX = newvalue
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

btnok = tk.Button(root, text=textbtn+str(0), height = 2,width = 32,activebackground='black',background='black',foreground='white',activeforeground='white')
btnok.place(x = 20,y = 280)
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
instructions = [
##################compiled test syntax########### 
                partial(MOV,"AH","36"),
                partial(MOV,"AL","5"),
                "label:",
                partial(ADD,"AH","1"),
                partial(SUB,"AL","8"),
                partial(ADD,"BX","5"),
                "GOTO label"
#################################################          
                ]
instructionsprint = [
################uncompiled test syntax###########               
                "MOVB AH,36",
                "MOVB AL,5",
                "label:",
                "ADDB AH,1",
                "SUBB AL,8",
                "ADD BX,5",
                "JMP label"
#################################################
                ]
#in compiling those tho variables will be taken from an external file,the first one is "my" compiled code
#the second one is just a string printing to make it readable to the user
for x in range(0,len(instructions),1):
  PCF = PCF + 1
PCF = PCF - 1
while PC <= PCF:
    if type(instructions[PC]) == str:
      btnok.config(text=textbtn + str(PC)+ "   instr: " + instructionsprint[PC])
      root.update()
      input("")
      if instructions[PC][0] == "G" and instructions[PC][1] == "O" and instructions[PC][2] == "T" and instructions[PC][3] == "O":
           tmp = ""
           for x in range(5,len(instructions[PC]),1):
              tmp = tmp + instructions[PC][x]
           GOTO(tmp)
    else:
        btnok.config(text=textbtn + str(PC)+ "   instr: " + instructionsprint[PC])
        root.update()
        input("")       
        instructions[PC]()
    PC = PC + 1

root.mainloop()
       



