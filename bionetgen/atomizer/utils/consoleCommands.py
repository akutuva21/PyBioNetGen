# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:11:35 2013

@author: proto
"""

import bionetgen


def setBngExecutable(executable):
    global bngExecutable
    bngExecutable = executable


def getBngExecutable():
    return bngExecutable


def bngl2xml(bnglFile, timeout=60):
    import subprocess
    import sys
    import os
    import tempfile

    script = """import bionetgen
import sys

bnglFile = sys.argv[1]
xml_file = bnglFile.replace('.bngl', '_bngxml.xml')
try:
    mdl = bionetgen.modelapi.bngmodel(bnglFile)
    with open(xml_file, 'w+') as f:
        mdl.bngparser.bngfile.write_xml(f, xml_type='bngxml', bngl_str=str(mdl))
except Exception as e:
    sys.exit(1)
"""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(script)
        script_path = f.name
    try:
        xml_file = bnglFile.replace(".bngl", "_bngxml.xml")

        proc = subprocess.Popen([sys.executable, script_path, bnglFile])
        try:
            proc.communicate(timeout=timeout)
            if proc.returncode != 0:
                if os.path.exists(xml_file):
                    os.remove(xml_file)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
            if os.path.exists(xml_file):
                os.remove(xml_file)
    except subprocess.TimeoutExpired:
        if os.path.exists(xml_file):
            os.remove(xml_file)
