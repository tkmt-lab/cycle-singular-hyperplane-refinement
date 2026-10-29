#!/usr/bin/env python3
"""Independent integer polynomial/Jacobian/minor computation; standard library only."""
from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path
import resource
import time

start = time.monotonic()
def add(*polys):
    result = {}
    for poly in polys:
        for powers, coefficient in poly.items():
            result[powers] = result.get(powers, 0) + coefficient
    return {p:c for p,c in result.items() if c}
def scale(poly, factor):
    return {p:c*factor for p,c in poly.items() if c*factor}
def mul(left, right):
    result = {}
    for p,c in left.items():
        for q,d in right.items():
            r=tuple(x+y for x,y in zip(p,q))
            result[r]=result.get(r,0)+c*d
    return {p:c for p,c in result.items() if c}
def diff(poly, i):
    result={}
    for p,c in poly.items():
        if p[i]:
            q=list(p); q[i]-=1; result[tuple(q)]=c*p[i]
    return result
def evaluate(poly, point):
    result=0
    for p,c in poly.items():
        for a,e in zip(point,p): c*=a**e
        result+=c
    return result
def determinant(matrix):
    size=len(matrix); result={}
    for permutation in permutations(range(size)):
        inversions=sum(permutation[i]>permutation[j] for i in range(size) for j in range(i+1,size))
        term={(0,)*4:(-1)**inversions}
        for i,j in enumerate(permutation): term=mul(term,matrix[i][j])
        result=add(result,term)
    return result
def rank(matrix):
    m=[[Fraction(v) for v in row] for row in matrix]; r=0
    for col in range(len(m[0])):
        pivot=next((i for i in range(r,len(m)) if m[i][col]),None)
        if pivot is None: continue
        m[r],m[pivot]=m[pivot],m[r]
        f=m[r][col]; m[r]=[v/f for v in m[r]]
        for i in range(len(m)):
            if i!=r:
                f=m[i][col]; m[i]=[a-f*b for a,b in zip(m[i],m[r])]
        r+=1
    return r
def serialize(poly):
    return [{'powers':list(p),'coefficient':c} for p,c in sorted(poly.items())]

A,B,C,L=[{tuple(int(i==j) for j in range(4)):1} for i in range(4)]
E=[A,add(B,L),C]
elementary=[{(0,)*4:1},{},{},{}]
for value in E:
    for d in range(3,0,-1): elementary[d]=add(elementary[d],mul(value,elementary[d-1]))
coefficients=[elementary[1],elementary[2],add(elementary[3],scale(mul(mul(A,B),C),-1)),A,mul(A,C)]
jacobian=[[diff(poly,i) for i in range(4)] for poly in coefficients]
point=(2,1,3,1)
numeric=[[evaluate(poly,point) for poly in row] for row in jacobian]
assert numeric==[[1,1,1,1],[5,5,4,5],[3,0,2,6],[1,0,0,0],[3,0,2,0]]
minors=[]
for rows in combinations(range(5),4):
    poly=determinant([jacobian[i] for i in rows])
    minors.append({'rows_1_based':[i+1 for i in rows],'polynomial':serialize(poly),'at_point':evaluate(poly,point)})
chosen=determinant([jacobian[i] for i in (0,2,3,4)])
assert chosen=={(2,0,1,0):-1}
assert rank(numeric)==4
assert evaluate(add(B,L,scale(A,-1)),point)==0
values=[evaluate(poly,point) for poly in coefficients]
assert values==[7,16,6,2,6]
result={'variables':['k21','k32','k13','k02'],'point':point,'coefficient_values':values,
        'coefficient_polynomials':[serialize(p) for p in coefficients],
        'jacobian_at_point':numeric,'maximal_minors':minors,'rank_over_Q':rank(numeric),
        'hyperplane_residual':0,'all_rates_positive':all(v>0 for v in point),
        'passed':True,'elapsed_seconds':time.monotonic()-start,
        'maxrss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'api_dollars':0}
Path(__file__).with_name('exact-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['coefficient_values','jacobian_at_point','rank_over_Q','hyperplane_residual','passed','elapsed_seconds','maxrss_bytes','api_dollars']},indent=2))
print('Maximal minors at point:',[m['at_point'] for m in minors])
