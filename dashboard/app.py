import os
import sys

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SRC_PATH = os.path.join(
    PROJECT_ROOT,
    "src",
)

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)


# ============================================================
# PROJECT IMPORTS
# ============================================================

from environment import CampusEnvironment
from utility_agent import UtilityBasedPatrolAgent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Autonomous Campus Security",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# CUSTOM TITLE
# ============================================================

st.title("🤖 Autonomous Campus Security")

st.markdown(
    """
    **AI-Based Autonomous Patrol & Surveillance System**

    The system uses utility-based decision making to select
    patrol destinations while considering security risk,
    patrol coverage, live alerts, travel cost and battery
    constraints.
    """
)


# ============================================================
# SESSION STATE
# ============================================================

if "campus" not in st.session_state:
    st.session_state.campus = CampusEnvironment()


if "agent" not in st.session_state:
    st.session_state.agent = UtilityBasedPatrolAgent(
        campus=st.session_state.campus,
        start_location="Main Gate",
        battery=100,
    )


if "step" not in st.session_state:
    st.session_state.step = 0


if "last_scores" not in st.session_state:
    st.session_state.last_scores = {}


if "last_destination" not in st.session_state:
    st.session_state.last_destination = "None"


# ============================================================
# REFERENCES
# ============================================================

campus = st.session_state.campus
agent = st.session_state.agent


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("⚙️ Simulation Controls")


if st.sidebar.button(
    "🔄 Reset Simulation",
    use_container_width=True,
):

    st.session_state.campus = CampusEnvironment()

    st.session_state.agent = UtilityBasedPatrolAgent(
        campus=st.session_state.campus,
        start_location="Main Gate",
        battery=100,
    )

    st.session_state.step = 0
    st.session_state.last_scores = {}
    st.session_state.last_destination = "None"

    st.rerun()


if st.sidebar.button(
    "🚶 Patrol One Step",
    use_container_width=True,
):

    destination, scores = agent.choose_best_destination()

    if destination is not None:

        st.session_state.last_destination = destination
        st.session_state.last_scores = scores

        success = agent.patrol_once()

        if success:
            st.session_state.step += 1

    st.rerun()


# ============================================================
# CURRENT SYSTEM METRICS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "📍 Current Location",
        agent.current_location,
    )


with col2:

    battery_percentage = (
        agent.battery_manager.get_percentage()
    )

    st.metric(
        "🔋 Battery",
        f"{battery_percentage:.0f}%",
    )


with col3:

    st.metric(
        "📏 Distance",
        agent.total_distance,
    )


with col4:

    st.metric(
        "🔄 Patrol Steps",
        agent.patrol_step,
    )


with col5:

    active_incidents = (
        agent.incident_manager.get_active_incidents()
    )

    st.metric(
        "🚨 Active Alerts",
        len(active_incidents),
    )


st.divider()


# ============================================================
# CAMPUS MAP
# ============================================================

st.subheader("🗺️ Campus Patrol Map")


# Fixed visual coordinates for the campus.

positions = {
    "Main Gate": (0, 2),
    "Academic Block": (2, 3),
    "Library": (4, 3),
    "Administration": (2, 1),
    "Security Office": (4, 0),
    "Parking": (1, 0),
    "Canteen": (6, 2),
    "Hostel": (8, 1),
    "Sports Ground": (6, 0),
}


# Campus paths.

edges = [
    ("Main Gate", "Academic Block"),
    ("Main Gate", "Parking"),
    ("Academic Block", "Library"),
    ("Academic Block", "Administration"),
    ("Library", "Canteen"),
    ("Library", "Hostel"),
    ("Canteen", "Hostel"),
    ("Canteen", "Sports Ground"),
    ("Parking", "Sports Ground"),
    ("Administration", "Security Office"),
    ("Security Office", "Hostel"),
    ("Sports Ground", "Hostel"),
]


fig = go.Figure()


# ------------------------------------------------------------
# Draw paths
# ------------------------------------------------------------

for start, end in edges:

    x_values = [
        positions[start][0],
        positions[end][0],
    ]

    y_values = [
        positions[start][1],
        positions[end][1],
    ]

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="lines",
            line=dict(
                width=3,
            ),
            hoverinfo="none",
            showlegend=False,
        )
    )


