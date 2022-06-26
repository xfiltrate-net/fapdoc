#!/usr/bin/env python3
#
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

from libs import pwndoc, console, utils, plugins

import sys
import argparse
import configparser

if __name__ == "__main__":
    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument('--list',   '-l', help="List available pwndoc's audits", required=False, dest='list_audits', action='store_true')
    parser.add_argument('--conf',   '-c', type=str,  help="specify configuration file", required=False)
    parser.add_argument('--audit',  '-a', type=str,  help="select an audit / list findings", required=False)
    parser.add_argument('--finding','-f', type=str,  help="print a finding", required=False)
    parser.add_argument('--test',   '-t', type=str,  help="test a plugin", required=False)
    parser.add_argument('--export', '-e', type=str,  help="export findings values: jira, csv", required=False)
    parser.add_argument('--import', '-i', type=str,  help="import findings to pwndoc from: csv, burpsuite", dest='import_data', required=False)
    parser.add_argument('file',           type=str,  help="replace input/output file from config", nargs='?', default="")
    args = parser.parse_args()
    
    # Check configuration file
    if args.conf:
        config_file = args.conf
    else:
        config_file = "config.ini"

    # Parse configuration file
    print("[-] Loading config...")
    try:
        config = configparser.ConfigParser()
        config.read(config_file)
        print ("[+] config ok.")
    except:
        print ("[!] Invalid configuration file.")
        sys.exit(0)
    
    # Check mongodb connection
    print("[-] Connecting to mongodb...")
    pdoc = pwndoc.pwndoc()
        
    if pdoc.db is None:
        print ("[!] Error connecting pwndoc's database")
        sys.exit(0)
    else:
        print("[+] Success")
        
    # replace input/output file in config
    if not args.file == "":
        if args.import_data:
            config[args.import_data]["import_path"] = args.file

        if args.export:
            config[args.export]["output_path"] = args.file

    # list audits
    if args.list_audits:
        print("[-] Available audits:")
        console.list_audits(pdoc)
    
    # list findings
    if args.audit:
        print("[-] Selected audit: %s" % console.audit_name(pdoc, args.audit))
        if not args.finding and not args.export and not args.import_data:
            console.list_findings(pdoc, args.audit)
            
    # Show finding
    if args.finding:
        if not args.audit:
            print("[!] Missing --audit parameter.")
            sys.exit(0)
            
        if not args.export and not args.import_data:
            console.show_finding(pdoc, args.audit, args.finding)
    
    # Test plugin
    if args.test:
        plugin = plugins.import_plugin(args.test, config)
        output = plugin.test()
            
        print("[-] output: %s" % output)

    # Export to plugin
    if args.export:
        plugin = plugins.import_plugin(args.export, pdoc, config)

        if not args.audit:
            print("[!] Missing --audit parameter.")
            sys.exit(0)
        
        if not args.finding:
            # export all findings if args.finding is not defined
            audit_findings = console.get_findings_ids(pdoc, args.audit)
        else:
            audit_findings = [args.finding]
        
        for fin in audit_findings:
            # pass screenshots and findings to the plugin and finally run exportation
            screenshots = console.dump_images(pdoc, args.audit, fin)
            finding     = utils.cleanhtml_dict(pdoc.get_finding(args.audit, fin))
                
            if plugin.export(finding, screenshots):
                print("[+] Done.")
            else:
                print("[!] Error.")

    # import from plugin
    if args.import_data:
        plugin = plugins.import_plugin(args.import_data, pdoc, config)

        if not args.audit:
            print("[!] Missing --audit parameter.")
            sys.exit(0)

        #pdoc.add_finding(args.audit)
        if plugin.importdata(args.audit):
            print("[+] Done.")
        else:
            print("[!] Error.")

    sys.exit(1)
