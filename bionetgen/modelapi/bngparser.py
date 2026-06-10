import xmltodict

from bionetgen.main import BioNetGen
from bionetgen.core.exc import BNGFileError, BNGParseError, BNGModelError
from tempfile import TemporaryFile

from .bngfile import BNGFile
from .xmlparsers import ParameterBlockXML, CompartmentBlockXML, ObservableBlockXML
from .xmlparsers import SpeciesBlockXML, MoleculeTypeBlockXML, FunctionBlockXML
from .xmlparsers import RuleBlockXML, EnergyPatternBlockXML, PopulationMapBlockXML
from .blocks import ActionBlock, ProtocolBlock
from bionetgen.core.utils.utils import ActionList

# This allows access to the CLIs config setup
app = BioNetGen()
app.setup()
conf = app.config["bionetgen"]
def_bng_path = conf["bngpath"]


def _normalize_action_text(action: str) -> str:
    """Strip BNGL comments and unquoted whitespace, keep quoted spans intact.

    `BNGFile.strip_actions` already removed unquoted spaces line-by-line,
    but quoted spans (e.g. ``param=>"-v -gml 1000000"`` in a simulate
    action) need to survive — so we run a quote-aware pass here.
    """
    text = _strip_comment_outside_quotes(action)
    text = _collapse_unquoted_whitespace(text)
    text = _strip_unquoted_backslashes(text)
    text = _collapse_unquoted_double_commas(text)
    return text.strip()


def _collapse_unquoted_double_commas(text: str) -> str:
    """Collapse repeated commas that appear outside string literals."""
    out = []
    in_single = False
    in_double = False
    escaped = False
    prev_was_comma = False
    for ch in text:
        if escaped:
            out.append(ch)
            escaped = False
            prev_was_comma = False
            continue
        if ch == "\\" and (in_single or in_double):
            out.append(ch)
            escaped = True
            prev_was_comma = False
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
            prev_was_comma = False
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
            prev_was_comma = False
            continue
        if ch == "," and not in_single and not in_double:
            if prev_was_comma:
                continue
            prev_was_comma = True
            out.append(ch)
            continue
        prev_was_comma = False
        out.append(ch)
    return "".join(out)


def _strip_unquoted_backslashes(text: str) -> str:
    """Drop ``\\`` characters that appear outside string literals."""
    return _filter_outside_quotes(text, lambda ch: ch != "\\")


def _filter_outside_quotes(text: str, keep) -> str:
    out = []
    in_single = False
    in_double = False
    escaped = False
    for ch in text:
        if escaped:
            out.append(ch)
            escaped = False
            continue
        if ch == "\\" and (in_single or in_double):
            out.append(ch)
            escaped = True
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
            continue
        if not in_single and not in_double and not keep(ch):
            continue
        out.append(ch)
    return "".join(out)


def _strip_comment_outside_quotes(text: str) -> str:
    out = []
    in_single = False
    in_double = False
    escaped = False
    for ch in text:
        if escaped:
            out.append(ch)
            escaped = False
            continue
        if ch == "\\" and (in_single or in_double):
            out.append(ch)
            escaped = True
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
            continue
        if ch == "#" and not in_single and not in_double:
            break
        out.append(ch)
    return "".join(out)


def _collapse_unquoted_whitespace(text: str) -> str:
    out = []
    in_single = False
    in_double = False
    escaped = False
    for ch in text:
        if escaped:
            out.append(ch)
            escaped = False
            continue
        if ch == "\\" and (in_single or in_double):
            out.append(ch)
            escaped = True
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
            continue
        if ch.isspace() and not in_single and not in_double:
            continue
        out.append(ch)
    return "".join(out)


