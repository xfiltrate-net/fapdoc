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

from libs.plugins import base
from jira import JIRA

class plugin(base):
    """ Jira export plugin """
    
    def init(self):
        
        self.__jira = JIRA(
            server=self.config["server"], 
            basic_auth=(
                self.config["username"], 
                self.config["password"]
        ))
        
        return True

    def test(self):
        """ Get all projects viewable by user. """
        projects = self.__jira.projects()
        
        out = ""
        for project in projects:
            out += "\t%s - %s\n" % (project.id, project.name)
        
        return out

    def importdata(self, audit):
        print ("[!] This plugin doesn't support importing")

        return False

    def export(self, finding, screenshots):
        """ Create new issue on jira """
        description = ""
        
        print("[+] Generating description...")
        for value in finding:
            # Filtering some things
            if not value in self.unwanted_data:
                if type(finding[value]) is list:
                    
                    # Add subtitle
                    description += "*%s* \n" % value
                    
                    # Add list content
                    for item in finding[value]:
                        description += "* %s\n" % item
                    
                    description += "\n\n"
                else:
                    # Add string content
                    description += "*%s*\n%s\n\n" % (value, finding[value])
        
        issue_dict = {
            'project'    : {'id': self.config["project_id"]},
            'assignee'   : {'name': self.config["assignee"]},
            'summary'    : finding["title"],
            'issuetype'  : {'name': 'Vulnerability'},
            'description': description,
        }
        
        try:
            # Create new issue on jira
            new_issue = self.__jira.create_issue(fields=issue_dict)
            print ("[+] New issue created: \"%s\"". % finding["title"])
            
        except Exception as E:
            print("[-] Issue creation failed \"%s\", Error:". % finding["title"])
            print(E)

            return False
    
        # upload finding's images
        for image in screenshots:
            print ("[-] uploading image %s" % image.replace("/tmp/",""))
            with open(image, 'rb') as f:
                self.__jira.add_attachment(issue=new_issue, attachment=f)
        
        return True
