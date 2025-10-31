# MLflow-Integrated Dynamic Pricing Model for Airlines using Q-learning

**Author**: Kusuma K                                                                                                                                                                                                              
**Project type**: Internship project  
**Domain**: Airline revenue management / dynamic pricing / reinforcement learning

## Project Overview  
In the airline industry, pricing of seats is a perishable-asset problem: once the flight departs, unsold seats yield zero revenue. Traditional revenue management uses fare-classes, demand forecasting and overbooking heuristics. In this project, I propose a reinforcement-learning (RL) based dynamic pricing model for airlines, leveraging Q-learning to adaptively set fares, and integrate experiment tracking via MLflow.

---

## Motivation  
- Dynamic pricing can significantly boost revenue by adjusting prices in response to remaining time to departure, seats left, and demand trends.  
- RL offers the possibility to learn pricing policies from simulation rather than fixed heuristics.  
- MLflow helps track multiple experiments, manage models, compare metrics, and reproduce results — valuable in a data-science project for internships/presentation.

---

## Objectives  
- Build a simulation environment for a single-leg airline seat inventory over a booking horizon.  
- Design a Q-learning agent that chooses price levels (or fare classes) at each time step/booking event.  
- Integrate MLflow to log metrics (e.g., revenue, seat occupancy, average price), parameters (learning rate, discount factor, exploration epsilon) and model artifacts.  
- Compare baseline pricing (e.g., static price or fixed fare class rule) to RL-based pricing.  
- Provide a professional prototype with clean code, modular design, and documentation—suitable for internship/final year.

---

## Solution Approach  
### Environment  
- State variables: time until departure, seats remaining, current fare class / price level, possibly demand zone, competitor effect (if modelled).  
- Action space: discrete price levels or fare class selections.  
- Reward: revenue for each booking, potentially weighted by empty seat cost at departure time.  
- Episode: Simulate one flight from start to departure.  
- Demand model: stochastic, maybe Poisson arrival of bookings, with price‐sensitive demand function.

### Q-learning Agent  
- Q-table (if state & action space is small) or Q-network (if larger).  
- Learning rate α, discount factor γ, exploration strategy (ε-greedy).  
- Training over many simulated episodes.  
- After training, fix policy and evaluate performance.

### MLflow Integration  
- Create MLflow experiment (e.g., `airline_dynamic_pricing_qlearning`).  
- Log parameters (α, γ, ε schedule, number of episodes, environment settings).  
- Log metrics (total revenue per episode, average seat occupancy, average price, number of unsold seats).  
- Log model artifact (trained Q-table or Q-network).  
- Use MLflow UI to compare runs and pick best setting.

---

## Architecture & Workflow  
1. Data/Simulation module → define environment.  
2. Agent module → Q-learning logic (initialise Q, policy, update rule).  
3. Training script → loops episodes, calls environment, records results to MLflow.  
4. Evaluation script → loads best model, runs evaluation episodes, plots results.  
5. MLflow integration ensures reproducibility and experiment tracking.  
6. Reporting / visualization module → e.g., plot revenue curves, unsold seats over episodes.

A block-diagram (optional) could show these modules and data flows.

---

## Getting Started  
### Requirements  
- Python 3.x (recommend 3.8+)  
- Libraries: `numpy`, `pandas`, `matplotlib`, `mlflow`, possibly `gym` (if you use OpenAI Gym style), `seaborn`.  
- (Optional) CUDA / GPU if you use deep Q-network.

