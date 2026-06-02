from bionetgen.main import BioNetGen
from bionetgen.network.networkparser import BNGNetworkParser
from bionetgen.core.exc import BNGModelError
from bionetgen.core.utils.logging import BNGLogger
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
logger = BNGLogger(app=None)


###### CORE OBJECT AND PARSING FRONT-END ######
class Network:
    """
    Main model object and entry point for model API. The goal of this
    object is to generate and read the BNGXML of a given BNGL model
    and give the user a pythonic interface to the resulting model object.

    Usage: bngmodel(bng_model)
           bngmodel(bng_model, BNGPATH)

    Attributes
    ----------
    active_blocks : list[str]
        a list of the blocks that have been parsed in the model
    bngnetworkparser : BNGNetworkParser
        BNGParser object that's responsible for .bngl file reading and model setup
    network_name : str
        name of the model, generally set from the given BNGL file

    Methods
    -------
    write_model(model_name)
        write the model in BNGL format to the path given
    setup_simulator(sim_type)
        sets up a simulator in bngmodel.simulator where the only current supported
        type of simulator is libRR for libRoadRunner simulator.
    """

    def __init__(self, bngl_model, BNGPATH=def_bng_path):
        self.active_blocks = []
        # We want blocks to be printed in the same order every time
        self.block_order = [
            "parameters",
            "species",
            "reactions",
            "groups",
        ]
        self.network_name = ""
        self.bngnetworkparser = BNGNetworkParser(bngl_model)
        self.bngnetworkparser.parse_network(self)
        for block in self.block_order:
            if block not in self.active_blocks:
                self.add_empty_block(block)
        # Check to see if there are no active blocks
        # If not, model is most likely not in BNGL format
        if not self.active_blocks:
            print(
                "WARNING: No active blocks. Please ensure model is in proper BNGL or BNG-XML format"
            )

    def __str__(self):
        """
        write the model to str
        """
        model_str = ""
        for block in self.block_order:
            # ensure we didn't get new items into a
            # previously inactive block, if we did
            # add them to the active blocks
            if hasattr(self, block):
                if len(getattr(self, block)) > 0:
                    if getattr(self, block).name not in self.active_blocks:
                        self.active_blocks.append(block)
                # if we removed items from a block and
                # it's now empty, we want to remove it
                # from the active blocks
                elif len(getattr(self, block)) == 0 and block in self.active_blocks:
                    self.active_blocks.remove(block)
            # print only the active blocks
            if block in self.active_blocks:
                if block != "actions" and len(getattr(self, block)) > 0:
                    model_str += str(getattr(self, block))
        return model_str

    def __repr__(self):
        return self.network_name

    def __iter__(self):
        active_ordered_blocks = [
            getattr(self, i) for i in self.block_order if i in self.active_blocks
        ]
        return active_ordered_blocks.__iter__()

    def add_block(self, block):
        block_adder = self._resolve_block_adder(block.name)
        block_adder(block)

    def add_empty_block(self, block_name):
        block_adder = self._resolve_block_adder(block_name)
        block_adder()

    def _resolve_block_adder(self, block_name):
        """
        Resolve supported block names to block adders.

        Block names are normalized by replacing spaces with underscores before
        dispatch so callers can use parser-style or attribute-style names.
        """
        normalized_name = block_name.replace(" ", "_")
        block_adders = {
            "parameters": self.add_parameters_block,
            "species": self.add_species_block,
            "reactions": self.add_reactions_block,
            "groups": self.add_groups_block,
        }
        if normalized_name not in block_adders:
            supported_names = ", ".join(block_adders)
            raise ValueError(
                f"Unsupported block name '{block_name}'. "
                f"Supported block names: {supported_names}"
            )
        return block_adders[normalized_name]

    def add_parameters_block(self, block=None):
        if block is not None:
            if not isinstance(block, NetworkParameterBlock):
                err_msg = "The given block is not a NetworkParameterBlock"
                logger.error(
                    err_msg, loc=f"{__file__} : Network.add_parameters_block()"
                )
                raise BNGModelError(self, message=err_msg)
            self.parameters = block
            if "parameters" not in self.active_blocks:
                self.active_blocks.append("parameters")
        else:
            self.parameters = NetworkParameterBlock()

    def add_species_block(self, block=None):
        if block is not None:
            if not isinstance(block, NetworkSpeciesBlock):
                err_msg = "The given block is not a NetworkSpeciesBlock"
                logger.error(err_msg, loc=f"{__file__} : Network.add_species_block()")
                raise BNGModelError(self, message=err_msg)
            self.species = block
            if "species" not in self.active_blocks:
                self.active_blocks.append("species")
        else:
            self.species = NetworkSpeciesBlock()

    def add_groups_block(self, block=None):
        if block is not None:
            if not isinstance(block, NetworkGroupBlock):
                err_msg = "The given block is not a NetworkGroupBlock"
                logger.error(err_msg, loc=f"{__file__} : Network.add_groups_block()")
                raise BNGModelError(self, message=err_msg)
            self.groups = block
            if "groups" not in self.active_blocks:
                self.active_blocks.append("groups")
        else:
            self.groups = NetworkGroupBlock()

    def add_reactions_block(self, block=None):
        if block is not None:
            if not isinstance(block, NetworkReactionBlock):
                err_msg = "The given block is not a NetworkReactionBlock"
                logger.error(err_msg, loc=f"{__file__} : Network.add_reactions_block()")
                raise BNGModelError(self, message=err_msg)
            self.reactions = block
            if "reactions" not in self.active_blocks:
                self.active_blocks.append("reactions")
        else:
            self.reactions = NetworkReactionBlock()

    def write_model(self, file_name):
        """
        write the model to file
        """
        with open(file_name, "w") as f:
            f.write("".join(str(getattr(self, block)) for block in self.active_blocks))
