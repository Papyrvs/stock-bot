from lxml import etree
from io import StringIO, BytesIO
import datetime
import sys
import inspect
import os

# PACKAGE_PARENT = '..'
# SCRIPT_DIR = os.path.dirname(os.path.realpath(
#     os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# from Degiro import degiro


class Simulate:
    def __init__(self, stock=None):
        if stock != None:
            # self.stck = degiro._Ticker(stock)
            self.stock = stock
        try:
            file = open("simulatorData.xml", "r")
            file.close
            # print("File already exists")
        except:
            print("Initializing files")
            file = open("simulatorData.xml", "w")
            docText = inspect.cleandoc("""<?xml version="1.0" encoding="UTF-8"?>
            <transactions>
                <buy>
            <!--    <stock>
                        <name>NIO</name>
                        <datetime>2020-03-17 18:04:51</datetime>
                        <price>2.10</price>
                    </stock>
                    <currency>
                        <name>USD/CHF</name>
                        <datetime>2020-03-17 18:04:51</datetime>
                        <price></price>
                    </currency>
                -->
                </buy>

                <sell>
            <!--    <stock>
                        <name>NIO</name>
                        <datetime>2020-03-17 18:04:51</datetime>
                        <price>2.88</price>
                    </stock>
                    <currency>
                        <name>USD/CHF</name>
                        <datetime>2020-03-17 18:04:51</datetime>
                        <price>2.88</price>
                    </currency>-->
                </sell>
            </transactions>""")
            file.write(docText)
            file.close()

        if not file:
            sys.exit("File \"simulateData.xlm\" failed to open. Error 1")

    def SimulateBuy(self, amount, price):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        # loads in document with the parser previously defined
        tree = etree.parse("simulatorData.xml", parser)
        root = tree.getroot()  # root = <transactions/> basically

        # root is a list object with all elements inside. This just get's us <buy/>
        buy = root[0]
        # finds where in the list to add next stock/currency
        buyIndex = len(buy)

        # start adding in all the elements our stock purchase needs and fills them out with text
        etree.SubElement(buy, "stock")
        etree.SubElement(buy[buyIndex], "name")
        etree.SubElement(buy[buyIndex], "datetime")
        etree.SubElement(buy[buyIndex], "price")
        etree.SubElement(buy[buyIndex], "amount")
        buy[buyIndex][0].text = self.stock
        buy[buyIndex][1].text = now
        # TODO: make dynamic like datetime
        buy[buyIndex][2].text = str(price)
        buy[buyIndex][3].text = str(amount)

        filestuff = etree.tostring(tree, pretty_print=True, encoding='unicode')

        file = open("simulatorData.xml", "w")
        file.write(filestuff)  # overwrite filedata

    def SimulateSell(self, amount, price):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        # loads in document with the parser previously defined
        tree = etree.parse("simulatorData.xml", parser)
        root = tree.getroot()  # root = <transactions/> basically

        # root is a list object with all elements inside. This just get's us <buy/>
        sell = root[1]
        # finds where in the list to add next stock/currency
        sellIndex = len(sell)

        # start adding in all the elements our stock purchase needs and fills them out with text
        etree.SubElement(sell, "stock")
        etree.SubElement(sell[sellIndex], "name")
        etree.SubElement(sell[sellIndex], "datetime")
        etree.SubElement(sell[sellIndex], "price")
        etree.SubElement(sell[sellIndex], "amount")
        sell[sellIndex][0].text = self.stock
        sell[sellIndex][1].text = now
        # TODO: make dynamic like datetime
        sell[sellIndex][2].text = str(price)
        sell[sellIndex][3].text = str(amount)

        filestuff = etree.tostring(tree, pretty_print=True, encoding='unicode')

        file = open("simulatorData.xml", "w")
        file.write(filestuff)  # overwrite filedata

    def buyValue(self):
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        # loads in document with the parser previously defined
        tree = etree.parse("simulatorData.xml", parser)
        root = tree.getroot()  # root = <transactions/> basically

        buy = root[0]
        value = 0

        for i in buy:
            value += float(i[2].text)
        return round(value, 5)

    def sellValue(self):
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        # loads in document with the parser previously defined
        tree = etree.parse("simulatorData.xml", parser)
        root = tree.getroot()  # root = <transactions/> basically

        sell = root[1]
        value = 0

        for i in sell:
            value += float(i[2].text)
        return round(value, 5)

    def totalValue(self):
        return round(self.sellValue()-self.buyValue(), 5)
