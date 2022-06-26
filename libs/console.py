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

from libs import utils

import html
import base64

def audit_name(pwndoc, audit_id):
    """ Get audit name by id """
    return pwndoc.get_audit(audit_id)["name"]

def list_audits(pwndoc):
    """ Print available pwndoc audits """
    
    for document in pwndoc.audits:
        print ("\t%s - %s" % (document["_id"], document["name"]))
        
    return True

def list_findings(pwndoc, audit_id):
    """ Print an audit's vulnerabilities """
    
    for finding in pwndoc.get_audit(audit_id)["findings"]:
        print ("\t%s - %s" % (finding["_id"], finding["title"]))
        
    return True

def get_findings_ids(pwndoc, audit_id):
    """ return list of findings ids by audit """
    ids = []
    
    for finding in pwndoc.get_audit(audit_id)["findings"]:
        ids.append(str(finding["_id"]))
        
    return ids

def show_finding(pwndoc, audit_id, finding_id):
    """ Show finding details """
    
    screenshots = []
    finding = pwndoc.get_finding(audit_id, finding_id)
    
    for key in finding:
        print("\t%s\t: %s" % (key, html.unescape(utils.cleanhtml(str(finding[key])))))
                
        # Get screenshots
        screenshots += utils.get_images(str(finding[key]))
                                                                      
    print("\tScreenshots\t: %s" % str(screenshots))
    
    return True

def dump_images(pwndoc, audit_id, finding_id):
    """ dump images to file on /tmp """
    
    screenshots = []
    out = []
    finding = pwndoc.get_finding(audit_id, finding_id)

    for key in finding:
        screenshots += utils.get_images(str(finding[key]))
                                                                      
    for image in screenshots:
        b64value = pwndoc.get_image(image)["value"]
        
        out.append("/tmp/screen-%s.png" % image)
        with open("/tmp/screen-%s.png" % image, "wb") as fh:
            fh.write(base64.decodebytes(b64value.split("base64,")[1].encode()))
    
    return out
