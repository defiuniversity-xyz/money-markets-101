# Money Markets GitBook - Infographic Specifications

## Overview

This document outlines the visual assets required for the Money Markets GitBook course. Infographics will enhance understanding of complex concepts including architecture diagrams, mathematical formulas, risk metrics, and protocol comparisons.

## Asset Categories

### 1. Architecture Diagrams

#### Monolithic vs Modular Architecture
- **Asset ID**: `mm01_01_architecture_comparison`
- **Type**: Diagram
- **Placement**: Lesson 1
- **Description**: Visual comparison of monolithic (Aave) vs modular (Morpho) architectures showing liquidity pools vs isolated markets

#### Aave V4 Hub and Spoke Model
- **Asset ID**: `mm05_01_aave_v4_hub_spoke`
- **Type**: Diagram
- **Placement**: Lesson 5
- **Description**: Visual representation of Aave V4's unified liquidity hub with multiple spokes

#### Morpho Blue Market Structure
- **Asset ID**: `mm06_01_morpho_blue_structure`
- **Type**: Diagram
- **Placement**: Lesson 6
- **Description**: Diagram showing isolated lending markets in Morpho Blue

#### Euler Vault Kit Architecture
- **Asset ID**: `mm07_01_euler_vault_kit`
- **Type**: Diagram
- **Placement**: Lesson 7
- **Description**: Visual of EVK and EVC architecture with sub-accounts

### 2. Mathematical Visualizations

#### Health Factor Formula
- **Asset ID**: `mm02_01_health_factor_formula`
- **Type**: Formula Visualization
- **Placement**: Lesson 2
- **Description**: Visual breakdown of Health Factor calculation with examples

#### Interest Rate Curve (Kinked Model)
- **Asset ID**: `mm02_02_interest_rate_curve`
- **Type**: Chart
- **Placement**: Lesson 2
- **Description**: Graph showing utilization rate vs interest rates with kink point

#### Utilization Impact Chart
- **Asset ID**: `mm02_03_utilization_impact`
- **Type**: Chart
- **Placement**: Lesson 2
- **Description**: Visual showing how utilization affects supply and borrow rates

### 3. Risk Management Visuals

#### Liquidation Mechanics Flow
- **Asset ID**: `mm03_01_liquidation_flow`
- **Type**: Flowchart
- **Placement**: Lesson 3
- **Description**: Step-by-step visual of liquidation process

#### Health Factor Zones
- **Asset ID**: `mm03_02_hf_zones`
- **Type**: Diagram
- **Placement**: Lesson 3
- **Description**: Color-coded zones showing safe, warning, danger, and critical Health Factor ranges

#### Risk Assessment Matrix
- **Asset ID**: `mm03_03_risk_matrix`
- **Type**: Matrix
- **Placement**: Lesson 3
- **Description**: Visual risk assessment framework

### 4. Protocol Comparison Charts

#### Protocol Feature Matrix
- **Asset ID**: `mm08_01_protocol_comparison`
- **Type**: Comparison Table
- **Placement**: Lesson 8
- **Description**: Side-by-side comparison of Aave, Morpho, Euler, Kamino, Suilend, JustLend

#### Architecture Comparison
- **Asset ID**: `mm01_02_architecture_features`
- **Type**: Comparison Chart
- **Placement**: Lesson 1
- **Description**: Visual comparison of key features between monolithic and modular

### 5. Operational Guides

#### First Position Setup Flow
- **Asset ID**: `mm04_01_position_setup_flow`
- **Type**: Flowchart
- **Placement**: Lesson 4
- **Description**: Step-by-step visual guide for setting up first position

#### Monitoring Dashboard Mockup
- **Asset ID**: `mm04_02_monitoring_dashboard`
- **Type**: Mockup
- **Placement**: Lesson 4
- **Description**: Example dashboard showing key metrics to monitor

#### Rebalancing Decision Tree
- **Asset ID**: `mm09_01_rebalancing_tree`
- **Type**: Decision Tree
- **Placement**: Lesson 9
- **Description**: Flowchart for deciding when and how to rebalance

### 6. Advanced Strategy Visuals

#### Looping Strategy Diagram
- **Asset ID**: `mm09_02_looping_strategy`
- **Type**: Flowchart
- **Placement**: Lesson 9
- **Description**: Visual representation of looping strategy with steps

#### Yield Optimization Framework
- **Asset ID**: `mm09_03_yield_framework`
- **Type**: Framework Diagram
- **Placement**: Lesson 9
- **Description**: Visual framework for yield optimization decisions

#### Portfolio Diversification Chart
- **Asset ID**: `mm10_01_portfolio_diversification`
- **Type**: Pie/Donut Chart
- **Placement**: Lesson 10
- **Description**: Visual allocation across protocols and strategies

### 7. Exercise Visuals

#### Calculation Templates
- **Asset ID**: `ex02_01_calculation_template`
- **Type**: Template
- **Placement**: Exercise 2
- **Description**: Fill-in-the-blank calculation worksheet template

#### Risk Assessment Template
- **Asset ID**: `ex03_01_risk_template`
- **Type**: Template
- **Placement**: Exercise 3
- **Description**: Risk assessment worksheet

## Technical Specifications

### Dimensions
- **Standard**: 1920x1080px (16:9 aspect ratio)
- **Wide Format**: 2400x1350px (for complex diagrams)
- **Square Format**: 1200x1200px (for comparison charts)

### Format
- **Primary**: PNG (high resolution, transparent background where appropriate)
- **Alternative**: SVG (for scalable diagrams)

### Style Guidelines
- Clean, professional design
- Consistent color scheme across all assets
- Clear typography (readable at small sizes)
- Icons and symbols for visual consistency
- Brand colors for different protocols (if applicable)

## Implementation Notes

### Priority Assets
1. Health Factor Formula visualization (Lesson 2)
2. Monolithic vs Modular comparison (Lesson 1)
3. Liquidation mechanics flow (Lesson 3)
4. Protocol comparison matrix (Lesson 8)
5. First position setup flow (Lesson 4)

### Future Enhancements
- Interactive calculators (web-based)
- Animated GIFs for complex processes
- 3D visualizations for architecture diagrams
- Video walkthroughs for operational guides

## Asset Generation Plan

### Phase 1: Core Concepts (Lessons 1-4)
- Architecture comparisons
- Mathematical formulas
- Risk management visuals
- Setup guides

### Phase 2: Protocols (Lessons 5-8)
- Protocol-specific architecture
- Feature comparisons
- Operational diagrams

### Phase 3: Advanced Topics (Lessons 9-12)
- Strategy frameworks
- Optimization visuals
- System architecture

## Integration

All images will be integrated into markdown files using relative paths:
- Lessons: `images/lessons/lesson_XX/`
- Exercises: `images/exercises/exercise_XX/`

Images will eventually be hosted on Google Cloud Storage (similar to liquidity provision GitBook) for production deployment.

