#Do not change function name in this cell
def bubbleSort(a):
  '''
  This is a function to sort a given list using Bubble Sort Algorithm.
  '''
  n=len(a)
  for i in range(n):
      for j in range(n-i-1):
          if(a[j] > a[j+1]):
            a[j+1], a[j] = a[j], a[j+1]
  return a
#Do not change variable names in this cell
import random
bubsort=[]
n=20
for i in range(n):
  bubsort.append(random.randint(0,n))
print(bubsort)
print(bubbleSort(bubsort))

