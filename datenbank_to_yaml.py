#!/usr/bin/env python3
import yaml
import sys
import xml.etree.ElementTree as ET

yaml_dict = {}

if len(sys.argv) != 2:
    sys.stderr.write("Usage: {0} <file>.xml".format(sys.argv[0]))

XML_NODE_CONTENT = 'inhalt'
ATTR_COMMENT = '' #'# Attribute'
def yamlout(node, parent):
    nodeattrs = node.attrib
    children = list(node)
    content = node.text.strip() if node.text else ''
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
    print(yaml_dict)
    with open(sys.argv[1]+".yml", 'w+',encoding="utf-8") as file:
        documents = yaml.safe_dump(yaml_dict, file,allow_unicode=True)