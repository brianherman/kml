
from __future__ import division

import sys
import json
import math
from argparse import ArgumentParser
from datetime import datetime
class Parse:
    def load(self,filename, output):
        try:
            json_data = open(filename).read()
        except:
            print("Error opening input file")
            return

        try:
            data = json.loads(json_data)
        except:
            print("Error decoding json")
            return

        if "locations" in data and len(data["locations"]) > 0:
            try:
                f_out = open(output_dir, "w")
            except:
                print("Error creating output file for writing")
                return

            items = data["locations"]
        f_out.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        f_out.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n")
        f_out.write("  <Document>\n")
        f_out.write("    <name>Location History</name>\n")
        for item in items:
            f_out.write("    <Placemark>\n")
            # Order of these tags is important to make valid KML: TimeStamp, ExtendedData, then Point
            f_out.write("      <TimeStamp><when>")
            f_out.write(datetime.fromtimestamp(int(item["timestampMs"]) / 1000).strftime("%Y-%m-%dT%H:%M:%SZ"))
            f_out.write("</when></TimeStamp>\n")
            if "accuracy" in item or "speed" in item or "altitude" in item:
                f_out.write("      <ExtendedData>\n")
                if "accuracy" in item:
                    f_out.write("        <Data name=\"accuracy\">\n")
                    f_out.write("          <value>%d</value>\n" % item["accuracy"])
                    f_out.write("        </Data>\n")
                if "speed" in item:
                    f_out.write("        <Data name=\"speed\">\n")
                    f_out.write("          <value>%d</value>\n" % item["speed"])
                    f_out.write("        </Data>\n")
                if "altitude" in item:
                    f_out.write("        <Data name=\"altitude\">\n")
                    f_out.write("          <value>%d</value>\n" % item["altitude"])
                    f_out.write("        </Data>\n")
                f_out.write("      </ExtendedData>\n")
            f_out.write("      <Point><coordinates>%s,%s</coordinates></Point>\n" % (item["longitudeE7"] / 10000000, item["latitudeE7"] / 10000000))
            f_out.write("    </Placemark>\n")
        f_out.write("  </Document>\n</kml>\n")
