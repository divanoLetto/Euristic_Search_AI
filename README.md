# Heuristic_Search_AI

## Assigment: 
  Solve a **state-search problem** processing and **defining a specific heuristic metrics** and implementing the A* search algorithm.
  Then compare the results and the performacy obtained with blind and informed search.
## Problem:
  The problem is defined as follow:  
    "The assembly of a certain product requires the performance of N tasks {c1,. . . , cn}, each of which requires a (discrete) time ti,i = 1,...,n to be completed.   
    Some tasks require certain prerequisites: the task ci requires that the tasks Pi⊂{c1,...,cn} to be completed before starting (Pi is the empty set if there has no prerequisites).  
    There are M employees who can be assigned tasks and every employee can just carry out a single task at a certain point in time.   
    Assuming it is necessary to assemble K identical copies of the product,  is required to find the best time sequence of assigningment of the products to the employees in order to minimize the overall time need to complete all assemblies." 
## Execution 
Run main.py
## Results
We created a specific **heuristic function h** composed of three functions **h1**, **h2** and **h3** for each problem area, which allowed us to demonstrate the greater efficiency of the informed research based on heuristics compared to the blind research. To see more details read *Heuristic_Search_AI_document.pdf*.
