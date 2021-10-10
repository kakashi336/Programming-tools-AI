#!/usr/bin/env python
# coding: utf-8

"""NUI Galway CT5132/CT5148 Programming and Tools for AI (James McDermott)

Skeleton/solution for Assignment 1: Numerical Integration

By writing my name below and submitting this file, I/we declare that
all additions to the provided skeleton file are my/our own work, and
that I/we have not seen any work on this assignment by another
student/group.

Student name(s): Arjun Prakash
Student ID(s): 21239525

"""

import numpy as np
import sympy
import itertools
import math


def numint_py(function, start_point, end_point, n):
    """Numerical integration. For a function f, calculate the definite
    integral of f from a to b by approximating with n "slices" and the
    "left" scheme. This function must use pure Python, no Numpy.

    >>> round(numint_py(math.sin, 0, 1, 100), 5)
    0.45549
    >>> round(numint_py(lambda x: x, 0, 1, 100000), 5)
    0.5
    >>> round(numint_py(lambda x: x, 0, 1, 6), 5)
    0.41667
    >>> round(numint_py(lambda x: 1, 0, 1, 100), 5)
    1.0
    >>> round(numint_py(lambda x: -1, 0, 1, 100), 5)
    -1.0
    >>> round(numint_py(math.exp, 1, 2, 100), 5)
    4.64746

    """
    # STUDENTS ADD CODE FROM HERE TO END OF FUNCTION
    dx=(end_point-start_point)/n          # This variable is the width of one slice
    area=0          # Declaring area and initializing it to zero
    
    
    for i in range(start_point,n+start_point):  # Running the loop for N iterations using starting point variable and 'n'
        
        # Calculating area starting from initial to final slice
        area+=function(start_point+i*dx-start_point*dx)*dx          
        
    return area                                 # Returning the calculated are under the curve of f(x)


def numint(function, start_point, end_point, n, scheme="left"):
    """Numerical integration. For a function f, calculate the definite
    integral of f from a to b by approximating with n "slices" and the
    given scheme. This function should use Numpy, and no for-loop. Eg
    np.linspace() will be useful.
    
    >>> round(numint(np.sin, 0, 1, 100, 'left'), 5)
    0.45549
    >>> round(numint(lambda x: np.ones_like(x), 0, 1, 100, 'left'), 5)
    1.0
    >>> round(numint(np.exp, 1, 2, 100, 'left'), 5)
    4.64746
    >>> round(numint(np.exp, 1, 2, 100, 'midpoint'), 5)
    4.67075
    >>> round(numint(np.sin, 0, 1, 100, 'midpoint'), 5)
    0.4597
    >>> round(numint(np.exp, 1, 2, 100, 'right'), 5)
    4.69417

    """
    # STUDENTS ADD CODE FROM HERE TO END OF FUNCTION
    
    # Initializing width(dx)
    dx=(end_point-start_point)/n
    
    if scheme=='left':
        rectangles=np.linspace(start_point,end_point,n,endpoint=False)          # Initializing the point for each slice for given scheme
    
    elif scheme=='midpoint':
        rectangles=np.linspace(start_point,end_point,n,endpoint=False)          # Initializing the point for each slice for given scheme
        
        # Now new we will calculate the midpoint by just adding dx/2 and return total area by passing the midpoints to the function
        return(np.sum(function(rectangles+dx/2)*dx))                            
    
    elif scheme=='right':
        rectangles=np.linspace(end_point,start_point,n,endpoint=False)          # Initializing the point for each slice for given scheme
    
    # Since the left and right scheme are similar, we can return the area using one return statement by passing the slice points to the function
    return(np.sum(function(rectangles)*dx))                                     
     


def true_integral(fstr, a, b):
    """Using Sympy, calculate the definite integral of f from a to b and
    return as a float. Here fstr is an expression in x, as a str. It
    should use eg "np.sin" for the sin function.

    This function is quite tricky, so you are not expected to
    understand it or change it! However, you should understand how to
    use it. See the doctest example.

    >>> true_integral("np.sin(x)", 0, 2 * np.pi)
    0.0
    >>> true_integral("x**2", 0, 1)
    0.3333333333333333
    """
    x = sympy.symbols("x")
    # make fsym, a Sympy expression in x, now using eg "sympy.sin"
    fsym = eval(fstr.replace("np", "sympy")) 
    A = sympy.integrate(fsym, (x, a, b)) # definite integral
    A = float(A.evalf()) # convert to float
    return A


