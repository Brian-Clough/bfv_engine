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

st.set_page_config(page_title="BFV Translation Layer Engine", layout="wide", page_icon="🌍")
st.title("🌍 BFV Framework: Institutional Translation Layer")
st.markdown("### Core Engine Linking dMRV Scientific Outputs to Management and Registry Operations")
st.write("---")

engine = BFVEngine(BetaBinomialExecutionModel(), WeibullPermanenceModel())
tab1, tab2, tab3 = st.tabs(["📊 Use Case 1: Single-Asset Rating Engine", "🏛️ Use Case 2: Three-Tiered Registry Solvency", "📈 Use Case 3: Investor Portfolio Optimizer"])

with tab1:
    st.header("Asset Risk Analysis & Verification Panel")
    col1, col2 = st.columns(2)
    with col1:
        p_type = st.selectbox("Asset Archetype", ["Industrial IFM (Forestry)", "Blue Carbon (Mangroves)"])
        nominal = st.number_input("Nominal Volume Capacity (Tons)", value=100000)
        successes = st.slider("On-Time Milestones (Successes)", 0, 30, 20)
        delays = st.slider("Delayed Milestones (Failed Events)", 0, 10, 2)
        reversal = st.slider("100-Year Baseline Reversal Risk", 0.0, 0.4, 0.05)
        k_shape = st.slider("Weibull Curve Intensity (k Profile)", 0.5, 2.0, 1.3)
        science_mean = st.slider("Expected Core Science Accuracy Mean", 0.5, 1.0, 0.90)
        science_var = st.slider("dMRV Canopy Measurement Variance", 0.0, 0.02, 0.002)
        co_benefit = st.slider("Symmetric Co-Benefit Scalar (Omega)", -0.1, 0.4, 0.05)
    with col2:
        mock_milestones = [1] * successes + [0] * delays
        mcmc_science = np.random.normal(loc=science_mean, scale=np.sqrt(max(1e-6, science_var)), size=1000).tolist()
        spec = ProjectSpecification("demo-01", p_type, float(nominal), mock_milestones, reversal, k_shape, mcmc_science, co_benefit)
        res = engine.calculate_fair_value(**spec.to_engine_inputs(), num_simulation_samples=1000)
        
        std_dev = res.get("bfv_standard_deviation", 0.0)
        p05_val = res.get("bfv_5th_percentile", res["bfv_unit_value"])
        p95_val = res.get("bfv_95th_percentile", res["bfv_unit_value"])
        
        st.metric("Calculated BFV Unit Value", f"{res['bfv_unit_value']:.4f}")
        st.metric("Downside Risk Volatility (σ)", f"{std_dev:.3f}")
        st.info(f"### Approved Circulating Market Supply: {res['issuable_bfv_units']:,.2f} Units")
        st.warning(f"### Retained in Layer 1 Safety Escrow: {res['escrow_retained_units']:,.2f} Units")

with tab2:
    st.header("The Three-Tiered Dynamic Uncertainty Bank")
    st.markdown("* **Layer 1: Project Escrow** ── Holds back fraction matching calculated Integrity Gap ($1 - BFV$).\n* **Layer 2: Central Repository Buffer** ── Mutualized insurance pool to absorb localized project shocks.\n* **Layer 3: Insurance Backstop** ── External commercial reinsurance lines protecting macro solvency.")
    st.success("💡 **Talking Point**: Framework transforms the registry from a passive, static ledger into an active, credit-solvency state machine driven by live dMRV monitoring logs.")

with tab3:
    st.header("Commercial Capital Allocation Sandbox")
    c1, c2 = st.columns(2)
    with c1:
        price_dac = st.slider("DAC Removal Credit Cost ($/Ton)", 200, 600, 450)
        price_nature = st.slider("Forestry Credit Cost ($/Ton)", 10, 50, 18)
        price_blue = st.slider("Blue Carbon Credit Cost ($/Ton)", 20, 100, 35)
    with col2:
        optimizer = BFVPortfolioOptimizer(engine=engine)
        s_dac = ProjectSpecification("dac", "DAC Removal", 1.0, [1]*10, 0.0, 1.0, 0.99, 0.0)
        s_nat = ProjectSpecification("nat", "Forestry", 1.0, [1]*15 + [0]*2, 0.05, 1.4, 0.88, 0.05)
        s_blu = ProjectSpecification("blu", "Blue Carbon", 1.0, [1]*8 + [0]*2, 0.02, 1.1, 0.82, 0.20)
        opt_res = optimizer.optimize_allocation([s_dac, s_nat, s_blu], total_budget=10000000.0, project_prices={"dac": price_dac, "nat": price_nature, "blu": price_blue})
        for pid, alloc in opt_res["portfolio_allocation_breakdown"].items():
            st.write(f" * **{alloc['asset_type']}** ── Allocation: {alloc['budget_weight_percentage']}% (${alloc['capital_allocated_dollars']:,})")
