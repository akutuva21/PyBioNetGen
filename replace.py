import re

with open('bionetgen/atomizer/bngModel.py', 'r') as f:
    text = f.read()

# Replace the specific lines
old_code = """                        if molec.name in self.observables:
                            obs = self.observables.pop(molec.name)
                            self.obs_map[obs.get_obs_name()] = molec.Id + "()"
                        elif molec.Id in self.observables:
                            obs = self.observables.pop(molec.Id)
                            self.obs_map[obs.get_obs_name()] = molec.Id + "()"
                        # for spec in self.species:
                        #     sobj = self.species[spec]
                        #     # if molec.name == sobj.Id or molec
                        if molec.name in self.species:
                            spec = self.species.pop(molec.name)
                        elif molec.Id in self.species:
                            spec = self.species.pop(molec.Id)"""

new_code = """                        if getattr(molec, "name", None) in self.observables:
                            obs = self.observables.pop(molec.name)
                            self.obs_map[obs.get_obs_name()] = molec.Id + "()"
                        elif molec.Id in self.observables:
                            obs = self.observables.pop(molec.Id)
                            self.obs_map[obs.get_obs_name()] = molec.Id + "()"
                        # for spec in self.species:
                        #     sobj = self.species[spec]
                        #     # if molec.name == sobj.Id or molec
                        if getattr(molec, "name", None) in self.species:
                            spec = self.species.pop(molec.name)
                        elif molec.Id in self.species:
                            spec = self.species.pop(molec.Id)"""

new_text = text.replace(old_code, new_code)

with open('bionetgen/atomizer/bngModel.py', 'w') as f:
    f.write(new_text)
