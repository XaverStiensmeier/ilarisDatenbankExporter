#!/usr/bin/env python3
import yaml
import sys
import xml.etree.ElementTree as ET

XML_NODE_TEXT = 'inhalt'
ATTR_COMMENT = '' #'# Attribute'

yaml_dict = {}

if len(sys.argv) != 2:
    sys.stderr.write("Usage: {0} <file>.xml".format(sys.argv[0]))

def count_all_data_types(yaml_dict):
    for key in yaml_dict.keys():
        print(f"{key}:{len(yaml_dict[key])}")
    all_keys = []
    for elem in yaml_dict[key]:
        all_keys = set(list(all_keys) + list(elem.keys()))
    print(" "*5 + f"{list(all_keys)}")

def add_type(yaml_dict):
    for talent_key, talent in yaml_dict["Talent"].items():
        talent_fertigkeiten = talent["fertigkeiten"].split(",")
        talent_fertigkeiten = [f.strip() for f in talent_fertigkeiten]
        fertigkeit_typen = set()  # NOTE: Liste ohne Doppelungen
        for fertigkeit in talent_fertigkeiten:
            fertigkeit_dict = yaml_dict["Übernatürliche-Fertigkeit"].get(fertigkeit)
            typ_key = "Fertigkeiten: Typen übernatürlich"
            if not fertigkeit_dict:
                fertigkeit_dict = yaml_dict["Fertigkeit"].get(fertigkeit)
                typ_key = "Fertigkeiten: Typen profan"
            if not fertigkeit_dict:
                print(f"Fertigkeit '{fertigkeit}' von Talent '{talent_key}' nicht gefunden")
                continue
            fertigkeits_typen = yaml_dict["Einstellung"][typ_key]["inhalt"].split(",")
            fertigkeits_typen_list = [ f.strip() for f in fertigkeits_typen ]
            fertigkeit_typ = fertigkeits_typen_list[int(fertigkeit_dict["printclass"])]
            fertigkeit_typen.add(fertigkeit_typ)
        yaml_dict["Talent"][talent_key]["typ"] = list(fertigkeit_typen)

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

add_type(yaml_dict)

with open(sys.argv[1]+".yml", 'w+',encoding="utf-8") as file:
    documents = yaml.safe_dump(yaml_dict, file,allow_unicode=True)
