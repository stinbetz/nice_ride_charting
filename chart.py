# import pygal
import plotly
from datetime import date, timedelta
from plotly.graph_objs import Scatter, Layout, Bar

# wx_chart = pygal.Line()
# wx_chart.title = "temperatures by day"
# wx_chart.x_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

datafile = open('NiceRideDataOut.dat', 'r')
data = datafile.readlines()
datafile.close()

temps = []
rides = []
start_date = date(2015, 1, 1)
day_increment = timedelta(days=1)
dates = [start_date + (day_increment * offset) for offset in range(365)]
for line in data:
    temp = eval(line)
    temps.append(temp[temp.keys()[0]]['avg_temp'])
    rides.append(temp[temp.keys()[0]]['ride_count']/28)



plotly.offline.plot({"data": [Scatter(y=temps, x=dates), Bar(y=rides, x=dates, text=["rides %d" % (x * 28) for x in rides])],
                    "layout": Layout(title="temperatures")})

# wx_chart.add('Temperature', temps)
# wx_chart.render_to_file('NiceRide.svg')
# print temps
