# Convert Markdown to PDF Test
## Headline test

Text *Test*: **Convert Markdown to PDF**

### LaTeX Test

$$
P_d(ad) = η_0 \cdot \left(1 + \alpha \cdot A_{age} + \beta \cdot \frac{L_{current}}{L_{max}} + \gamma \cdot \frac{S_{density}}{S_{max}}\right)
$$

### Graph Test

```mermaid
graph TD
    A[Ad Post Generation] --> B{Survival Check}
    B -->|Every Time Step| C[Calculate P_d]
    C --> D{Random Number < P_d?}
    D -->|Yes| E[Mark for Deletion]
    D -->|No| F[Continue Survival]
```
### Table Test

| Parameter                  | Type             | Description                                      |
|----------------------------|------------------|--------------------------------------------------|
| `Global Detection Base η₀` | Environment Variable | Base detection probability (0.1-0.9)             |
| `Time Sensitivity α`       | Environment Variable | Coefficient for ad survival time impact (default 0.05) |
| `Popularity Penalty β`     | Environment Variable | Coefficient for like growth penalty (default 0.02)     |
| `Coordination Penalty γ`   | Environment Variable | Coefficient for shill density penalty (default 0.01)   |
