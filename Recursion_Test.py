from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Quantum circuit with 5 qubits (1 observer + 2 entangled pairs)
qc = QuantumCircuit(5, 5)

# Entangle qubits 1 & 2 (pair 1)
qc.h(1)
qc.cx(1, 2)

# Entangle qubits 3 & 4 (pair 2)
qc.h(3)
qc.cx(3, 4)

# Observer: Qubit 0 - apply H randomly to simulate conscious "pulse"
qc.h(0)
qc.barrier()

# Add decoherence simulation (noise model)
noise_model = NoiseModel()

# Entanglement pairs: more noise (simulate decay zones)
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.15, 1), ['h'])
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.25, 2), ['cx'])

# Observer: less noise (observer acts as stabilizer)
noise_model.add_quantum_error(depolarizing_error(0.01, 1), ['h'], [0])

# Measure all qubits
qc.measure([0, 1, 2, 3, 4], [0, 1, 2, 3, 4])

# Run simulation
backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=backend, noise_model=noise_model, shots=2048)
result = job.result()
counts = result.get_counts()

# Display results
print("Meta-Recursion Simulation Results:")
print(counts)
plot_histogram(counts)
plt.show()