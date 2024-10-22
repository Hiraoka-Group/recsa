from collections.abc import Iterable

from recsa import Assembly, load_bondsets, load_structure_data, save_assemblies

from .single_assembly import convert_bondset_to_assembly

__all__ = ['convert_bondsets_to_assemblies_from_file']

def convert_bondsets_to_assemblies_from_file(
        bond_list_path: str, template_path: str) -> Iterable[Assembly]:
    assems_by_bond_list = load_bondsets(bond_list_path)
    args = load_structure_data(template_path)

    for bondset in assems_by_bond_list:
        yield convert_bondset_to_assembly(
            set(bondset), args.components, args.bond_id_to_bindsites)
