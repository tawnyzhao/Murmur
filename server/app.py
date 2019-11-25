import os, requests, module as an
from flask import *
from functions import *

###############################################################################
# OBJECTS
###############################################################################
# Sound sample
class Sound:
	def __init__(self, vol = 0, direc = 0, time = 0):
		self.vol = vol
		self.dir = direc
		self.time = time

# Data transfer to website
class Data:
	def __init__(self, n = 0, avgvol = 0, time = 0):
		self.n = n
		self.avgvol = avgvol
		self.time = time

class Module:
	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

###############################################################################
# CONSTANTS
###############################################################################
UPLOAD_FOLDER = 'uploads'
x = 3 # size of grid: width
y = 3 # size of grid: height
grid = []
modules = [] # list of Module objects (contains locations of modules)
tdelta = 3.0 # refresh delay
FILE_NAME = ''
nSamples = 5
module = an.Module
zoom = 50

# App initialization
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

###############################################################################
# HELPERS
###############################################################################
# Run a function periodically
def refresh(f, delay):
	t = Timer(delay, f)
	t.start()

# Update sample data datetime.now().strftime('%I:%M:%S%p')
def update():
	global grid, nSamples, zoom
	module.read_files()
	module.process_files()

	smooth1 = module.chonk_avg(module.channel1, zoom)
	smooth2 = module.chonk_avg(module.channel2, zoom)
	smooth3 = module.chonk_avg(module.channel3, zoom)
	drawPlot(smooth1, 1)
	grid = module.convertToVolumeList(module.find_module_events(smooth1, smooth2, smooth3), smooth1, smooth2, smooth3)
	# convert(grid)
	nSamples = len(grid)
	# nSamples = round(random() * 8 + 1)
	# grid = []
	# for i in range(nSamples):
	# 	grid.append(gen_random())
	# refresh(update, tdelta)

# Print info to console
def printGrid():
	global tdelta, x, y, grid
	points = list(map(exact, grid))
	for data in points:
		print('-------------------------------')
		print('Volume: ' + str(data.vol) + ', Direction: ' + str(data.dir) + ', Time: ' + str(data.time))
		print('-------------------------------')

# Put relevant data in Data object to send to front-end
def genData(points):
	global nSamples
	average = round(sum([point.vol for point in points]) / nSamples, 2)
	return Data(nSamples, average, points[0].time)

###############################################################################
# ROUTES 
###############################################################################
# Upload
@app.route('/upload', methods = ['GET', 'POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file']
		f.save(os.path.join(UPLOAD_FOLDER, f.filename))
	return redirect(url_for(index))

# Home
@app.route('/', methods = ['GET', 'POST'])
def index():
	global grid, tdelta, nSamples
	update()
	# printGrid()
	points = list(map(exact, grid))
	for display in points:
		display.vol = round(display.vol, 2)
		display.dir = round(display.dir, 2)
	address = gen_radar(points)
	data = genData(points)
	return render_template('index.html', data=data, address=address, tdelta=tdelta)

# Test POST Requests
@app.route('/listen', methods = ['POST'])
def listen():
	global FILE_NAME
	if request.method == 'POST':
		print('RECEIVED')
		f = request.files['file']
		f.save(os.path.join('uploads2', f.filename))
		FILE_NAME = f.filename
		print('File name: ' + FILE_NAME)
		# print('IP Address:' + )
	return redirect('/')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=5000)