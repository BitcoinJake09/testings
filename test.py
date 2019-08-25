#!/usr/bin/python
#EpicBot in development by @bitcoinjake09 7/10/2019
#EpicBot Update by @bitcoinjake09 & @bountywolf 8/24/2019+
from steem import Steem
from beem.steem import Steem
from beem.nodelist import NodeList
from steem.transactionbuilder import TransactionBuilder
from steembase import operations
import sys
import time
from steem.account import Account
from steem.amount import Amount
from steem import utils
import json
from steem.blockchain import Blockchain
import logging
import threading


nodes = ['https://steemd.minnowsupportproject.org/']


PK = ''
accountname = 'bitcoinjake09' #replace my name with your STEEM name

startBet = 0.1
maxBet = 5
AboveOrBelow = 'Above' # can be 'Above' or 'Below'
OverUnderNum = 91

stopLose = 150 #set the amount(acount balance) you want to stop at when losing.
stopWin = 250 #set the amount(acount balance) you want to stop at when winning.

#betAmount = 1
#AboveOrBelow = 'Below' # can be 'Above' or 'Below'
#OverUnderNum = 95

s = Steem(node = nodes, keys=[PK])
blockchain = Blockchain()
stream = blockchain.stream()

nums = muchWon = 0
betAmount = startBet

count = roundBets = 1 #do not modify - is part of loop + display
minimumBet = 0.1
houseEdge = (1 - 0.02)

#get balance
userAcct = Account(accountname)
def didWin():
	nums = muchWon = 0
	whichAmt = fromWho = memoWhat = betAmount = accFrom = memoDatas = amountDatas = ""
	winLose = fromEpic = None
	for post in stream:
	    if accountname in str(post):
		dataStr = str(post).replace("u'","'")
		dataStr = dataStr.replace("'","")
		dataStr = dataStr.replace('"',"")
		dataStr = dataStr.replace('{',"")
		dataStr = dataStr.replace('}',"")
		dataArray = dataStr.split(",")
		for datas in dataArray:
			if datas.find("from") != -1:
				fromWho = datas
				accFrom = fromWho.split(":")
				if accFrom[1].strip()=="epicdice":
					fromEpic = True
				elif accFrom[1].strip()==accountname:
					fromEpic = False
			if datas.find("memo") != -1:
				memoWhat = datas
				memoDatas = memoWhat.split(":")
				if memoDatas[1].strip()=="You have Won! Dice Rolled":
					winLose = True
				elif memoDatas[1].strip()=="You Lost. Dice Rolled":
					winLose = False

			if datas.find("betAmount") != -1:
				betAmount = datas
				amountDatas = betAmount.split(":")
				tempWon = amountDatas[1].strip()
				muchWon =tempWon.split(" ")
				
		if fromEpic is True:
			if winLose is True:
				print(accountname + " Won! " + str(muchWon[0]) + " STEEM")
				return True
			elif winLose is False:
				print(accountname + " Lost! :,( " + str(muchWon[0]) + " STEEM")
				return False
	        nums = nums + 1
# end def
def isTooBig(args2):
	bet100 = args2 * 100
	if (AboveOrBelow == 'Above'):
		oUn = 100 - OverUnderNum
	    	isTooMuch = bet100 / oUn * (1 - 0.02)
	elif (AboveOrBelow == 'Below'):
    		oUn = OverUnderNum - 1
   	 	isTooMuch = bet100 / oUn * (1 - 0.02)
   	if (isTooMuch > 100):
	  	print("IS TOO MUCH!")
		return True
	else:
		return False
# end def
while(count <= 10000):
	betTX = []
	betTX.append({
        'from': accountname,
        'to': 'epicdice',
        'amount': (str(betAmount) + ' STEEM'),
        'memo': (AboveOrBelow + ' ' + str(OverUnderNum)),
	})
	tb = TransactionBuilder()
	ops = None
	ops = [operations.Transfer(**x) for x in betTX]
	tb.appendOps(ops)
	tb.appendSigner(accountname, "active")
	tb.sign()
	tb.broadcast()
	userAcct = Account(accountname)
	steemBalance = Amount(userAcct['balance']).amount
	print("Balance: %s STEEM" % steemBalance)
	print ('bet # ' + str(count))
	print((str(betAmount) + ' STEEM ') + ((AboveOrBelow + ' ' + str(OverUnderNum))))
	if steemBalance <= stopLose:
		print("%s STEEM left, hit stopLose." % steemBalance)
		break
	elif steemBalance >= stopWin:
		print("%s STEEM left, hit stopWin." % steemBalance)
		break
	#if (didWin()):
	#	if (betAmount < maxBet):
	#		betAmount = betAmount + (betAmount*0.1)
	#	elif (betAmount >= maxBet):
	#		betAmount = startBet
	#elif not (didWin()):
	#	betAmount = startBet
	print("waiting for Win/Lose...")
	if didWin():
		boolDidWin=True
	else:
		boolDidWin=False
	if (roundBets<=3 and (not boolDidWin)):
		betAmount=startBet
	elif ((roundBets>=4 and roundBets<=12) and (not boolDidWin)):
		betAmount=betAmount + startBet
	elif ((roundBets>=13 and roundBets<=23) and (not boolDidWin)):
		betAmount=betAmount + (startBet*5)
	elif ((roundBets>=24 and roundBets<=29) and (not boolDidWin)):
		betAmount=betAmount + (startBet*10)
	if (isTooBig(betAmount) or boolDidWin or (betAmount == maxBet)):
		betAmount=startBet
		roundBets = 0
	count = count + 1
	roundBets = roundBets + 1
