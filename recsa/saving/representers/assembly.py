from types import MappingProxyType

import yaml

from recsa import Assembly

__all__ = ['add_assembly_representer', 'assembly_representer']


def assembly_representer(dumper, data: Assembly):
    assembly_dict = {
        'component_id_to_kind': dict(data.comp_id_to_kind),
        'bonds': [
            sorted([u, v]) for u, v 
            in sorted(data.bonds, key=lambda x: sorted(x))]
    }
    return dumper.represent_dict(assembly_dict)


def add_assembly_representer():
    yaml.add_representer(Assembly, assembly_representer)
