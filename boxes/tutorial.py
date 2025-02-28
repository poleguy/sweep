#git clone git@github.com:florianfesti/boxes.git
#python setup.py install 
#step one copy boxes/generators/electronicsbox.py or cardbox.py




#use tests/test_svg.py as a tutorial for now.

#pip install qrcode lxml
#pytest

#to see if it passes. yup. everything is installed okay.

#initial setup window didn't work. it was mixing pytest python3.11 and python3.12 somehow.

#python
import boxes
import boxes.generators
from pathlib import Path

# this was hard to figure out because it has a side-effect of creating boxes.generators.electronicsbox
boxes.generators.getAllBoxGenerators()
# this was hard to figure out. I kept trying box = boxes.genorators.electronicsbox() or other variations
box = boxes.generators.electronicsbox.ElectronicsBox()


box.parseArgs("")
box.open()
box.render()
boxData = box.close()
print(boxData.__sizeof__())
#45977
file = Path('electronicsbox.svg')
file.write_bytes(boxData.getvalue())
#45879
#exit

#xdg-open electronixbox.svg

