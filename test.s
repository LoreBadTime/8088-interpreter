_EXIT = 1
_PRINTF = 127
_INPUT = 117
_CONVERT = 48

!IFEQ = JE
!IFNOTEQ = JNE
!IFMAG = JG
!IFMAGEQ = JGE
!IFMIN = JL
!IFMINEQ = JLE


.SECT .TEXT
label:
   MOV AX, 0
   MOV AX, 1
   MOV AX, 0xff
   MOV AX, 0x7fff
   MOV AX, 0x8000
   MOV AX, 0xffff
   MOV AX, 0x10000
   MOV AX, -1
   MOV AX, -0xff
   MOV AX, -0x7fff
   MOV AX, -0x8000
   MOV AX, -0xffff
   MOV AX, -0x10000
   MOVB AL, 32
   MOVB BH, AL
   MOVB CL, BH
   MOV DX, CL
   ADD AX, BX
   JMP label
   CALL _EXIT
!___________USCITA_______________
exit:
   MOV SP, BP !reset stack
   POP BP !necessitiomo di tornare in BP
   RET

.SECT .DATA

   v: .BYTE 1, 2, 3, 4, 5, 6
   v_end: .BYTE 0
   v1: .BYTE 7, 8, 9, 10, 11, 12
   n: .BYTE 0 
   m: .BYTE 0 
   s: .ASCII "%d \0"

.SECT .BSS
   get: .SPACE 1


