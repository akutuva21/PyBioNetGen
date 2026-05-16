# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:11:35 2013

@author: proto
"""

import bionetgen
import multiprocessing


def setBngExecutable(executable):
    global bngExecutable
    bngExecutable = executable


def getBngExecutable():
    return bngExecutable


def _bngl2xml_worker(bnglFile):
    mdl = bionetgen.modelapi.bngmodel(bnglFile)
    xml_file = bnglFile.replace(".bngl", "_bngxml.xml")
    with open(xml_file, "w+") as f:
        mdl.bngparser.bngfile.write_xml(f, xml_type="bngxml", bngl_str=str(mdl))

def bngl2xml(bnglFile, timeout=60):
    p = multiprocessing.Process(target=_bngl2xml_worker, args=(bnglFile,))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        # cleanup partially written file if exists
        import os
        xml_file = bnglFile.replace(".bngl", "_bngxml.xml")
        if os.path.exists(xml_file):
            os.remove(xml_file)
        raise TimeoutError(f"bngl2xml timed out after {timeout} seconds")
    if p.exitcode != 0:
        raise RuntimeError(f"bngl2xml worker failed with exit code {p.exitcode}")
