from qiskit import QuantumCircuit, Aer, transpile
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
import matplotlib.pyplot as plt

# Step 1: Create a 4-qubit entangled circuit
qc = QuantumCircuit(4)
qc.h([0, 1, 2, 3])
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.measure_all()

# Step 2: Define Spacedecay noise model (protecting Qubit 0 = Observer)
noise_model = NoiseModel()

# Apply 1-qubit gate noise to qubits 1, 2, 3 (skip 0)
for q in [1, 2, 3]:
    noise_model.add_quantum_error(depolarizing_error(0.1, 1), ['h'], [q])

# Apply 2-qubit gate noise to specific pairs (not involving Qubit 0)
noise_model.add_quantum_error(depolarizing_error(0.1, 2), ['cx'], [1, 2])
noise_model.add_quantum_error(depolarizing_error(0.1, 2), ['cx'], [2, 3])

# Step 3: Simulate using qasm_simulator
backend = Aer.get_backend('qasm_simulator')
transpiled = transpile(qc, backend)
result = backend.run(transpiled, noise_model=noise_model, shots=1024).result()
counts = result.get_counts()

# Step 4: Plot the measurement results
plt.figure(figsize=(10, 5))
plt.bar(counts.keys(), counts.values())
plt.xticks(rotation=90)
plt.ylabel('Frequency')
plt.title('Spacedecay with Observer Injection (Qubit 0 Protected)')
plt.tight_layout()
plt.show()