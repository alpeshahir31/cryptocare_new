# -*- coding: utf-8 -*-
# -*- File: app.py -*-
# -*- Author: aB9 -*-
# -*- Date: 03/12 -*-

import json

#List of supported cryptocurrencies
cryptocurrencies_dict = {'Bitcoin': 'BTC',
                         'Ripple':'XRP',
                         'Iota':'IOT',
                         'Ethereum': 'ETH',
                         'Litecoin':'LTC',
                         #                         'Nem':'XEM',
                         #                         'Neo':'NEO',
                         #                         'Dashcoin':'DSH',
                         #                         'Numerai':'NMR',
                         #                         'OmiseGo':'OMG',
                         #                         'QTUM':'QTUM',
                         #                         'Stratis':'STRAT',
                         #                         'Waves':'WAVES'
                         }

cryptocurrencies_list = ['BTC','XRP','IOT','ETH','LTC','NEO','STRAT','WAVES']

#Cryptocurrency Object Class
class CryptoCurrency:
    def __init__(self, asset_id="", name="", cr_price=0, cr_close=0, cr_high=0, cr_low=0, cr_open=0, cr_volume_from=0, cr_volume_to=0, symbol=None, url=None, image_url = None,cr_change_24_hr=None,cr_low_24_hr=None,cr_high_24_hr=None,cr_open_24_hr=None,cr_vol_24_hr=None,cr_last_vol_to=None):
        self.asset_id = asset_id
        self.name = name
        self.cr_price = cr_price
        self.cr_close = cr_close
        self.cr_high = cr_high
        self.cr_low = cr_low
        self.cr_open = cr_open
        self.cr_volume_from = cr_volume_from
        self.cr_volume_to = cr_volume_to
        self.symbol = symbol
        self.url = url
        self.image_url = image_url
        self.cr_change_24_hr = cr_change_24_hr
        self.cr_low_24_hr=cr_low_24_hr
        self.cr_high_24_hr=cr_high_24_hr
        self.cr_open_24_hr=cr_open_24_hr
        self.cr_vol_24_hr=cr_vol_24_hr
        self.cr_last_vol_to=cr_last_vol_to

        ####End of __init__ ####

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
####End of Class Cryptocurrency#####
        

#CrypotCurrency in details Object class        
class CryptoCurrencyDetails:
#    def __init__(self,FROMSYMBOL, FROMSYMBOL_D, TOSYMBOL, TOSYMBOL_D, PRICE, PRICE_D, 
#                 LASTUPDATE, VOLUMEDAY_CRY, VOLUMEDAY_CUR, OPENDAY, OPENDAY_D, HIGHDAY, HIGHDAY_D,
#                 LOWDAY, LOWDAY_D, OPEN24HOUR, OPEN24HOUR_D, HIGH24HOUR, HIGH24HOUR_D, LOW24HOUR, LOW24HOUR_D,
#                 CHANGE24HOUR, CHANGE24HOUR_D, CHANGEDAY, CHANGEDAY_D, SUPPLY, SUPPLY_D, MKTCAP, MKTCAP_D):
#        self.FROMSYMBOL = FROMSYMBOL
#        self.FROMSYMBOL_D = FROMSYMBOL_D
#        self.TOSYMBOL = TOSYMBOL
#        self.TOSYMBOL_D = TOSYMBOL_D
#        self.PRICE = PRICE
#        self.PRICE_D = PRICE_D
#        self.LASTUPDATE = LASTUPDATE
#        self.VOLUMEDAY_CRY = VOLUMEDAY_CUR
#        self.OPENDAY = OPENDAY
#        self.OPENDAY_D = OPENDAY_D
#        self.HIGHDAY = HIGHDAY
#        self.HIGHDAY_D = HIGHDAY_D
#        self.LOWDAY = LOWDAY
#        self.LOWDAY_D = LOWDAY_D
#        self.OPEN24HOUR = OPEN24HOUR
#        self.OPEN24HOUR_D = OPEN24HOUR_D
#        self.HIGH24HOUR = HIGH24HOUR
#        self.HIGH24HOUR_D = HIGH24HOUR_D
#        self.LOW24HOUR = LOW24HOUR
#        self.LOW24HOUR_D = LOW24HOUR_D
#        self.CHANGE24HOUR = CHANGE24HOUR
#        self.CHANGE24HOUR_D = CHANGE24HOUR_D
#        self.CHANGEDAY = CHANGEDAY
#        self.CHANGEDAY_D = CHANGEDAY_D
#        self.SUPPLY = SUPPLY
#        self.SUPPLY_D = SUPPLY_D
#        self.MKTCAP = MKTCAP
#        self.MKTCAP_D = MKTCAP_D
    
    def __init__(self, values_dict=[], display_values_dict=[]):
        self.values = values_dict
        self.display_values = display_values_dict
        ####End of __init__
####End of CrypoCurrencyDetails
                