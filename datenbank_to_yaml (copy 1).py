#!/usr/bin/env python3
import yaml
import sys
import xml.etree.ElementTree as ET

XML_NODE_CONTENT = 'inhalt'
ATTR_COMMENT = '' #'# Attribute'

yaml_dict = {}

if len(sys.argv) != 2:
    sys.stderr.write("Usage: {0} <file>.xml".format(sys.argv[0]))

def parse_entry(node):
    nodeattrs = node.attrib
    content = node.text.strip() if node.text else ''
    return nodeattrs, content

def yamlout(node, parent):  
    children = list(node)
    input(children)
    nodeattrs, content = parse_entry(node)
    if content:
        if not (nodeattrs or children):
            # Write as just a name value, nothing else nested
            parent[node.tag] = content or ''
            return
        else:
            nodeattrs[XML_NODE_CONTENT] = node.text
    if parent.get(node.tag):
        parent[node.tag].append({})
    else: 
        parent[node.tag] = [{}]
    parent = parent[node.tag][-1]
    for n,v in nodeattrs.items():
        parent[n] = v or ''
    # Write nested nodes
    for child in children:
        yamlout(child, parent)

with open(sys.argv[1]) as xmlf:
    tree = ET.parse(xmlf)

yamlout(tree.getroot(), yaml_dict)
yaml_dict = yaml_dict["Datenbank"][0]
for key in yaml_dict.keys():
    print(f"{key}:{len(yaml_dict[key])}")
    all_keys = []
    for elem in yaml_dict[key]:
        all_keys = set(list(all_keys) + list(elem.keys()))
    print(" "*5 + f"{list(all_keys)}")

for talent in yaml_dict["Talent"]:
    any_fertigkeit_of_talent = talent["fertigkeiten"].split(",")[0]
    if talent["fertigkeiten"]:
        for fertigkeit in yaml_dict["Übernatürliche-Fertigkeit"]:
            if fertigkeit["name"] == any_fertigkeit_of_talent:
                for einstellung in yaml_dict["Einstellung"]:
                    if einstellung["name"] == "Fertigkeiten: Typen übernatürlich":
                        talent["typ"] = einstellung["inhalt"].split(",")[int(fertigkeit["printclass"])]
                        break
                break
    #else:
    #    talent["Typ"] = yaml_dict["Einstellung"]["Fertigkeiten: Typen profan"][int(talent["fertigkeiten"].split(",")[0]["printclass"])]


with open(sys.argv[1]+".yml", 'w+',encoding="utf-8") as file:
    documents = yaml.safe_dump(yaml_dict, file,allow_unicode=True)