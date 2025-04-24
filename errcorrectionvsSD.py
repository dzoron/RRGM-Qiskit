from qiskit import QuantumCircuit, Aer, transpile
from qiskit.visualization import plot_histogram
from qiskit.providers.aer.noise import NoiseModel, depolarizing_error
from qiskit.execute_function import execute

# Create a simple 3-qubit repetition code (bit-flip code)
def bit_flip_code_circuit():
    circuit = QuantumCircuit(3, 1)
    circuit.barrier()
    circuit.cx(0, 1)
    circuit.cx(0, 2)
    circuit.barrier()
    circuit.h(0)
    circuit.barrier()
    circuit.cx(0, 1)
    circuit.cx(0, 2)
    circuit.ccx(1, 2, 0)
    circuit.barrier()
    circuit.measure(0, 0)
    return circuit

def basic_circuit():
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    return circuit

# Noise model
noise_model = NoiseModel()
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.1, 1), ['h'])
noise_model.add_all_qubit_quantum_error(depolarizing_error(0.1, 2), ['cx'])

# Circuits
basic = basic_circuit()
encoded = bit_flip_code_circuit()

# Simulator
sim = Aer.get_backend('qasm_simulator')

# Run with new syntax (no deprecation)
counts_basic = sim.run(transpile(basic, sim), shots=1024, noise_model=noise_model).result().get_counts()
counts_encoded = sim.run(transpile(encoded, sim), shots=1024, noise_model=noise_model).result().get_counts()

print("Basic Circuit Results:", counts_basic)
print("Encoded Circuit Results:", counts_encoded)