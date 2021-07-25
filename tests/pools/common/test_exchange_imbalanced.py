import pytest

pytestmark = pytest.mark.usefixtures("add_initial_liquidity", "approve_bob")


@pytest.mark.parametrize("sending,receiving", [(0, 1), (1, 0)])
def test_min_dy(bob, swap, plain_coins, sending, receiving, decimals):

    amounts = [10 ** i for i in decimals]
    scaler = amounts.copy()  # used to scale token amounts when decimals are different

    amounts[sending] = 0
    amounts[receiving] = amounts[receiving] * 10 ** 8

    for i, amount in enumerate(amounts):
        plain_coins[i]._mint_for_testing(bob, amount, {"from": bob})

    swap.add_liquidity(amounts, 0, {"from": bob})

    plain_coins[sending]._mint_for_testing(bob, scaler[sending], {"from": bob})

    # we need to scale these appropriately for tokens with different decimal values
    min_dy_sending = swap.get_dy(sending, receiving, scaler[sending]) / scaler[receiving]
    min_dy_receiving = swap.get_dy(receiving, sending, scaler[receiving]) / scaler[sending]

    assert min_dy_sending > min_dy_receiving
