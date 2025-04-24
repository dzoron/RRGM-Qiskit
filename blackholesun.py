from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create the quantum circuit
qc = QuantumCircuit(5, 5)

# Core entanglement zone (simulate black hole)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

# Outer ring (simulate higher spacedecay)
qc.h(3)
qc.cx(3, 4)

# Measure
qc.measure(range(5), range(5))

# Define noise model
noise_model = NoiseModel()

# Core (lower noise to simulate time slowdown / gravitational stability)
core_1q_error = depolarizing_error(0.01, 1)  # Very low decay
core_2q_error = depolarizing_error(0.02, 2)

# Outer ring (higher decay simulates spacedecay)
outer_1q_error = depolarizing_error(0.15, 1)
outer_2q_error = depolarizing_error(0.25, 2)

# Apply noise to specific qubits
noise_model.add_quantum_error(core_1q_error, ['h'], [0])
noise_model.add_quantum_error(core_2q_error, ['cx'], [0, 1])
noise_model.add_quantum_error(core_2q_error, ['cx'], [1, 2])

noise_model.add_quantum_error(outer_1q_error, ['h'], [3])
noise_model.add_quantum_error(outer_2q_error, ['cx'], [3, 4])

# Simulate
backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend=backend, noise_model=noise_model, shots=1024).result()
counts = result.get_counts()

# Display results
print("Black Hole Simulation Results:")
print(counts)
plot_histogram(counts)
plt.show()