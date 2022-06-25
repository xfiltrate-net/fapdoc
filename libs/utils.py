# fapdoc - pwndoc export/import tool
#
# Copyright (C) 2022 <Giuseppe `r3vn` Corti>
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

import re
import html

CLEAN_HTML = re.compile('<.*?>') 

def cleanhtml_list(list):
    cleanlist = []
    
    for item in list:
        cleanlist.append(html.unescape(cleanhtml(str(item))))
    
    return cleanlist

def cleanhtml_dict(dict):
    cleandict = {}
    
    for item in dict:
        if type(dict[item]) is not str:
            cleandict[item] = dict[item]
        
        elif item == "scope":
            cleandict[item] = cleanhtml_list(dict[item].split("</p><p>"))
    
        else:
            # Clean html if item is string
            cleandict[item] = html.unescape(cleanhtml(str(dict[item])))
    
    return cleandict

def cleanhtml(raw_html):
    """ https://stackoverflow.com/a/12982689 """
    cleantext = re.sub(CLEAN_HTML, '', raw_html)
    
    return cleantext

def get_images(raw_html):
    images = re.findall ('src="(.*?)"', raw_html, re.DOTALL)
    
    return images
