#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Andre Augusto Giannotti Scota (https://sites.google.com/view/a2gs/)

from sys import exit, argv
from time import strftime, gmtime
from os import getenv

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceWithdrawException, BinanceRequestException

class order_c:
	_symb         = str("")
	_side         = str("")
	_qtd          = int(0)
	_priceLimit   = float(0.0)
	_priceTrigger = float(0.0)
	_orderId      = str("")
	_type         = int(0)

	def __init__(self,
	             Psymb         : str = "",
	             Pside         : str = "",
	             Pqtd          : int = 0,
	             PpriceLimit   : float = 0.0,
	             PpriceTrigger : float = 0.0,
	             PorderId      : str = "",
	             Ptype         : str = ""):
		self.symb         = Psymb
		self.side         = Pside
		self.qtd          = Pqtd
		self.priceLimit   = PpriceLimit
		self.priceTrigger = PpriceTrigger
		self.orderId      = PorderId
		self.type         = binanceOrderType[Ptype]

	def print(self):
		print(f"Symbol.......: [{self.symb}]")
		print(f"Side.........: [{self.side}]")
		print(f"Qtd..........: [{self.qtd}]")
		print(f"Price Limit..: [{self.priceLimit}]")
		print(f"Price Trigger: [{self.priceTrigger}]")
		print(f"Id...........: [{self.orderId}]")
		print(f"Type.........: [{self.type}]")

	@property
	def symb(self) -> str:
		return self._symb

	@symb.setter
	def symb(self, value : str = ""):
		self._symb = value

	@property
	def side(self) -> str:
		return self._side

	@side.setter
	def side(self, value : str = ""):
		self._side = value

	@property
	def qtd(self):
		return self._qtd

	@qtd.setter
	def qtd(self, value : int = 0):
		self._qtd = value

	@property
	def priceLimit(self):
		return self._priceLimit

	@priceLimit.setter
	def priceLimit(self, value : int = 0):
		self._priceLimit = value

	@property
	def priceTrigger(self):
		return self._priceTrigger

	@priceTrigger.setter
	def priceTrigger(self, value : int = 0):
		self._priceTrigger = value

	@property
	def orderId(self):
		return self._orderId

	@orderId.setter
	def orderId(self, value : str = ""):
		self._orderId = value

	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, value : str = ""):
		try:
			self._type = binanceOrderType[value]
		except:
			self._type =  ""

binanceOrderType = {
	'LIMIT'             : Client.ORDER_TYPE_LIMIT,
	'LIMIT_MAKER'       : Client.ORDER_TYPE_LIMIT_MAKER,
	#'MARKET'            : Client.ORDER_TYPE_MARKET,
	'STOP_LOSS'         : Client.ORDER_TYPE_STOP_LOSS,
	'STOP_LOSS_LIMIT'   : Client.ORDER_TYPE_STOP_LOSS_LIMIT,
	'TAKE_PROFIT'       : Client.ORDER_TYPE_TAKE_PROFIT,
	'TAKE_PROFIT_LIMIT' : Client.ORDER_TYPE_TAKE_PROFIT_LIMIT
}

def printHelp():
	print("0) ENVIRONMENT VARIABLES:")
	print("BINANCE_APIKEY - ")
	print("BINANCE_SEKKEY - ")
	print("")
	print("1) PLACE A NEW ORDER AND TRAILING STOP (-n):")
	print("./TrailingStop -n SYMBOL SIDE PRICE_LIMIT QTD_LIMIT PRICE_REFRESH_SECONDS TRIGGER_PERCENTAGE(Stop price) NEW_POSITION_PERCENTAGE(Limit price)")
	print("SYMBOL")
	print("SIDE - SELL / BUY")
	print("PRICE_LIMIT")
	print("QTD_LIMIT")
	print("PRICE_REFRESH_SECONDS")
	print("TRIGGER_PERCENTAGE - How much distance from placed order to current price to replace the order")
	print("NEW_POSITION_PERCENTAGE - How much from current price to replace the new order")
	print("")
	print("./TrailingStop -n BTCUSDT BUY 10000 2 3 10 4")
	print("")
	print("2) TRAILING STOP FOR AN EXISTING ORDER:")
	print("./TrailingStop -f ORDERE_ID PRICE_REFRESH_SECONDS TRIGGER_PERCENTAGE NEW_POSITION_PERCENTAGE")
	print("")
	print("3) LIST ALL ORDERS INFORMATION:")
	print("./TrailingStop -i")
	print("")
	print("4) CANCEL AN ORDER:")
	print("./TrailingStop -c ORDER_SYMBOL ORDER_ID")
	print("")
	print("5) SYMBOL LAST PRICE:")
	print("./TrailingStop -p SYMBOL")

