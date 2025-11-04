# BloomNet — Foundational Quantum Algorithms (Qiskit)

BloomNet is a hands-on collection of **foundational quantum computing algorithms** implemented in **Qiskit**. Each example is compact, well-commented, and designed to run locally on simulators (and easily swap to real backends).

## What’s inside

- **Deutsch–Jozsa** — detect constant vs balanced Boolean functions in one shot.
- **Bernstein–Vazirani** — recover a hidden bitstring with a single oracle query.
- **Simon’s Algorithm** — find the XOR mask for 2-to-1 functions (pre-Shor history).
- **Grover’s Search** — quadratic speedup for marked-item search.
- **Quantum Fourier Transform (QFT)** — key primitive for phase-based algorithms.
- **Quantum Phase Estimation (QPE)** — estimate eigenphases (gateway to Shor/Hamiltonian learning).
- **Amplitude Estimation (QAE, iterative)** — quadratic sample efficiency boost over classical MC.
- **Intros to VQE & QAOA** — near-term hybrid algorithms for chemistry & optimization.

Each folder/script includes:
- a **plain Python** implementation,
- **transpile-safe** execution on `AerSimulator`,
- short **takeaways** about what the circuit demonstrates.

---

## Requirements

- Python **3.10–3.12**
- Qiskit ≥ **1.0**, Aer ≥ **0.14**

```bash
python -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install "qiskit>=1.0" "qiskit-aer>=0.14" "qiskit-optimization>=0.6" \
            "qiskit-nature>=0.7"  # (only needed for VQE chemistry examples)
