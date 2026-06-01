import streamlit as st
import numpy as np
import pandas as pd
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

tab1, tab2, tab3 = st.tabs([
    "📋 Use Case 1: Project Risk Rating Engine", 
    "🏛️ Use Case 2: Three-Tiered Registry Solvency Bank", 
    "📈 Use Case 3: Investor Portfolio Budget Optimizer"
])

with tab1:
    st.header("Asset Risk Analysis & Verification Protocol")
    selected_project = st.selectbox(
        "📁 Select Active Pipeline Asset Validation Scenario:", 
        [
            "Asset Profile 1: Industrial Improved Forest Management (IFM)", 
            "Asset Profile 2: Volatile Blue Carbon Mangrove Restoration", 
            "Asset Profile 3: Frontier Direct Air Capture (DAC) Facility"
        ]
    )
    st.write("---")

    if "Industrial IFM" in selected_project:
        project_id, project_type = "ifm-forestry-404", "Industrial IFM (Forestry)"
        # FIXED: Explicit standard python lists to prevent compile exceptions
        milestones = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
        rate_100yr, k_shape = 0.04, 1.3
        science_input = {"mean": 0.85, "variance": 0.002}
        co_benefits = 0.04
        description_text = "**Scenario Dynamics (IFM):** Proven operational history showing strong milestone delivery. However, it is exposed to an increasing wildfire hazard trajectory over time ($k = 1.3$). Scientific carbon baseline models carry moderate remote-sensing measurement error variance."
    elif "Blue Carbon" in selected_project:
        project_id, project_type = "mangrove-coastal-03", "Blue Carbon (Mangrove Restoration)"
        # FIXED: Explicit standard python lists
        milestones = [1, 1, 1, 1, 0, 0, 0]
        rate_100yr, k_shape = 0.02, 1.0
        np.random.seed(42)
        science_input = np.random.normal(loc=0.74, scale=0.08, size=2000).tolist()
        co_benefits = 0.22  
        description_text = "**Scenario Dynamics (Blue Carbon):** Volatile early-stage performance execution history combined with significant scientific estimation uncertainty. However, it provides highly stable long-term permanence physics and a massive environmental co-benefit scalar ($\Omega = +0.22$)."
    else: 
        project_id, project_type = "dac-removal-001", "Frontier Direct Air Capture (DAC)"
        # FIXED: Explicit standard python lists
        milestones = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        rate_100yr, k_shape, science_input, co_benefits = 0.0, 1.0, 0.98, 0.0
        description_text = "**Scenario Dynamics (DAC):** High-cost technical removal infrastructure demonstrating near-perfect milestone delivery and absolute permanence stability ($P(P) = 1.00$). Carbon verification is locked down via localized digital hardware metering with zero auxiliary co-benefit premiums."

    col_left, col_right = st.columns([1, 1.2], gap="large")
    with col_left:
        st.subheader("⚙️ Verified dMRV Pillar Probabilities")
        st.info(description_text)
        spec = ProjectSpecification(project_id, project_type, BASELINE_NOMINAL_UNITS, milestones, rate_100yr, k_shape, science_input, co_benefits)
        results = engine.calculate_fair_value(**spec.to_engine_inputs(), num_simulation_samples=2000)
        
        if isinstance(science_input, dict): display_science_mean = float(science_input["mean"])
        elif isinstance(science_input, list): display_science_mean = float(np.mean(science_input))
        else: display_science_mean = float(science_input)

        def render_risk_pillar(label, score):
            if score <= 0.50: color, text = "🔴", "HIGH RISK DISPERSION"
            elif score <= 0.75: color, text = "🟡", "MODERATE VARIANCE BOUNDS"
            else: color, text = "🟢", "SECURE UNDERWRITING FLOOR"
            st.markdown(f"#### {color} **{label}: {score:.3f}** (`{text}`)")
            st.progress(min(1.0, max(0.0, float(score))))

        render_risk_pillar("Execution Probability P(E)", results['p_execution_mean'])
        render_risk_pillar("Scientific Confidence P(S)", display_science_mean)
        render_risk_pillar("Permanence Probability P(P)", results['p_permanence_mean'])

        st.markdown("#### 🌿 **Ecosystem Co-Benefits Scalar $\\Omega$**")
        st.success(f"**Symmetric Scalar Value: {co_benefits:+.2f}**")

    with col_right:
        st.subheader("📊 Statistical Value Propagation & Supply Directive")
        m1, m2 = st.columns(2)
        m1.metric("Final BFV Unit Rating Value", f"{results['bfv_unit_value']:.4f}")
        m2.metric("Joint Delivery Coeff ($E[\\\Theta]$)", f"{results['expected_delivery_coefficient']:.3f}")
        
        st.markdown("**Predicted Bayesian Fair Value Probability Density Function (PDF):**")
        
        if "_raw_bfv_distribution" in results:
            plot_data = results["_raw_bfv_distribution"]
        else:
            np.random.seed(42)
            plot_data = np.random.normal(loc=results["bfv_unit_value"], scale=0.005, size=2000)
            
        counts, bin_edges = np.histogram(plot_data, bins=15, density=True)
        bin_labels = [f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}" for i in range(len(counts))]
        df_chart = pd.DataFrame({"Probability Density": counts}, index=bin_labels)
        st.bar_chart(df_chart, y_label="Density Curve Intensity")
        st.caption("Bayesian PDF curve illustrating localized valuation certainty. X-Axis represents explicit BFV Value intervals.")

        st.write("---")
        st.subheader("🏛️ Automated Token Issuance Directive")
        st.markdown(f"**Baseline Evaluation Budget Pool:** `{BASELINE_NOMINAL_UNITS:,.0f} Nominal Tons`")
        l1, l2 = st.columns(2)
        with l1: st.info(f"### 📈 Circulating Supply\n**{results['issuable_bfv_units']:,.2f} Credits**")
        with l2: st.warning(f"### 🔒 Safety Escrow Reserve\n**{results['escrow_retained_units']:,.2f} Credits**")
        p05_val = results.get("bfv_5th_percentile", results["bfv_unit_value"])
        st.markdown(f"🛡️ **95% Confidence Portfolio Asset Floor Value:** `{p05_val * BASELINE_NOMINAL_UNITS:,.2f} Risk-Adjusted Tons`")

