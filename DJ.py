# deutsch_jozsa.py
# Qiskit >= 1.0

from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit import transpile

def build_oracle_linear(n: int, a_bits: str, b: int) -> QuantumCircuit:
    """
    Build an oracle U_f for f(x) = a·x ⊕ b over n input bits.
    a_bits: length-n bitstring, MSB is qubit n-1 (left) down to LSB qubit 0 (right).
    b: 0 or 1.
    The circuit acts on n input qubits + 1 ancilla (last qubit).
    """
    assert len(a_bits) == n and set(a_bits) <= {"0", "1"}
    assert b in (0, 1)

    oracle = QuantumCircuit(n + 1, name="U_f")

    # Apply X to ancilla if b == 1 (adds constant term)
    if b == 1:
        oracle.x(n)

    # For each a_i == 1, apply CNOT from input qubit i to ancilla
    # Map a_bits[i] to input qubit i (0 is LSB/rightmost in counts)
    for i, bit in enumerate(reversed(a_bits)):  # reversed so leftmost of string -> highest qubit index
        q = i  # input qubit index 0..n-1
        if bit == "1":
            oracle.cx(q, n)

    return oracle

def deutsch_jozsa_circuit(n: int, a_bits: str, b: int) -> QuantumCircuit:
    """
    Full DJ circuit for n input qubits using linear oracle parameters (a_bits, b).
    Returns a circuit that measures only the n input qubits.
    For ideal simulation:
      - If a_bits == "0"*n (constant), result will be 0...0.
      - Otherwise (balanced), result will be the bitstring a_bits.
    """
    qc = QuantumCircuit(n + 1, n, name="Deutsch-Jozsa")

    # 1) Prepare |0...0>_n ⊗ |1>
    qc.x(n)

    # 2) Hadamards: inputs to superposition, ancilla to |-> 
    qc.h(range(n + 1))

    # 3) Oracle U_f
    oracle = build_oracle_linear(n, a_bits=a_bits, b=b)
    qc.append(oracle.to_gate(), range(n + 1))

    # 4) Hadamards on inputs again
    qc.h(range(n))

    # 5) Measure inputs (ancilla can be ignored)
    qc.measure(range(n), range(n))
    return qc

def run(qc: QuantumCircuit, shots: int = 1024):
    backend = AerSimulator()
    tqc = transpile(qc, backend=backend, optimization_level=3)
    result = backend.run(tqc, shots=shots).result()
    return result.get_counts()

if __name__ == "__main__":
    n = 5

    # --- CONSTANT example: a = 00000, b can be 0 or 1
    const_circ = deutsch_jozsa_circuit(n, a_bits="0"*n, b=1)
    const_counts = run(const_circ)
    print("CONSTANT oracle counts:", const_counts)
    # Expect {'00000': shots}

    # --- BALANCED example: choose any nonzero a (e.g., 10110)
    balanced_a = "10110"
    bal_circ = deutsch_jozsa_circuit(n, a_bits=balanced_a, b=0)
    bal_counts = run(bal_circ)
    print("BALANCED oracle counts:", bal_counts)
    # Expect {balanced_a: shots} (bit order matches the printed bitstring)
