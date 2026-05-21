import re, os
from bionetgen.main import BioNetGen
from bionetgen.network.blocks import (
    NetworkGroupBlock,
    NetworkParameterBlock,
    NetworkReactionBlock,
    NetworkSpeciesBlock,
    NetworkCompartmentBlock,
    NetworkFunctionBlock,
    NetworkEnergyPatternBlock,
    NetworkPopulationMapBlock,
)

# This allows access to the CLIs config setup
app = BioNetGen()
app.setup()
conf = app.config["bionetgen"]
def_bng_path = conf["bngpath"]


class BNGNetworkParser:
    """
    Parser object that deals with reading in the BNGL file and
    setting up the model object

    Usage: BNGParser(bngl_path)
           BNGParser(bngl_path, BNGPATH)

    Attributes
    ----------
    bngfile : BNGFile
        BNGFile object that's responsible for .bngl file manipulations

    Methods
    -------
    parse_model(model_file)
        parses the BNGL model at the given path and adds everything to a given model object
    parse_xml(xml_str)
        parses given xml string and adds everything to a given model object
    """

    def __init__(self, path) -> None:
        self.path = path
        self.network_name = os.path.splitext(os.path.basename(path))[0]
        with open(self.path, "r") as f:
            self.network_lines = f.readlines()

    def parse_network(self, network_obj) -> None:
        """
        Will determine the parser route eventually and call the right
        parser
        """
        # network name
        network_obj.network_name = self.network_name

        pblock, sblock, rblock, gblock = self._find_blocks()

        if pblock[0] > 0 and pblock[1] > 0:
            self._parse_parameters(network_obj, pblock)
        if sblock[0] > 0 and sblock[1] > 0:
            self._parse_species(network_obj, sblock)
        if rblock[0] > 0 and rblock[1] > 0:
            self._parse_reactions(network_obj, rblock)
        if gblock[0] > 0 and gblock[1] > 0:
            self._parse_groups(network_obj, gblock)

    def _find_blocks(self):
        pblock = [-1, -1]
        sblock = [-1, -1]
        rblock = [-1, -1]
        gblock = [-1, -1]
        for iline, line in enumerate(self.network_lines):
            if line.strip() == "begin parameters":
                pblock[0] = iline
            if line.strip() == "end parameters":
                pblock[1] = iline
            if line.strip() == "begin species":
                sblock[0] = iline
            if line.strip() == "end species":
                sblock[1] = iline
            if line.strip() == "begin reactions":
                rblock[0] = iline
            if line.strip() == "end reactions":
                rblock[1] = iline
            if line.strip() == "begin groups":
                gblock[0] = iline
            if line.strip() == "end groups":
                gblock[1] = iline
        return pblock, sblock, rblock, gblock

    def _parse_parameters(self, network_obj, pblock):
        param_block = NetworkParameterBlock()
        for iline in range(pblock[0] + 1, pblock[1]):
            m = re.match("([^#]*)(#.*)?", self.network_lines[iline])
            if m.group(1).strip() != "":
                splt = m.group(1).split()
                pid = splt[0]
                pname = splt[1]
                pvalue = splt[2]
                comment = m.group(2)
                param_block.add_parameter(pid, pname, pvalue, comment=comment)
        network_obj.add_block(param_block)

    def _parse_species(self, network_obj, sblock):
        spec_block = NetworkSpeciesBlock()
        for iline in range(sblock[0] + 1, sblock[1]):
            m = re.match("([^#]*)(#.*)?", self.network_lines[iline])
            if m.group(1).strip() != "":
                splt = m.group(1).split()
                sid = splt[0]
                name = splt[1]
                try:
                    count = splt[2]
                except:
                    import IPython

                    IPython.embed()
                spec_block.add_species(sid, name, count)
        network_obj.add_block(spec_block)

    def _parse_reactions(self, network_obj, rblock):
        rxns_block = NetworkReactionBlock()
        for iline in range(rblock[0] + 1, rblock[1]):
            m = re.match("([^#]*)(#.*)?", self.network_lines[iline])
            if m.group(1).strip() != "":
                splt = m.group(1).split()
                rid = splt[0]
                reactants = splt[1].split(",")
                products = splt[2].split(",")
                rate_constant = splt[3]
                comment = m.group(2)
                rxns_block.add_reaction(
                    rid,
                    reactants=reactants,
                    products=products,
                    rate_constant=rate_constant,
                    comment=comment,
                )
        network_obj.add_block(rxns_block)

    def _parse_groups(self, network_obj, gblock):
        grps_block = NetworkGroupBlock()
        for iline in range(gblock[0] + 1, gblock[1]):
            m = re.match("([^#]*)(#.*)?", self.network_lines[iline])
            if m.group(1).strip() != "":
                splt = m.group(1).split()
                rid = splt[0]
                name = splt[1]
                members = splt[2].split(",")
                comment = m.group(2)
                grps_block.add_group(rid, name, members, comment=comment)
        network_obj.add_block(grps_block)