# ------------------------------------------------------------
# Draw campus locations
# ------------------------------------------------------------

location_x = []
location_y = []
location_text = []


for location, (x, y) in positions.items():

    location_x.append(x)
    location_y.append(y)
    location_text.append(location)


fig.add_trace(
    go.Scatter(
        x=location_x,
        y=location_y,
        mode="markers+text",
        text=location_text,
        textposition="top center",
        marker=dict(
            size=20,
        ),
        name="Campus Locations",
        hovertemplate=(
            "<b>%{text}</b>"
            "<extra></extra>"
        ),
    )
)


# ------------------------------------------------------------
# Highlight current agent position
# ------------------------------------------------------------

agent_x, agent_y = positions[
    agent.current_location
]


fig.add_trace(
    go.Scatter(
        x=[agent_x],
        y=[agent_y],
        mode="markers",
        marker=dict(
            size=30,
            symbol="star",
        ),
        name="🤖 Patrol Agent",
        hovertemplate=(
            "<b>Patrol Agent</b><br>"
            + agent.current_location
            + "<extra></extra>"
        ),
    )
)


fig.update_layout(
    height=500,
    xaxis=dict(
        visible=False,
    ),
    yaxis=dict(
        visible=False,
    ),
    showlegend=True,
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20,
    ),
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


# ============================================================
# PATROL HISTORY
# ============================================================

st.subheader("📍 Patrol History")


if agent.patrol_history:

    history_text = " → ".join(
        agent.patrol_history
    )

    st.info(history_text)


# ============================================================
# ACTIVE SECURITY INCIDENTS
# ============================================================

st.subheader("🚨 Security Incidents")


active_incidents = (
    agent.incident_manager.get_active_incidents()
)


if active_incidents:

    for incident in active_incidents:

        st.warning(
            f"**{incident.incident_type}** | "
            f"{incident.location} | "
            f"Priority: {incident.priority}\n\n"
            f"{incident.description}"
        )

else:

    st.success(
        "No active security incidents."
    )


# ============================================================
# INCIDENT RESPONSE METRICS
# ============================================================

st.subheader("⏱️ Incident Response Metrics")


all_incidents = (
    agent.incident_manager.active_incidents
)


if all_incidents:

    for incident in all_incidents:

        response_time = (
            incident.get_response_time()
        )

        if incident.active:

            st.warning(
                f"🚨 **{incident.incident_type}** — "
                f"{incident.location}\n\n"
                f"Status: Active\n"
                f"Detected at patrol step: "
                f"{incident.detected_at_step}"
            )

        else:

            st.success(
                f"✅ **{incident.incident_type}** — "
                f"{incident.location}\n\n"
                f"Status: Resolved\n"
                f"Response time: "
                f"{response_time} patrol steps"
            )

else:

    st.info(
        "No incidents have been recorded yet."
    )


# ============================================================
# CREATE TEST INCIDENT
# ============================================================

st.subheader("🚨 Simulate Security Incident")


incident_location = st.selectbox(
    "Select location",
    campus.get_locations(),
)


incident_type = st.selectbox(
    "Select incident type",
    [
        "Unauthorized Entry",
        "Suspicious Activity",
        "Fire Alert",
        "Emergency",
    ],
)


if st.button(
    "🚨 Create Incident",
):

    descriptions = {

        "Unauthorized Entry":
            "Unauthorized person detected.",

        "Suspicious Activity":
            "Suspicious activity detected.",

        "Fire Alert":
            "Possible fire detected.",

        "Emergency":
            "Emergency situation reported.",
    }

    agent.incident_manager.create_incident(
        incident_type,
        incident_location,
        descriptions[incident_type],
        detected_at_step=agent.patrol_step,
    )

    st.success(
        f"{incident_type} created at "
        f"{incident_location}."
    )

    st.rerun()


# ============================================================
# AI DECISION ANALYSIS
# ============================================================

st.subheader("🧠 AI Decision Analysis")


