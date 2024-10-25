import pytest

from recsa import Assembly, Component, assemblies_equal, perform_inter_exchange


def test_inter_exchange() -> None:
    COMPONENT_KINDS = {
        'M': Component('M', {'a', 'b'}),
        'L': Component('L', {'a'}),
        'X': Component('X', {'a'})}
    
    # X1(a)--(a)M1(a)--(a)X2
    
    MX2 = Assembly(
        COMPONENT_KINDS,
        {'M1': 'M', 'X1': 'X', 'X2': 'X'},
        [('X1.a', 'M1.a'), ('M1.b', 'X2.a')])
    # (a)L1(b)
    L = Assembly(COMPONENT_KINDS, {'L1': 'L'}, [])
    # expected product: MLX
    # (b)L1(a)--(a)M1(b)--(a)X2
    MLX = Assembly(
        COMPONENT_KINDS,
        {'M1': 'M', 'L1': 'L', 'X2': 'X'},
        [('L1.a', 'M1.a'), ('M1.b', 'X2.a')])
    MLX = MLX.rename_component_ids(
        {'M1': 'init_M1', 'L1': 'entering_L1', 'X2': 'init_X2'})
    X = Assembly(COMPONENT_KINDS, {'X1': 'X'}, [])
    X = X.rename_component_ids({'X1': 'init_X1'})
    
    product, leaving = perform_inter_exchange(
        MX2, L, 'M1.a', 'X1.a', 'L1.a')

    assert assemblies_equal(product, MLX)
    assert leaving is not None
    assert assemblies_equal(leaving, X)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
