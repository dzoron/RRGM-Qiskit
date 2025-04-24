from qiskit import QuantumCircuit, Aer, transpile
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
import matplotlib.pyplot as plt

# Step 1: Create a 4-qubit circuit with entanglement
qc = QuantumCircuit(4)
qc.h([0, 1, 2, 3])
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)

# Step 2: Add measurements
qc.measure_all()

# Step 3: Define spacedecay noise (10% on 1- and 2-qubit gates)
noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.1, 1), ['h'])
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.1, 2), ['cx'])

# Step 4: Run the noisy simulation
backend = Aer.get_backend('qasm_simulator')
transpiled = transpile(qc, backend)
result = backend.run(transpiled, noise_model=noise_model, shots=1024).result()
counts = result.get_counts()

# Step 5: Plot the measurement results (entanglement decay pattern)
plt.figure(figsize=(10, 5))
plt.bar(counts.keys(), counts.values())
plt.xticks(rotation=90)
plt.ylabel('Frequency')
plt.title('Spacedecay Simulation - Measurement Outcomes')
plt.tight_layout()
plt.show()
