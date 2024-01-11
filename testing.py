import assigntools.LoLa.tp
from assigntools.LoLa.tp import prover9_prove, gen_syllogism

PROVER9_BIN = "/content/prover9/bin"
prover9_prove(PROVER9_BIN, "some y. not man(y)", ["all x.(man(x) -> walks(x))", "not walks(Alex)"])
