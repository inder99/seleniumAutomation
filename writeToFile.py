import sys

print("Inderjeet")
sys.stdout = open('./filename', 'w')
print("Vashista")
sys.stdout.close()