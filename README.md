# Markov_Chain_Simulation

The main code of this repository can be found in the Python program 'churn_simulator_class.py'.
It contains the definition of two Python classes, namely the Customer class and the Simulation class.
It provides a tool to run simulations on customer churn given:

- The total number of periods the process should be simulated.
- The number of customers in the initial state of the simulation.
- The number of customers entering the market (or new customers for this specific company) after eacht transition.
- All possible states a customer can be in at the start of the simulation.
- All possible states a customer can be in during the simulation.
- The transition probabilities between states for each customer (which is fixed and the same for each customer).
  
  The transition probabilities can be changed for the instantiation of the Simulation but a originial transition probability
  matrix is provided in the file 'transition_probabilities.csv' in the directory 'data'. The probabilities are calculated
  based on the file 'customer_matrix.csv' in the directory 'data'.

The outcome and working of the code can be inspected in the Jupyter Notebook 'churn_simulator_class.ipynb'.
