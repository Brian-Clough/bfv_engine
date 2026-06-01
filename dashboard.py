import streamlit as st
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from bfv.statistics.execution import BetaBinomialExecutionModel
from bfv.statistics.permanence import WeibullPermanenceModel
from bfv.statistics.engine import BFVEngine
from bfv.models.specs import ProjectSpecification
from bfv.portfolio.optimizer import BFVPortfolioOptimizer

st.set_page_config(page_title="BFV Secretariat Platform", layout="wide", page_icon="🌍")

st.title("🌍 BFV Framework: Institutional Translation Layer")
st.markdown("### **Secretariat Risk Accounting & Asset Validation Dashboard**")
st.markdown("This platform serves as the **Institutional Translation Layer**, programmatically converting raw dMRV data streams and scientific uncertainty bounds into immutable, risk-adjusted registry issuance vectors.")
st.write("---")

engine = BFVEngine(BetaBinomialExecutionModel(), WeibullPermanenceModel())
BASELINE_NOMINAL_UNITS = 10000.0

tab1, tab2, tab3 = st.tabs(["📋 Use Case 1: Project Risk Rating Engine", "🏛️ Use Case 2: Three-Tiered Registry Solvency Bank", "📈 Use Case 3: Investor Portfolio Budget Optimizer"])

with tab1:
    st.header("Asset Risk Analysis & Verification Protocol")
    selected_project = st.selectbox("📁 Select Active Pipeline Asset Validation Scenario:", ["Asset Profile 1: Industrial Improved Forest Management (IFM)", "Asset Profile 2: Volatile Blue Carbon Mangrove Restoration", "Asset Profile 3: Frontier Direct Air Capture (DAC) Facility"])
    st.write("---")

    if "Industrial IFM" in selected_project:
        project_id, project_type = "ifm-forestry-404", "Industrial IFM (Forestry)"
        milestones = [1] * 18 + [0] * 2
        rate_100yr, k_shape, science_input, co_benefits = 0.04, 1.4, {"mean": 0.88, "variance": 0.003}, 0.05
        description_text = "**Scenario Dynamics:** Strong performance history but exposed to an increasing wildfire hazard trajectory over time ($k = 1.4$). Scientific accounting models carry standard measurement error variance."
    elif "Blue Carbon" in selected_project:
        project_id, project_type = "mangrove-coastal-03", "Blue Carbon (Mangrove Restoration)"
        milestones = [1] * 4 + [0] * 3
        rate_100yr, k_shape = 0.02, 1.1
        np.random.seed(42)
        science_input = np.random.normal(loc=0.75, scale=0.09, size=1000).tolist()
        co_benefits = 0.25
        description_text = "**Scenario Dynamics:** Early-stage project exhibiting highly volatile performance execution metrics and large scientific carbon baseline uncertainty. High ecosystem co-benefits ($\\Omega = 0.25$)."
    else:
        project_id, project_type = "dac-removal-001", "Frontier Direct Air Capture (DAC)"
        milestones = [1] * 12
        rate_100yr, k_shape, science_input, co_benefits = 0.0, 1.0, 0.98, 0.0
        description_text = "**Scenario Dynamics:** High-cost technical removal facility displaying absolute, permanent geological sequestration capability ($P(P) = 1.0$) and tight scientific measurement confidence bounds."

    col_left, col_right = st.columns([1, 1.2], gap="large")
    with col_left:
        st.subheader("⚙️ Verified dMRV Pillar Probabilities")
        st.info(description_text)
        spec = ProjectSpecification(project_id, project_type, BASELINE_NOMINAL_UNITS, milestones, rate_100yr, k_shape, science_input, co_benefits)
        results = engine.calculate_fair_value(**spec.to_engine_inputs(), num_simulation_samples=2000)
        
        if isinstance(science_input, dict): display_science_mean = float(science_input["mean"])
        elif isinstance(science_input, list): display_science_mean = float(np.mean(science_input))
        else: display_science_mean = float(science_input)

        st.markdown("#### **Execution Probability $P(E)$**")
        st.success(f"**Expected Mean: {results['p_execution_mean']:.3f}**")
        st.markdown("#### **Scientific Confidence $P(S)$**")
        st.success(f"**Expected Mean: {display_science_mean:.3f}**")
        st.markdown("#### **Permanence Probability $P(P)$**")
        st.success(f"**Expected Mean: {results['p_permanence_mean']:.3f}**")
        st.markdown("#### **Ecosystem Co-Benefits Scalar $\\Omega$**")
        st.success(f"**Symmetric Scalar Value: {co_benefits:+.2f}**")

    with col_right:
        st.subheader("📊 Statistical Value Propagation & Supply Directive")
        m1, m2 = st.columns(2)
        m1.metric("Final BFV Unit Rating Value", f"{results['bfv_unit_value']:.4f}")
        m2.metric("Joint Delivery Coeff ($E[\\Theta]$)", f"{results['expected_delivery_coefficient']:.3f}")
        
        if "_raw_bfv_distribution" in results:
            st.markdown("**Predicted Bayesian Fair Value Posterior Distribution:**")
            counts, bin_edges = np.histogram(results["_raw_bfv_distribution"], bins=15)
            st.bar_chart(data=np.atleast_2d(counts).T)
            st.caption("Monte Carlo density map showing asset value dispersion under full error propagation accounting.")
        else:
            st.markdown("**Predicted Bayesian Fair Value Distribution:**")
            st.info("💡 Degenerate Single Point Estimate: Asset carries 100% mathematical certainty variables.")

        st.write("---")
        st.subheader("🏛️ Automated Token Issuance Directive")
        st.markdown(f"**Baseline Evaluation Budget Pool:** `{BASELINE_NOMINAL_UNITS:,.0f} Nominal Tons`")
        l1, l2 = st.columns(2)
        with l1: st.info(f"### 📈 Circulating Supply\n**{results['issuable_bfv_units']:,.2f} Credits**")
        with l2: st.warning(f"### 🔒 Safety Escrow Reserve\n**{results['escrow_retained_units']:,.2f} Credits**")
        p05_val = results.get("bfv_5th_percentile", results["bfv_unit_value"])
        st.markdown(f"🛡️ **95% Confidence Portfolio Asset Floor Value:** `{p05_val * BASELINE_NOMINAL_UNITS:,.2f} Risk-Adjusted Tons`")

