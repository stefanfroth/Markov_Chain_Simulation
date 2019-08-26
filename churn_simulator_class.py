'''
The program churn_simulator_class defines a class Customer and
a class Simulation. Using the two classes you can run simulation
of Markov Chain Models.
'''

import pandas as pd
import numpy as np
import names
import matplotlib.pyplot as plt


## 1) Define the class customer
class Customer:
    '''
    The class Customer takes the possible initial states of the customer,
    the general possible states of the model and the transition
    probabilities between each state as inputs. Transitions of Customers
    between states can be modeled.
    '''

    def __init__(self\
                 , possible_initial_states\
                 , possible_states\
                 , transition_probabilities
                ):
        '''

        :param possible_initial_states:
        :param possible_states:
        :param transition_probabilities:
        '''

        self.name = names.get_full_name()
        self.possible_states = possible_states
        self.transition_probabilities = transition_probabilities
        self.state = np.asscalar(np.random.choice(possible_initial_states, size=1))
        self.history = [self.state]


    def transition(self):
        '''
        Running this function simulates a customers transition to the next period.
        '''
        # retrieve the transition probabilities for the current state from the transition matrix
        transition_prob = self.transition_probabilities.loc[self.state]

        # simulate the transition to a new state and save it
        self.state = np.asscalar(np.random.choice(self.possible_states, p=transition_prob, size=1))

        # append the state to self.history in order to track the history
        self.history.append(self.state)


    def __repr__(self):
        return f'''{self.name}'''


## 2.2) Create class Simulation
class Simulation:
    '''
    The class Simulation takes the following input parameters:

    total_periods: total number of periods to simulate
    initial_cust_nr: number of customers in period 0
    new_cust_per_period: number of customers that are added to the market after
    each period
    prices: the price of each good
    possible_initial_states: all states that can be the initial states of a
    customer
    transition_probabilities: transition probabilities between states
    mapping_items_ints: mapping between the goods and integer values
    '''

    def __init__(self\
    , total_periods\
    , initial_cust_nr\
    , new_cust_per_period\
    , prices\
    , possible_initial_states\
    , possible_states\
    , transition_probabilities\
    , mapping_items_ints):

        self.total_periods = total_periods
        self.initial_cust_nr = initial_cust_nr
        self.new_cust_per_period = new_cust_per_period
        self.customers = []
        self.history = pd.DataFrame()
        self.prices = prices
        self.possible_initial_states = possible_initial_states
        self.possible_states = possible_states
        self.transition_probabilities = transition_probabilities
        self.mapping_items_ints = mapping_items_ints


    def create_customers(self):
        '''
        This method creates x customers where x is the prespecified
        number of customers in period 0.
        '''
        for i in range(self.initial_cust_nr):
            customer = Customer(self.possible_initial_states\
                                , self.possible_states\
                                , self.transition_probabilities)

            self.customers.append(customer)


    def one_period_transition(self):
        '''
        This method simulates the transition of all existing customers
        over one period.
        '''
        for cust in self.customers:
            cust.transition()


    def create_history(self):
        '''
        This method creates a DataFrame containing the purchase history of
        all customers over all periods.
        '''
        self.history = pd.DataFrame()

        for cust in self.customers:
            self.history = pd.concat([self.history, pd.DataFrame(cust.history)], axis=1)

        self.history = self.history.T.reset_index(drop=True)
        self.history.index.name = 'customer_id'


    def run_simulation(self):
        '''
        This method runs the whole simulation of the transition of m Customers
        over n periods adding nc customers randomly to the states after
        each period.
        '''
        # first create the customers if they have not been created:
        if len(self.customers) > self.initial_cust_nr:
            print('''Something went awefully wrong!\n
            Please reinitialize the simulation!''')
            return 0
        elif len(self.customers) < self.initial_cust_nr:
            self.create_customers()
            print('Customers have been created.')


        #count how many periods have been simulated
        count = 0

        # run the simulation and add new customers for each period
        for per in range(self.total_periods):
            count += 1

            # simulate the transition for each customer
            for cust in self.customers:
                cust.transition()

            # add the new customers
            for new_cust in range(self.new_cust_per_period):
                customer = Customer(self.possible_initial_states\
                                    , self.possible_states\
                                    , self.transition_probabilities)
                customer.history = [None] * count + customer.history
                self.customers.append(customer)

        self.create_history()
        print('The simulation has ended successfully!')


    def plot_purchase_history(self):
        '''
        This method will plot the whole purchase history over all periods.
        '''
        # create a dataframe containing the number of instances for each state in each period
        num = pd.DataFrame()

        for col in self.history.columns:

            counts = []

            for state in self.possible_states:

                out = self.history[col].str.count(state).sum()
                counts.append(out)

            counts = pd.Series(counts, name=f'{col}')
            num = pd.concat([num, counts], axis=1)

        # invert the mapping between goods and integer values D
        inv_d = {v: k for k, v in self.mapping_items_ints.items()}

        # rename the indices of the matrix
        num = num.rename(mapper=inv_d, axis='index').drop('churned', axis=0)

        # plot the simulation results
        num.iloc[:, :-1].T.plot(figsize=(15, 6)\
        , title='Nr. of purchases per item in each period')

        plt.xlabel('Period')
        plt.ylabel('Nr. of purchases')


    def __repr__(self):
        return f'''This simulation of a companie's customer purchase history runs for {self.total_periods} periods.
                \nInitialy the customer has {self.initial_cust_nr} customers.
                \n{self.new_cust_per_period} customers are added to the market in each period.
                \nThe prices for the goods are {self.prices}.
                \nLets run the simulation!!!'''
