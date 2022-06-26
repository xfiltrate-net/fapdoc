# fapdoc - pwndoc exporting/importing tool
#
# Copyright (C) 2018 <Giuseppe `r3vn` Corti>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from libs.plugins import base
from os.path import exists

import csv

class plugin(base):
    
    def init(self):
        """ csv export plugin """
        return True

    def test(self):
        """ Get all projects viewable by user. """
        try:
            with open(self.config["output_path"], 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
        except:
            return False
        
        return "ok"

    def importdata(self, audit):
        """ Import csv file """

        reader = csv.DictReader(open(self.config["import_path"]))

        findings = {}
        for row in reader:
            key = row.pop('title')
            if key in findings:
                pass

            findings[key] = row


        for fin in findings:
            findings[fin]["title"] = fin
            self.pwndoc.add_finding(audit, findings[fin])

        return True

    def export(self, finding, screenshots):
        """ Create new csv """
        
        try:
            header = self.config["columns"].replace(" ","").split(",")

        except:
            header = []
            
        data = []
        file_empty = True
                
        # opening the csv file
        if exists(self.config["output_path"]):
            try:
                with open(self.config["output_path"], 'r', encoding='UTF8') as csv_file:
                    # init reader
                    csv_reader = csv.DictReader(csv_file)
                    
                    # get header from file
                    header_new = list(dict(list(csv_reader)[0]).keys())
                    
                    if len(header_new) > 0:
                        # replace user defined header with existent one
                        header = header_new
                        # allow to append data without header
                        file_empty = False
            except:
                pass
        
        if len(header) <= 0:
            # generate header from finding
            for key in finding:
                if not key in self.unwanted_data:
                    header.append(key)
            
        for key in header:
            try:
                data.append(finding[key])
            except:
                data.append("")
            
        with open(self.config["output_path"], 'a+', encoding='UTF8') as f:
            # init writer
            writer = csv.writer(f)

            if file_empty:
                # write the header
                writer.writerow(header)

            # write the data
            writer.writerow(data)

        return True
