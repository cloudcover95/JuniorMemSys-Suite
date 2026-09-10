# MemSys vs Module-SIS (a16z Jolt, Sep 2026)

Jolt moved its *proof system* from elliptic curves to **Module-SIS** lattices (Akita polynomial commitment). That is a zkVM prover, not a memory palace.

| Layer | Jolt lattice | JuniorMemSys today |
|-------|----------------|--------------------|
| Object | RISC-V execution proof | bit-drift / TDA notes |
| Hardness | Module-SIS | none (hash + optional sign) |
| Alphabet | short integers | ternary `{-1,0,1}` in JuniorLLM FieldCore |
| Size | &lt;100 KB proofs | dict slots / graphs |
| Claim | 128-bit PQ SNARK | **we do not claim this** |

Overlap that *is* real: SIS “short” solutions are often in `{-1,0,1}`. BitNet weights live in that set. So a palace entry can carry a **toy SIS commitment** `c = A z (mod q)` where `z` is the ternary embedding. That is an integrity tag, not a Jolt proof and not Dilithium.

Code: `junior_memsys_suite/lattice/msis_commit.py`
