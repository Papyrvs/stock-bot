from lxml import etree
from io import StringIO, BytesIO
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

parser = etree.XMLParser(remove_blank_text=True, remove_comments=True)
tree = etree.parse("simulatorData.xml",parser) #loads in document with the parser previously defined
root = tree.getroot() #root = <transactions/> basically

buy = root[0]
sell = root[1]

buyIndex = len(buy)
sellIndex = len(sell)

etree.SubElement(buy, "stock")
etree.SubElement(buy[buyIndex], "name")
etree.SubElement(buy[buyIndex], "datetime")
etree.SubElement(buy[buyIndex], "price")
buy[buyIndex][0].text = "NIO"
buy[buyIndex][1].text = now
buy[buyIndex][2].text = "12.23"

etree.SubElement(sell, "stock")
etree.SubElement(sell[sellIndex], "name")
etree.SubElement(sell[sellIndex], "datetime")
etree.SubElement(sell[sellIndex], "price")
sell[sellIndex][0].text = "NIO"
sell[sellIndex][1].text = now
sell[sellIndex][2].text = "13.33"




filestuff = etree.tostring(tree, pretty_print=True, encoding='unicode')

file = open("simulatorData.xml", "w")
file.write(filestuff)