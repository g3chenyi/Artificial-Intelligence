from BayesianNetwork import *

import itertools
##Implement all of the following functions

## Do not modify any of the objects passed in as parameters!
## Create a new Factor object to return when performing factor operations




    
'''
multiply_factors(factors)

Parameters :
              factors : a list of factors to multiply
Return:
              a new factor that is the product of the factors in "factors"
'''
def multiply_factors(factors):
    if len(factors) == 1:
        return factors[0]
        
    factor1 = factors[0]
  
    for i in range(1,len(factors)):
        factor2 = factors[i]
        factor1 = multiply_two_factors(factor1, factor2)
    
    return factor1

def non_duplicate_vars_index(factor1, factor2):
    non_duplicate_vars_index = []
    
    scope1 = factor1.get_scope()
    scope2 = factor2.get_scope()
    for var_index  in range(len(scope2)):
        var = scope2[var_index]
        if var not in scope1:
            non_duplicate_vars_index.append(var_index)
    return non_duplicate_vars_index
    

def get_union_vars(factor1, factor2):
    unique_vars_index = non_duplicate_vars_index(factor1, factor2)
    union_vars = factor1.get_scope()[:]
    for i in unique_vars_index:
        union_vars.append(factor2.get_scope()[i])
    return union_vars

def get_assignment2(factor1, factor2, assignment1, assignment):
    scope1 = factor1.get_scope()
    scope2 = factor2.get_scope()
    assignment2 = []
    replacement_index = 0
    for i in range(len(scope2)):
        var = scope2[i]
        if var not in scope1:
            assignment2.append(assignment[replacement_index+len(assignment1)])
            replacement_index += 1
        else:
            index = scope1.index(var)
            assignment2.append(assignment[index])
    return assignment2
            
    
    
def multiply_two_factors(factor1, factor2):
    
    # todo consider empty case

    if (len(factor1.get_scope()) == 0 and len(factor2.get_scope()) == 0):
        new_factor = Factor('{}*{}'.format(factor1.name, factor2.name), [])
        new_factor.add_value_at_assignment(factor1.get_value([])*factor2.get_value([]), [])
        return new_factor
    
    
    union_vars = get_union_vars(factor1, factor2)
    new_factor = Factor('{}*{}'.format(factor1.name, factor2.name), union_vars)    
        
    
    for assignment in new_factor.get_assignment_iterator():
        assignment1 = assignment[:len(factor1.get_scope())]
        assignment2 = get_assignment2(factor1, factor2, assignment1, assignment)
        if (len(factor1.get_scope()) == 0):
            factor1_value = factor1.get_value([])
        else:
            factor1_value = factor1.get_value(assignment1)
        if(len(factor2.get_scope()) == 0):
            facor2_value = factor2_get_value([])
        else:
            factor2_value = factor2.get_value(assignment2)
        product = factor1_value * factor2_value
        new_factor.add_value_at_assignment(product, assignment)
        
    return new_factor
            
    
    
    

'''
restrict_factor(factor, variable, value):

Parameters :
              factor : the factor to restrict
              variable : the variable to restrict "factor" on
              value : the value to restrict to
Return:
              A new factor that is the restriction of "factor" by
              "variable"="value"
      
              If "factor" has only one variable its restriction yields a 
              constant factor
'''
def restrict_factor(factor, variable, value):
    scope = factor.get_scope()
    restricted_index = scope.index(variable)

    new_scope = scope[:restricted_index] + scope[restricted_index+1:]
    newFactor = Factor('restricted {},{},{}'.format(factor.name,variable.name,value), new_scope)
    if len(new_scope) == 0:
        newFactor.add_value_at_assignment(factor.get_value([value]), [])
        return newFactor
    for assignment in factor.get_assignment_iterator():
        if assignment[restricted_index] == value:
            new_assignment = assignment[:restricted_index] + assignment[restricted_index+1:]
            newFactor.add_value_at_assignment( factor.get_value(assignment), new_assignment)
    return newFactor
    
'''    
sum_out_variable(factor, variable)

Parameters :
              factor : the factor to sum out "variable" on
              variable : the variable to sum out
Return:
              A new factor that is "factor" summed out over "variable"
'''
def sum_out_variable(factor, variable):
    scope = factor.get_scope()
    var_index = scope.index(variable)
    new_scope = scope[:var_index] + scope[var_index+1:]
    
    new_factor = Factor('sum {}.{}'.format(factor.name, variable.name), new_scope)
    if (len(scope) == 0):
        return factor
    for assignment in new_factor.get_assignment_iterator():
        s = 0
        for val in variable.domain():
            factor_assignment = assignment[:]
            factor_assignment.insert(var_index, val)
            #print(factor_assignment)
            s += factor.get_value(factor_assignment)
        new_factor.add_value_at_assignment(s, assignment)
    return new_factor


    
'''
VariableElimination(net, queryVar, evidenceVars)

 Parameters :
              net: a BayesianNetwork object
              queryVar: a Variable object
                        (the variable whose distribution we want to compute)
              evidenceVars: a list of Variable objects.
                            Each of these variables should have evidence set
                            to a particular value from its domain using
                            the set_evidence function. 

 Return:
         A distribution over the values of QueryVar
 Format:  A list of numbers, one for each value in QueryVar's Domain
         -The distribution should be normalized.
         -The i'th number is the probability that QueryVar is equal to its
          i'th value given the setting of the evidence
 Example:

 QueryVar = A with Dom[A] = ['a', 'b', 'c'], EvidenceVars = [B, C]
 prior function calls: B.set_evidence(1) and C.set_evidence('c')

 VE returns:  a list of three numbers. E.g. [0.5, 0.24, 0.26]

 These numbers would mean that Pr(A='a'|B=1, C='c') = 0.5
                               Pr(A='b'|B=1, C='c') = 0.24
                               Pr(A='c'|B=1, C='c') = 0.26
'''       
def VariableElimination(net, queryVar, evidenceVars):
    
    
    factors_modified = net.factors()[:]
  
    
    for i in range(len(factors_modified)):
        for evidenceVar in evidenceVars:
            if evidenceVar in factors_modified[i].get_scope():
                factors_modified[i] = restrict_factor(factors_modified[i], evidenceVar, evidenceVar.get_evidence())
    
    min_order = min_fill_ordering(factors_modified, queryVar)
    for elimVar in min_order:
        elimFactors_index = []
        for i in range(len(factors_modified)):
            if elimVar in factors_modified[i].get_scope():
                elimFactors_index.append(i)
        
        elimFactors_index.reverse()
        elimFactors = [factors_modified[i] for i in elimFactors_index]
        new_factor = multiply_factors(elimFactors)
        
        new_factor = sum_out_variable(new_factor, elimVar)

        for i in elimFactors_index:
            factors_modified.pop(i)
        factors_modified.append(new_factor)
        

    
    result_factor = multiply_factors(factors_modified)
    result_values = [value/sum(result_factor.values[:]) for value in result_factor.values[:]]
    return result_values
        
            
