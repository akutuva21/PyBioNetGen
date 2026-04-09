## 2026-04-09 - Optimization of Molecule.addComponent
**Learning:** Avoid generating list comprehensions inside loops for membership tests, especially if there's an existing method that searches for the item and returns it or `None`.
**Action:** Replaced `if component.name not in [x.name for x in self.components]:` with a direct call to `getComponent(component.name)`.
