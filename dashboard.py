# Save this block directly as your updated dashboard layout
import streamlit as st
import numpy as np
import sys
import os

# Ensure the bfv core logic folder path is recognized
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from bfv.statistics.execution import BetaBinomialExecutionModel
from bfv.statistics.permanence import WeibullPermanenceModel
from bfv.statistics.engine import BFVEngine
from bfv.models.specs import ProjectSpecification

st.set_page_config(page_title="BFV Secretariat Platform", layout="wide", page_icon="🌍")

# --- Institutional Header Styling ---
st.title("🌍 Bayesian Fair Value (BFV) Framework")
st.markdown("### **Secretariat Risk Accounting & Asset Validation Dashboard**")
st.markdown(
    "This platform serves as the **Institutional Translation Layer**, programmatically converting raw dMRV data streams "
    "and scientific uncertainty bounds into immutable, risk-adjusted registry issuance vectors."
)
st.write("---")

# Initialize underlying framework calculators
exec_mod = BetaBinomialExecutionModel()
perm_mod = WeibullPermanenceModel()
engine = BFVEngine(execution_model=exec_mod, permanence_model=perm_mod)

# Standardized Baseline Issuance Allocation across all scenarios
BASELINE_NOMINAL_UNITS = 10000.0

# --- Tab Layout ---
tab1, tab2, tab3 = st.tabs([
    "📋 Use Case 1: Project Risk Rating Engine", 
    "🏛️ Use Case 2: Three-Tiered Registry Solvency Bank", 
    "📈 Use Case 3: Investor Portfolio Budget Optimizer"
])

