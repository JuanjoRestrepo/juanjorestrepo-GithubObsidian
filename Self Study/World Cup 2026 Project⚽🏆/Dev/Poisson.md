
# Poisson Goal Model

Modelamos:

- $\lambda_{home} = E[goles\_home]$
- $\lambda_{away} = E[goles\_away]$

Luego:

$$
P(score = i,j) = Poisson(i, \lambda_{home}) \cdot Poisson(j, \lambda_{away})
$$

Y de ahí:

- $Win → i>j$
- $Draw → i=j$
- $Loss → i<j$

