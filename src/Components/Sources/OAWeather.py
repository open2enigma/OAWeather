# -*- coding: utf-8 -*-


# Copyright (C) 2023 jbleyel, Mr.Servo
#
# OAWeather is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dogtag is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OAWeather.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
from Components.config import config
from Components.Sources.Source import Source
from Plugins.Extensions.OAWeather.plugin import weatherhandler


# --------------------------- Logfile -------------------------------
from os import remove
from os.path import isfile
# from Plugins.Extensions.OAWeather.plugin import logstatusin
# log file loeschen ##################################

myfile = "/tmp/OAWeatherSource.log"

# If file exists, delete it ##
if isfile(myfile):
    remove(myfile)
# File copieren ############################################
# fuer py2 die int und str anweisung raus genommen und das Grad zeichen

# log file anlegen ##################################
# kitte888 logfile anlegen die eingabe in logstatus

logstatus = "on"
# logstatus = logstatusin

# ________________________________________________________________________________


def write_log(msg):
    if logstatus == ('on'):
        with open(myfile, "a") as log:

            log.write(datetime.now().strftime("%Y/%d/%m, %H:%M:%S.%f") + ": " + msg + "\n")

            return
    return

# ****************************  test ON/OFF Logfile ************************************************


def logout(data):
    if logstatus == ('on'):
        write_log(data)
        return
    return


# ----------------------------- so muss das commando aussehen , um in den file zu schreiben  ------------------------------
logout(data="start")


