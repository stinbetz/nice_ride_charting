import csv
import re
import datetime
import string
import collections

def get_nr_data():
    ''' returns a list of lists each entry represents one row of NiceRide data
     in form -- [[11/1/2015, 21:55], '4th Street & 13th Ave SE', '30009',
     [11/1/2015, 22:05], 'Logan Park', '30104', '565', 'Casual'] where the
     indices are
     0: [start_date, start_time]
     1: start_station,
     2: start_terminal,
     3: [end_date, end_time]
     4: end_station,
     5: end_terminal,
     6: duration (seconds),
     7: account_type (member/casual)
     '''
    nr_datafile = open('NiceRideData2015.csv', 'r')
    nr_data = []
    reader = csv.reader(nr_datafile)
    for line in reader:
        nr_data.append(reader.next())
    nr_datafile.close()
    nr_data = nr_data[1:]
    index = 0
    for line in nr_data:
        # print line
        date_data = re.match('(\d+)/(\d+)/(\d+) (\d+):(\d+)', line[0])
        start_date = datetime.date(int(date_data.group(3)),
                                   int(date_data.group(1)),
                                   int(date_data.group(2)))
        start_time = datetime.time(int(date_data.group(4)),
                                   int(date_data.group(5)),
                                   0)
        nr_data[index][0] = [start_date, start_time]

        date_data = re.match('(\d+)/(\d+)/(\d+) (\d+):(\d+)', line[3])
        end_date = datetime.date(int(date_data.group(3)),
                                 int(date_data.group(1)),
                                 int(date_data.group(2)))
        end_time = datetime.time(int(date_data.group(4)),
                                 int(date_data.group(5)),
                                 0)
        nr_data[index][3] = [end_date, end_time]

        index += 1

    return nr_data

def get_wx_data(filename):
    ''' returns a list of lists, each entry represents a day of weather data in
    the form -- ['1', '30', '11', '21', '5', '44', '0', 'T', 'T', '3', '10.4',
     '20', '330', 'M', 'M', '8', '26', '330'] where the indices are
     0: day_of_month,
     1: max_temp,
     2: min_temp,
     3: avg_temp,
     4: dev_from_norm,
     5: heating/cooling_day,
     6: tot_precip,
     7: tot_snowfall,
     8: snow_depth,
     9: avg_wind_speed,
     10: max_wind_speed,
     11: wind_dir,
     12: min_sun (if reported),
     13: percent_possible_sun (if reported),
     14: avg_sky_cover [0(clear) - 10(cloudy)],
     15: wx_event
        [
         1: fog,
         2: fog reducing vis to < 1/4 mile,
         3: thunder,
         4: ice pellets,
         5: hail,
         6: glaze/rime,
         7: blowing particulate < 1/4 mile vis,
         8:smoke/haze,
         9: blowing snow,
         X: tornado
        ],
     16: max_wind_gust,
     17: max_wind_gust_dir
     '''
    wxfile = open('wx_data/%s' % filename, 'r')
    wxdata = wxfile.readlines()
    wxfile.close()
    wxdata = wxdata[13:]
    index = 0
    for line in wxdata:
        wxdata[index] = [x for x in string.split(line.strip()) if x != '']
        index += 1
    # print wxdata
    return wxdata

def get_all_wx_data():
    '''combines all months of weather data into a dict with month abbrevs as
    keys'''
    wx_data = collections.OrderedDict()
    wx_data['jan'] = get_wx_data('1_wx.dat')
    wx_data['feb'] = get_wx_data('2_wx.dat')
    wx_data['mar'] = get_wx_data('3_wx.dat')
    wx_data['apr'] = get_wx_data('4_wx.dat')
    wx_data['may'] = get_wx_data('5_wx.dat')
    wx_data['jun'] = get_wx_data('6_wx.dat')
    wx_data['jul'] = get_wx_data('7_wx.dat')
    wx_data['aug'] = get_wx_data('8_wx.dat')
    wx_data['sep'] = get_wx_data('9_wx.dat')
    wx_data['oct'] = get_wx_data('10_wx.dat')
    wx_data['nov'] = get_wx_data('11_wx.dat')
    wx_data['dec'] = get_wx_data('12_wx.dat')
    return wx_data