if st.session_state.last_scores:

    sorted_scores = sorted(
        st.session_state.last_scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )


    score_names = [
        item[0]
        for item in sorted_scores
    ]


    score_values = [
        item[1]
        for item in sorted_scores
    ]


    score_fig = go.Figure(
        go.Bar(
            x=score_names,
            y=score_values,
            text=[
                f"{value:.2f}"
                for value in score_values
            ],
            textposition="auto",
        )
    )


    score_fig.update_layout(
        height=400,
        xaxis_title="Campus Location",
        yaxis_title="Utility Score",
    )


    st.plotly_chart(
        score_fig,
        use_container_width=True,
    )


    st.info(
        f"Last selected destination: "
        f"**{st.session_state.last_destination}**"
    )


else:

    st.info(
        "Run a patrol step to generate AI "
        "utility scores."
    )


# ============================================================
# EXPLAINABLE AI DECISION
# ============================================================

st.subheader("💡 Why Did the AI Choose This Destination?")


last_decision = getattr(
    agent,
    "last_decision",
    {},
)


if last_decision:

    selected_destination = last_decision.get(
        "destination",
        "Unknown",
    )

    utility_score = last_decision.get(
        "utility_score",
        0,
    )

    decision_factors = last_decision.get(
        "factors",
        {},
    )

    st.success(
        f"**Selected destination:** "
        f"{selected_destination}"
    )

    st.metric(
        "Final Utility Score",
        f"{utility_score:.2f}",
    )

    if decision_factors:

        st.markdown("### Decision Factors")

        factor_col1, factor_col2 = st.columns(2)

        with factor_col1:

            st.write(
                f"**Risk Score:** "
                f"{decision_factors.get('risk_score', 0)}"
            )

            st.write(
                f"**Coverage Score:** "
                f"{decision_factors.get('coverage_score', 0)}"
            )

            st.write(
                f"**Alert Score:** "
                f"{decision_factors.get('alert_score', 0)}"
            )

        with factor_col2:

            st.write(
                f"**Revisit Time:** "
                f"{decision_factors.get('revisit_time', 0)}"
            )

            st.write(
                f"**Travel Cost:** "
                f"{decision_factors.get('travel_cost', 0)}"
            )

            st.write(
                f"**Battery Cost:** "
                f"{decision_factors.get('battery_cost', 0)}"
            )

    reasons = []

    if decision_factors.get("alert_score", 0) > 0:
        reasons.append(
            "an active security alert is present"
        )

    if decision_factors.get("risk_score", 0) >= 7:
        reasons.append(
            "the area has high security risk"
        )

    if decision_factors.get("coverage_score", 0) >= 7:
        reasons.append(
            "the area requires greater patrol coverage"
        )

    if decision_factors.get("revisit_time", 0) >= 3:
        reasons.append(
            "the area has not been visited recently"
        )

    if decision_factors.get("travel_cost", 0) <= 3:
        reasons.append(
            "the destination is relatively close"
        )

    if decision_factors.get("battery_cost", 0) > 5:
        reasons.append(
            "the destination requires significant battery usage"
        )

    if reasons:

        st.info(
            "The AI selected this destination because "
            + ", ".join(reasons)
            + "."
        )

    else:

        st.info(
            "The destination achieved the highest "
            "overall utility score among reachable locations."
        )

else:

    st.info(
        "Run a patrol step to generate an explainable "
        "AI decision."
    )


# ============================================================
# AGENT STATUS
# ============================================================

st.subheader("🤖 Agent Status")


status_col1, status_col2 = st.columns(2)


with status_col1:

    st.write(
        f"**Current Location:** "
        f"{agent.current_location}"
    )

    st.write(
        f"**Battery:** "
        f"{agent.battery}/"
        f"{agent.battery_manager.capacity}"
    )

    st.write(
        f"**Total Distance:** "
        f"{agent.total_distance}"
    )


with status_col2:

    st.write(
        f"**Patrol Steps:** "
        f"{agent.patrol_step}"
    )

    st.write(
        f"**Charging Station:** "
        f"{agent.charging_station}"
    )

    st.write(
        f"**Areas Visited:** "
        f"{len(set(agent.patrol_history))}"
    )


# ============================================================
# EXPERIMENTAL PERFORMANCE COMPARISON
# ============================================================

st.divider()

st.header("📊 Patrol Strategy Comparison")


st.markdown(
    """
    This section compares the three patrol strategies
    using repeated experimental trials:

    - Random Patrol
    - Fixed Route
    - Utility Based
    """
)


results_file = os.path.join(
    PROJECT_ROOT,
    "results",
    "patrol_results.csv",
)


