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

import importlib
import traceback

def import_plugin(plugin_name, config):
    try:
        module = importlib.import_module("plugins.%s" % plugin_name)
        class_ = getattr(module, "plugin")
        plugin = class_(config[plugin_name])
            
        return plugin
                            
    except Exception as ex:
        print("".join(traceback.TracebackException.from_exception(ex).format()))


class base():
    """
    base plugin template
    """
    def __init__(self, config):
        
        self.unwanted_data = ["_id","title","identifier", "customFields", "status", "paragraphs"]
        self.config = config
        self.init()
