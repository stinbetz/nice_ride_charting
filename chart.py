# import pygal
import plotly
from plotly.graph_objs import Scatter, Layout, Bar

# wx_chart = pygal.Line()
# wx_chart.title = "temperatures by day"
# wx_chart.x_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

datafile = open('NiceRideDataOut.dat', 'r')
data = datafile.readlines()
datafile.close()

temps = []
rides = []
for line in data:
    temp = eval(line)
    temps.append(temp[temp.keys()[0]]['avg_temp'])
    rides.append(temp[temp.keys()[0]]['ride_count']/28)


plotly.offline.plot({"data": [Scatter(y=temps), Bar(y=rides)],
                    "layout": Layout(title="temperatures")})

# wx_chart.add('Temperature', temps)
# wx_chart.render_to_file('NiceRide.svg')
# print temps
