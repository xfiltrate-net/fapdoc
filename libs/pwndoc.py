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

from bson import ObjectId

import pymongo


class pwndoc:
    def __init__(self, url="mongodb://localhost:27017/"):
        self.dburl  = url
        self.db     = self.__init_pwndoc()
        self.audits = self.db.audits.find()

    def __init_pwndoc(self):
        """ Init connection to mongodb and return pwndoc database """
        try:
            myclient = pymongo.MongoClient(self.dburl)
            
            dblist = myclient.list_database_names()
            
            if not "pwndoc" in dblist:
                return False
            
            return myclient["pwndoc"]
        
        except E as Exception:
            print(E)
            return False 

    def get_audit(self, audit_id):
        """ Get a raw audit by id """
        objInstance = ObjectId(audit_id)
        
        return self.db.audits.find_one({
            "_id": objInstance
        })
        
    def get_image(self, image_id):
        """ Get a base64 image by id """
        objInstance = ObjectId(image_id)
        
        return self.db.images.find_one({
            "_id": objInstance
        })
    
    def get_finding(self, audit_id, finding_id):
        """ Get finding """
       
        for finding in self.get_audit(audit_id)["findings"]:
            if str(finding["_id"]) in finding_id:
                return finding

    def add_finding(self, audit_id, finding):
        """ add finding """
        objInstance = ObjectId(audit_id)

        finding["_id"] = ObjectId()

        self.db.audits.update_one(
            { "_id": objInstance },
            {
                "$push": {
                    "findings": finding
                }
            }
        )
