

from synchronous_deepak import nextBlockMalicious
import random

def deliver_message(new_chain_length, nodes, honest):
    if (honest):
        for node in nodes:
            if (node['honest']) and (node['chain_length'] < new_chain_length):
                node['chain_length'] = new_chain_length
                node['pending_messages'] = []
    else:
        for node in nodes:
            if (not node['honest']) and (node['chain_length'] < new_chain_length):
                node['chain_length'] = new_chain_length
                node['pending_messages'] = []       
        
def nakamoto_malicious_simulation(q, z, get_delay, private_lead=0, timestep = 1, node_success_probability = 0.0001) -> bool:
    num_honest = (1-q)*100
    num_dishonest = q*100
    nodes = []
    for i in range(int(num_dishonest)):
        dishonest_node = {"honest": False, "chain_length": private_lead, "pending_messages": []}
        nodes.append(dishonest_node.copy())
        
    for i in range(int(num_honest)):
        honest_node = {"honest": True, "chain_length": 0, "pending_messages": []}
        nodes.append(honest_node.copy())
    
    public_chain = 0
    private_chain = private_lead
    random.shuffle(nodes)

    def process_node(node, nodes):
        to_deliver = list(filter(lambda message: message["delivery_time"] <= curr_time, node["pending_messages"]))
        deliver_message(new_chain_length=node["chain_length"] - len(node["pending_messages"]) + len(to_deliver), nodes=nodes, honest=node["honest"])
        node["pending_messages"] = list(filter(lambda message: message["delivery_time"] > curr_time, node["pending_messages"]))
        
        for message in node["pending_messages"]:
            if (message['delivery_time'] < curr_time):
                deliver_message(new_chain_length=node["chain_length"] - len(node["pending_messages"]), nodes=nodes, honest=node["honest"])
        
        if (nextBlockMalicious(node_success_probability)):
            node["chain_length"] += 1
            node["pending_messages"].append({"delivery_time": curr_time + get_delay(honest=node["honest"])})
            
    curr_time = 0
    while (public_chain < z):
        for node in nodes:
            process_node(node, nodes)
        
        #print(public_chain, private_chain)
        public_chain = max([k['chain_length'] for k in list(filter(lambda node: node["honest"], nodes))])
        private_chain = max([k['chain_length'] for k in list(filter(lambda node: not node["honest"], nodes))])
        curr_time += timestep

    # Attacker wins
    if (private_chain >= public_chain):
        return True
    # Attacker needs to catch up
    failure_threshold = max(3*z, 100)
    while (public_chain - private_chain < failure_threshold):
        for node in nodes:
            process_node(node, nodes)
        
        
        public_chain = max([k['chain_length'] for k in list(filter(lambda node: node["honest"], nodes))])
        private_chain = max([k['chain_length'] for k in list(filter(lambda node: not node["honest"], nodes))])
        
        if (private_chain >= public_chain):
            return True

        curr_time += timestep
    return False

# Computes empirical probability of attacker success by running many simulations
def computeEmpiricalSuccess(attack, q, z, delay_function, node_success_probability, iter=10000):
    num_success = 0
    print(node_success_probability)
    for i in range(iter):
        num_success += int(attack(q, z, delay_function, node_success_probability=node_success_probability))
        if i > 0 and i%50 == 0:
            print(i, num_success/(i + 1))
    return num_success/iter

def delay_function(honest):
    if (honest):
        return 3
    
    return 0

def main():
    inputs = [.01]
    for input in inputs:
        print("Nakamoto attack empirical attacker success with input " + str(input) + ": " + str(computeEmpiricalSuccess(nakamoto_malicious_simulation, 0.2, 6, delay_function, node_success_probability=input)))


# Using the special variable 
# __name__
if __name__=="__main__":
    main()