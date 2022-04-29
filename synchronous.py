import random
import math
import numpy as np

def build_lead_simulation(q) -> int:
    private_lead = 0
    target_t_time = random.randint(50,100)
    for i in range(target_t_time):
        if (nextBlockMalicious(q)):
            private_lead += 1
        else:
            private_lead = max(private_lead-1, 0)
    return private_lead

def lead_distribution(q, num_iter=100000):
    distribution = dict()
    for i in range(num_iter):
        j = build_lead_simulation(q)
        distribution[j] = distribution.get(j, 0) + 1
    
    for i in range(10):
        if i in distribution:
            p_i = distribution[i]/num_iter
            print("Probability of " + str(i) + ": " + str(p_i))
    
    # x = np.arange(0, len(distribution), 1)
    # y = np.array([distribution[i]/num_iter for i in range(len(distribution))])
    # fit = np.polyfit(x, np.log(y), 1)
    # print(fit)

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
    return (random.randint(1,100) <= (q*100))

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
def computeBestAttackSuccessProb(q, n):
    p = 1-q
    p_win = 0
    for i in range(n):
        p_y_i = (1-q/p)*((q/p)**i)
        p_win_y_i = 0
        for j in range(2*n - i + 1):
            p_w_xj_yi = 1
            p_xj_yi = math.comb(2*n-i, j)*(q**j)*(p**(2*n-i-j))
            if (j < n - i):
                p_w_xj_yi = (q/p)**(2*n-2*i-2*j)
            p_win_y_i += p_w_xj_yi*p_xj_yi
        p_win += p_win_y_i*p_y_i
    p_win += (q/p)**n
    return p_win
        


def main():
    #print("Computed attacker success: " + str(computeAttackerSuccessProb(0.05, 6)))
    #print("Nakamoto attack empirical attacker success: " + str(computeEmpiricalSuccess(nakamoto_malicious_simulation, 0.2, 6, 10000)))
    #print("Best attack empirical attacker success: " + str(computeEmpiricalSuccess(best_attack_simulation, 0.2, 6, 100000)))
    #print("Best attack computed attacker success: " + str(computeBestAttackSuccessProb(0.2, 6)))
    # lead_distribution(0.02)
    
    delta = 0.05
    print("         Empirical success Prob | Theoretical Prob")
    for i in range(2,9):
        q = delta*i
        best_emp_p = computeEmpiricalSuccess(best_attack_simulation, q, 6, 30003)
        best_comp_p = computeBestAttackSuccessProb(q, 6)
        space = "   "
        if i%2==1:
            space = "  "
        print("q: " + str(round(q,2)) + space + str(round(best_emp_p,8)) + "               " + str(round(best_comp_p, 8)))
    
# Using the special variable 
# __name__
if __name__=="__main__":
    main()