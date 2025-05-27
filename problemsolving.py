import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
num_agents = 100
num_steps = 300
dt = 0.1

# Strategy assignment
np.random.seed(42)
strategies = np.random.choice(['denial', 'yes'], size=num_agents)

# Initialization
phi = np.full((num_agents, num_steps), 1.0)
omega = np.full((num_agents, num_steps), 1.0)
emotional_cost = np.zeros((num_agents, num_steps))
accuracy = np.zeros((num_agents, num_steps))

# Problem-solving simulation
for i in range(num_agents):
    strategy = strategies[i]
    for t in range(1, num_steps):
        # Simulate a new problem with a "hidden" correct answer
        correct_solution = np.random.choice([0, 1])
        noise = np.random.rand()  # Simulates irrelevant/conflicting information

        # Decision accuracy model
        if strategy == 'denial':
            # Fast decision, more likely to guess incorrectly if noise is high
            answer = correct_solution if noise < 0.4 else 1 - correct_solution
            accuracy[i, t] = 1 if answer == correct_solution else 0
            omega[i, t] = omega[i, t-1] * 0.98
            emotional_cost[i, t] = 1.0 * (1 - omega[i, t])

        elif strategy == 'yes':
            # Slower resolution but integrates noise
            integration_factor = omega[i, t-1] * (1 - noise)
            answer = correct_solution if integration_factor > 0.4 else 1 - correct_solution
            accuracy[i, t] = 1 if answer == correct_solution else 0
            omega[i, t] = omega[i, t-1] * (1 + 0.002)
            emotional_cost[i, t] = 1.0 * np.exp(-0.03 * t)

# Aggregate statistics
acc_yes = accuracy[strategies == 'yes'].mean(axis=0)
acc_denial = accuracy[strategies == 'denial'].mean(axis=0)
cost_yes = emotional_cost[strategies == 'yes'].mean(axis=0)
cost_denial = emotional_cost[strategies == 'denial'].mean(axis=0)

# Plot accuracy
plt.figure(figsize=(10, 6))
plt.plot(acc_denial, label='Denial Accuracy', linestyle='--')
plt.plot(acc_yes, label='Yes Accuracy', linestyle='-')
plt.title('Problem Solving Accuracy Over Time')
plt.xlabel('Time Step')
plt.ylabel('Accuracy (mean)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()