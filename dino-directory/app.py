from flask import Flask, url_for, redirect, render_template, abort, json
import os
app = Flask(__name__)


class Dinosaur:
    def __init__(self, name, dinotype, timeperiod, continent, desc, img):
        self.name=name
        self.dinotype=dinotype
        self.timeperiod=timeperiod
        self.continent=continent
        self.desc=desc
        self.img=img


dinosaurlist = []
jsonurl = os.path.join(app.static_folder, 'data.json')
jsonfile = open(jsonurl)
jsondata = json.load(jsonfile)

def loadDinosaurs():
    jsonfile = os.path.join(app.static_folder, 'data.json')
    jsondata = json.load(open(jsonfile))

    newdinosaurlist = []
    for item in jsondata:
        newdinosaurlist.append(Dinosaur(item['name'], item['dinotype'], item['timeperiod'], item['continent'], item['desc'], item['img']))
    return newdinosaurlist

dinosaurlist = loadDinosaurs()

@app.route('/')
def noPath():
	return redirect(url_for('dinosaurs'))

@app.route('/<filterItem>')
def filterOptions(filterItem='dinotype'):
	dinosaurlist = loadDinosaurs()
	try:
		return render_template('list.html', option=filterItem, title=filterItem, optionlist=getFilterList(filterItem))
	except:
		abort(404)

@app.route('/<filterItem>/<name>')
def filterResults(filterItem='timeperiod', name=None):
	Dinosaurlist = loadDinosaurs()
	try:
		optionlist = list(filter(lambda x: getattr(x,filterItem) == name, dinosaurlist))
		return render_template('list.html', option=filterItem, dinosaurs='true', title=name, optionlist=optionlist)
	except:
		abort(404)

@app.route('/dinosaurs/<name>')
def dinosaur(name=None):
        dinosaurlist = loadDinosaurs()
	dinosaur = list(filter(lambda x: x.name == name, dinosaurlist))
	try:
		return render_template('dinosaur.html', dinosaur=dinosaur[0])
	except:
		abort(404)

@app.route('/dinosaurs')
def dinosaurs():
	dinosaurlist = loadDinosaurs()
	return render_template('list.html',option='dinosaurs', dinosaurs='true', title='All', optionlist=dinosaurlist)

def getFilterList(filterOption):
	dinosaurlist = loadDinosaurs()
        optionList = []
	for dinosaur in dinosaurlist:
		value = getattr(dinosaur, filterOption)
		if value not in optionList:
			optionList.append(value)
	return optionList

@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
