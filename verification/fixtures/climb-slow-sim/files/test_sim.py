from sim.presets import PRESETS
from sim.world import World


def test_cars_stay_on_the_road() -> None:
    world = World(PRESETS["ring"], seed=1)
    for _ in range(300):
        world.step()
    assert all(0 <= x < PRESETS["ring"].road_length for _, x in world.frame())


def test_cars_move() -> None:
    world = World(PRESETS["grid"], seed=1)
    start = [x for _, x in world.frame()]
    for _ in range(90):
        world.step()
    assert [x for _, x in world.frame()] != start


def test_every_car_merges_out_of_the_ending_lane() -> None:
    world = World(PRESETS["highway_merge"], seed=1)
    for _ in range(30 * 180):
        world.step()
    assert all(lane == 0 for lane, _ in world.frame())