class OAWeather(Source):
    logout(data="class OAWeather(Source)")
    YAHOOnightswitch = {
                    "3": "47", "4": "47", "11": "45", "12": "45", "13": "46", "14": "46", "15": "46", "16": "46", "28": "27",
                    "30": "29", "32": "31", "34": "33", "37": "47", "38": "47", "40": "45", "41": "46", "42": "46", "43": "46"
                    }
    METEOnightswitch = {"1": "2", "3": "4", "B": "C", "H": "I", "J": "K"}

    YAHOOdayswitch = {"27": "28", "29": "30", "31": "32", "33": "34", "45": "39", "46": "16", "47": "4"}

    METEOdayswitch = {"2": "1", "3": "4", "C": "B", "I": "H", "K": "J"}

    services = {"MSN": "msn", "OpenMeteo": "omw", "openweather": "owm"}

    logout(data="class OAWeather(Source) 1")

    def __init__(self):
        logout(data="init")
        Source.__init__(self)
        self.enabledebug = config.plugins.OAWeather.debug.value
        weatherhandler.onUpdate.append(self.callbackUpdate)
        self.data = weatherhandler.getData() or {}
        self.valid = weatherhandler.getValid()
        self.skydirs = weatherhandler.getSkydirs()
        self.na = _("n/a")
        self.tempunit = self.getVal("tempunit")
        self.precipitationtext = "Precipitation"
        self.humiditytext = "Humidity"
        self.feelsliketext = "Feels like"
        self.logo = self.services.get(config.plugins.OAWeather.weatherservice.value, "msn")
        self.pluginpath = None
        self.iconpath = None
        logout(data="init ende")

    def debug(self, text):
        logout(data="debug")
        if self.enabledebug:
            print("[OAWeather] Source DEBUG %s" % text)

    def callbackUpdate(self, data):
        logout(data="callbackUpdate")
        self.debug("callbackUpdate: %s" % str(data))
        self.data = data or {}
        self.logo = self.services.get(config.plugins.OAWeather.weatherservice.value, "msn")
        self.tempunit = self.getVal("tempunit")
        self.changed((self.CHANGED_ALL,))
        # self.tempunit = " "

    def getValid(self):
        logout(data="get Vaild")
        return self.valid

    def getVal(self, key):
        logout(data="getVal")
        return self.data.get(key, self.na) if self.data else self.na

    def getCurrentVal(self, key, default=_("n/a")):
        logout(data="getCurrentVal")
        self.debug("getCurrentVal:%s" % key)
        logout(data="getCurrentVal debug zurueck zu data.get")
        logout(data=str(key))
        val = self.data.get("current", {}).get(key, default)
        logout(data=str(val))
        logout(data="getCurrentVal von data.get zu debug ")
        self.debug("current key val: %s" % val)
        logout(data="getCurrentVal zurueck von debug")
        logout(data="getCurrentVal / key:%s / val:%s" % (key, val))
        logout(data="getCurrentVal ende return val")
        return val

    def getObservationTime(self):
        logout(data="getObservationTime")
        val = str(self.getCurrentVal("observationTime", ""))  # achtung muss str sein sonst keine zeichen weg nehmbar
        logout(data=str(val))
        logout(data="getObservationTime---------------val")

        observation_time_str = self.na
        if val:
            logout(data="val ok observation_time")
            observation_time_str = val[11:16]
            logout(data=str(observation_time_str))
        return observation_time_str
        # return datetime.fromisoformat(val).strftime("%H:%M") if val else self.na

    # def getSunrise(self):
    #    logout(data="getSunrise")
    #    val = self.getCurrentVal("sunrise", "")
    #    logout(data=str(val))

    #    logout(data="getSunrise 1")
        # new_string = val[11:]
        # s = new_string
        # pos = 5

        # valneu = s[0:pos]
        # logout(data="getSunrise 2")
        # logout(data=str(valneu))
    #    return datetime.fromisoformat(val).strftime("%H:%M") if val else self.na
        # return valneu

    def getSunrise(self):
        logout(data="Sunrise in")
        val = self.getCurrentVal("sunrise", "")
        logout(data="val")
        logout(data=str(val))
        formatted_timesunrise = self.na
        if val:
            logout(data="val formattedsunrise")
            formatted_timesunrise = val[11:16]
            logout(data=str(formatted_timesunrise))
        return formatted_timesunrise

    # def getDate(self, day):
    #    logout(data="getDate")
    #    val = self.getKeyforDay("date", day, "")
    #    return datetime.fromisoformat(val).strftime("%d. %b") if val else self.na

    def getDate(self, day):
        logout(data="getData in")
        log_text = "getDate day:%s" % day
        logout(data=log_text)  # Schreibt die Information in die Logdatei , z.B getDate day:1
        logout(data="getData zu getKeyforDay")
        val = self.getKeyforDay("date", day, "")
        logout(data="getData back getKeyforDay")

        formatted_date = self.na
        if val:
            date_obj = datetime.strptime(val, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d. %b")

        logout(data="getData out")
        log_text = "getDate day:%s / val:%s / formatted_date:%s" % (day, val, formatted_date)
        logout(data=log_text)  # Schreibt die Information in die Logdatei , z.B so getDate day:1 / val:2023-08-02 / formatted_date:02. Aug
        return formatted_date

    def getSunset(self):
        logout(data="getSunset")
        val = self.getCurrentVal("sunset", "")
        logout(data="val")
        logout(data=str(val))
        formatted_timesunset = self.na
        if val:
            logout(data="val formattedsunset")
            formatted_timesunset = val[11:16]
            logout(data=str(formatted_timesunset))
        return formatted_timesunset
        # return datetime.fromisoformat(val).strftime("%H:%M") if val else self.na

    def getIsNight(self):
        logout(data="getIsNight")
        return str(self.getCurrentVal("isNight", "False")) == "True"

    def getTemperature(self):
        logout(data="getTemperature")
        # self.tempunit = " "
        return "%s %s" % (self.getCurrentVal("temp"), self.tempunit)

    def getFeeltemp(self, full=False):
        logout(data="getFeeltemp")
        text = "%s " % self.feelsliketext if full else ""
        # self.tempunit = " "
        return "%s%s %s" % (text, self.getCurrentVal("feelsLike"), self.tempunit)

    def getHumidity(self, full=False):
        logout(data="getHumidity")
        text = "%s " % self.humiditytext if full else ""
        return "%s%s %s" % (text, self.getCurrentVal("humidity"), "%")

    # def getWindSpeed(self):
    #    logout(data="getWindSpeed")
    #    return "%s %s" % (self.getCurrentVal("windSpeed"), self.getVal("windunit"))

    def getWindSpeed(self):
        logout(data="getWindSpeed")
        wind_speed = self.getCurrentVal("windSpeed")
        wind_unit = self.getVal("windunit")
        logout(data="wind_speed received from source: %s" % wind_speed)     # zahl
        logout(data="wind_unit received from source: %s" % wind_unit)       # km/h
        return "%s %s" % (wind_speed, wind_unit)

    def getWindDir(self):
        logout(data="getWindDir")
        val = self.getCurrentVal("windDir")
        return ("%s " % val) if val else self.na

    def getWindDirName(self):
        logout(data="getWindDirName")
        skydirection = self.getCurrentVal("windDirSign", "")
        logout(data=str(skydirection))
        if skydirection:
            logout(data="getWindDirName if")
            skydirection = skydirection.split(" ")
            logout(data=str(skydirection))
            # die self.skydirs ist in der plugin.py da macht er aus dem W dann West
            return self.skydirs[skydirection[0]] if skydirection[0] in self.skydirs else skydirection[0]
        else:
            return self.na

    def getWindDirShort(self):
        logout(data="getWindDirShort")
        return self.getCurrentVal("windDirSign").split(" ")[1]

    def getMaxTemp(self, day):
        logout(data="getMaxTemp")
        log_text = "getMaxTemp day:%s" % day
        logout(data=log_text)  # Schreibt die Information in die Logdatei
        # self.tempunit = " "
        return "%s %s" % (self.getKeyforDay("maxTemp", day), self.tempunit)

    def getMinTemp(self, day):
        logout(data="getMinTemp")
        log_text = "getMinTemp day:%s" % day
        logout(data=log_text)  # Schreibt die Information in die Logdatei
        temp = self.getKeyforDay("minTemp", day)
        logout(data="Temp")
        logout(data=str(temp))
        # self.tempunit =" "
        return "%s %s" % (temp, self.tempunit)

    def getMaxMinTemp(self, day):
        logout(data="getMaxMinTemp")
        log_text = "getMaxMinTemp day:%s" % day
        logout(data=log_text)  # Schreibt die Information in die Logdatei
        # self.tempunit = " "
        return "%s / %s %s" % (self.getKeyforDay("minTemp", day), self.getKeyforDay("maxTemp", day), self.tempunit)

    def getPrecipitation(self, day, full=False):
        logout(data="getPrecipitation")
        text = "%s " % self.precipitationtext if full else ""
        return "%s%s %s" % (text, self.getKeyforDay("precipitation", day), self.getVal("precunit"))

    def getYahooCode(self, day):
        logout(data="getYahooCode")
        iconcode = self.getKeyforDay("yahooCode", day, "")
        if day == 0 and config.plugins.OAWeather.nighticons.value and self.getIsNight() and iconcode in self.YAHOOnightswitch:
            iconcode = self.YAHOOnightswitch[iconcode]
        else:
            self.YAHOOdayswitch.get(iconcode, iconcode)
        return iconcode

    def getMeteoCode(self, day):
        logout(data="getMeteoCode")
        iconcode = self.getKeyforDay("meteoCode", day, "")
        if day == 0 and config.plugins.OAWeather.nighticons.value and self.getIsNight() and iconcode in self.METEOnightswitch:
            iconcode = self.METEOnightswitch[iconcode]
        else:
            self.METEOdayswitch.get(iconcode, iconcode)
        return iconcode

    def getKeyforDay(self, key, day, default=_("n/a")):
        logout(data="getKeyforDay in")
        log_text = "getKeyforDay key:%s day:%s default:%s" % (key, day, default)
        logout(data=log_text)  # in logschreiben , z.B getKeyforDay key:date day:1 default: , getKeyforDay key:shortDay day:1 default:n/v

        try:
            logout(data="getKeyforDay day")
            logout(data="getKeyforDay day int")
            logout(data=str(day))
        except ValueError:
            logout(data="getKeyforDay Ungueltiger Wert für day")
            return default

        self.debug(log_text)  # hier debug aufrufen

        if day == 0:
            logout(data="getKeyforDay 1")
            return self.data.get("current", {}).get(key, default) if self.data else default

        else:
            logout(data="getKeyforDay 2 out")
            index = day - 1
            val = self.data.get("forecast", {}).get(index, {}).get(key, default)
            log_text = "getKeyforDay key:%s day:%s / val:%s" % (key, day, val)
            logout(data=log_text)  # in logscreiben z.B getKeyforDay key:date day:1 / val:2023-08-02 , getKeyforDay key:shortDay day:1 / val:Mi
            self.debug(log_text)  # hier debug aufrufen
            return val

    def destroy(self):
        logout(data="destroy")
        weatherhandler.onUpdate.remove(self.callbackUpdate)
        Source.destroy(self)
