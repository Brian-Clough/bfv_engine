import streamlit as st
import numpy as np
import os
import sys

# Append project root path to handle module lookups dynamically
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from bfv.statistics.execution import BetaBinomialExecutionModel
from bfv.statistics.permanence import WeibullPermanenceModel
from bfv.statistics.engine import BFVEngine
from bfv.models.specs import ProjectSpecification
from bfv.portfolio.optimizer import BFVPortfolioOptimizer

st.set_page_config(page_title="BFV Translation Layer Engine", layout="wide", page_icon="🌍")

st.title("🌍 BFV Framework: Institutional Translation Layer")
st.markdown("### Connecting dMRV Scientific Uncertainty to Dynamic Ledger State Operations")
st.write("---")

# Initialize backend models
exec_mod = BetaBinomialExecutionModel()
perm_mod = WeibullPermanenceModel()
engine = BFVEngine(execution_model=exec_mod, permanence_model=perm_mod)
optimizer = BFVPortfolioOptimizer(engine=engine)

# FIXED: Explicitly pass weights [sidebar width, main content width] to st.columns
col_sidebar, col_main = st.columns([1, 2])

with col_sidebar:
    st.header("⚙️ 1. dMRV Sensor Inputs")
    project_type = st.selectbox("Project Archetype", ["Industrial IFM (Forestry)", "Blue Carbon (Mangroves)"])
    nominal_units = st.number_input("Nominal Project Capital Pool ($)", min_value=10000, max_value=10000000, value=1000000, step=50000)
    
    st.subheader("📊 Execution Risk (Milestones)")
    successes = st.slider("Successful Milestones (On-Time)", 0, 30, 18)
    delays = st.slider("Delayed / Failed Milestones", 0, 10, 2)
    mock_milestones = [1] * successes + [0] * delays
    
    st.subheader("🔥 Permanence Risk (Weibull Hazard)")
    reversal_100yr = st.slider("100-Year Baseline Reversal Rate", 0.0, 0.5, 0.04, step=0.01)
    k_shape = st.slider("Weibull Curve Intensity (k Profile)", 0.5, 2.0, 1.4, step=0.1)
    st.caption("k > 1.0 implies rising risk over time due to climate feedback loops.")
    
    st.subheader("🔬 Science Risk Measurement (dMRV Variance)")
    science_mean = st.slider("Expected Core Science Confidence Mean", 0.5, 1.0, 0.88, step=0.01)
    science_var = st.slider("dMRV Remote Sensing Variance", 0.0, 0.02, 0.003, step=0.001)
    
    st.subheader("🌱 Symmetric Co-Benefits (Omega)")
    co_benefit_mean = st.slider("Co-Benefit Value Scalar", -0.2, 0.5, 0.05, step=0.01)

with col_main:
    st.header("🧮 2. Joint Bayesian Valuation Distribution")
    
    # Generate parametric representation based on slider data
    mcmc_science = np.random.normal(loc=science_mean, scale=np.sqrt(max(1e-6, science_var)), size=2000).tolist()
    
    spec = ProjectSpecification(
        project_id="live-demo-asset-01",
        project_type=project_type,
        nominal_units=float(nominal_units),
        execution_milestones=mock_milestones,
        historical_reversal_rate_100yr=reversal_100yr,
        k_shape=k_shape,
        science_risk=mcmc_science,
        co_benefits=co_benefit_mean
    )
    
    # Fire the Monte Carlo engine
    results = engine.calculate_fair_value(**spec.to_engine_inputs(), num_simulation_samples=2000)
    
    # Display top-level metric sheets
    m1, m2, m3 = st.columns(3)
    m1.metric("Calculated BFV Unit Rating", f"{results['bfv_unit_value']:.3f}")
    m2.metric("Expected Delivery Coeff (E[Θ])", f"{results['expected_delivery_coefficient']:.3f}")
    m3.metric("Downside Risk Volatility (σ)", f"{results['bfv_standard_deviation']:.3f}")
    
    st.subheader("🏛️ 3. Automated Three-Tiered Registry Allocations")
    st.markdown("Translating scientific parameter distributions into actionable ledger balances.")
    
    l1, l2 = st.columns(2)
    with l1:
        st.info(f"### 📈 Approved Circulating Pool\n**${results['issuable_bfv_units']:,.2f}**")
        st.caption("Liquid credits approved for immediate trading based on current delivery confidence parameters.")
    with l2:
        st.warning(f"### 🔒 Retained in Risk Escrow\n**${results['escrow_retained_units']:,.2f}**")
        st.caption("Credits held back in Layer 1 reserve to hedge against the calculated Integrity Gap.")
        
    st.subheader("📊 95% Confidence Risk Brackets")
    st.write(f" * **5th Percentile Floor Value**: ${results['bfv_5th_percentile'] * nominal_units:,.2f}")
    st.write(f" * **95th Percentile Ceiling Value**: ${results['bfv_95th_percentile'] * nominal_units:,.2f}")
    
    st.success("✨ **Vision Explained**: This interface proves that our team can link shifting canopy monitoring data straight to ledger actions on the fly. If a wildfire occurs, moving the sliders instantly recalculates the escrow requirement—ensuring systemic solvency automatically.")