def milliTime(t):
	return(strftime(f"%d/%b/%Y %a %H:%M:%S.{t % 1000}", gmtime(t / 1000)))

def printOrders(spotOrder):
	print(f"Symbol: [{spotOrder['symbol']}]")
	print(f"\tOrder Id: [{spotOrder['orderId']}] | Time: [{milliTime(spotOrder['time'])}]")
	print(f"\tSide: [{spotOrder['side']}] | Type: [{spotOrder['type']}]")
	print(f"\tQtd: [{spotOrder['origQty']}] | Qtd executed: [{spotOrder['executedQty']}]")
	print(f"\tPrice (limit): [{spotOrder['price']}] | Stop price (trigger): [{spotOrder['stopPrice']}]")

def listOpenOrders(client) -> bool:

	try:
		openOrders = client.get_open_orders() #recvWindow

	except BinanceRequestException as e:
		print(f"Erro at client.get_open_orders() BinanceRequestException: [{e.status_code} - {e.message}]")
		return False

	except BinanceAPIException as e:                                                                                                
		print(f"Erro at client.get_open_orders() BinanceAPIException: [{e.status_code} - {e.message}]")
		return False

	except Exception as e:
		print("Erro at client.get_open_orders(): {e}")
		return False

	print(f"Spot open orders ({len(openOrders)}):")
	[printOrders(i) for i in openOrders]

	print("")

	try:
		openOrders = client.get_open_margin_orders()

	except BinanceRequestException as e:
		print(f"Erro at client.get_open_margin_orders() BinanceRequestException: [{e.status_code} - {e.message}]")
		return False

	except BinanceAPIException as e:                                                                                                
		print(f"Erro at client.get_open_margin_orders() BinanceAPIException: [{e.status_code} - {e.message}]")
		return False

	except Exception as e:
		print("Erro at client.get_open_margin_orders(): {e}")
		return False

	print(f"Margin open orders ({len(openOrders)}):")
	[printOrders(i) for i in openOrders]

	return True

def cancelOrder(client, idOrder : int, symb : str) -> bool:

	try:
		cancOrd = client.cancel_order(symbol = symb, orderId = idOrder)

	except BinanceRequestException as e:
		print(f"Erro at client.cancel_order() BinanceRequestException: [{e.status_code} - {e.message}]")
		return False

	except BinanceAPIException as e:
		print(f"Erro at client.cancel_order() BinanceAPIException: [{e.status_code} - {e.message}]")
		return False

	except Exception as e:
		print("Erro at client.cancel_order(): {e}")
		return False

	print("Canceled order:")
	print(f"Symbol: [{cancOrd['symbol']}]")
	print(f"\tOrder Id.............: [{cancOrd['orderId']}]")
	print(f"\tPrice................: [{cancOrd['price']}]")
	print(f"\tOriginal Qtd.........: [{cancOrd['origQty']}]")
	print(f"\tExecuted Qty.........: [{cancOrd['executedQty']}]")
	print(f"\tCummulative Quote Qty: [{cancOrd['cummulativeQuoteQty']}]")
	print(f"\tStatus...............: [{cancOrd['status']}]")
	print(f"\tType.................: [{cancOrd['type']}]")
	print(f"\tSide.................: [{cancOrd['side']}]")

	return True

