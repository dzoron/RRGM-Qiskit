from qiskit import QuantumCircuit, Aer, transpile
from qiskit.providers.aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

# Create the black hole-like quantum circuit
qc = QuantumCircuit(5)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)
qc.cx(3, 4)
qc.measure_all()

# Build the noise model (Hawking-like emission)
noise_model = NoiseModel()

# One-qubit "decay" noise — boundary particle emission
one_qubit_error = depolarizing_error(0.02, 1)
noise_model.add_quantum_error(one_qubit_error, ['h'], [0])  # Only on the boundary gate

# Two-qubit entanglement decay — like event horizon turbulence
two_qubit_error = depolarizing_error(0.05, 2)
noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx'])

# Simulate
sim = AerSimulator(noise_model=noise_model)
t_qc = transpile(qc, sim)
result = sim.run(t_qc, shots=1024).result()

counts = result.get_counts()
print("🌀 Hawking Radiation Simulation Output:")
print(counts)

# Show histogram
plot_histogram(counts)
plt.show()