
from qiskit import QuantumCircuit, Aer, execute
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
from qiskit.quantum_info import entropy
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Create a 4-qubit grid (2x2) representing a region of spacetime
qc = QuantumCircuit(4, 4)

# Step 1: Entangle qubits into a simple square lattice
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.cx(1, 3)
qc.cx(2, 3)

# Step 2: Apply depolarizing noise (simulating Spacedecay)
noise_model = NoiseModel()
depol1 = depolarizing_error(0.1, 1)  # For 1-qubit gates
depol2 = depolarizing_error(0.1, 2)  # For 2-qubit gates

noise_model.add_all_qubit_quantum_error(depol1, ['h'])
noise_model.add_all_qubit_quantum_error(depol2, ['cx'])

# Step 3: Measure all qubits
qc.barrier()
qc.measure(range(4), range(4))

# Step 4: Run simulation
simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, backend=simulator, noise_model=noise_model, shots=1024)
result = job.result()
counts = result.get_counts()

# Step 5: Show the result
print("Spacedecay Entanglement Results:", counts)
plot_histogram(counts)
plt.title("Spacedecay Simulation - Entanglement With Decay")
plt.show()
