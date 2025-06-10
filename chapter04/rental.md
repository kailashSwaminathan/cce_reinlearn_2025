# jack's car rental

Let $p_{req1}$ be the poisson probability function of number of car requests at location 1.
```math
$$
\begin{equation}
\begin{aligned}
v_1(n) &= \sum_{r=0}^{20} p_{req1}(r) \left[ \min(n,r) \cdot 10 + \gamma v_1(n - \min(n,r)) \right]  \\
n &\in \{0, 1, \dots, 20\}
\end{aligned}
\end{equation}
$$
```

Let $p_{drop1}$ be the poisson probability function of the number of car dropoffs at location 1.
```math
$$
\begin{equation}
\begin{aligned}
v_1(n) &= \sum_{r=0}^{20} \sum_{d=0}^{20} p_{req1}(r) \cdot p_{drop1}(d) \left[ \min(n,r) \cdot 10 + \gamma v_1(n - \min(n,r) + d) \right] \\
n &\in \{ 0, 1, \dots, 20 \}
\end{aligned}
\end{equation}
$$
```
The reward function is computed as
```math
\begin{equation}
\begin{aligned}
R(n) = \sum_{k=0}^{20} p_{req}(k) \cdot \min(n,k) \cdot 10
\end{aligned}
\end{equation}
```