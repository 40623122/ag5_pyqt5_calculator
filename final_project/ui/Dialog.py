# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QDialog
from .Ui_Dialog import Ui_Dialog

class Dialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.setupUi(self)

        '''以下為使用者自行編寫程式碼區'''
        self.display.setText('0')
          
      

        self.equalButton.clicked.connect(self.equalClicked)    
        self.clearButton.clicked.connect(self.clear)
        self.clearAllButton.clicked.connect(self.clearAll)
        self.clearMemoryButton.clicked.connect(self.clearMemory)
        self.readMemoryButton.clicked.connect(self.readMemory)
        self.setMemoryButton.clicked.connect(self.setMemory)
        self.sumSoFar = 0.0
    
   



        self.waitingForOperand = True
        #數字鈕連接函式 (Function)
        for button in [
            self.one,
            self.two,
            self.three,
            self.four,
            self.five,
            self.six,
            self.seven,
            self.eight,
            self.nine,
            self.zero
        ]:
            button.clicked.connect(self.digitClicked)
        #Clear 鈕連接函式
        self.clearButton.clicked.connect(self.clear)
        #Clear all 鈕連接函式
        self.clearAllButton.clicked.connect(self.clearAll)
        #backspace 鈕連接函式
        self.backspaceButton.clicked.connect(self.backspaceClicked)
        #小數點按鈕連接函式
        self.pointButton.clicked.connect(self.pointClicked)
        #運算子 (加減、乘除)
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        #加減號按鈕連接函式
        for button in [self.plusButton, self.minusButton]:
            button.clicked.connect(self.additiveOperatorClicked)
        #乘除號按鈕連接函式
        for button in [self.timesButton, self.divisionButton]:
            button.clicked.connect(self.multiplicativeOperatorClicked)
        #等於按鈕連接函式
        self.equalButton.clicked.connect(self.equalClicked)
        # 按下變號
        self.pos_neg.clicked.connect(self.changeSignClicked)
    

    def digitClicked(self):
        #取得傳送信號的物件
        clickedButton = self.sender()
        #按鈕上的數字
        digitValue = int(clickedButton.text())
        #當顯示的文字為 0，而且此數字為 0。
        if self.display.text() == '0' and digitValue == 0.0:
            #回傳 (終止函式)
            return
        #如果需要等待操作
        if self.waitingForOperand:
            #清除顯示
            self.display.clear()
            #重設此物件的狀態
            self.waitingForOperand = False
        #顯示數字
        self.display.setText(self.display.text() + str(digitValue))
        
    def clear(self):
        if self.waitingForOperand:
            return
        #重新顯示 0
        self.display.setText('0')
        self.waitingForOperand = True
    
    #重設所有狀態
    def clearAll(self):
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.display.setText('0')
        self.waitingForOperand = True
    
    def backspaceClicked(self):
        if self.waitingForOperand:
            return
        #取得螢幕上的文字 (拿走最後一項)
        text = self.display.text()[:-1]
        #如果沒有文字
        if not text:
            text = '0'
            self.waitingForOperand = True
        #設定數字到螢幕上
        self.display.setText(text)
    
    def pointClicked(self):
        '''
        如果等待輸入，
        按下小數點，相當於輸入 0.xxx，
        因此自動補零。
        '''

        #pass
        clickedButton = self.sender()
        
        digitValue = int(clickedButton.text())
       
        if self.display.text() == '0' and digitValue == 0.0:
            return
        
            self.display.clear()
           
            self.waitingForOperand = False
      
        self.display.setText(self.display.text() + str(digitValue))
    
        
    
        
        
       

    def unaryOperatorClicked(self):
        '''單一運算元按下後處理方法'''
        pass
        

        if self.waitingForOperand:
            self.display.setText('0')
        #若沒有小數點，補上。
        if "." not in self.display.text():
            self.display.setText(self.display.text() + ".")
        self.waitingForOperand = False
    

    def additiveOperatorClicked(self):
        clickedButton = self.sender()
        #取得按鈕符號 (運算子)
        clickedOperator = clickedButton.text()
        #取得螢幕上的文字，轉成小數
        operand = float(self.display.text())
        #如果有乘除運算子
        if self.pendingMultiplicativeOperator:
            #如果計算，且失敗。
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            #先顯示結果
            self.display.setText(str(self.factorSoFar))
            #儲存結果到 operand 名稱 (name) 裡。
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
        #如果有加減運算子
        if self.pendingAdditiveOperator:
            #如果計算，且失敗。
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            #顯示結果
            self.display.setText(str(self.sumSoFar))
        else:
            #如果沒有加減運算子，儲存乘除的結果。
            self.sumSoFar = operand
        #儲存按鈕符號
        self.pendingAdditiveOperator = clickedOperator
        self.waitingForOperand = True
    
    def multiplicativeOperatorClicked(self):

        '''乘或除按下後進行的處理方法'''
        #pass
        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())

        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
 
        
            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand
 
        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True
        
    def equalClicked(self):
        '''等號按下後的處理方法'''
        #pass
        operand = float(self.display.text())
 
    
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
 
    
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
 
            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand
 
        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True
        
    def pointClicked(self):
        '''小數點按下後的處理方法'''
        #pass
        if self.waitingForOperand:
            self.display.setText('0')
 
        if "." not in self.display.text():
            self.display.setText(self.display.text() + ".")
 
        self.waitingForOperand = False
 
        
    def changeSignClicked(self):
        '''變號鍵按下後的處理方法'''
        #pass
        text = self.display.text()
        value = float(text)
 
        if value > 0.0:
            text = "-" + text
        elif value < 0.0:
            text = text[1:]
 
        self.display.setText(text)
        
    def backspaceClicked(self):
        '''回復鍵按下的處理方法'''
        #pass
        if self.waitingForOperand:
            return
 
        text = self.display.text()[:-1]
        if not text:
            text = '0'
            self.waitingForOperand = True
 
        self.display.setText(text)
        
    def clear(self):
        '''清除鍵按下後的處理方法'''
        #pass

        self.display.setText('0')
        self.waitingForOperand = True
       
    def clearAll(self):
        '''全部清除鍵按下後的處理方法'''
        #pass
        self.sumSoFar = 0.0
        self.factorSoFar = 0.0
        self.pendingAdditiveOperator = ''
        self.pendingMultiplicativeOperator = ''
        self.display.setText('0')
        self.waitingForOperand = True
       
        
    def clearMemory(self):
        '''清除記憶體鍵按下後的處理方法'''
        #pass
        self.sumInMemory = 0.0
        
    def readMemory(self):
        '''讀取記憶體鍵按下後的處理方法'''
        #pass
        self.display.setText(str(self.sumInMemory))
        self.waitingForOperand = True
 
        
    def setMemory(self):
        '''設定記憶體鍵按下後的處理方法'''
        #pass
        self.equalClicked()
        self.sumInMemory = float(self.display.text())
        
    def addToMemory(self):
        '''放到記憶體鍵按下後的處理方法'''
        #pass
        self.equalClicked()
        self.sumInMemory += float(self.display.text())
 
        
    def createButton(self):
        ''' 建立按鍵處理方法, 以 Qt Designer 建立對話框時, 不需要此方法'''
        #pass
        

        clickedButton = self.sender()
        clickedOperator = clickedButton.text()
        operand = float(self.display.text())
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            self.display.setText(str(self.factorSoFar))
        else:
            self.factorSoFar = operand
        self.pendingMultiplicativeOperator = clickedOperator
        self.waitingForOperand = True
    
    """
    計算 (被除數, 運算子)，回傳計算結果
    True: 成功
    False: 失敗
    """
    def calculate(self, rightOperand, pendingOperator):
        if pendingOperator == "+":
            self.sumSoFar += rightOperand
        elif pendingOperator == "-":
            self.sumSoFar -= rightOperand
        elif pendingOperator == "*":
            self.factorSoFar *= rightOperand
        elif pendingOperator == "/":
            #防止除零
            if rightOperand == 0.0:
                return False
            self.factorSoFar /= rightOperand
        return True
    
    #Error 畫面 "####"

    def abortOperation(self):
        self.clearAll()
        self.display.setText("Nope!! Don't copy our calculator.")
    
     def equalClicked(self):
        operand = float(self.display.text())
        if self.pendingMultiplicativeOperator:
            if not self.calculate(operand, self.pendingMultiplicativeOperator):
                self.abortOperation()
                return
            operand = self.factorSoFar
            self.factorSoFar = 0.0
            self.pendingMultiplicativeOperator = ''
        if self.pendingAdditiveOperator:
            if not self.calculate(operand, self.pendingAdditiveOperator):
                self.abortOperation()
                return
            self.pendingAdditiveOperator = ''
        else:
            self.sumSoFar = operand
        self.display.setText(str(self.sumSoFar))
        self.sumSoFar = 0.0
        self.waitingForOperand = True
        
    def changeSignClicked(self):
        text = self.display.text()
        value = float(text)
 
        if value > 0.0:
            text = "-" + text
        elif value < 0.0:
            text = text[1:]
 
        self.display.setText(text)
