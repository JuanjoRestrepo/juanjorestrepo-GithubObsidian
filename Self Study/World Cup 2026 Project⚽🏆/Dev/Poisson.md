
# Poisson Goal Model

Modelamos:

- $\lambda_{home} = E[goles\_home]$
- $\lambda_{away} = E[goles\_away]$

Luego:

$P(score=i,j)=Poisson(i,λhome)⋅Poisson(j,λaway)P(score = i,j) = Poisson(i, \lambda_{home}) \cdot Poisson(j, \lambda_{away})P(score=i,j)=Poisson(i,λhome​)⋅Poisson(j,λaway​)$

Y de ahí:

- Win → i>ji > ji>j
- Draw → i=ji = ji=j
- Loss → i<ji < ji<j