class BNGParser:
    """
    Parser object that deals with reading in the BNGL file and
    setting up the model object

    Usage: BNGParser(bngl_path)
           BNGParser(bngl_path, BNGPATH)

    Attributes
    ----------
    bngfile : BNGFile
        BNGFile object that's responsible for .bngl file manipulations
    to_parse_actions : bool
        whether to parse the actions in a BNGL file or not
    alist : ActionList
        action list object that is used to deal with all things related to actions

    Methods
    -------
    parse_model(model_obj)
        parses the BNGL model at the given path and adds everything to a given model object
    parse_xml(xml_str)
        parses given xml string and adds everything to a given model object
    """

    def __init__(
        self,
        path,
        BNGPATH=def_bng_path,
        parse_actions=True,
        generate_network=False,
        suppress=True,
        verbose=False,
    ) -> None:
        self.to_parse_actions = parse_actions
        self.verbose = verbose
        self.bngfile = BNGFile(path, generate_network=generate_network, suppress=True)
        self.alist = ActionList()
        self.alist.define_parser()

    def parse_model(self, model_obj) -> None:
        """
        Will determine the parser route eventually and call the right
        parser
        """
        self._parse_model_bngpl(model_obj)
        if self.to_parse_actions:
            self.parse_actions(model_obj)

    def _parse_model_bngpl(self, model_obj) -> None:
        """
        Uses BNG2.pl to generate the BNG-XML file and passes that
        to parse_xml method to fill up the model object appropriately
        """
        # get file path
        model_file = self.bngfile.path

        # this route runs BNG2.pl on the bngl and parses
        # the XML instead
        if model_file.endswith(".bngl"):
            if self.verbose:
                print("Attempting to generate XML")
            with TemporaryFile("w+") as xml_file:
                try:
                    self.bngfile.generate_xml(xml_file)
                except BNGFileError as exc:
                    raise BNGModelError(
                        self.bngfile.path,
                        message=f"XML file couldn't be generated: {exc.message}",
                    ) from exc
                if self.verbose:
                    print("Parsing XML")
                xmlstr = xml_file.read()
                # < is not a valid XML character, we need to replace it
                xmlstr = xmlstr.replace('relation="<', 'relation="&lt;')
                self.parse_xml(xmlstr, model_obj)
                model_obj.reset_compilation_tags()
        elif model_file.endswith(".xml"):
            with open(model_file, "r") as f:
                xml_str = f.read()
                # < is not a valid XML character, we need to replace it
                xmlstr = xml_str.replace('relation="<', 'relation="&lt;')
                self.parse_xml(xml_str, model_obj)
            model_obj.reset_compilation_tags()
        else:
            raise NotImplementedError(
                "The extension of {} is not supported".format(model_file)
            )

    def parse_actions(self, model_obj):
        """
        Uses ActionList object to parse actions and turn them into
        action objects and fill up the ActionsBlock with them.

        Parses both top-level actions (BNGFile.parsed_actions) and
        protocol-block actions (BNGFile.parsed_protocol_actions) — both
        share the same action grammar; only the receiving block class
        differs.
        """
        ablock = self._parse_action_block(self.bngfile.parsed_actions, ActionBlock)
        if ablock is not None:
            model_obj.add_block(ablock)

        protocol_actions = getattr(self.bngfile, "parsed_protocol_actions", [])
        pblock = self._parse_action_block(protocol_actions, ProtocolBlock)
        if pblock is not None:
            model_obj.add_block(pblock)

    def _parse_action_block(self, action_lines, block_cls):
        if len(action_lines) == 0:
            return None
        ablock = block_cls()
        for action in action_lines:
            self._parse_action_line(action, ablock)
        if len(ablock) == 0:
            return None
        return ablock

    def _parse_action_line(self, action, ablock):
        # Strip comments and unquoted whitespace. The walker preserves
        # quoted spans so that e.g. ``param=>"-v -gml 1000000"`` keeps its
        # internal spaces (the older ``re.sub(r"\s", "", action)`` pass
        # would have collapsed them).
        action = _normalize_action_text(action)
        if len(action) == 0:
            return
        try:
            action_list = self.alist.action_parser.parseString(action)
        except Exception as e:
            raise BNGParseError(
                self.bngfile.path, f"Failed to parse action {action}"
            ) from e
        if action_list[-1] == ";":
            _ = action_list.pop(-1)
        atype = action_list.pop(0)
        # all actions have "()", remove
        action_list = action_list[1:-1]
        if len(action_list) == 0:
            ablock.add_action(atype, {})
            return
        if atype in self.alist.no_setter_syntax:
            if len(action_list) == 1:
                ablock.add_action(atype, {action_list[0]: None})
                return
            if len(action_list) == 3 and action_list[1] == ",":
                ablock.add_action(atype, {action_list[0]: None, action_list[2]: None})
                return
        elif atype in self.alist.square_braces:
            if action_list[0] == "[":
                action_list = action_list[1:-1]
            arg_dict = {}
            for arg in action_list:
                arg_dict[arg] = None
            ablock.add_action(atype, arg_dict)
            return
        elif atype in self.alist.normal_types:
            if action_list[0] == "{":
                action_list = action_list[1:-1]
            arg_dict = {}
            if len(action_list) == 0:
                ablock.add_action(atype, arg_dict)
                return
            while len(action_list) > 0:
                arg_name = action_list.pop(0)
                connector = action_list.pop(0)
                if connector != "=>":
                    raise BNGParseError(
                        self.bngfile.path, f"Action {action} is malformed"
                    )
                if arg_name in self.alist.irregular_args:
                    arg_type = self.alist.irregular_args[arg_name]
                    if arg_type == "dict":
                        start_curly = action_list.pop(0)
                        if start_curly != "{":
                            raise BNGParseError(
                                self.bngfile.path,
                                f"Action {action} is malformed",
                            )
                        value_str = "{"
                        end_curly = None
                        while end_curly is None:
                            dict_key = action_list.pop(0)
                            if dict_key == "}":
                                end_curly = dict_key
                            else:
                                if len(value_str) > 1:
                                    value_str += ","
                                dict_conn = action_list.pop(0)
                                dict_val = action_list.pop(0)
                                if dict_conn != "=>":
                                    raise BNGParseError(
                                        self.bngfile.path,
                                        f"Action {action} is malformed",
                                    )
                                value_str += dict_key + dict_conn + dict_val
                        value_str += "}"
                        arg_value = value_str
                    elif arg_type == "list":
                        start_curly = action_list.pop(0)
                        if start_curly != "[":
                            raise BNGParseError(
                                self.bngfile.path,
                                f"Action {action} is malformed",
                            )
                        value_str = "["
                        end_curly = None
                        while end_curly is None:
                            argument_element = action_list.pop(0)
                            if argument_element == "]":
                                end_curly = argument_element
                            else:
                                if len(value_str) > 1:
                                    value_str += ","
                                value_str += argument_element
                        value_str += "]"
                        arg_value = value_str
                else:
                    arg_value = action_list.pop(0)
                arg_dict[arg_name] = arg_value
            ablock.add_action(atype, arg_dict)
            return
        raise BNGParseError(
            self.bngfile.path, f"Action type {atype} is not recognized."
        )

    def parse_xml(self, xml_str, model_obj) -> None:
        """
        The main parsing method that parses the contents of a dictionary
        created from the BNG-XML file using `xmltodict` library. This method
        will use XML parser objects to generate each block to attach to the
        model object
        """
        xml_dict = xmltodict.parse(xml_str, disable_entities=True)
        # catch non-BNG XML files
        if "sbml" not in xml_dict:
            if "model" not in xml_dict["sbml"]:
                raise BNGParseError(
                    self.bngfile.path,
                    "Input model is invalid. Please ensure model is in proper BNGL or BNG-XML format",
                )
        model_obj.xml_dict = xml_dict
        first_key = list(xml_dict.keys())[0]
        xml_model = xml_dict[first_key]["model"]
        model_obj.model_name = xml_model["@id"]
        for listkey in xml_model.keys():
            if listkey == "ListOfParameters":
                param_list = xml_model[listkey]
                if param_list is not None:
                    params = param_list["Parameter"]
                    xml_parser = ParameterBlockXML(params)
                    model_obj.add_block(xml_parser.parsed_obj)
            elif listkey == "ListOfObservables":
                obs_list = xml_model[listkey]
                if obs_list is not None:
                    obs = obs_list["Observable"]
                    xml_parser = ObservableBlockXML(obs)
                    model_obj.add_block(xml_parser.parsed_obj)
            elif listkey == "ListOfCompartments":
                comp_list = xml_model[listkey]
                if comp_list is not None:
                    comps = comp_list["compartment"]
                    xml_parser = CompartmentBlockXML(comps)
                    model_obj.add_block(xml_parser.parsed_obj)
            elif listkey == "ListOfMoleculeTypes":
                mtypes_list = xml_model[listkey]
                if mtypes_list is not None:
                    mtypes = mtypes_list["MoleculeType"]
                    xml_parser = MoleculeTypeBlockXML(mtypes)
                    model_obj.add_block(xml_parser.parsed_obj)
            elif listkey == "ListOfSpecies":
                species_list = xml_model[listkey]
                if species_list is not None:
                    species = species_list["Species"]
                    xml_parser = SpeciesBlockXML(species)
                    model_obj.add_block(xml_parser.parsed_obj)
            elif listkey == "ListOfReactionRules":
                rrules_list = xml_model[listkey]
                if rrules_list is not None:
                    rrules = rrules_list["ReactionRule"]
                    xml_parser = RuleBlockXML(rrules)
                    model_obj.add_block(xml_parser.parsed_obj)
            elif listkey == "ListOfFunctions":
                # TODO: Optional expression parsing?
                # TODO: Add arguments correctly
                func_list = xml_model[listkey]
                if func_list is not None:
                    funcs = func_list["Function"]
                    xml_parser = FunctionBlockXML(funcs)
                    model_obj.add_block(xml_parser.parsed_obj)
            elif listkey == "ListOfEnergyPatterns":
                ep_list = xml_model[listkey]
                if ep_list is not None:
                    eps = ep_list["EnergyPattern"]
                    xml_parser = EnergyPatternBlockXML(eps)
                    model_obj.add_block(xml_parser.parsed_obj)
            elif listkey == "ListOfPopulationMaps":
                pm_list = xml_model[listkey]
                if pm_list is not None:
                    pms = pm_list["PopulationMap"]
                    xml_parser = PopulationMapBlockXML(pms)
                    model_obj.add_block(xml_parser.parsed_obj)
        # And that's the end of parsing
        if self.verbose:
            print("Parsing complete")