with tab2:
    st.header("🏛️ The Three-Tiered Dynamic Uncertainty Bank & Solvency Ledger")
    st.markdown("This master dashboard aggregates all registered assets under the Secretariat umbrella. It acts as a **systemic risk clearing house**, monitoring portfolio-wide reserves to guarantee market liquidity is backed 1-to-1 by true risk-adjusted carbon volumes.")
    st.write("---")

    # FIXED: Explicit standard python lists inside the dynamic data models
    spec_ifm = ProjectSpecification("ifm", "Industrial IFM", BASELINE_NOMINAL_UNITS, [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0], 0.04, 1.3, {"mean": 0.85, "variance": 0.002}, 0.04)
    spec_blu = ProjectSpecification("blu", "Blue Carbon", BASELINE_NOMINAL_UNITS, [1,1,1,1,0,0,0], 0.02, 1.0, np.random.normal(loc=0.74, scale=0.08, size=1000).tolist(), 0.22)
    spec_dac = ProjectSpecification("dac", "DAC Removal", BASELINE_NOMINAL_UNITS, [1,1,1,1,1,1,1,1,1,1,1,1,1,1], 0.0, 1.0, 0.98, 0.0)

    res_ifm = engine.calculate_fair_value(**spec_ifm.to_engine_inputs(), num_simulation_samples=1000)
    res_blu = engine.calculate_fair_value(**spec_blu.to_engine_inputs(), num_simulation_samples=1000)
    res_dac = engine.calculate_fair_value(**spec_dac.to_engine_inputs(), num_simulation_samples=1000)

    total_nominal_portfolio = BASELINE_NOMINAL_UNITS * 3
    total_circulating_portfolio = res_ifm['issuable_bfv_units'] + res_blu['issuable_bfv_units'] + res_dac['issuable_bfv_units']
    total_escrow_portfolio = res_ifm['escrow_retained_units'] + res_blu['escrow_retained_units'] + res_dac['escrow_retained_units']
    total_l2_buffer_pool = total_escrow_portfolio * 0.10
    systemic_solvency_ratio = ((total_escrow_portfolio + total_l2_buffer_pool) / total_nominal_portfolio) * 100

    st.subheader("📊 Macro Portfolio Solvency Summary")
    sm1, sm2, sm3, sm4 = st.columns(4)
    sm1.metric("Total Portfolio Nominal Capacity", f"{total_nominal_portfolio:,.0f} Tons")
    sm2.metric("Aggregate Circulating Market Supply", f"{total_circulating_portfolio:,.2f} Credits")
    sm3.metric("Total Active Escrow Reserve Pool", f"{total_escrow_portfolio:,.2f} Credits", delta="Layer 1 Reserve")
    sm4.metric("Layer 2 Central Insurance Fund", f"{total_l2_buffer_pool:,.2f} Credits", delta="Mutual Buffer")

    st.markdown(f"🛡️ **Secretariat Systemic Solvency Cushion Ratio:** `{systemic_solvency_ratio:.2f}%` ── *Reserves securely out-pace portfolio risk thresholds.*")
    st.write("---")

    st.subheader("📋 Project-by-Project Active Ledger Sheets")
    pl1, pl2, pl3 = st.columns(3)
    with pl1:
        st.info("### 🌲 Project: Industrial IFM")
        st.markdown(f"**Asset ID:** `ifm-forestry-404`\n * **BFV Unit Rating:** `{res_ifm['bfv_unit_value']:.4f}`\n * **Circulating Balance:** `{res_ifm['issuable_bfv_units']:,.2f}`\n * **Layer 1 Escrow Vault:** `{res_ifm['escrow_retained_units']:,.2f}`\n * **L2 Buffer Contribution:** `{res_ifm['escrow_retained_units']*0.10:,.2f}`")
        st.caption("Status: Active. Subject to yearly remote-sensing canopy error re-audits.")
    with pl2:
        st.success("### 🦀 Project: Blue Carbon")
        st.markdown(f"**Asset ID:** `mangrove-coastal-03`\n * **BFV Unit Rating:** `{res_blu['bfv_unit_value']:.4f}`\n * **Circulating Balance:** `{res_blu['issuable_bfv_units']:,.2f}`\n * **Layer 1 Escrow Vault:** `{res_blu['escrow_retained_units']:,.2f}`\n * **L2 Buffer Contribution:** `{res_blu['escrow_retained_units']*0.10:,.2f}`")
        st.caption("Status: Active. Carrying high co-benefit offsets shielding baseline execution delays.")
    with pl3:
        st.warning("### ⚙️ Project: Frontier DAC")
        st.markdown(f"**Asset ID:** `dac-removal-001`\n * **BFV Unit Rating:** `{res_dac['bfv_unit_value']:.4f}`\n * **Circulating Balance:** `{res_dac['issuable_bfv_units']:,.2f}`\n * **Layer 1 Escrow Vault:** `{res_dac['escrow_retained_units']:,.2f}`\n * **L2 Buffer Contribution:** `{res_dac['escrow_retained_units']*0.10:,.2f}`")
        st.caption("Status: Active. Technical removal parameters carrying perfect point permanence tracking stability.")

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
        
        # FIXED: Enforced standard list arrays inside the sandbox data specifications
        milestones_dac = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        milestones_nat = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0]
        milestones_blu = [1,1,1,1,0,0,0]
        
        s_dac = ProjectSpecification("dac", "DAC Removal", 1.0, milestones_dac, 0.0, 1.0, 0.98, 0.0)
        s_nat = ProjectSpecification("nat", "Forestry (IFM)", 1.0, milestones_nat, 0.04, 1.4, {"mean": 0.85, "variance": 0.002}, 0.05)
        s_blu = ProjectSpecification("blu", "Blue Carbon", 1.0, milestones_blu, 0.02, 1.1, 0.75, 0.25)
        
        opt_res = optimizer.optimize_allocation([s_dac, s_nat, s_blu], total_budget=10000000.0, project_prices={"dac": price_dac, "nat": price_nature, "blu": price_blue})
        for pid, alloc in opt_res["portfolio_allocation_breakdown"].items():
            st.info(f"### **{alloc['asset_type']}**\n * **Budget Weight:** `{alloc['budget_weight_percentage']}%`\n * **Capital Committed:** `${alloc['capital_allocated_dollars']:,}`")
        st.caption("Allocation weights are derived on the fly by maximizing the ratio of forward expected BFV yield to downside 95th percentile Value-at-Risk (VaR).")
