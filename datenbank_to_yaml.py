#!/usr/bin/env python3
import yaml
import sys
import xml.etree.ElementTree as ET

XML_NODE_TEXT = 'inhalt'
ATTR_COMMENT = '' #'# Attribute'

yaml_dict = {}

if len(sys.argv) != 2:
    sys.stderr.write("Usage: {0} <file>.xml".format(sys.argv[0]))

def count_all_types(yaml_dict):
    for key in yaml_dict.keys():
        print(f"{key}:{len(yaml_dict[key])}")
    all_keys = []
    for elem in yaml_dict[key]:
        all_keys = set(list(all_keys) + list(elem.keys()))
    print(" "*5 + f"{list(all_keys)}")

def add_type(yaml_dict):
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

def parse_entry(node):
    #if node.tag == "talent":
    #    pass
    #else:
    nodeattrs = node.attrib
    content = node.text.strip() if node.text else ''
    return nodeattrs, content

def get_child_dict(child_node):
    nodeattrs = child_node.attrib
    child_dict = {}
    child_dict[XML_NODE_TEXT] = child_node.text
    for n,v in nodeattrs.items():
        child_dict[n] = v or ''
    return child_dict

def yaml_out(node):
    yaml_dict = {}
    children = list(node)
    
    for child_node in children:
        if not yaml_dict.get(child_node.tag):
            yaml_dict[child_node.tag] = {}
        yaml_dict[child_node.tag].update({child_node.attrib.get("name") or child_node.text:get_child_dict(child_node)})
    return yaml_dict

with open(sys.argv[1]) as xmlf:
    tree = ET.parse(xmlf)

yaml_dict = yaml_out(tree.getroot())

with open(sys.argv[1]+".yml", 'w+',encoding="utf-8") as file:
    documents = yaml.safe_dump(yaml_dict, file,allow_unicode=True)