def monthindex(month):
    ''' given a three char month abbreviation, return the integer month index'''
    if month == 'jan':
        return 1
    elif month == 'feb':
        return 2
    elif month == 'mar':
        return 3
    elif month == 'apr':
        return 4
    elif month == 'may':
        return 5
    elif month == 'jun':
        return 6
    elif month == 'jul':
        return 7
    elif month == 'aug':
        return 8
    elif month == 'sep':
        return 9
    elif month == 'oct':
        return 10
    elif month == 'nov':
        return 11
    else:
        return 12

def main():
    '''main, do all the things'''
    # load nr_data
    nr_data = get_nr_data()

    # load each month wx data into a dict
    wx_data = get_all_wx_data()

    combined_data_table = collections.OrderedDict()
    for month in wx_data:
        # print month
        for day in wx_data[month]:
            # print day[0]
            this_day = datetime.date(2015, monthindex(month), int(day[0]))
            # print this_day
            # print day
            # rides = [x for x in nr_data if x[0][0] == this_day]
            rides = []
            for row in nr_data:
                # print row[0][0]
                if row[0][0] == this_day:
                    rides.append(row)
            data = {'avg_temp': int(day[3]), 'precip': int(day[6]), 'ride_count': len(rides)}
            combined_data_table['%s_%s' % (month, day[0])] = data

    # print_data(combined_data_table)
    new_print(combined_data_table)

def new_print(table):
    outfile = open('NiceRideDataOut.dat', 'w')
    for row in table:
        outfile.write("{'%s': %s}\n" % (row, table[row]))
        # print row, ": ", table[row]
    outfile.close()

def print_data(table):
    jan_data = {}
    feb_data = {}
    mar_data = {}
    apr_data = {}
    may_data = {}
    jun_data = {}
    jul_data = {}
    aug_data = {}
    sep_data = {}
    oct_data = {}
    nov_data = {}
    dec_data = {}

    for row in table:
        if row.startswith('jan'):
            jan_data[row] = table[row]
        elif row.startswith('feb'):
            feb_data[row] = table[row]
        elif row.startswith('mar'):
            mar_data[row] = table[row]
        elif row.startswith('apr'):
            apr_data[row] = table[row]
        elif row.startswith('may'):
            may_data[row] = table[row]
        elif row.startswith('jun'):
            jun_data[row] = table[row]
        elif row.startswith('jul'):
            jul_data[row] = table[row]
        elif row.startswith('aug'):
            aug_data[row] = table[row]
        elif row.startswith('sep'):
            sep_data[row] = table[row]
        elif row.startswith('oct'):
            oct_data[row] = table[row]
        elif row.startswith('nov'):
            nov_data[row] = table[row]
        elif row.startswith('dec'):
            dec_data[row] = table[row]

    for key in sorted(jan_data):
        print "%s: %s" % (key, jan_data[key])
    for key in sorted(feb_data):
        print "%s: %s" % (key, feb_data[key])
    for key in sorted(mar_data):
        print "%s: %s" % (key, mar_data[key])
    for key in sorted(apr_data):
        print "%s: %s" % (key, apr_data[key])
    for key in sorted(may_data):
        print "%s: %s" % (key, may_data[key])
    for key in sorted(jun_data):
        print "%s: %s" % (key, jun_data[key])
    for key in sorted(jul_data):
        print "%s: %s" % (key, jul_data[key])
    for key in sorted(aug_data):
        print "%s: %s" % (key, aug_data[key])
    for key in sorted(sep_data):
        print "%s: %s" % (key, sep_data[key])
    for key in sorted(oct_data):
        print "%s: %s" % (key, oct_data[key])
    for key in sorted(nov_data):
        print "%s: %s" % (key, nov_data[key])
    for key in sorted(dec_data):
        print "%s: %s" % (key, dec_data[key])



if __name__ == '__main__':
    main()
