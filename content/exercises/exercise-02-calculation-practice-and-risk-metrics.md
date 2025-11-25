# Exercise 2: Calculation Practice and Risk Metrics

⏰ Time Investment: 45-60 minutes  
🎯 Goal: Master Health Factor calculations, LTV analysis, and interest rate mathematics

📚 Required Reading Integration  
📖 Primary: Lesson 2: The Mathematics of Lending and Borrowing  
📖 Supporting: Lesson 3: Risk Management Fundamentals

## 🔢 Phase 1: Health Factor Calculations (20 minutes)

### Basic HF Calculation

**Scenario**: You deposit 5 ETH @ $2,000/ETH and borrow $6,000 USDC
- Collateral: $10,000
- Debt: $6,000
- Liquidation Threshold: 85%

**Exercise 1**: Calculate Health Factor

Formula: $$HF = \frac{Collateral Value \times LT}{Total Debt}$$

- HF = (_____ × 0.85) ÷ _____ = _____

**Exercise 2**: What does this HF mean?
- Your answer: _________________________________

### HF with Price Changes

**Scenario**: ETH drops to $1,500

**Exercise 3**: Calculate new HF
- New collateral value: _____
- New HF = _____
- Status: _____ (Safe/Warning/Danger)

**Exercise 4**: At what ETH price would liquidation trigger? (HF = 1.0)
- Calculation: _____
- Liquidation price: $_____


![Health Factor Calculation Template](https://storage.googleapis.com/money-markets-gitbook-images/exercises/exercise_02/ex02_01_health_factor_calculation_template.png)


## 💧 Phase 2: Utilization and Interest Rates (15 minutes)

### Utilization Calculation

**Pool Statistics**:
- Total Supplied: 100 USDC
- Total Borrowed: 70 USDC

**Exercise 5**: Calculate utilization rate
- Utilization = _____ ÷ _____ = _____%

**Exercise 6**: If utilization is 70%, what happens to rates?
- Supply rate trend: _____
- Borrow rate trend: _____

### Interest Rate Impact

**Scenario**: Pool utilization spikes to 95% (above kink)

**Exercise 7**: What happens?
- Supply rate: _____ (increases dramatically)
- Borrow rate: _____ (increases dramatically)
- Risk: _____ (liquidity freeze possible)


![Utilization Rate Worksheet](https://storage.googleapis.com/money-markets-gitbook-images/exercises/exercise_02/ex02_02_utilization_rate_worksheet.png)


## 📊 Phase 3: LTV Analysis (10 minutes)

### Maximum Borrowing Capacity

**Scenario**: 
- Collateral: $20,000 ETH
- Maximum LTV: 75%
- Liquidation Threshold: 80%

**Exercise 8**: Calculate maximum borrow
- Max borrow = $20,000 × _____ = $_____

**Exercise 9**: If you borrow $12,000, what's your safety buffer?
- Current LTV: $12,000 ÷ $20,000 = _____%
- Safety buffer: _____% - _____% = _____%

## ✅ Self-Assessment

Rate your calculation skills:
- [ ] Health Factor calculations: __/5
- [ ] Utilization rate analysis: __/5
- [ ] LTV and safety buffer: __/5
- [ ] Interest rate dynamics: __/5

**Areas needing practice**: _________________________________

---

[← Back to Summary](../SUMMARY.md) | [Next: Exercise 3 →](exercise-03-risk-assessment-and-position-management.md)

