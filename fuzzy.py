from click import confirmation_option
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as controller

simulation_controller = None

def load_fuzzy_controller():
    # inputs
    price = controller.Antecedent(np.arange(50000, 20000000, 1000000), 'price')
    price['cheap'] = fuzz.trimf(price.universe, [50000, 50000, 6000000])
    price['standard'] = fuzz.trimf(price.universe, [50000, 6000000, 10000000])
    price['expensive'] = fuzz.trimf(price.universe, [6000000, 20000000, 20000000])
    comfort = controller.Antecedent(np.arange(0, 11, 1), 'comfort')
    comfort['poor'] = fuzz.trimf(comfort.universe, [0, 0, 5])
    comfort['acceptable'] = fuzz.trimf(comfort.universe, [3, 6, 8])
    comfort['comfortable'] = fuzz.trimf(comfort.universe, [6, 10, 10])
    travelTime = controller.Antecedent(np.arange(0.5, 48, 0.5), 'travelTime')
    travelTime['short'] = fuzz.trimf(travelTime.universe, [0.5, 0.5, 6])
    travelTime['standard'] = fuzz.trimf(travelTime.universe, [4, 10, 15])
    travelTime['long'] = fuzz.trimf(travelTime.universe, [10, 48, 48])

    # output
    advise = controller.Consequent(np.arange(0, 11, 1), 'advise')
    advise['not recommendable'] = fuzz.trimf(advise.universe, [0, 0, 5])
    advise['very recommendable'] = fuzz.trimf(advise.universe, [5, 10, 10])
    advise['advisable'] = fuzz.trimf(advise.universe, [2, 4, 8])

    # rules
    rule1 = controller.Rule((price['cheap'] & comfort['comfortable'] & (travelTime['short']| (travelTime['standard']))) | (price['cheap']& comfort['acceptable'] & travelTime['short']), advise['very recommendable'])
    rule2 = controller.Rule(price['cheap'] & comfort['poor'] & travelTime['long'], advise['not recommendable'])
    rule3 = controller.Rule((price['cheap'] & comfort['poor'] & (travelTime['short'] | travelTime['standard']))|(price['cheap'] & comfort['acceptable'] & (travelTime['standard'] | travelTime['long'])), advise['advisable'])
    rule4 = controller.Rule(price['standard'] & comfort['acceptable'] & travelTime['short'], advise['very recommendable'])
    rule5 = controller.Rule((price['standard'] & comfort['poor'] & travelTime['short'])|(price['standard'] & comfort['comfortable'] & (travelTime['standard']|travelTime['long']))|(price['standard'] & comfort['acceptable'] & (travelTime['standard']|travelTime['short'])), advise['advisable'])
    rule6 = controller.Rule((price['standard'] & comfort['poor'] & (travelTime['standard']|travelTime['long']))| (price['standard'] & comfort['acceptable'] & travelTime['long']), advise['not recommendable'])
    rule7 = controller.Rule((price['expensive'] & comfort['comfortable'])|(price['expensive'] & comfort['acceptable'] & travelTime['short']), advise['advisable'])
    rule8 = controller.Rule((price['expensive'] & comfort['poor'])|(price['expensive'] & comfort['acceptable'] & (travelTime['standard']|travelTime['long'])), advise['not recommendable'])

    global simulation_controller
    simulation_controller = controller.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])



def simulate(price, comfort, travel_time):
    if simulation_controller == None:
        print('initializing')
        load_fuzzy_controller()
    
    simulation = controller.ControlSystemSimulation(simulation_controller)
    simulation.input['price'] = price
    simulation.input['comfort'] = comfort
    simulation.input['travelTime'] = travel_time
    simulation.compute()
    return simulation.output

