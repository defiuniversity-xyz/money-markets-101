{% embed url="https://storage.googleapis.com/money-markets-media/lesson-07/audio/lesson7%20Euler_Finance_Rebuild_Ultimate_DeFi_Security.m4a" %}

{% embed url="https://storage.googleapis.com/money-markets-media/lesson-07/video/lesson7%20Euler__%24197M_Rebirth.mp4" %}

# Lesson 7: Euler and Advanced Customization

## 🎯 Core Concept: The Resilient Toolkit

Euler Finance's story is defined by resilience. After a $197M exploit in v1, Euler spent 18 months rebuilding from scratch, launching v2 in 2025 as one of the most secure and modular lending protocols—boasting 31+ audits and massive security competitions.

**Key Innovation**: Euler Vault Kit (EVK) + Ethereum Vault Connector (EVC) enable highly customized, permissionless vault creation with sub-accounts for granular risk isolation.

## 📜 The Evolution: v1 to v2

### Euler v1: The Monolithic Era

**What It Was**:
- Permissionless lending protocol
- Uniswap v3 TWAP oracles (allowed any asset)
- Shared state across all assets
- Three-tier system (Isolation, Cross, Collateral)

**The Failure** (March 2023):
- $197M exploit via donateToReserves function
- Missing invariant check allowed debt-free donations
- Highlighted risks of tightly coupled logic
- Shared state meant one failure affected everything

**The Recovery**:
- Funds recovered through negotiation
- Team committed to complete rebuild
- 18-month development cycle
- Result: Euler v2

### Euler v2: The Modular Rebirth

**The Paradigm Shift**: From "Pool" to "Vault" architecture

**Core Changes**:
- Independent ERC-4626 vaults (not single pool)
- Each vault manages own solvency
- Risk isolation at vault level
- Permissionless vault creation

## 🏗️ The Architecture: EVK and EVC

### Euler Vault Kit (EVK)

**What It Is**: Factory for deploying ERC-4626 compliant lending vaults

**Capabilities**:
- Custom asset/liability logic
- Flexible interest rate models (linear, kinked, PID-controlled)
- Oracle agnostic (any oracle adapter)
- Nested vaults (vault shares as collateral)

**Example Use Cases**:
- Standard lending vault (like Aave)
- Synthetic asset vaults
- Sub-collateralized loans
- Complex reward structures

### Ethereum Vault Connector (EVC)

**What It Is**: Communication layer enabling vault interoperability

**Key Features**:
1. **Sub-Accounts**: Use deposits in Vault A as collateral for loan in Vault B
2. **Unified Account View**: Check solvency across all enabled vaults
3. **Flash Liquidity**: Flash loans across entire ecosystem
4. **Defer Checks**: Batch operations, check solvency at end (gas savings)

**The Power**: Combines Aave's cross-margin efficiency with Morpho's isolation benefits.


