from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit import transpile

n = 3
qc = QuantumCircuit(n, n)

# --- Oracle marking |101> (q2 q1 q0 interpretation = [2,1,0]) ---
oracle = QuantumCircuit(n, name="Oracle")
# Flip the qubits that should be 0 (q1) so that the marked state maps to |111>
oracle.x(1)
# Implement multi-controlled Z using H-CCX-H on the last qubit
oracle.h(2)
oracle.ccx(0, 1, 2)
oracle.h(2)
# Undo the X
oracle.x(1)
oracle_gate = oracle.to_gate()

# --- Diffuser (Grover diffusion) ---
def diffuser(num):
    d = QuantumCircuit(num, name="Diffuser")
    d.h(range(num))
    d.x(range(num))
    d.h(num - 1)
    d.mcx(list(range(num - 1)), num - 1)
    d.h(num - 1)
    d.x(range(num))
    d.h(range(num))
    return d.to_gate()

# --- Grover iteration ---
qc.h(range(n))
qc.append(oracle_gate, range(n))
qc.append(diffuser(n), range(n))

# Measure
qc.measure(range(n), range(n))

# Transpile and run on Aer
backend = AerSimulator()
tqc = transpile(qc, backend=backend, optimization_level=3)
result = backend.run(tqc, shots=2048).result()
print(result.get_counts())
