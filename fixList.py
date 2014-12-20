def fix(l):
    '''takes a list of ints (taken from another game) and makes them usable in my python program'''
    n = []
    for i in range(0,len(l),2):
	    n.append((l[i]+50,l[i+1]+50))
    return n

'''
taken from:http://www.playmycode.com/build/edit/1284

$largeRock1 = [-39,-25, -33,-8, -38,21, -23,25, -13,39, 24,34, 38,7, 33,-15, 38,-31, 16,-39, -4,-34, -16,-39]                        
$largeRock2 = [-32, 35, -4, 32, 24, 38, 38, 23, 31, -4, 38, -25, 14, -39, -28, -31, -39, -16, -31, 4, -38, 22]                        
$largeRock3 = [12, -39, -2, -26, -28, -37, -38, -14, -21, 9, -34, 34, -6, 38, 35, 23, 21, -14, 36, -25]           
$medRock1   = [-7, -19, -19, -15, -12, -5, -19, 0, -19, 13, -9, 19, 12, 16, 18, 11, 13, 6, 19, -1, 16, -17]        
$medRock2   = [9, -19, 18, -8, 7, 0, 15, 15, -7, 13, -16, 17, -18, 3, -13, -6, -16, -17]          
$medRock3   = [2, 18, 18, 10, 8, 0, 18, -13, 6, -18, -17, -14, -10, -3, -13, 15]            
$smallRock1 = [-8, -8, -5, -1, -8, 3, 0, 9, 8, 4, 8, -5, 1, -9]        
$smallRock2 = [-6, 8, 1, 4, 8, 7, 10, -1, 4, -10, -8, -6, -4, 0]           
$smallRock3 = [-8, -9, -5, -2, -8, 5, 6, 8, 9, 6, 7, -3, 9, -9, 0, -7]
'''
def fix2(l,nx,ny):
    '''takes a list of ints (taken from another game) and makes them usable in my python program'''
    n = []
    for i in l:
            n.append((i[0]+nx,i[1]+ny))
    return n
