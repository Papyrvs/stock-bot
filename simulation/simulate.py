from lxml import etree
from io import StringIO, BytesIO
import datetime, sys, inspect, os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from Degiro import degiro
class Simulate:
    def __init__(self, stock):
        self.stck = degiro._Ticker(stock)
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

    def SimulateBuy(self, amount):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        tree = etree.parse("simulatorData.xml",parser) #loads in document with the parser previously defined
        root = tree.getroot() #root = <transactions/> basically

        buy = root[0] #root is a list object with all elements inside. This just get's us <buy/>
        buyIndex = len(buy) #finds where in the list to add next stock/currency

        #start adding in all the elements our stock purchase needs and fills them out with text
        etree.SubElement(buy, "stock")
        etree.SubElement(buy[buyIndex], "name")
        etree.SubElement(buy[buyIndex], "datetime")
        etree.SubElement(buy[buyIndex], "price")
        etree.SubElement(buy[buyIndex], "amount")
        buy[buyIndex][0].text = self.stock
        buy[buyIndex][1].text = now
        buy[buyIndex][2].text = str(self.stck.checkPrice()[self.stock]) #TODO: make dynamic like datetime
        buy[buyIndex][3].text = str(amount)

        filestuff = etree.tostring(tree, pretty_print=True, encoding='unicode')

        file = open("simulatorData.xml", "w")
        file.write(filestuff) #overwrite filedata
    

    def SimulateSell(self, amount):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
        tree = etree.parse("simulatorData.xml",parser) #loads in document with the parser previously defined
        root = tree.getroot() #root = <transactions/> basically

        sell = root[1] #root is a list object with all elements inside. This just get's us <buy/>
        sellIndex = len(sell) #finds where in the list to add next stock/currency

        #start adding in all the elements our stock purchase needs and fills them out with text
        etree.SubElement(sell, "stock")
        etree.SubElement(sell[sellIndex], "name")
        etree.SubElement(sell[sellIndex], "datetime")
        etree.SubElement(sell[sellIndex], "price")
        etree.SubElement(sell[sellIndex], "amount")
        sell[sellIndex][0].text = self.stock
        sell[sellIndex][1].text = now
        sell[sellIndex][2].text = str(self.stck.checkPrice()[self.stock])#TODO: make dynamic like datetime
        sell[sellIndex][3].text = str(amount)

        filestuff = etree.tostring(tree, pretty_print=True, encoding='unicode')

        file = open("simulatorData.xml", "w")
        file.write(filestuff) #overwrite filedata
