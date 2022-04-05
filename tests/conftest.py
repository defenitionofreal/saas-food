import pytest

pytest_plugins = (
    "tests.fixtures.api",
    "tests.fixtures.settings",
    "tests.fixtures.users",
)

#
# def pytest_addoption(parser):
#     parser.addoption(
#         "--runslow", action="store_true", default=False, help="run slow tests",
#     )
#
#
# def pytest_collection_modifyitems(config, items):
#     if config.getoption("-m") == "slow":
#         return
#     else:
#         skip = pytest.mark.skip(reason="need -m slow option to run")
#         for item in items:
#             if "slow" in item.keywords:
#                 item.add_marker(skip)
