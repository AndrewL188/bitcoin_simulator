import random
import math

def best_attack_simulation(q, z) -> bool:
    private_lead = 0
    target_t_time = random.randint(1,200)
    for i in range(target_t_time):
        if (nextBlockMalicious(q)):
            private_lead += 1
        else:
            private_lead = max(private_lead-1, 0)
    return nakamoto_malicious_simulation(q, z, private_lead)
    

# Runs a simulation of an attacker using private chain 
# mining strategy proposed in Bitcoin white paper. Attacker
# will start mining on a private chain when a target transaction
# t appears. Synchronous 0-delay case.
# Attacker has mining power q and commit depth z
# Returns whether attacker was successful in overwriting t.
# Assume that attacker "gives up" after public chain has > 3z lead.
def nakamoto_malicious_simulation(q, z, private_lead=0) -> bool:
    public_chain = 0
    private_chain = private_lead
    while (public_chain < z):
        if (nextBlockMalicious(q)):
            private_chain += 1
        else:
            public_chain += 1
    # Attacker wins
    if (private_chain >= public_chain):
        return True
    # Attacker needs to catch up
    failure_threshold = max(3*z, 100)
    while (public_chain - private_chain < failure_threshold):
        if (nextBlockMalicious(q)):
            private_chain += 1
        else:
            public_chain += 1
        if (private_chain >= public_chain):
            return True
    return False

# Computes empirical probability of attacker success by running many simulations
def computeEmpiricalSuccess(attack, q, z, iter=10000):
    num_success = 0
    for i in range(iter):
        num_success += int(attack(q, z))
    return num_success/iter

# Assume q is rounded to two decimal places
def nextBlockMalicious(q) -> bool:
    return (random.randint(1,1000000) <= (q*1000000))

# Function that computes actual probability of attacker success under
# 0 delay synchrony assumption
# Params: q - Malicious mining rate
#         z - blocks deep considered "committed" block
def computeAttackerSuccessProb(q, z):
    p = 1 - q
    pwin = 0
    for j in range(0, 2*z+1):
        pwin_numAblocks = 1
        if (j < z):
            pwin_numAblocks = (q/p)**(2*z-2*j)
        p_numAblocks = math.comb(2*z, j)*(q**j)*(p**(2*z-j))
        pwin += pwin_numAblocks*p_numAblocks
    return pwin

def main():
    print("Computed attacker success: " + str(computeAttackerSuccessProb(0.2, 6)))
    alpha = .8
    e = (1/2.71828)**((0.001)*200*3)
    p = alpha*e
    print("p: ", p)
    q = .2
    print("old q: ", q)
    q = .2 / (.2+p)
    q = .2
    print("new q", q)
    print("Nakamoto attack empirical attacker success: " + str(computeEmpiricalSuccess(nakamoto_malicious_simulation, q, 6, 10000)))
    print("Best attack empirical attacker success: " + str(computeEmpiricalSuccess(best_attack_simulation, 0.2, 6, 10000)))

    
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()