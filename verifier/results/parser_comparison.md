# Parser bake-off

| parser | our cleanup first | correct parses | keeps written form | ms / parse |
|---|---|---|---|---|
| sympy-lark | no | 34/42 | 0/4 | 29.6 |
| sympy-lark | yes | 36/42 | 0/4 | 37.4 |
| latex2sympy2_extended | no | 38/42 | 4/4 | 13.4 |
| latex2sympy2_extended | yes | 42/42 | 4/4 | 5.8 |

- sympy-lark (without our cleanup) gets wrong: `x(x-4)`, `2\left(x - 4\right) + 3(x + 1)`, `\cos(3x^2) \cdot 6x`, `3x^2 \sin x + x^3 \cos x`, `e^{2x}`, `2^{3}x`, `\pi r^2`, `−2x + 1`
- sympy-lark (after our cleanup) gets wrong: `x(x-4)`, `\cos(3x^2) \cdot 6x`, `3x^2 \sin x + x^3 \cos x`, `e^{2x}`, `2^{3}x`, `\pi r^2`
- latex2sympy2_extended (without our cleanup) gets wrong: `\left(x+1\right)^2`, `2\left(x - 4\right) + 3(x + 1)`, `2(3)`, `\frac12`
