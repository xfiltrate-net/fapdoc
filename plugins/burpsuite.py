#!/usr/bin/env python3
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
from xml.etree import ElementTree

class plugin(base):
    def init(self):
        """ burpsuite import plugin """
        return True

    def test(self):
        """ test plugin """
        return "ok"

    def importdata(self, audit):
        """ import data from burpsite xml export """
        mytree = ElementTree.parse(self.config["import_path"])
        myroot = mytree.getroot()

        findings = {}

        for child in myroot.findall('issue'):
            vuln_name = child.find("name").text

            description = ""
            observation = ""
            remediation = ""
            references  = ""
            scope       = ""

            try:
                references = child.find("references").text
            except:
                references = ""
            try:
                scope = "%s%s" % (child.find("host").text, child.find("location").text)
            except:
                scope = "%s%s" % (child.find("host").text, child.find("path").text)

            try:
                description = child.find("issueBackground").text
                observation = child.find("issueDetail").text
            except:
                description = child.find("issueDetail").text

            try:
                remediation = child.find("remediationDetail").text
            except:
                pass

            if not vuln_name in findings:
                findings[vuln_name] = {
                    "title"       : vuln_name,
                    "scope"       : scope,
                    "description" : description,
                    "observation" : observation,
                    "remediation" : remediation,
                    "references"  : references,
                }
            else:
                findings[vuln_name]["scope"] = ("%s\n%s%s" % (findings[vuln_name]["scope"], child.find("host").text, child.find("location").text))

        for finding in findings:
            self.pwndoc.add_finding(audit, findings[finding])

        return True

    def export(self, finding):
        print("[!] This plugin doesn't support exporting.")
        return False
