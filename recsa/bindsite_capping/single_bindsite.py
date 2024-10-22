from typing import Literal, overload

from recsa import Assembly

__all__ = ['cap_single_bindsite']


@overload
def cap_single_bindsite(
        assembly: Assembly, target_bindsite: str,
        cap_id: str, cap_component_kind: str, cap_bindsite: str,
        copy: Literal[True] = True
        ) -> Assembly: ...
@overload
def cap_single_bindsite(
        assembly: Assembly, target_bindsite: str,
        cap_id: str, cap_component_kind: str, cap_bindsite: str,
        copy: Literal[False]
        ) -> None: ...
def cap_single_bindsite(
        assembly: Assembly, target_bindsite: str,
        cap_id: str, cap_component_kind: str, cap_bindsite: str, 
        copy: bool = True
        ) -> Assembly | None:
    """Add a leaving ligand (cap) to the assembly."""
    if copy:
        assembly = assembly.deepcopy()

    assembly.add_component(cap_id, cap_component_kind)
    assembly.add_bond(Assembly.rel_to_abs(cap_id, cap_bindsite), target_bindsite)

    return assembly
