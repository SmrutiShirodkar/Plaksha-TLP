stock_list=[2,1.5,4,0.5,7,5,3,4,1,6]
stock_list_fin=[]
flag=0

def stock_cal(stock_list):
    
    for i in range(len(stock_list)-1):
        
        if i == i+1:
            
            stock_list_fin.append("W")
    
        elif i < i+1:
            stock_list_fin.append("B")
    
        elif i > i+1:
            stock_list_fin.append("S")
    
    return stock_list_fin

print(stock_cal(stock_list))


first take the string input
def a function to compare the stocks with next stocks to assign w,b,s:
    as you compare the stocks,
    make sure you buy at the smallest element and sell at the highest
    in between if the stocks arent very enticing, wait for next
    compute the best sequence of buying and selling to get max profit
    
            