def numint_err(fstr, start_point, end_point, n, scheme):
    """For a given function fstr and bounds a, b, evaluate the error
    achieved by numerical integration on n points with the given
    scheme. Return the true value (given by true_integral),
    absolute error, and relative error, as a tuple.

    Notice that the absolute error and relative error must both be
    positive.

    Notice that the relative error will be infinity when the true
    value is zero. None of the examples in our assignment will have a
    true value of zero.

    >>> print("%.4f %.4f %.4f" % numint_err("x**2", 0, 1, 10, 'left'))
    0.3333 0.0483 0.1450
    >>> print("%.4f %.4f %.4f" % numint_err("-x**2", 0, 1, 10, 'left'))
    -0.3333 0.0483 0.1450
    >>> print("%.4f %.4f %.4f" % numint_err("x**2", 0, 1, 10, 'left'))
    0.3333 0.0483 0.1450

    """
    # STUDENTS ADD CODE FROM HERE TO END OF FUNCTION
    
    function = eval("lambda x: " + fstr) # f is a Python function
    true_value = true_integral(fstr, start_point, end_point)            # Finding True integral by just calling the true_integral function
    
    # Calculating error by finding difference between our answer and the true_integral for a given scheme
    error=abs(true_value-numint(function,start_point,end_point,n,scheme)) 

    # Return True value, absolute value of error and calculate Relative error by dividing error with True Integral and getting absolute value of it. 
    return true_value,error,abs(error/true_value)


def make_table(f_ab_s, ns, schemes):
    """For each function f with associated bounds (a, b), and each value
    of n and each scheme, calculate the absolute and relative error of
    numerical integration and print out one line of a table. This
    function doesn't need to return anything, just print. Each
    function and bounds will be a tuple (f, a, b), so the argument
    f_ab_s is a list of tuples.

    Hint: use print() with the format string
    "%s,%.2f,%.2f,%d,%s,%.4g,%.4g,%.4g". Hint 2: consider itertools.

    >>> make_table([("x**2", 0, 1), ("np.sin(x)", 0, 1)], [10, 100], ['left', 'midpoint'])
    x**2,0.00,1.00,10,left,0.3333,0.04833,0.145
    x**2,0.00,1.00,10,midpoint,0.3333,0.0008333,0.0025
    x**2,0.00,1.00,100,left,0.3333,0.004983,0.01495
    x**2,0.00,1.00,100,midpoint,0.3333,8.333e-06,2.5e-05
    np.sin(x),0.00,1.00,10,left,0.4597,0.04246,0.09236
    np.sin(x),0.00,1.00,10,midpoint,0.4597,0.0001916,0.0004168
    np.sin(x),0.00,1.00,100,left,0.4597,0.004211,0.009161
    np.sin(x),0.00,1.00,100,midpoint,0.4597,1.915e-06,4.167e-06
    
    """
    # STUDENTS ADD CODE FROM HERE TO END OF FUNCTION
    import itertools as iter
    
    
    for function,n,scheme in iter.product(f_ab_s,ns,schemes):
        
        #Storing values of 'True Value', Absolute Error, Relative Error by calling "numint_err" Function
        true_value,absolute_error,relative_error=numint_err(function[0],function[1],function[2],n,scheme)
        
        
        #Printing all the values (Function, bounds, Schemes, True Value, Absolute Erorr, Relative Error).
        #print(absolute_error,relative_error)
        print("%s,%.2f,%.2f,%d,%s,%.4g,%.4g,%.4g"%(function[0],function[1],function[2],n,scheme,true_value,absolute_error,relative_error))


def main():
    """Call make_table() as specified in the pdf."""
    # STUDENTS ADD CODE FROM HERE TO END OF FUNCTION
    make_table([("np.cos(x)", 0, np.pi), ("np.sin(2*x)", 0, 1),("np.exp(x)", 0, 1)], [10, 100,1000], ['left', 'midpoint'])
    
    """ Intepration:
    To obtain the best results for the area under the curve with function f(x), range {a-b} and a scheme, we need to maximize the 
    number of partitions i.e, the 'n' value should be high as this could lower the error rate along with the scheme set at 
    midpoint. The errors in left and midpoint is significant, midpoint scheme can get us the area which is very close to the 
    true value than the 'left/right' scheme.
    
    """
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    main()

