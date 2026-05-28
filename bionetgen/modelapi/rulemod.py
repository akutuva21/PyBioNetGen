class RuleMod:
    """
    Rule modifiers class for storage and printing.
    """

    def __init__(self, mod_type=None, mod_kwargs=None) -> None:
        # valid mod types
        self.valid_mod_names = [
            "DeleteMolecules",
            "MoveConnected",
            "TotalRate",
            "IncludeReactants",
            "ExcludeReactants",
            "IncludeProducts",
            "ExcludeProducts",
        ]
        self.type = mod_type
        self.kwargs = mod_kwargs if mod_kwargs is not None else {}
        self.mods = []

    def __str__(self) -> str:
        res = []
        if self.type is not None:
            if self.type in [
                "IncludeReactants",
                "ExcludeReactants",
                "IncludeProducts",
                "ExcludeProducts",
            ]:
                if "item_names" in self.kwargs:
                    res.append(f"{self.type}({','.join(self.kwargs['item_names'])})")
                else:
                    res.append(self.type)
            else:
                res.append(self.type)
        if len(self.mods) > 0:
            for m in self.mods:
                res.append(str(m))
        return ",".join(res)

    def __repr__(self) -> str:
        types = []
        if self.type is not None:
            types.append(self.type)
        if len(self.mods) > 0:
            for m in self.mods:
                if m.type is not None:
                    types.append(m.type)
        if len(types) > 0:
            return "Rule modifiers of type " + ",".join(types)
        return f"Rule modifier of type {self.type}"

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, val):
        if val in self.valid_mod_names or val is None:
            self._type = val
        else:
            print(f"Rule modifier type {val} is not a valid type")
