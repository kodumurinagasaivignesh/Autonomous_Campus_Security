import os
import sys

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ============================================================
# PROJECT PATHS
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
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# MODERN DARK UI
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       GLOBAL
    -------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(0, 180, 255, 0.08),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(0, 255, 170, 0.05),
                transparent 30%
            ),
            #07111f;
        color: #e8f1ff;
    }

    .main {
        background: transparent;
    }

    header[data-testid="stHeader"] {
        background: rgba(7, 17, 31, 0.85);
    }

    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #081525 0%,
                #050d18 100%
            );
        border-right: 1px solid rgba(0, 200, 255, 0.15);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #dcecff !important;
    }

    /* --------------------------------------------------------
       HEADERS
    -------------------------------------------------------- */

    h1, h2, h3 {
        color: #f1f7ff !important;
        letter-spacing: -0.02em;
    }

    h1 {
        font-size: 2.3rem !important;
    }

    h2 {
        font-size: 1.5rem !important;
    }

    h3 {
        font-size: 1.1rem !important;
    }

    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid rgba(0, 200, 255, 0.25);
        background: linear-gradient(
            135deg,
            rgba(0, 150, 255, 0.18),
            rgba(0, 255, 190, 0.08)
        );
        color: #eaf7ff;
        font-weight: 600;
        padding: 0.65rem 1rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        border-color: rgba(0, 220, 255, 0.75);
        background: linear-gradient(
            135deg,
            rgba(0, 150, 255, 0.28),
            rgba(0, 255, 190, 0.15)
        );
        transform: translateY(-1px);
    }

    /* --------------------------------------------------------
       CUSTOM HERO
    -------------------------------------------------------- */

    .hero {
        padding: 26px 30px;
        border-radius: 18px;
        border: 1px solid rgba(0, 200, 255, 0.18);
        background:
            linear-gradient(
                135deg,
                rgba(0, 160, 255, 0.12),
                rgba(0, 255, 190, 0.04)
            );
        box-shadow:
            0 15px 45px rgba(0, 0, 0, 0.25);
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        color: #f4f9ff;
        margin-bottom: 5px;
    }

    .hero-subtitle {
        color: #8ea9c5;
        font-size: 0.95rem;
    }

    .online-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 7px 12px;
        border-radius: 999px;
        background: rgba(0, 255, 150, 0.08);
        border: 1px solid rgba(0, 255, 150, 0.2);
        color: #7fffc0;
        font-size: 0.78rem;
        font-weight: 700;
        margin-top: 14px;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #36f49b;
        box-shadow: 0 0 12px #36f49b;
    }

    /* --------------------------------------------------------
       KPI CARDS
    -------------------------------------------------------- */

    .kpi-card {
        min-height: 125px;
        padding: 18px;
        border-radius: 15px;
        border: 1px solid rgba(150, 190, 220, 0.12);
        background: rgba(12, 28, 47, 0.75);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
    }

    .kpi-label {
        color: #7f9ab7;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .kpi-value {
        color: #f4f9ff;
        font-size: 1.55rem;
        font-weight: 800;
        margin-top: 9px;
    }

    .kpi-subtitle {
        color: #718ba7;
        font-size: 0.72rem;
        margin-top: 5px;
    }

    /* --------------------------------------------------------
       PANELS
    -------------------------------------------------------- */

    .panel {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(150, 190, 220, 0.12);
        background: rgba(10, 25, 43, 0.72);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.16);
        margin-bottom: 18px;
    }

    .panel-title {
        color: #eaf5ff;
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .panel-description {
        color: #718ba7;
        font-size: 0.78rem;
        margin-bottom: 12px;
    }

    /* --------------------------------------------------------
       INCIDENT CARDS
    -------------------------------------------------------- */

    .incident-card {
        padding: 14px;
        border-radius: 12px;
        background: rgba(255, 70, 70, 0.07);
        border: 1px solid rgba(255, 90, 90, 0.18);
        margin-bottom: 10px;
    }

    .incident-title {
        color: #ff9c9c;
        font-weight: 700;
    }

    .incident-text {
        color: #91a8bf;
        font-size: 0.8rem;
        margin-top: 4px;
    }

    .safe-card {
        padding: 14px;
        border-radius: 12px;
        background: rgba(0, 255, 150, 0.05);
        border: 1px solid rgba(0, 255, 150, 0.15);
        color: #8fffc2;
    }

    /* --------------------------------------------------------
       AI DECISION CARD
    -------------------------------------------------------- */

    .ai-card {
        padding: 20px;
        border-radius: 15px;
        background:
            linear-gradient(
                135deg,
                rgba(0, 150, 255, 0.12),
                rgba(130, 70, 255, 0.08)
            );
        border: 1px solid rgba(80, 170, 255, 0.2);
    }

    .ai-destination {
        font-size: 1.4rem;
        font-weight: 800;
        color: #eaf6ff;
    }

    .ai-score {
        font-size: 2rem;
        font-weight: 800;
        color: #70d8ff;
        margin-top: 5px;
    }

    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .footer {
        text-align: center;
        padding: 25px 0 10px 0;
        color: #526b85;
        font-size: 0.72rem;
    }

    /* --------------------------------------------------------
       DATAFRAME
    -------------------------------------------------------- */

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
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


if "last_scores" not in st.session_state:
    st.session_state.last_scores = {}


if "last_destination" not in st.session_state:
    st.session_state.last_destination = "None"


campus = st.session_state.campus
agent = st.session_state.agent


# ============================================================
# HERO HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-title">
            🛡️ Autonomous Campus Security
        </div>

        <div class="hero-subtitle">
            AI-Powered Patrol & Surveillance Command Center
        </div>

        <div class="online-status">
            <span class="status-dot"></span>
            AUTONOMOUS SYSTEM ONLINE
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR CONTROL CENTER
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:1.25rem;
        font-weight:800;
        color:#eef7ff;
        margin-bottom:4px;
    ">
        🛰️ CONTROL CENTER
    </div>

    <div style="
        color:#718ba7;
        font-size:0.75rem;
        margin-bottom:20px;
    ">
        Autonomous patrol operations
    </div>
    """,
    unsafe_allow_html=True,
)


if st.sidebar.button(
    "▶  PATROL ONE STEP",
    use_container_width=True,
):

    destination, scores = (
        agent.choose_best_destination()
    )

    st.session_state.last_destination = (
        destination if destination else "None"
    )

    st.session_state.last_scores = scores

    agent.patrol_once()

    st.rerun()


if st.sidebar.button(
    "↻  RESET SIMULATION",
    use_container_width=True,
):

    st.session_state.campus = (
        CampusEnvironment()
    )

    st.session_state.agent = (
        UtilityBasedPatrolAgent(
            campus=st.session_state.campus,
            start_location="Main Gate",
            battery=100,
        )
    )

    st.session_state.last_scores = {}
    st.session_state.last_destination = "None"

    st.rerun()


st.sidebar.divider()


st.sidebar.markdown(
    """
    <div style="
        color:#7f9ab7;
        font-size:0.72rem;
        text-transform:uppercase;
        letter-spacing:0.08em;
        margin-bottom:8px;
    ">
        System
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.success("● AI ENGINE ONLINE")

st.sidebar.write(
    f"📍 {agent.current_location}"
)

st.sidebar.write(
    f"🔋 {agent.battery}/"
    f"{agent.battery_manager.capacity}"
)

st.sidebar.write(
    f"🚨 "
    f"{len(agent.incident_manager.get_active_incidents())} "
    f"active alerts"
)


# ============================================================
# TOP KPI ROW
# ============================================================

battery_percentage = (
    agent.battery_manager.get_percentage()
)

active_incidents = (
    agent.incident_manager.get_active_incidents()
)


unique_locations = len(
    set(agent.patrol_history)
)


kpi_columns = st.columns(5)


kpi_data = [
    (
        "📍 CURRENT LOCATION",
        agent.current_location,
        "Agent position",
    ),
    (
        "🔋 BATTERY",
        f"{battery_percentage:.0f}%",
        "Energy remaining",
    ),
    (
        "🚨 ACTIVE ALERTS",
        str(len(active_incidents)),
        "Security incidents",
    ),
    (
        "📏 DISTANCE",
        str(agent.total_distance),
        "Patrol movement",
    ),
    (
        "🗺️ AREAS VISITED",
        str(unique_locations),
        "Unique locations",
    ),
]


for column, data in zip(
    kpi_columns,
    kpi_data,
):

    with column:

        st.markdown(
            f"""
            <div class="kpi-card">

                <div class="kpi-label">
                    {data[0]}
                </div>

                <div class="kpi-value">
                    {data[1]}
                </div>

                <div class="kpi-subtitle">
                    {data[2]}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


st.write("")


# ============================================================
# MAIN MAP + AGENT STATUS
# ============================================================

map_column, status_column = st.columns(
    [2.15, 1]
)


# ============================================================
# CAMPUS MAP
# ============================================================

with map_column:

    st.markdown(
        """
        <div class="panel-title">
            🗺️ LIVE CAMPUS OPERATIONS
        </div>

        <div class="panel-description">
            Real-time simulated patrol environment
        </div>
        """,
        unsafe_allow_html=True,
    )


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


    map_fig = go.Figure()


    # --------------------------------------------------------
    # PATHS
    # --------------------------------------------------------

    for start, end in edges:

        map_fig.add_trace(
            go.Scatter(
                x=[
                    positions[start][0],
                    positions[end][0],
                ],
                y=[
                    positions[start][1],
                    positions[end][1],
                ],
                mode="lines",
                line=dict(
                    width=2,
                ),
                hoverinfo="none",
                showlegend=False,
            )
        )


    # --------------------------------------------------------
    # LOCATIONS
    # --------------------------------------------------------

    map_fig.add_trace(
        go.Scatter(
            x=[
                positions[name][0]
                for name in positions
            ],
            y=[
                positions[name][1]
                for name in positions
            ],
            mode="markers+text",
            text=list(positions.keys()),
            textposition="top center",
            marker=dict(
                size=14,
            ),
            name="Campus",
            hovertemplate=(
                "<b>%{text}</b>"
                "<extra></extra>"
            ),
        )
    )


    # --------------------------------------------------------
    # PATROL HISTORY ROUTE
    # --------------------------------------------------------

    history = agent.patrol_history


    if len(history) >= 2:

        history_x = [
            positions[location][0]
            for location in history
            if location in positions
        ]

        history_y = [
            positions[location][1]
            for location in history
            if location in positions
        ]


        map_fig.add_trace(
            go.Scatter(
                x=history_x,
                y=history_y,
                mode="lines+markers",
                line=dict(
                    width=4,
                    dash="dot",
                ),
                marker=dict(
                    size=7,
                ),
                name="Patrol Route",
                hoverinfo="skip",
            )
        )


    # --------------------------------------------------------
    # CURRENT AGENT
    # --------------------------------------------------------

    current_x, current_y = positions[
        agent.current_location
    ]


    map_fig.add_trace(
        go.Scatter(
            x=[current_x],
            y=[current_y],
            mode="markers",
            marker=dict(
                size=26,
                symbol="star",
            ),
            name="🤖 AI Agent",
            hovertemplate=(
                "<b>AI PATROL AGENT</b><br>"
                + agent.current_location
                + "<extra></extra>"
            ),
        )
    )


    # --------------------------------------------------------
    # INCIDENT LOCATIONS
    # --------------------------------------------------------

    incidents_to_plot = (
        agent.incident_manager.active_incidents
    )


    incident_locations = []


    for incident in incidents_to_plot:

        if (
            incident.active
            and incident.location in positions
        ):

            incident_locations.append(
                incident
            )


    if incident_locations:

        map_fig.add_trace(
            go.Scatter(
                x=[
                    positions[i.location][0]
                    for i in incident_locations
                ],
                y=[
                    positions[i.location][1]
                    for i in incident_locations
                ],
                mode="markers",
                marker=dict(
                    size=24,
                    symbol="diamond",
                ),
                name="🚨 Active Incident",
                text=[
                    i.incident_type
                    for i in incident_locations
                ],
                hovertemplate=(
                    "<b>🚨 %{text}</b>"
                    "<extra></extra>"
                ),
            )
        )


    map_fig.update_layout(
        height=570,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,15,27,0.55)",
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10,
        ),
        xaxis=dict(
            visible=False,
        ),
        yaxis=dict(
            visible=False,
            scaleanchor="x",
            scaleratio=1,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0,
            xanchor="left",
            x=0,
        ),
    )


    st.plotly_chart(
        map_fig,
        use_container_width=True,
    )


# ============================================================
# AGENT STATUS PANEL
# ============================================================

with status_column:

    st.markdown(
        """
        <div class="panel-title">
            🤖 AI AGENT STATUS
        </div>

        <div class="panel-description">
            Autonomous patrol unit
        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        f"""
        <div class="ai-card">

            <div style="
                color:#7fffc0;
                font-size:0.72rem;
                font-weight:700;
            ">
                ● AGENT 01 ONLINE
            </div>

            <div style="
                color:#7f9ab7;
                font-size:0.75rem;
                margin-top:14px;
            ">
                CURRENT LOCATION
            </div>

            <div class="ai-destination">
                {agent.current_location}
            </div>

            <div style="
                color:#7f9ab7;
                font-size:0.75rem;
                margin-top:18px;
            ">
                BATTERY
            </div>

            <div class="ai-score">
                {battery_percentage:.0f}%
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.write("")


    st.markdown(
        f"""
        <div class="panel">

            <div class="panel-title">
                📡 PATROL STATUS
            </div>

            <div style="
                color:#91a8bf;
                line-height:2;
                font-size:0.85rem;
            ">

                <b>Patrol Steps:</b>
                {getattr(agent, "patrol_step", 0)}

                <br>

                <b>Total Distance:</b>
                {agent.total_distance}

                <br>

                <b>Charging Station:</b>
                {agent.charging_station}

                <br>

                <b>Last Target:</b>
                {st.session_state.last_destination}

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PATROL HISTORY
# ============================================================

st.markdown(
    """
    <div class="panel-title">
        🧭 PATROL ROUTE HISTORY
    </div>
    """,
    unsafe_allow_html=True,
)


if agent.patrol_history:

    route = "  →  ".join(
        agent.patrol_history
    )

    st.code(
        route,
        language="text",
    )

else:

    st.info(
        "No patrol movement recorded yet."
    )


# ============================================================
# INCIDENTS + AI DECISION
# ============================================================

incident_column, decision_column = st.columns(
    2
)


# ============================================================
# INCIDENT CENTER
# ============================================================

with incident_column:

    st.markdown(
        """
        <div class="panel-title">
            🚨 SECURITY INCIDENT CENTER
        </div>

        <div class="panel-description">
            Live security events and response status
        </div>
        """,
        unsafe_allow_html=True,
    )


    if active_incidents:

        for incident in active_incidents:

            st.markdown(
                f"""
                <div class="incident-card">

                    <div class="incident-title">
                        🚨 {incident.incident_type}
                    </div>

                    <div class="incident-text">
                        Location:
                        <b>{incident.location}</b>
                    </div>

                    <div class="incident-text">
                        Priority:
                        <b>{incident.priority}</b>
                    </div>

                    <div class="incident-text">
                        Detected at patrol step:
                        <b>{incident.detected_at_step}</b>
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.markdown(
            """
            <div class="safe-card">
                ✓ No active security incidents
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# AI DECISION
# ============================================================

with decision_column:

    st.markdown(
        """
        <div class="panel-title">
            🧠 AI DECISION ENGINE
        </div>

        <div class="panel-description">
            Explainable utility-based destination selection
        </div>
        """,
        unsafe_allow_html=True,
    )


    last_decision = getattr(
        agent,
        "last_decision",
        {},
    )


    if last_decision:

        selected_destination = (
            last_decision.get(
                "destination",
                "Unknown",
            )
        )


        utility_score = float(
            last_decision.get(
                "utility_score",
                0,
            )
        )


        st.markdown(
            f"""
            <div class="ai-card">

                <div style="
                    color:#7f9ab7;
                    font-size:0.72rem;
                    text-transform:uppercase;
                ">
                    Selected Destination
                </div>

                <div class="ai-destination">
                    {selected_destination}
                </div>

                <div style="
                    color:#7f9ab7;
                    font-size:0.72rem;
                    margin-top:15px;
                ">
                    UTILITY SCORE
                </div>

                <div class="ai-score">
                    {utility_score:.2f}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        factors = last_decision.get(
            "factors",
            {},
        )


        if factors:

            factor_col1, factor_col2 = (
                st.columns(2)
            )


            with factor_col1:

                st.write(
                    f"🛡️ Risk: "
                    f"**{factors.get('risk_score', 0)}**"
                )

                st.write(
                    f"🗺️ Coverage: "
                    f"**{factors.get('coverage_score', 0)}**"
                )

                st.write(
                    f"🚨 Alert: "
                    f"**{factors.get('alert_score', 0)}**"
                )


            with factor_col2:

                st.write(
                    f"🔄 Revisit: "
                    f"**{factors.get('revisit_time', 0)}**"
                )

                st.write(
                    f"📏 Travel: "
                    f"**{factors.get('travel_cost', 0)}**"
                )

                st.write(
                    f"🔋 Battery: "
                    f"**{factors.get('battery_cost', 0)}**"
                )

    else:

        st.info(
            "Run a patrol step to generate an "
            "explainable AI decision."
        )


# ============================================================
# CREATE INCIDENT
# ============================================================

st.divider()

st.subheader("🚨 Simulate Security Event")


incident_col1, incident_col2, incident_col3 = (
    st.columns([1, 1, 1])
)


with incident_col1:

    incident_location = st.selectbox(
        "Incident Location",
        campus.get_locations(),
    )


with incident_col2:

    incident_type = st.selectbox(
        "Incident Type",
        [
            "Unauthorized Entry",
            "Suspicious Activity",
            "Fire Alert",
            "Emergency",
        ],
    )


with incident_col3:

    st.write("")

    st.write("")

    create_incident = st.button(
        "🚨 CREATE SECURITY ALERT",
        use_container_width=True,
    )


if create_incident:

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
        detected_at_step=getattr(
            agent,
            "patrol_step",
            0,
        ),
    )


    st.success(
        f"{incident_type} created at "
        f"{incident_location}."
    )


    st.rerun()


# ============================================================
# INCIDENT RESPONSE METRICS
# ============================================================

st.subheader("⏱️ Incident Response History")


all_incidents = (
    agent.incident_manager.active_incidents
)


if all_incidents:

    response_rows = []


    for incident in all_incidents:

        response_rows.append(
            {
                "Incident":
                    incident.incident_type,

                "Location":
                    incident.location,

                "Priority":
                    incident.priority,

                "Status":
                    (
                        "Active"
                        if incident.active
                        else "Resolved"
                    ),

                "Detected Step":
                    incident.detected_at_step,

                "Resolved Step":
                    (
                        incident.resolved_at_step
                        if incident.resolved_at_step
                        is not None
                        else "-"
                    ),

                "Response Time":
                    (
                        incident.get_response_time()
                        if incident.get_response_time()
                        is not None
                        else "-"
                    ),
            }
        )


    response_df = pd.DataFrame(
        response_rows
    )


    st.dataframe(
        response_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No incident response history available."
    )


# ============================================================
# UTILITY SCORE ANALYSIS
# ============================================================

st.divider()

st.header("🧠 Utility Decision Analysis")


if st.session_state.last_scores:

    sorted_scores = sorted(
        st.session_state.last_scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )


    utility_df = pd.DataFrame(
        {
            "Location": [
                item[0]
                for item in sorted_scores
            ],
            "Utility Score": [
                float(item[1])
                for item in sorted_scores
            ],
        }
    )


    utility_fig = px.bar(
        utility_df,
        x="Location",
        y="Utility Score",
        text="Utility Score",
    )


    utility_fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
    )


    utility_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,15,27,0.55)",
        height=420,
        xaxis_title="Campus Location",
        yaxis_title="Utility Score",
    )


    st.plotly_chart(
        utility_fig,
        use_container_width=True,
    )

else:

    st.info(
        "Run a patrol step to generate utility scores."
    )


# ============================================================
# PATROL STRATEGY COMPARISON
# ============================================================

st.divider()

st.header("📊 Patrol Strategy Intelligence")


results_file = os.path.join(
    PROJECT_ROOT,
    "results",
    "patrol_results.csv",
)


if os.path.exists(results_file):

    results_df = pd.read_csv(
        results_file
    )


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
        "Strategy Performance"
    )


    st.dataframe(
        average_df.round(2),
        use_container_width=True,
        hide_index=True,
    )


    strategy_col1, strategy_col2 = (
        st.columns(2)
    )


    with strategy_col1:

        distance_fig = px.bar(
            average_df,
            x="Strategy",
            y="Distance",
            text="Distance",
            title="Average Patrol Distance",
        )


        distance_fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
        )


        distance_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,15,27,0.55)",
            height=400,
        )


        st.plotly_chart(
            distance_fig,
            use_container_width=True,
        )


    with strategy_col2:

        battery_fig = px.bar(
            average_df,
            x="Strategy",
            y="Final Battery",
            text="Final Battery",
            title="Average Final Battery",
        )


        battery_fig.update_traces(
            texttemplate="%{text:.2f}",
            textposition="outside",
        )


        battery_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(5,15,27,0.55)",
            height=400,
        )


        st.plotly_chart(
            battery_fig,
            use_container_width=True,
        )


    coverage_fig = px.bar(
        average_df,
        x="Strategy",
        y="Unique Areas",
        text="Unique Areas",
        title="Average Unique Areas Covered",
    )


    coverage_fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
    )


    coverage_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,15,27,0.55)",
        height=400,
    )


    st.plotly_chart(
        coverage_fig,
        use_container_width=True,
    )


else:

    st.warning(
        "Patrol evaluation results were not found."
    )


# ============================================================
# MULTI-AGENT COMMAND CENTER
# ============================================================

st.divider()

st.header("👥 Multi-Agent Command Center")


multi_agent_results_file = os.path.join(
    PROJECT_ROOT,
    "results",
    "multi_agent_results.csv",
)


if os.path.exists(
    multi_agent_results_file
):

    multi_agent_df = pd.read_csv(
        multi_agent_results_file
    )


    multi_agent_metrics = dict(
        zip(
            multi_agent_df["Metric"],
            multi_agent_df["Average"],
        )
    )


    # --------------------------------------------------------
    # MULTI-AGENT KPIs
    # --------------------------------------------------------

    multi_col1, multi_col2, multi_col3, multi_col4 = (
        st.columns(4)
    )


    with multi_col1:

        st.metric(
            "🌐 Campus Coverage",
            f"{float(
                multi_agent_metrics.get(
                    "Total Campus Coverage (%)",
                    0,
                )
            ):.2f}%",
        )


    with multi_col2:

        st.metric(
            "🤖 Agent 1",
            f"{float(
                multi_agent_metrics.get(
                    "Agent 1 Territory Coverage (%)",
                    0,
                )
            ):.2f}%",
        )


    with multi_col3:

        st.metric(
            "🤖 Agent 2",
            f"{float(
                multi_agent_metrics.get(
                    "Agent 2 Territory Coverage (%)",
                    0,
                )
            ):.2f}%",
        )


    with multi_col4:

        st.metric(
            "🔄 Overlap",
            f"{float(
                multi_agent_metrics.get(
                    "Average Overlap Count",
                    0,
                )
            ):.2f}",
        )


    # --------------------------------------------------------
    # TERRITORY COVERAGE CHART
    # --------------------------------------------------------

    territory_data = pd.DataFrame(
        {
            "Agent": [
                "Agent 1",
                "Agent 2",
            ],
            "Coverage": [
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


    territory_fig = px.bar(
        territory_data,
        x="Agent",
        y="Coverage",
        text="Coverage",
        title="Territory Coverage",
    )


    territory_fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )


    territory_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,15,27,0.55)",
        yaxis_title="Coverage (%)",
        xaxis_title="Agent",
        yaxis_range=[0, 100],
        height=420,
    )


    st.plotly_chart(
        territory_fig,
        use_container_width=True,
    )


    # --------------------------------------------------------
    # MULTI-AGENT PERFORMANCE
    # --------------------------------------------------------

    multi_performance_data = pd.DataFrame(
        {
            "Metric": [
                "Campus Coverage",
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
        multi_performance_data,
        x="Metric",
        y="Value",
        text="Value",
        title="Multi-Agent System Performance",
    )


    performance_fig.update_traces(
        texttemplate="%{text:.2f}",
        textposition="outside",
    )


    performance_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(5,15,27,0.55)",
        height=420,
        xaxis_tickangle=-20,
    )


    st.plotly_chart(
        performance_fig,
        use_container_width=True,
    )


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


    if overlap == 0:

        st.success(
            f"✓ Excellent coordination: "
            f"zero average patrol overlap."
        )

    else:

        st.info(
            f"Average patrol overlap: "
            f"{overlap:.2f} locations."
        )


    st.info(
        f"Current evaluated campus coverage: "
        f"**{campus_coverage:.2f}%**."
    )


else:

    st.warning(
        "Multi-agent evaluation results were not found."
    )


# ============================================================
# FINAL PROJECT STATUS
# ============================================================

st.divider()

st.markdown(
    """
    <div class="panel">

        <div class="panel-title">
            🛡️ AUTONOMOUS SECURITY SYSTEM
        </div>

        <div style="
            color:#718ba7;
            font-size:0.8rem;
            margin-top:8px;
        ">
            AI Foundations Project •
            Autonomous Patrol & Surveillance Agent
            for Campus Security
        </div>

        <div style="
            color:#526b85;
            font-size:0.72rem;
            margin-top:10px;
        ">
            Simulation environment •
            Explainable AI •
            Battery-aware patrol •
            Multi-agent coordination
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="footer">
        Autonomous Campus Security Command Center
        <br>
        CSE276 - Artificial Intelligence Foundations
    </div>
    """,
    unsafe_allow_html=True,
)