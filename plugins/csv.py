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
            with open(self.config["output_file"], 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
        except:
            return False
        
        return "ok"

    def export(self, finding, screenshots):
        """ Create new csv """
        
        header = []
        data   = []
        
        file_empty = True
                
        # opening the csv file
        if exists(self.config["output_file"]):
            with open(self.config["output_file"], 'r', encoding='UTF8') as csv_file:
                # init reader
                csv_reader = csv.DictReader(csv_file)
                dict_from_csv = dict(list(csv_reader)[0])
                header = list(dict_from_csv.keys())
                if len(header) > 0:
                    # allow to append data without header
                    file_empty = False

        for key in finding:
            if not key in self.unwanted_data:
                if file_empty:
                    # Add value to header
                    header.append(key)
                    
                # Add value to row  
                data.append(finding[key])
        
        with open(self.config["output_file"], 'a+', encoding='UTF8') as f:
            # init writer
            writer = csv.writer(f)

            if file_empty:
                # write the header
                writer.writerow(header)

            # write the data
            writer.writerow(data)

        return True