with tab2:
    st.header("🏛️ The Three-Tiered Dynamic Uncertainty Bank")
    st.markdown("Demonstrating how a Registry Secretariat manages systemic solvency balance sheets. When an asset undergoes an active change, credits are programmatically re-balanced across our multi-tiered risk stack.")
    st.write("---")
    st.subheader(f"Active Systemic Ledger Balance Breakdown: {project_type}")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.info("### 📈 Layer 1: Project Escrow")
        st.markdown(f"**Reserved Balance:** `{results['escrow_retained_units']:,.2f} Credits`")
        st.caption("Holds back an asset-specific fraction matching the calculated Integrity Gap ($1 - BFV$) to insulate buyers from forward default.")
    with t2:
        l2_buffer = results['escrow_retained_units'] * 0.10
        st.success("### 🤝 Layer 2: Central Buffer Pool")
        st.markdown(f"**Pooled Contribution:** `{l2_buffer:,.2f} Credits`")
        st.caption("A mutualized cross-project liquidity pool designed to absorb localized project shocks by extending credit bridge loans.")
    with t3:
        st.warning("### 🛡️ Layer 3: Insurance Backstop")
        st.markdown("**Status:** `Standby Contingent Capital Locked`")
        st.caption("External systemic capital injections (commercial reinsurance) that activate only if lower layers face exhaustion.")
    st.write("---")
    st.success("💡 **Talking Point for the Director:** This framework transforms the registry from a passive, static ledger into an active, credit-solvency state machine driven by live dMRV monitoring logs.")

with tab3:
    st.header("📈 Commercial Capital Allocation Sandbox")
    st.markdown("How the Secretariat helps institutional carbon investors minimize downside delivery risk. This engine runs a joint Monte Carlo search to optimize a **$10,000,000 budget** across decoupled credit cost curves.")
    st.write("---")
    c1, c2 = st.columns([1, 1.2], gap="large")
    with c1:
        st.subheader("💵 Financial Price Parameter Matrix")
        st.markdown("Adjust these commercial prices to see how the optimizer re-balances capital weights:")
        price_dac = st.slider("Frontier DAC Removal Credit Cost ($/Ton)", 200, 600, 450)
        price_nature = st.slider("Industrial Forestry Credit Cost ($/Ton)", 10, 50, 18)
        price_blue = st.slider("Blue Carbon Mangrove Credit Cost ($/Ton)", 20, 100, 35)
    with c2:
        st.subheader("💼 Optimized Strategic Allocations")
        optimizer = BFVPortfolioOptimizer(engine=engine)
        milestones_dac, milestones_nat, milestones_blu = [1] * 12, [1] * 18 + [0] * 2, [1] * 4 + [0] * 3
        s_dac = ProjectSpecification("dac", "DAC Removal", 1.0, milestones_dac, 0.0, 1.0, 0.98, 0.0)
        s_nat = ProjectSpecification("nat", "Forestry (IFM)", 1.0, milestones_nat, 0.04, 1.4, {"mean": 0.88, "variance": 0.003}, 0.05)
        s_blu = ProjectSpecification("blu", "Blue Carbon", 1.0, milestones_blu, 0.02, 1.1, 0.75, 0.25)
        opt_res = optimizer.optimize_allocation([s_dac, s_nat, s_blu], total_budget=10000000.0, project_prices={"dac": price_dac, "nat": price_nature, "blu": price_blue})
        for pid, alloc in opt_res["portfolio_allocation_breakdown"].items():
            st.info(f"### **{alloc['asset_type']}**\n * **Budget Weight:** `{alloc['budget_weight_percentage']}%`\n * **Capital Committed:** `${alloc['capital_allocated_dollars']:,}`")
        st.caption("Allocation weights are derived on the fly by maximizing the ratio of forward expected BFV yield to downside 95th percentile Value-at-Risk (VaR).")
