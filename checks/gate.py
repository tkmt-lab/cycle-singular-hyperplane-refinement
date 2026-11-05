"""Exact fixed-point check, two model derivations and two arithmetic routes.
Run from the package root via: python3 -B reproduce.py
"""
import itertools
import json
import platform
import resource
import time
from fractions import Fraction
from math import prod

import sympy as sp

resource.setrlimit(resource.RLIMIT_CPU, (60,60))
started=time.monotonic()
r1,r2,r3,r4,L2,L4,s=sp.symbols('r1 r2 r3 r4 L2 L4 s')
params=(r1,r2,r3,r4,L2,L4)
r=(r1,r2,r3,r4)
d=(r1,r2+L2,r3,r4+L4)
M=sp.Matrix([[-r1,0,0,r4],[r1,-r2-L2,0,0],[0,r2,-r3,0],[0,0,r3,-r4-L4]])
Q=s*sp.eye(4)-M
D=sp.expand(Q.det(method='domain-ge'))
N=sp.expand(Q.minor_submatrix(0,2).det())  # cofactor (input row 1, output column 3)
assert sp.expand(D-(prod(s+x for x in d)-prod(r)))==0
assert sp.expand(N-r1*r2*(s+d[3]))==0

def elementary(values,k):
    return sum(prod(values[i] for i in subset) for subset in itertools.combinations(range(len(values)),k))
c=sp.Matrix([elementary(d,k) for k in range(1,4)]+[prod(d)-prod(r),r1*r2,r1*r2*d[3]])
coeff_from_matrix=sp.Matrix([sp.Poly(D,s).coeff_monomial(s**i) for i in (3,2,1,0)]+
                            [sp.Poly(N,s).coeff_monomial(s**i) for i in (1,0)])
assert all(sp.expand(x)==0 for x in c-coeff_from_matrix)
J=c.jacobian(params)
# Polynomial direction, without dividing by an edge rate.
v=sp.Matrix([r1,-r2,0,0,r2-r1,0])
h=r2+L2-r1
expected=sp.Matrix([0,r1*h,r1*h*(d[2]+d[3]),r1*h*d[2]*d[3],0,0])
assert all(sp.expand(x)==0 for x in J*v-expected)
# The polynomial direction can vanish; check the separate column relation there.
assert all(sp.expand(x)==0 for x in (J[:,0]-J[:,4]).subs({r1:0,r2:0,L2:0}))

# Independent numeric differentiation: expand products by the product rule.
def explicit_jacobian(point):
    rr=point[:4]
    dd=[rr[0],rr[1]+point[4],rr[2],rr[3]+point[5]]
    gradients=[[int(j==i or (i==1 and j==4) or (i==3 and j==5)) for j in range(6)] for i in range(4)]
    out=[]
    for k in range(1,5):
        out.append([sum(sum(gradients[i][j]*prod(dd[t] for t in subset if t!=i) for i in subset)
                        for subset in itertools.combinations(range(4),k)) for j in range(6)])
    for j in range(4):
        out[3][j]-=prod(rr[t] for t in range(4) if t!=j)
    kap=[rr[1],rr[0],0,0,0,0]
    out.append(kap)
    out.append([dd[3]*kap[j]+rr[0]*rr[1]*gradients[3][j] for j in range(6)])
    return out


def rank_fraction(matrix):
    a=[[Fraction(x) for x in row] for row in matrix]
    pivot=0
    for j in range(len(a[0])):
        hit=next((i for i in range(pivot,len(a)) if a[i][j]),None)
        if hit is None:
            continue
        a[pivot],a[hit]=a[hit],a[pivot]
        q=a[pivot][j]
        a[pivot]=[x/q for x in a[pivot]]
        for i in range(pivot+1,len(a)):
            q=a[i][j]
            a[i]=[x-q*y for x,y in zip(a[i],a[pivot])]
        pivot+=1
        if pivot==len(a):break
    return pivot


def det_fraction(matrix):
    a=[[Fraction(x) for x in row] for row in matrix]
    det=Fraction(1)
    for j in range(len(a)):
        hit=next((i for i in range(j,len(a)) if a[i][j]),None)
        if hit is None:return Fraction(0)
        if hit!=j:a[j],a[hit]=a[hit],a[j];det=-det
        q=a[j][j];det*=q
        for i in range(j+1,len(a)):
            factor=a[i][j]/q
            for k in range(j,len(a)):a[i][k]-=factor*a[j][k]
    return det


records=[]
for label,point in [('on_H',(3,1,5,7,2,11)),('off_H',(4,1,5,7,2,11))]:
    sub=dict(zip(params,point))
    js=J.subs(sub)
    matrix=[[int(x) for x in row] for row in js.tolist()]
    assert explicit_jacobian(point)==matrix
    rank=rank_fraction(matrix)
    assert rank==js.rank()
    det=det_fraction(matrix)
    assert det==int(js.det())
    record={'label':label,'point':list(point),'all_positive':all(x>0 for x in point),
            'H_value':int(h.subs(sub)),'coefficients':[int(x) for x in c.subs(sub)],
            'jacobian':matrix,'rank_fraction':rank,'rank_sympy':int(js.rank()),
            'det_fraction':str(det),'det_sympy':int(js.det()),'independent_product_derivatives_match':True}
    if label=='on_H':
        vv=v.subs(sub)
        assert vv!=sp.zeros(6,1) and js*vv==sp.zeros(6,1)
        assert rank==5 and det==0
        record['kernel_vector']=[int(x) for x in vv]
        found=None
        for rows in itertools.combinations(range(6),5):
            for cols in itertools.combinations(range(6),5):
                mm=[[matrix[i][j] for j in cols] for i in rows]
                minor=det_fraction(mm)
                if minor:
                    assert minor==int(js.extract(rows,cols).det())
                    found={'rows_one_based':[i+1 for i in rows],'cols_one_based':[i+1 for i in cols],
                           'det_fraction':str(minor),'det_sympy':int(js.extract(rows,cols).det())}
                    break
            if found:break
        assert found
        record['rank_lower_bound_minor']=found
    else:assert rank==6 and det!=0
    # Positivity keeps numerator roots away from denominator roots in this example.
    record['denominator_at_numerator_root']=int(D.subs(sub).subs(s,-int(d[3].subs(sub))))
    assert record['denominator_at_numerator_root']!=0
    records.append(record)

print(json.dumps({'status':'PASS','n':4,'input':[1],'output':[3],'leaks':[2,4],'a':1,'ell':2,
    'parameter_order':[str(x) for x in params],
    'coefficient_map':[str(sp.expand(x)) for x in c],
    'matrix_and_symmetric_coefficients_match':True,'zero_direction_column_relation':True,
    'symbolic_kernel_identity':{'direction':[str(x) for x in v],'H':str(h),'Jv':[str(x) for x in expected]},
    'points':records,'python':platform.python_version(),'sympy':sp.__version__,
    'elapsed_seconds':time.monotonic()-started,'maxrss_bytes_macos':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    'cpu_limit_seconds':60,'processes':1,'additional_cost_usd':0,
    'independent_agent_review':False,'general_n_proof_machine_checked':False},ensure_ascii=False,indent=2))
