N=int(input(""))
pegs=[[N-1-i for i in range(N)],[],[]]#每個柱子上有多少碟子
Npegs=[N,0,0]
cspeg=0 #最小的碟子在哪裡 ，因為每兩步一定要移一次
dir=1-N%2*2 #N為偶數時 +1  N為奇數時 -1  
while len(pegs[2])<N:
    tpeg=(cspeg+dir+3)%3  #S要移去哪
    print(str(cspeg+1)+"->"+str(tpeg+1))
    k=pegs[cspeg].pop(-1)
    pegs[tpeg].append(k)
    cspeg=tpeg
    speg=0  #從哪裡
    tgpeg=0  #移到哪裡
    if len(pegs[2])>=N:
        break
    if (cspeg==0):
        if pegs[1]==[]:
            speg=2
            tgpeg=1
        elif pegs[2]==[]:
            speg=1
            tgpeg=2
        elif pegs[1][-1]<pegs[2][-1]:
            speg=1
            tgpeg=2
        else:
            speg=2
            tgpeg=1

    if (cspeg==1):
        if pegs[2]==[]:
            speg=0
            tgpeg=2
        elif pegs[0]==[]:
            speg=2
            tgpeg=0
        elif pegs[0][-1]<pegs[2][-1]:
            speg=0
            tgpeg=2
        else:
            speg=2
            tgpeg=0

    if (cspeg==2):
        if pegs[1]==[]:
            speg=0
            tgpeg=1
        elif pegs[0]==[]:
            speg=1
            tgpeg=0
        elif pegs[0][-1]<pegs[1][-1]:
            speg=0
            tgpeg=1
        else:
            speg=1
            tgpeg=0
    print(str(speg+1)+"->"+str(tgpeg+1))
    t=pegs[speg].pop(-1)
    pegs[tgpeg].append(t)



    

