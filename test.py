#!/usr/bin/python
#EpicBot in development by @bitcoinjake09 7/10/2019
#EpicBot in Update by @bitcoinjake09 & @bountywolf 8/24/2019from steem import Steem
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


PK = ''#put your private key here
accountname = 'bitcoinjake09' #replace my name with your STEEM name

startBet = 0.1
AboveOrBelow = 'Above' # can be 'Above' or 'Below'
OverUnderNum = 6

stopLose = 0 #set the amount(acount balance) you want to stop at when losing.
stopWin = 150 #set the amount(acount balance) you want to stop at when winning.

#betAmount = 1
#AboveOrBelow = 'Below' # can be 'Above' or 'Below'
#OverUnderNum = 95


s = Steem(node = nodes, keys=[PK])
blockchain = Blockchain()
stream = blockchain.stream()

nums = muchWon = 0
whichAmt = fromWho = memoWhat = accFrom = memoDatas = amountDatas = ""
winLose = fromEpic = None
betAmount = startBet

count = 1 #do not modify - is part of loop + display
minimumBet = 0.1
sleepAmt = 4
isTooMuch = bet100 = oUn = 0.00
houseEdge = (1 - 0.02)

#get balance
userAcct = Account(accountname)
steemBalance = Amount(userAcct['balance']).amount
print("%s STEEM" % steemBalance)
while(count <= 10000):
	bet100 = betAmount * 100
	if (AboveOrBelow == 'Above'):
		oUn = 100 - OverUnderNum
	    	isTooMuch = bet100 / oUn * (1 - 0.02)
	elif (AboveOrBelow == 'Below'):
    		oUn = OverUnderNum - 1
   	 	isTooMuch = bet100 / oUn * (1 - 0.02)
   	if (isTooMuch > 100):
	  	print("IS TOO MUCH!")
    		betAmount = startBet
	
	betTX = [operations.Transfer(**{
        "from": accountname,
        "to": "epicdice",
        "amount": str(betAmount) + " STEEM",
        "memo": str(AboveOrBelow) + " " + str(OverUnderNum),
    })]
	tb = TransactionBuilder()
	tb.appendOps(betTX)
	tb.appendSigner(accountname, "active")
	tb.sign()
	tb.broadcast()
	print ('bet # ' + str(count))
	count = count + 1
	userAcct = Account(accountname)
	steemBalance = Amount(userAcct['balance']).amount
	print("%s STEEM" % steemBalance)
	if steemBalance <= stopLose:
	   	print("%s STEEM left, hit stopLose." % steemBalance)
		break
	elif steemBalance >= stopWin:
    		print("%s STEEM left, hit stopWin." % steemBalance)
    		break
	betAmount = betAmount + (betAmount*0.1)


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
			nums = nums + 1
			if fromEpic is True:
				if winLose is True:
					print(accountname + " Won! " + str(muchWon[0]) + " STEEM")
					break
				elif winLose is False:
					print(accountname + " Lost! :,( " + str(muchWon[0]) + " STEEM")
					break
