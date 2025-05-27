
import numpy as np
import matplotlib.pyplot as plt

# Reinitialize simulation parameters
num_agents = 100
num_steps = 500
phi0 = 1.0
omega0 = 1.0
dt = 0.1

# Randomly assign strategies again for balanced test
np.random.seed(42)
strategies = np.random.choice(['denial', 'yes'], size=num_agents)

# Initialize arrays
phi = np.full((num_agents, num_steps), phi0)
omega = np.full((num_agents, num_steps), omega0)
emotional_cost = np.zeros((num_agents, num_steps))

# Emotional flux parameters
epsilon = 1.0
k_decay = 0.03  # rate at which emotional cost decays in yes strategy

for i in range(num_agents):
    strategy = strategies[i]
    for t in range(1, num_steps):
        entropy_input = np.random.uniform(0.1, 0.5)

        if strategy == 'denial':
            gamma = 1.2
            phi[i, t] = phi[i, t-1] * np.exp(-gamma * dt)
            omega[i, t] = omega[i, t-1] * 0.98
            # Emotional cost rises as omega shrinks (recursive memory lost)
            emotional_cost[i, t] = epsilon * (1 - omega[i, t])

        elif strategy == 'yes':
            coupling = 1 - np.exp(-0.3 * t * dt)
            grad_S_ent = 1 / (1 + 0.3 * (t * dt)**2)
            alignment = coupling / (1 + grad_S_ent)
            phi[i, t] = phi[i, t-1] + 0.35 * alignment * dt
            phi[i, t] = min(phi[i, t], 1.0)
            omega[i, t] = omega[i, t-1] * (1 + 0.002)
            # Emotional cost starts high, decays over time
            emotional_cost[i, t] = epsilon * np.exp(-k_decay * t)

# Compute averages
emotional_yes_avg = emotional_cost[strategies == 'yes'].mean(axis=0)
emotional_denial_avg = emotional_cost[strategies == 'denial'].mean(axis=0)

# Plot the result
plt.figure(figsize=(10, 6))
plt.plot(emotional_denial_avg, label='Denial Emotional Cost', linestyle='--')
plt.plot(emotional_yes_avg, label='Yes Emotional Cost', linestyle='-')
plt.xlabel('Time Step')
plt.ylabel('Emotional Effort (via F_info)')
plt.title('Emotional Weight of Perspective Collapse Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()