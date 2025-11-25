# Exercise 1: Money Markets Knowledge Assessment

⏰ Time Investment: 30-45 minutes  
🎯 Goal: Test your understanding of money market fundamentals and identify knowledge gaps

📚 Required Reading Integration  
📖 Primary: Lesson 1: Understanding DeFi Money Markets Fundamentals  
📖 Supporting: Lesson 2: The Mathematics of Lending and Borrowing

## 🔍 Phase 1: Knowledge Check (10 minutes)

### Understanding Check

Answer these questions to assess your comprehension:

**1. What is the fundamental difference between monolithic and modular money market architectures?**
   - Your answer: _________________________________

**2. How does over-collateralization protect lenders?**
   - Your answer: _________________________________

**3. What are the two paths to Aave and when would you use each?**
   - Your answer: _________________________________

**4. Why can't you be liquidated if you're only supplying assets (not borrowing)?**
   - Your answer: _________________________________

**5. What is the difference between LTV (Loan-to-Value) and Liquidation Threshold?**
   - Your answer: _________________________________

## 📊 Phase 2: Architecture Comparison (15 minutes)

### Monolithic vs Modular Analysis

**Scenario**: You're evaluating two protocols for a $10,000 USDC deposit.

**Protocol A (Monolithic)**:
- Single shared liquidity pool
- Governance manages all parameters
- All assets in same pool
- Insurance fund covers all markets

**Protocol B (Modular)**:
- Isolated markets per asset pair
- Permissionless market creation
- Risk isolated to each market
- No shared insurance fund

**Exercise 1**: Compare the risks and benefits of each approach:

| Factor | Monolithic (Protocol A) | Modular (Protocol B) |
|--------|------------------------|---------------------|
| Risk Isolation | | |
| Capital Efficiency | | |
| Ease of Use | | |
| Flexibility | | |

**Exercise 2**: Which would you choose for your first position and why?

- Your choice: _________________________________
- Reasoning: _________________________________


![Architecture Comparison Template](https://storage.googleapis.com/money-markets-gitbook-images/exercises/exercise_01/ex01_01_architecture_comparison_template.png)


## 💡 Phase 3: Real-World Application (10 minutes)

### Protocol Selection Exercise

You want to earn yield on $5,000 USDC. Analyze these options:

**Option 1**: Aave App
- APY: 6.5%
- Insurance: $1M coverage
- Interface: Mobile app, simple
- Network: Ethereum (via app)

**Option 2**: Aave V3 on Arbitrum
- APY: 5%
- Insurance: Safety Module (shared)
- Interface: Web dApp
- Network: Arbitrum (low gas)

**Option 3**: Morpho Vault
- APY: 5.5%
- Insurance: None (isolated markets)
- Interface: Web dApp
- Network: Ethereum

**Exercise 3**: Compare and rank these options for a beginner:

**Ranking** (1 = Best, 3 = Least suitable):
- Option 1: ___ 
- Option 2: ___
- Option 3: ___

**Reasoning for #1 choice**: _________________________________

## 📝 Phase 4: Key Concepts Review (10 minutes)

### Fill in the Blanks

**1. The _______________ model pools all assets together, while the _______________ model isolates markets.**

**2. When you supply assets to a protocol, you receive _______________ tokens that represent your deposit.**

**3. The _______________ is the percentage of the pool currently lent out and drives interest rates.**

**4. _______________ are bridges that feed off-chain price data to on-chain smart contracts.**

**5. The Aave App uses a "_____________" strategy: Fintech in the front, DeFi in the back.**

## ✅ Self-Assessment

Rate your understanding (1 = Need more review, 5 = Fully understand):

- [ ] Money market fundamentals: __/5
- [ ] Monolithic vs modular architectures: __/5
- [ ] Basic operational concepts: __/5
- [ ] Protocol selection criteria: __/5

**Areas needing more review**: _________________________________

## 🎯 Next Steps

If you scored < 4 on any topic:
- Review Lesson 1 material on that topic
- Re-read the Beginner's Corner sections
- Look up additional resources on unclear concepts

If all topics ≥ 4:
- Proceed to Exercise 2 (Calculation Practice)
- Move forward with confidence!

---

[← Back to Summary](../SUMMARY.md) | [Next: Lesson 2 →](../lessons/lesson-02-the-mathematics-of-lending-and-borrowing.md)

