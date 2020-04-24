# TDF from the CDH Assumption

## Recycle One-Way Function with Encryption
* **OWFE**: An OWFE scheme consists of four probabilistic polynomial-time algorithms **K**, **f**, **E**, and **D** With the following syntax:
  * `K(1^\lambda)`: Takes the security parameter `1^lambda` and outputs a public parameter `pp` for a function `f` from `n` bits to `v` bits.
  * `f(pp,x)`: Takes a public parameter `pp` and a preimage `x \in {0,1}^n`, and outputs `y \in {0, 1}^v`.
  * `E(pp, y, (i,b);rho)`: Takes a public parameter `pp`, a value `y`, an index `i \in [n]`, a bit `b \in {0, 1}` and randomness `rho`, and outputs a ciphertext `ct` and a bit `e`.
  * `D(pp, x, ct)`: Takes a public parameter `pp`, a value `x` and a ciphertext `ct`, and deterministically outputs `e' \in {0,1} \cup {\perp}`.