![Euler Vault Kit Architecture](https://storage.googleapis.com/money-markets-gitbook-images/lessons/lesson_07/mm07_01_euler_vault_kit_architecture.png)


## 🎛️ Vault Classes: Risk Segmentation

### Core Vaults

**Characteristics**:
- Governed by Euler DAO or high-reputation curators (Gauntlet)
- Blue-chip assets (USDC, WETH, WBTC)
- Reliable oracles (Chainlink)
- Cross-collateralization enabled

**Best For**: Institutional liquidity, conservative strategies

### Edge Vaults

**Characteristics**:
- Permissionless, ungoverned
- Long-tail assets (meme coins, niche tokens)
- Custom oracle configurations
- Risk isolation (can't affect Core vaults)

**Best For**: Experimental strategies, high-risk tolerance

### Escrow Vaults

**Innovation**: Accept assets as collateral but don't lend them out

**Use Cases**:
- Governance tokens (borrow without losing voting power)
- Rebasing tokens (complex transfer mechanics)
- Assets with no yield (need liquidity, not interest)

**Result**: Safe harbor for collateral types v1 couldn't support


![Euler Vault Classes Diagram](https://storage.googleapis.com/money-markets-gitbook-images/lessons/lesson_07/mm07_02_euler_vault_classes_diagram.png)


## 🔒 Managed vs Trustless Vaults

### Trustless Vaults

**Characteristics**:
- Immutable parameters (set at deployment)
- No curator control
- "Set and forget"
- Best for: Robust, well-understood pairs

**Example**: ETH/USDC vault with immutable 80% LTV, Chainlink oracle

### Managed Vaults

**Characteristics**:
- Risk Curator can adjust parameters dynamically
- Can respond to changing volatility
- Best for: Newer assets with evolving risk profiles

**Example**: New memecoin vault with curator adjusting LTV based on volatility

## 🔐 Sub-Accounts: Granular Risk Isolation

### How Sub-Accounts Work

**The Innovation**: Create virtually infinite sub-accounts under single wallet

**Use Cases**:
- **Account A**: Low-risk strategy (lending USDC only)
- **Account B**: High-risk strategy (borrowing against volatile tokens)
- **Isolation**: If Account B liquidated, Account A unaffected

**Comparison**: Superior to Aave's single-account model, offering Morpho-like isolation with Aave-like efficiency.

### EulerSwap Integration

**Feature**: DEX integrated directly into lending interface

**Capability**: Seamless looping—swap USDC for ETH and deposit as collateral in single atomic transaction

**Benefit**: Convenience
**Risk**: Encourages leverage—use with caution


![Sub-Account Risk Isolation](https://storage.googleapis.com/money-markets-gitbook-images/lessons/lesson_07/mm07_03_sub_account_risk_isolation.png)


## 🛡️ Oracle Freedom

### Oracle Agnosticism

**Unlike Aave**: Not limited to Chainlink

**Options**:
- Chainlink (established, reliable)
- Pyth Network (high-frequency, low-latency)
- RedStone (on-demand updates)
- Custom oracles

**Result**: Can list long-tail assets Chainlink doesn't cover

## ⚠️ Operational Considerations

### Verified vs Ungoverned Vaults

**For Beginners**: Stick to Verified/Governed vaults only

**Why**:
- Verified vaults have risk managers
- Can adjust parameters if conditions change
- Better documented and audited

**Ungoverned Vaults**:
- Immutable parameters
- No human intervention possible
- If flaw found in parameters, can't fix
- "Purely decentralized" but dangerous for beginners

### Due Diligence Checklist

Before depositing into Euler vault:
1. ✅ Is vault verified/governed or ungoverned?
2. ✅ What's the curator's track record?
3. ✅ What oracle does it use? Is it reliable?
4. ✅ What are the LTV/risk parameters?
5. ✅ Is there documentation/audit?

## 📊 Euler vs Competitors

| Feature | Aave | Morpho | Euler v2 |
|---------|------|--------|----------|
| Architecture | Monolithic pools | Isolated markets | Modular vaults |
| Customization | Limited (governance) | Market parameters | Full vault control |
| Sub-Accounts | No | No | Yes |
| Oracle Choice | Primarily Chainlink | Oracle agnostic | Oracle agnostic |
| Vault Nesting | No | Limited | Yes (nested vaults) |
| Gas Efficiency | Medium | High | Medium-High |

## 🎯 When to Use Euler

### Best For:
- ✅ Advanced users wanting customization
- ✅ Strategies requiring sub-accounts
- ✅ Long-tail assets not on other protocols
- ✅ Complex nested strategies

### Not Ideal For:
- ❌ Beginners (start with Aave)
- ❌ Users wanting simplicity
- ❌ Those uncomfortable with vault selection

## 🚀 Getting Started with Euler

### Step 1: Choose a Vault

**For Beginners**: Start with Core vaults (verified, governed)
- Standard USDC/ETH pairs
- Established curators
- Chainlink oracles

### Step 2: Understand the Vault

1. Check if verified or ungoverned
2. Review curator documentation
3. Understand risk parameters
4. Check oracle reliability

### Step 3: Use Sub-Accounts

1. Create separate accounts for different strategies
2. Isolate risk between positions
3. Monitor each account independently

### Step 4: Monitor

- Check vault parameters regularly
- Monitor curator updates (if managed)
- Review sub-account health factors

## 🎓 Beginner's Corner

**Q: Is Euler safe after the v1 exploit?**
A: v2 is a complete rebuild with 31+ audits. Architecture fundamentally different (modular vs monolithic).

**Q: Should I use ungoverned vaults?**
A: No, as a beginner. Stick to verified/managed vaults with curators.

**Q: What are sub-accounts good for?**
A: Risk isolation. Keep high-risk and low-risk strategies separate.

## 🔬 Advanced Deep-Dive: Nested Vaults

### How Nesting Works

**Mechanism**: Vault shares (ERC-20 tokens) can be deposited into other vaults

**Example**:
1. Deposit USDC into Core USDC Vault → Receive eUSDC
2. Deposit eUSDC into RWA Vault as collateral
3. Borrow tokenized treasuries

**Result**: Recursive leverage and "fund of funds" structures natively supported.

## 📈 Real-World Example

**Scenario**: Using Euler sub-accounts for risk isolation

**Account A (Conservative)**:
- Supply: $10,000 USDC
- Strategy: Earn yield only
- Risk: Low

**Account B (Aggressive)**:
- Collateral: $5,000 ETH
- Borrowed: $3,000 USDC (60% LTV)
- Strategy: Trading
- Risk: High

**Isolation**: If Account B liquidated, Account A completely unaffected.

## 🎯 Key Takeaways

1. **Euler v2** is a complete rebuild after v1 exploit
2. **EVK + EVC** enable highly customizable vaults
3. **Sub-accounts** provide granular risk isolation
4. **Vault classes** (Core/Edge/Escrow) segment risk
5. **Stick to verified vaults** as a beginner
6. **Oracle freedom** enables long-tail asset listing

## 🚀 Next Steps

Lesson 8 explores alternative chain protocols—Kamino (Solana), Suilend (Sui), and JustLend (Tron)—showing how high-performance chains handle money markets differently.

Complete **Exercise 7** to practice Euler market creation and risk analysis.

---

**Remember**: Euler offers maximum customization but requires deep understanding. Master Aave and Morpho first, then explore Euler for advanced strategies.

[← Back to Summary](../SUMMARY.md) | [Next: Exercise 7 →](../exercises/exercise-07-euler-market-creation-and-risk-analysis.md) | [Previous: Lesson 6 ←](lesson-06-morpho-modular-lending-infrastructure.md)

