def plot_figure(elements):
    #create lists X and Y for points of the element based on the input
    X, Y=(range(2**n))            
    #create another list of matrix C for the output of elements  
    C = (range(4**n))
    #Append (0,0) to list C as per the range(len(C))
    for i in range(len(C)):
        C.append([0,0])
    #create list of elements accordingly to be appended in list C
    for i in range(len(C)):
    #for the ith value of C, we need to insert the jth value 
        for j in range(len(C)):
        #for every jth value of C, replace (0,0) with ith values of X and Y 
        #ie (1,1)
            C[i][j]=(C[i][j]).append(X[i],Y[j])
            if n%2!=0:
            #check if the input number is odd
              for i in range(len(C)):
                  for j in range(len(C)):
                #for the jth value of C, replace with the below pattern
                    C[j]=2*[(X[i+1],Y[j]),(X[i],Y[j+1])]
            elif n%2==0:
            #check if the input number is even
                for i in range(len(C)):
                  for j in range(len(C)):
                #if even, for the jth value of C, swap and replace the pattern
                      C[j]=2*[(X[i],Y[j+1]),(X[i+1],Y[j])]    
          #the figure is plotted such that, after every 4 steps
          #the increamenting values are swaped
    return C
    #the function ends as we return the list C with elements of plotted figure
n=int(input("Enter the number of elements you want for the plot figure: "))
print(plot_figure(n))