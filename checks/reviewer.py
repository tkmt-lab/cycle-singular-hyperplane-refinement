from fractions import Fraction as F
from itertools import combinations
from functools import reduce
import json,time,resource

class Dual:
    def __init__(self,x,g): self.x,self.g=F(x),list(map(F,g))
    def __add__(self,b): return Dual(self.x+b.x,[a+c for a,c in zip(self.g,b.g)])
    def __sub__(self,b): return Dual(self.x-b.x,[a-c for a,c in zip(self.g,b.g)])
    def __mul__(self,b): return Dual(self.x*b.x,[a*b.x+c*self.x for a,c in zip(self.g,b.g)])

def determinant(a):
    a=[list(row) for row in a];v=F(1)
    for j in range(len(a)):
        p=next((i for i in range(j,len(a)) if a[i][j]),None)
        if p is None:return F(0)
        if p!=j:a[p],a[j]=a[j],a[p];v=-v
        q=a[j][j];v*=q
        for i in range(j+1,len(a)):
            z=a[i][j]/q
            for k in range(j+1,len(a)):a[i][k]-=z*a[j][k]
    return v

def rank(a):
    a=[list(row) for row in a];r=0
    for j in range(len(a[0])):
        p=next((i for i in range(r,len(a)) if a[i][j]),None)
        if p is None:continue
        a[r],a[p]=a[p],a[r];q=a[r][j]
        for i in range(r+1,len(a)):
            z=a[i][j]/q
            for k in range(j,len(a[0])):a[i][k]-=z*a[r][k]
        r+=1
    return r

def jac(r,p,ell,leak):
    n=len(r);m=n+1
    xs=[Dual(x,[int(i==j) for j in range(m)]) for i,x in enumerate(r+[leak])]
    one=Dual(1,[0]*m);zero=Dual(0,[0]*m)
    prod=lambda ys:reduce(lambda a,b:a*b,ys,one)
    def es(ys):
        e=[one]+[zero]*len(ys)
        for x in ys:
            for j in range(len(ys),0,-1):e[j]=e[j]+x*e[j-1]
        return e
    d=xs[:n];d[ell-1]=d[ell-1]+xs[-1]
    e=es(d);k=prod(xs[:p-1]);tail=es(d[p:])
    c=e[1:n]+[e[n]-prod(xs[:n]),k]+[k*x for x in tail[1:]]
    return [x.g for x in c]

start=time.perf_counter();out=[]
cases=[(4,3,2,1,[1,3,4,5],2),(5,4,1,3,[3,4,1,5,7],2),
       (4,3,2,1,[0,0,4,5],0),(5,4,1,3,[0,4,0,5,7],0),
       (5,4,1,3,[-2,3,1,5,7],-3),
       (3,2,1,2,[2,1,3],1),(4,3,1,3,[2,3,1,5],1),(5,4,1,4,[2,3,5,1,7],1)]
for n,p,a,ell,r,l in cases:
    assert r[a-1]==r[ell-1]+l
    j=jac(r,p,ell,l);v=[F(0)]*(n+1)
    v[a-1]=F(r[a-1]);v[ell-1]=-F(r[ell-1]);v[-1]=F(r[ell-1]-r[a-1])
    residual=[sum(x*y for x,y in zip(row,v)) for row in j]
    rk=rank(j);minor=None
    if ell<p:
        assert not any(residual) and rk<n+1
        if not any(v):assert all(row[a-1]==row[-1] for row in j)
    else:
        assert rk==n+1
        for rows in combinations(range(len(j)),n+1):
            det=determinant([j[i] for i in rows])
            if det:minor={'rows_1based':[i+1 for i in rows],'det':str(det)};break
    out.append({'n':n,'p':p,'a':a,'ell':ell,'r':r,'leak':l,'rank':rk,'columns':n+1,
                'kernel_zero':not any(v),'residual':list(map(str,residual)),'full_rank_minor':minor})
print(json.dumps({'cases':out,'elapsed_seconds':time.perf_counter()-start,
                  'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},indent=2))
