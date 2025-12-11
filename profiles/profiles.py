from .writers.alice import agent_alice
from .editors.bob import agent_bob
from .marketers.carol import agent_carol


profiles = {
    "alice": agent_alice,
    "bob": agent_bob,
    "carol": agent_carol,
}