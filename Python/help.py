import os
import sys
out = sys.stdout
sys.stdout = open('help.txt','w')
help(os)
sys.stdout.close()
sys.stdout= out
