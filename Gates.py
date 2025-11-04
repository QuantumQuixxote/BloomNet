from qiskit import QuantumCircuit
from qiskit.circuit.library import *

# Single-qubit gates
qc = QuantumCircuit(2)
qc.h(0)        # Hadamard
qc.rx(π/4, 0)  # Rotation
qc.s(1)        # Phase gate

# Two-qubit gates  
qc.cx(0, 1)    # CNOT
qc.cz(0, 1)    # Controlled-Z

# Advanced gates
qc.append(QFT(3), [0,1,2])  # Quantum Fourier Transform