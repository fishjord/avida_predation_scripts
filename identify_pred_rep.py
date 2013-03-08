#!/usr/bin/python

"""
The first line of this file (#!/usr/bin/python) tells our shell how to 
run this file so we can simply type ./sample_population.py and have it
be equivelent to typing 'python sample_population.py' 
"""

"""
In python you can specify comments in two ways, the triple quotes means
that everything until the next triple quote is a comment
"""

#we can also do single line comments by using the # sign

"""
most python files will start with a set of imports, basically listing
what modules we intend to use

two common imports are 'sys' and 'os'
"""
import os
import sys
import avida_utils #make sure the avida_utils.py file is in the same directory as this script
                   #you can read that file, but it does contain some advanced python constructs

#Check to see if we have the right number of arguments
#by default the first argument is the script name
if len(sys.argv) < 2:
    print "USAGE: sample_population.py data_dirs..."
    sys.exit(1)     #we don't have the information we need, exit with an error value

best_look_ratio = 0
best_file = None

# Structured Population Save                                                                                                                                                                                                                                         
# Fri Feb 15 18:31:22 2013                                                                                                                                                                                                                                           
#  1: ID                                                                                                                                                                                                                                                             
#  2: Source                                                                                                                                                                                                                                                         
#  3: Source Args                                                                                                                                                                                                                                                    
#  4: Parent ID(s)                                                                                                                                                                                                                                                   
#  5: Number of currently living organisms                                                                                                                                                                                                                           
#  6: Total number of organisms that ever existed                                                                                                                                                                                                                    
#  7: Genome Length                                                                                                                                                                                                                                                  
#  8: Average Merit                                                                                                                                                                                                                                                  
#  9: Average Gestation Time                                                                                                                                                                                                                                         
# 10: Average Fitness                                                                                                                                                                                                                                                
# 11: Generation Born                                                                                                                                                                                                                                                
# 12: Update Born                                                                                                                                                                                                                                                    
# 13: Update Deactivated                                                                                                                                                                                                                                             
# 14: Phylogenetic Depth                                                                                                                                                                                                                                             
# 15: Hardware Type ID                                                                                                                                                                                                                                               
# 16: Inst Set Name                                                                                                                                                                                                                                                  
# 17: Genome Sequence                                                                                                                                                                                                                                                
# 18: Occupied Cell IDs                                                                                                                                                                                                                                              
# 19: Gestation (CPU) Cycle Offsets                                                                                                                                                                                                                                  
# 20: Lineage Label                                                                                                                                                                                                                                                  
# 21: Current Group IDs                                                                                                                                                                                                                                              
# 22: Current Forager Types                                                                                                                                                                                                                                          
# 23: Birth Cells                                                                                                                                                                                                                                                    
# 24: Current Avatar Cell Locations                                                                                                                                                                                                                                  
# 25: Avatar Birth Cell                                                                                                                                                                                                                                              
# 26: Parent forager type                                                                                                                                                                                                                                            
# 27: Was Parent a Teacher                                                                                                                                                                                                                                           
# 28: Parent Merit 

print >>sys.stderr, "file\tnum organisms\tnum predators\taverage looks per predator"
for f in sys.argv[1:]:
    inst_file = os.path.join(f, "predator_instruction.dat")
    pop_file = os.path.join(f, "detail-2000000.spop")

    last_update = avida_utils.read_avida_dat(inst_file)[1][-1]  #Load the data from the file specified by the user

    avida_data = avida_utils.read_avida_dat(pop_file)[1]

    num_preds = 0
    num_orgs = 0

    for genotype in avida_data:
        forager_type = genotype["Current Forager Types"]
        if type(forager_type) != list:
            forager_type = [forager_type]

        num_preds += forager_type.count(-2)

        num_orgs += genotype["Number of currently living organisms"]

    look_counts = last_update["look-ahead-intercept"]
    ratio = float(look_counts) / num_preds

    print >>sys.stderr, "%s\t%s\t%s\t%s" % (f, num_orgs, num_preds, float(look_counts) / num_preds)

    if ratio > best_look_ratio:
        best_look_ratio = ratio
        best_file = f

print "Best look instruction ratio %s in run %s" % (best_look_ratio, best_file)
