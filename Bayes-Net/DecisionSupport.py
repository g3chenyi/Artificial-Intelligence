#Implement the function DecisionSupport

'''
For this question you may use the code from part 1

Note however that part 2 will be marked independent of part 1

The solution for VariableElimination.py will be used for testing part2 instead
of the copy you submit. 
'''

from MedicalBayesianNetwork import *
from VariableElimination import *

'''
Parameters:
             medicalNet - A MedicalBayesianNetwork object                        

             patient    - A Patient object
                          The patient to calculate treatment-outcome
                          probabilites for
Return:
         -A factor object

         This factor should be a probability table relating all possible
         Treatments to all possible outcomes
'''
def DecisionSupport(medicalNet, patient):
    
    medicalNet.set_evidence_by_patient(patient)
    evidenceVars = patient.evidenceVariables()
    evidenceVals = patient.evidenceValues()
        
    # treatmentVars and outcomeVars are mutual exclusive
    treatmentVars = medicalNet.getTreatmentVars()
    outcomeVars = medicalNet.getOutcomeVars()
    queryVars = treatmentVars + outcomeVars
    
    bNet = medicalNet.net
    bNet_factors = bNet.factors()[:]
    bNet_variables = bNet.variables()[:]
  
    
    for i in range(len(bNet_factors)):
        for evidenceVar in evidenceVars:
            if evidenceVar in bNet_factors[i].get_scope():
                bNet_factors[i] = restrict_factor(bNet_factors[i], evidenceVar, evidenceVar.get_evidence())
    
    min_order = min_fill_ordering_queryVars(bNet_factors, queryVars)

    for elimVar in min_order:
        elimFactors_index = []
        for i in range(len(bNet_factors)):
            if elimVar in bNet_factors[i].get_scope():
                elimFactors_index.append(i)
            
        elimFactors_index.reverse()
        elimFactors = [bNet_factors[i] for i in elimFactors_index]
        new_factor = multiply_factors(elimFactors)
            
        new_factor = sum_out_variable(new_factor, elimVar)
    
        for i in elimFactors_index:
            bNet_factors.pop(i)
        bNet_factors.append(new_factor)
            
    
        
    result_factor = multiply_factors(bNet_factors)    
    
    # normalize result
    total_probability = 0.0
    
    for assignment in result_factor.get_assignment_iterator():
        probability = result_factor.get_value(assignment)
        total_probability += probability
        #result_factor.add_value_at_assignment(normalized, assignment)
    
    for assignment in result_factor.get_assignment_iterator():
        probability = result_factor.get_value(assignment)
        normalized = probability / total_probability
        result_factor.add_value_at_assignment(normalized, assignment)
    return result_factor
    
    
    
def min_fill_ordering_queryVars(bNet_factors, queryVars):
    '''Compute a min fill ordering given a list of factors. Return a list
    of variables from the scopes of the factors in Factors. The QueryVars is 
    NOT part of the returned ordering'''
    scopes = []
    for f in bNet_factors:
        scopes.append(list(f.get_scope()))
    Vars = []
    for s in scopes:
        for v in s:
            if not v in Vars and v not in queryVars:
                Vars.append(v)
    
    ordering = []
    while Vars:
        (var,new_scope) = min_fill_var(scopes,Vars)
        ordering.append(var)
        if var in Vars:
            Vars.remove(var)
        scopes = remove_var(var, new_scope, scopes)
    return ordering    