from collections.abc import Iterable, Mapping

from recsa import Assembly, ComponentStructure
from recsa.algorithms.hashing import calc_wl_hash_of_assembly
from recsa.algorithms.isomorphism import is_isomorphic


def find_isomorphic_assembly(
        target_assembly: Assembly,
        id_to_assembly: Mapping[str, Assembly],
        hash_to_ids: Mapping[str, Iterable[str]],
        component_structures: Mapping[str, ComponentStructure]
        ) -> str | None:
    # TODO: Reduce the number of calls to calc_wl_hash_of_assembly.
    # Maybe we can use the numbers of each component kind in the assembly.
    hash_ = calc_wl_hash_of_assembly(target_assembly, component_structures)
    if hash_ not in hash_to_ids:
        return None
    for candidate_id in hash_to_ids[hash_]:
        candidate = id_to_assembly[candidate_id]
        if is_isomorphic(
                target_assembly, candidate, component_structures):
            return candidate_id
    return None