def TS(client, order : order_c) -> bool:
#order.print()

	return True

#def getOrderInfo(client, symb : str, orderid : int) -> (bool, order_c):
def getOrderInfo(client, orderid : int) -> (bool, order_c):

	try:
#		o = client.get_all_orders(symbol = "*", orderId = orderid, limit = 1)
		o = client.get_open_margin_orders() #recvWindow

	except BinanceAPIException as e:
		print(f"Erro at client.get_all_orders() BinanceAPIException: [{e.status_code} - {e.message}]")
		return (False, None)

	except BinanceRequestException as e:
		print(f"Erro at client.get_all_orders() BinanceRequestException: [{e.status_code} - {e.message}]")
		return (False, None)

	except Exception as e:
		print("Erro at client.get_all_orders(): {e}")
		return (False, None)

	if len(o) != 1:
		return (False, None)

	oa = next((item for item in o if item['orderId'] == orderid), None)

	order = order_c(oa['symbol'], oa['side'], oa['origQty'], oa['price'], oa['orderId'], oa['type'])

	return (True, order)

def TS_createOrder(client, symb, side, priceLimit, qtdLimit, priceRefreshSeconds, triggerPercent, newPositPercent) -> bool:
	order = order_c()
	if TS(client, order) == False:
		return False

def TS_existingOrder(client, orderId : int, priceRefreshSeconds, triggerPercent, newPositPercent) -> bool:
	(retORderInfo, order) = getOrderInfo(client, orderId)
	order.print()
	if TS(client, order) == False:
		return False

def printPrice(client, symb : str) -> bool:

	try:
		pa = client.get_ticker(symbol = symb)

	except BinanceAPIException as e:
		print(f"Erro at client.get_avg_price() BinanceAPIException: [{e.status_code} - {e.message}]")
		return False

	except BinanceRequestException as e:
		print(f"Erro at client.get_avg_price() BinanceRequestException: [{e.status_code} - {e.message}]")
		return False

	except Exception as e:
		print("Erro at client.get_avg_price(): {e}")
		return False

	print(f"Symbol: [{symb}] | Price.: [{pa['lastPrice']}]")

	return True

# APIs:
# order_limit_sell()

binanceAPIKey = getenv("BINANCE_APIKEY", "NOTDEF_APIKEY")
if binanceAPIKey == "NOTDEF_APIKEY":
	print("Environment variable BINANCE_APIKEY not defined!")
	exit(1)

binanceSEKKey = getenv("BINANCE_SEKKEY", "NOTDEF_APIKEY")
if binanceSEKKey == "NOTDEF_APIKEY":
	print("Environment variable BINANCE_SEKKEY not defined!")
	exit(1)

try:
	client = Client(binanceAPIKey, binanceSEKKey, {"verify": True, "timeout": 20})

except BinanceAPIException as e:
	print(f"Binance API exception: [{e.status_code} - {e.message}]")
	exit(1)

except BinanceRequestException as e:
	print(f"Binance request exception: [{e.status_code} - {e.message}]")
	exit(1)

except BinanceWithdrawException as e:
	print(f"Binance withdraw exception: [{e.status_code} - {e.message}]")
	exit(1)

except Exception as e:
	print("Binance connection error: {e}")
	exit(1)

if len(argv) >= 2:

	if argv[1] == '-n' and len(argv) == 9:
		TS_createOrder(client, argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8])

	elif argv[1] == '-f' and len(argv) == 6:
		TS_existingOrder(client, int(argv[2]), argv[3], argv[4], argv[5])

	elif argv[1] == '-i' and len(argv) == 2:
		listOpenOrders(client)

	elif argv[1] == '-c' and len(argv) == 4:
		cancelOrder(client, int(argv[2]), argv[3])

	elif argv[1] == '-p' and len(argv) == 3:
		printPrice(client, argv[2])

	else:
		print("Parameters error.")
		printHelp()
else:
	printHelp()