if os.path.exists(results_file):

    results_df = pd.read_csv(
        results_file
    )


    # --------------------------------------------------------
    # AVERAGE RESULTS
    # --------------------------------------------------------

    average_df = (
        results_df
        .groupby("Strategy")
        .agg(
            {
                "Distance": "mean",
                "Unique Areas": "mean",
                "Total Visits": "mean",
                "Final Battery": "mean",
            }
        )
        .reset_index()
    )


    st.subheader(
        "📋 Average Performance"
    )


    st.dataframe(
        average_df,
        use_container_width=True,
        hide_index=True,
    )


    # --------------------------------------------------------
    # DISTANCE COMPARISON
    # --------------------------------------------------------

    st.subheader(
        "📏 Average Distance Travelled"
    )


    distance_fig = go.Figure(
        go.Bar(
            x=average_df["Strategy"],
            y=average_df["Distance"],
            text=[
                f"{value:.2f}"
                for value in average_df["Distance"]
            ],
            textposition="auto",
        )
    )


    distance_fig.update_layout(
        xaxis_title="Patrol Strategy",
        yaxis_title="Average Distance",
        height=400,
    )


    st.plotly_chart(
        distance_fig,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # COVERAGE COMPARISON
    # --------------------------------------------------------

    st.subheader(
        "🗺️ Average Unique Areas Covered"
    )


    coverage_fig = go.Figure(
        go.Bar(
            x=average_df["Strategy"],
            y=average_df["Unique Areas"],
            text=[
                f"{value:.2f}"
                for value in average_df["Unique Areas"]
            ],
            textposition="auto",
        )
    )


    coverage_fig.update_layout(
        xaxis_title="Patrol Strategy",
        yaxis_title="Average Unique Areas",
        height=400,
    )


    st.plotly_chart(
        coverage_fig,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # BATTERY COMPARISON
    # --------------------------------------------------------

    st.subheader(
        "🔋 Average Final Battery"
    )


    battery_fig = go.Figure(
        go.Bar(
            x=average_df["Strategy"],
            y=average_df["Final Battery"],
            text=[
                f"{value:.2f}"
                for value in average_df["Final Battery"]
            ],
            textposition="auto",
        )
    )


    battery_fig.update_layout(
        xaxis_title="Patrol Strategy",
        yaxis_title="Average Final Battery",
        height=400,
    )


    st.plotly_chart(
        battery_fig,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # EXPERIMENTAL INTERPRETATION
    # --------------------------------------------------------

    st.subheader(
        "🔬 Experimental Interpretation"
    )


    st.info(
        """
        The comparison is based on repeated simulation trials.

        **Random Patrol** provides a stochastic baseline.

        **Fixed Route** provides a deterministic patrol baseline.

        **Utility Based** dynamically selects destinations
        using security risk, coverage, live alerts, travel
        cost and battery constraints.

        The results should be interpreted using multiple
        metrics rather than assuming that one strategy is
        universally superior.
        """
    )


else:

    st.warning(
        """
        Evaluation results have not been generated yet.

        Run:

        `python experiments/evaluate_patrol.py`

        to generate the experimental results.
        """
    )


# ============================================================
# MULTI-AGENT PERFORMANCE ANALYSIS
# ============================================================

st.divider()

st.header("👥 Multi-Agent Performance Analysis")


multi_agent_results_file = os.path.join(
    PROJECT_ROOT,
    "results",
    "multi_agent_results.csv",
)


if os.path.exists(multi_agent_results_file):

    multi_agent_df = pd.read_csv(
        multi_agent_results_file
    )


    # Convert CSV into dictionary
    multi_agent_metrics = dict(
        zip(
            multi_agent_df["Metric"],
            multi_agent_df["Average"],
        )
    )


    # --------------------------------------------------------
    # KPI METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🌐 Campus Coverage",
            f"{float(
                multi_agent_metrics.get(
                    "Total Campus Coverage (%)",
                    0,
                )
            ):.2f}%",
        )


    with col2:

        st.metric(
            "👤 Agent 1 Coverage",
            f"{float(
                multi_agent_metrics.get(
                    "Agent 1 Territory Coverage (%)",
                    0,
                )
            ):.2f}%",
        )


    with col3:

        st.metric(
            "👤 Agent 2 Coverage",
            f"{float(
                multi_agent_metrics.get(
                    "Agent 2 Territory Coverage (%)",
                    0,
                )
            ):.2f}%",
        )


    col4, col5, col6 = st.columns(3)


    with col4:

        st.metric(
            "📏 Average Distance",
            f"{float(
                multi_agent_metrics.get(
                    "Average Total Distance",
                    0,
                )
            ):.2f}",
        )


    with col5:

        st.metric(
            "🔋 Average Battery",
            f"{float(
                multi_agent_metrics.get(
                    "Average Battery Remaining",
                    0,
                )
            ):.2f}",
        )


    with col6:

        st.metric(
            "🔄 Average Overlap",
            f"{float(
                multi_agent_metrics.get(
                    "Average Overlap Count",
                    0,
                )
            ):.2f}",
        )


    # --------------------------------------------------------
    # TERRITORY COVERAGE
    # --------------------------------------------------------

    st.subheader("📊 Territory Coverage")


    # IMPORTANT:
    # coverage_data must be created BEFORE px.bar().

    coverage_data = pd.DataFrame(
        {
            "Agent": [
                "Agent 1",
                "Agent 2",
            ],
            "Coverage (%)": [
                float(
                    multi_agent_metrics.get(
                        "Agent 1 Territory Coverage (%)",
                        0,
                    )
                ),
                float(
                    multi_agent_metrics.get(
                        "Agent 2 Territory Coverage (%)",
                        0,
                    )
                ),
            ],
        }
    )


    coverage_fig = px.bar(
        coverage_data,
        x="Agent",
        y="Coverage (%)",
        title="Agent Territory Coverage",
        text="Coverage (%)",
    )


    coverage_fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )


    coverage_fig.update_layout(
        xaxis_title="Agent",
        yaxis_title="Coverage (%)",
        yaxis_range=[0, 100],
        height=400,
    )


    st.plotly_chart(
        coverage_fig,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # SYSTEM PERFORMANCE
    # --------------------------------------------------------

    st.subheader("⚙️ System Performance")


    performance_data = pd.DataFrame(
        {
            "Metric": [
                "Campus Coverage (%)",
                "Average Distance",
                "Average Battery",
                "Average Overlap",
            ],
            "Value": [
                float(
                    multi_agent_metrics.get(
                        "Total Campus Coverage (%)",
                        0,
                    )
                ),
                float(
                    multi_agent_metrics.get(
                        "Average Total Distance",
                        0,
                    )
                ),
                float(
                    multi_agent_metrics.get(
                        "Average Battery Remaining",
                        0,
                    )
                ),
                float(
                    multi_agent_metrics.get(
                        "Average Overlap Count",
                        0,
                    )
                ),
            ],
        }
    )


    performance_fig = px.bar(
        performance_data,
        x="Metric",
        y="Value",
        title="Multi-Agent System Performance",
        text="Value",
    )


    performance_fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
    )


    performance_fig.update_layout(
        xaxis_tickangle=-25,
        height=450,
    )


    st.plotly_chart(
        performance_fig,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # MULTI-AGENT INTERPRETATION
    # --------------------------------------------------------

    st.subheader("🧠 Multi-Agent Interpretation")


    campus_coverage = float(
        multi_agent_metrics.get(
            "Total Campus Coverage (%)",
            0,
        )
    )


    overlap = float(
        multi_agent_metrics.get(
            "Average Overlap Count",
            0,
        )
    )


    if campus_coverage >= 75:

        st.success(
            f"High campus coverage achieved: "
            f"{campus_coverage:.2f}%."
        )

    else:

        st.info(
            f"Current campus coverage is "
            f"{campus_coverage:.2f}%. "
            f"Further patrol optimization could "
            f"improve coverage."
        )


    if overlap == 0:

        st.success(
            "The coordinated agents produced "
            "no overlapping visited locations "
            "in the evaluated trials."
        )

    else:

        st.warning(
            f"The agents had an average overlap "
            f"of {overlap:.2f} locations."
        )


else:

    st.warning(
        "Multi-agent evaluation results were not "
        "found. Run "
        "`python experiments/evaluate_multi_agent.py` "
        "first."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Autonomous Patrol & Surveillance Agent "
    "for Campus Security | AI Foundations Project"
)