with tab1:
    st.header("Asset Risk Analysis & Verification Protocol")
    st.markdown(
        "Select a verified pipeline asset scenario below to audit how its specialized dMRV telemetry profile "
        "propagates variance to derive its formal regulatory credit allocation metrics."
    )
    st.write("")

    # 1. Pipeline Project Picker Dropdown
    selected_project = st.selectbox(
        "📁 Select Active Pipeline Asset Validation Scenario:",
        [
            "Asset Profile 1: Industrial Improved Forest Management (IFM)",
            "Asset Profile 2: Volatile Blue Carbon Mangrove Restoration",
            "Asset Profile 3: Frontier Direct Air Capture (DAC) Facility"
        ]
    )
    st.write("---")

    # 2. Establish Static Project Specifications Based on Selection
    if "Industrial IFM" in selected_project:
        project_id = "ifm-forestry-404"
        project_type = "Industrial IFM (Forestry)"
        
        # 18 successful milestones on time, 2 delays -> P(E) expected mean = 0.833
        milestones = [1]*18 + [0]*2
        # Near-term baseline risk of 4% under an increasing climate hazard curve (k=1.4)
        rate_100yr = 0.04
        k_shape = 1.4
        # Standardized analytical science risk distribution representation
        science_input = {"mean": 0.88, "variance": 0.003}
        co_benefits = 0.05
        
        description_text = (
            "**Scenario Dynamics:** This project shows strong performance history but is exposed to an increasing "
            "wildfire hazard trajectory over time ($k = 1.4$). Its scientific accounting models carry standard measurement error variance."
        )

    elif "Blue Carbon" in selected_project:
        project_id = "mangrove-coastal-03"
        project_type = "Blue Carbon (Mangrove Restoration)"
        
        # 4 successful milestones, 3 delays -> P(E) expected mean = 0.545
        milestones = [1]*4 + [0]*3
        # Low near-term risk (2%), stable constant trajectory (k=1.1)
        rate_100yr = 0.02
        k_shape = 1.1
        # Significant scientific measurement uncertainty simulated via random draws mimicking a volatile MCMC chain
        np.random.seed(42)
        science_input = np.random.normal(loc=0.75, scale=0.09, size=1000).tolist()
        co_benefits = 0.25 # Massive social/environmental ecosystem scalar
        
        description_text = (
            "**Scenario Dynamics:** Early-stage project exhibiting highly volatile performance execution metrics "
            "and large scientific carbon baseline uncertainty. However, it carries significant environmental co-benefits "
            "($\\Omega = 0.25$) and stable long-term permanence physics."
        )

    else: # Frontier DAC Facility
        project_id = "dac-removal-001"
        project_type = "Frontier Direct Air Capture (DAC)"
        
        # 12 successful milestones on time, 0 delays -> P(E) expected mean = 0.875
        milestones = [1]*12
        # Absolute structural permanence, zero reversal possibility over 1000-year anchor
        rate_100yr = 0.0
        k_shape = 1.0
        # Highly accurate chemical/engineering metering calibration
        science_input = 0.98
        co_benefits = 0.00
        
        description_text = (
            "**Scenario Dynamics:** High-cost technical removal facility displaying absolute, permanent geological "
            "sequestration capability ($P(P) = 1.0$) and tight scientific measurement confidence bounds, with no auxiliary co-benefit impact."
        )

    # 3. Render the Dual Panel Interface Layout
    col_left, col_right = st.columns([1, 1.2], gap="large")

    with col_left:
        st.subheader("⚙️ Verified dMRV Pillar Probabilities")
        st.info(description_text)
        
        # Process the specification through the math core to capture explicit means
        spec = ProjectSpecification(
            project_id=project_id, project_type=project_type, nominal_units=BASELINE_NOMINAL_UNITS,
            execution_milestones=milestones, historical_reversal_rate_100yr=rate_100yr,
            k_shape=k_shape, science_risk=science_input, co_benefits=co_benefits
        )
        results = engine.calculate_fair_value(**spec.to_engine_inputs(), num_simulation_samples=2000)
        
        # Display the crisp, clean top-level probability variables
        st.markdown(f"#### **Execution Probability $P(E)$**")
        st.success(f"**Expected Mean: {results['p_execution_mean']:.3f}**")
        st.caption("Derived via a Bayesian Beta-Binomial conjugate update over binary milestone history metrics.")
        
        st.markdown(f"#### **Scientific Confidence $P(S)$**")
        if isinstance(science_input, (int, float)):
            st.success(f"**Expected Mean: {results['p_science_mean']:.3f}** (Point Estimate)")
        else:
            st.success(f"**Expected Mean: {results['p_science_mean']:.3f}** (Probabilistic Vector Mapping)")
        st.caption("Reflects baseline remote-sensing carbon quantification accuracy and data measurement error variance.")
        
        st.markdown(f"#### **Permanence Probability $P(P)$**")
        st.success(f"**Expected Mean: {results['p_permanence_mean']:.3f}**")
        st.caption("Evaluated using a non-linear Weibull Survival Hazard model extended to a terminal 1,000-year climate horizon.")

        st.markdown(f"#### **Ecosystem Co-Benefits Scalar $\\Omega$**")
        st.success(f"**Symmetric Scalar Value: {co_benefits:+.2f}**")
        st.caption("Positive or negative carbon-equivalent adjustments driving secondary ecological impact values.")

    with col_right:
        st.subheader("📊 Statistical Value Propagation & Supply Directive")
        
        # Display the primary target calculation metrics
        m1, m2 = st.columns(2)
        m1.metric("Final BFV Unit Rating Value", f"{results['bfv_unit_value']:.4f}")
        m2.metric("Joint Delivery Coeff ($E[\\Theta]$)", f"{results['expected_delivery_coefficient']:.3f}")
        
        # 4. Generate and display the native distribution chart if the run is probabilistic
        if "_raw_bfv_distribution" in results:
            st.markdown("**Predicted Bayesian Fair Value Posterior Distribution:**")
            
            # Form histogram counts natively using numpy
            counts, bin_edges = np.histogram(results["_raw_bfv_distribution"], bins=20)
            
            # Format clean key-value dictionary structure to map onto native charts safely
            chart_data = {}
            for i in range(len(counts)):
                bin_label = f"{bin_edges[i]:.2f} to {bin_edges[i+1]:.2f}"
                chart_data[bin_label] = int(counts[i])
                
            st.bar_chart(chart_data)
            st.caption("Monte Carlo density map showing asset value dispersion under full error propagation accounting.")
        else:
            st.markdown("**Predicted Bayesian Fair Value Distribution:**")
            st.info("💡 Degenerate Single Point Estimate: Asset carries 100% mathematical certainty variables. Standard Deviation = 0.0000.")

        st.write("---")
        st.subheader("🏛️ Automated Token Issuance Directive")
        st.markdown(f"**Baseline Evaluation Budget Pool:** `{BASELINE_NOMINAL_UNITS:,.0f} Nominal Tons`")
        
        # Render the concrete Ledger Allocation metrics
        l1, l2 = st.columns(2)
        with l1:
            st.info(f"### 📈 Circulating Supply\\n**{results['issuable_bfv_units']:,.2f} Credits**")
            st.caption("Approved for liquid market trading and forward commercial contract procurement operations.")
        with l2:
            st.warning(f"### 🔒 Safety Escrow Reserve\\n**{results['escrow_retained_units']:,.2f} Credits**")
            st.caption("Retained in the Layer 1 project escrow account vault matching the precise calculated Integrity Gap.")

        # Display risk floor boundaries
        p05_val = results.get("bfv_5th_percentile", results["bfv_unit_value"])
        st.markdown(f"🛡️ **95% Confidence Portfolio Asset Floor Value:** `{p05_val * BASELINE_NOMINAL_UNITS:,.2f} Risk-Adjusted Tons`")

with tab2:
    st.header("The Three-Tiered Dynamic Uncertainty Bank")
    st.markdown("Detailed registry architecture blueprints will be rendered here.")

with tab3:
    st.header("Commercial Capital Allocation Sandbox")
    st.markdown("Detailed portfolio optimization parameters will be rendered here.")

