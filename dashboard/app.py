import sys
import html
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ============================================================
# PROJECT PATHS
# ============================================================

DASHBOARD_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DASHBOARD_DIR.parent

SRC_PATH = PROJECT_ROOT / "src"
STATIC_PATH = DASHBOARD_DIR / "static"
TEMPLATES_PATH = DASHBOARD_DIR / "templates"
RESULTS_PATH = PROJECT_ROOT / "results"


# ============================================================
# PYTHON PATH
# ============================================================

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


# ============================================================
# PROJECT IMPORTS
# ============================================================

from environment import CampusEnvironment
from utility_agent import UtilityBasedPatrolAgent
from multi_agent import MultiAgentPatrolSystem


# ============================================================
# STREAMLIT CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Autonomous Campus Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# FILE HELPERS
# ============================================================

def load_file(path):
    """Read a UTF-8 text file safely."""

    try:
        return path.read_text(
            encoding="utf-8"
        )

    except FileNotFoundError:
        return ""


def render_template(filename, replacements=None):
    """
    Load an HTML template and replace placeholders.

    Supported:
        {{KEY}}
        {KEY}
    """

    path = TEMPLATES_PATH / filename

    content = load_file(path)

    if not content:
        return ""

    if replacements:

        for key, value in replacements.items():

            escaped_value = html.escape(
                str(value)
            )

            # Replace {{KEY}}
            content = content.replace(
                f"{{{{{key}}}}}",
                escaped_value,
            )

            # Replace {KEY}
            content = content.replace(
                f"{{{key}}}",
                escaped_value,
            )

    return content


def render_html(content):
    """
    Render HTML directly with Streamlit.

    Using st.html() prevents multiline HTML
    from being interpreted as Markdown/code.
    """

    if content:
        st.html(content)


# ============================================================
# LOAD DASHBOARD CSS
# ============================================================

css_content = load_file(
    STATIC_PATH / "style.css"
)

if css_content:

    st.html(
        f"<style>{css_content}</style>"
    )


# ============================================================
# SESSION STATE
# ============================================================

def create_agent():
    """Create a fresh autonomous patrol agent."""

    campus = st.session_state.campus

    return UtilityBasedPatrolAgent(
        campus=campus,
        start_location="Main Gate",
        battery=100,
    )


def initialize_session():
    """Initialize dashboard simulation state."""

    if "campus" not in st.session_state:

        st.session_state.campus = (
            CampusEnvironment()
        )

    if "agent" not in st.session_state:

        st.session_state.agent = (
            create_agent()
        )

    if "patrol_step" not in st.session_state:

        st.session_state.patrol_step = 0

    if "last_destination" not in st.session_state:

        st.session_state.last_destination = None

    if "last_scores" not in st.session_state:

        st.session_state.last_scores = {}

    if "multi_agent_system" not in st.session_state:

        st.session_state.multi_agent_system = (
            MultiAgentPatrolSystem(
                st.session_state.campus
            )
        )


def reset_simulation():
    """Reset the complete dashboard simulation."""

    st.session_state.agent = create_agent()

    st.session_state.patrol_step = 0

    st.session_state.last_destination = None

    st.session_state.last_scores = {}

    st.session_state.multi_agent_system = (
        MultiAgentPatrolSystem(
            st.session_state.campus
        )
    )


initialize_session()

campus = st.session_state.campus

agent = st.session_state.agent

multi_agent_system = (
    st.session_state.multi_agent_system
)


# ============================================================
# SIDEBAR — COMMAND CENTER
# ============================================================

with st.sidebar:

    render_html(
        """
        <div style="
            padding: 8px 0 18px 0;
            border-bottom: 1px solid #1d3348;
            margin-bottom: 18px;
        ">

            <div style="
                font-size: 1.05rem;
                font-weight: 800;
                color: #eef7ff;
            ">
                🛡️ COMMAND CENTER
            </div>

            <div style="
                margin-top: 5px;
                font-size: 0.72rem;
                color: #8fa8bf;
            ">
                Autonomous Campus Security
            </div>

        </div>
        """
    )


    st.subheader(
        "🎛️ Simulation Control"
    )


    # --------------------------------------------------------
    # PATROL ONE STEP
    # --------------------------------------------------------

    if st.button(
        "▶ PATROL ONE STEP",
        use_container_width=True,
        type="primary",
    ):

        destination, scores = (
            agent.choose_best_destination()
        )

        st.session_state.last_destination = (
            destination
        )

        st.session_state.last_scores = scores

        agent.patrol_once()

        st.session_state.patrol_step += 1

        st.rerun()


    # --------------------------------------------------------
    # RESET SIMULATION
    # --------------------------------------------------------

    if st.button(
        "↻ RESET SIMULATION",
        use_container_width=True,
    ):

        reset_simulation()

        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # AGENT STATUS
    # --------------------------------------------------------

    st.subheader(
        "🤖 Agent Status"
    )

    st.metric(
        "Current Location",
        agent.current_location,
    )

    st.metric(
        "Battery",
        f"{agent.battery}%",
    )

    st.metric(
        "Patrol Distance",
        f"{agent.total_distance}",
    )

    st.metric(
        "Patrol Steps",
        st.session_state.patrol_step,
    )


    st.divider()


    # --------------------------------------------------------
    # CREATE INCIDENT
    # --------------------------------------------------------

    st.subheader(
        "🚨 Create Incident"
    )

    incident_type = st.selectbox(
        "Incident Type",
        [
            "Unauthorized Entry",
            "Suspicious Activity",
            "Fire Alert",
            "Emergency",
        ],
    )

    incident_location = st.selectbox(
        "Location",
        campus.get_locations(),
    )

    incident_description = st.text_input(
        "Description",
        value="Security incident detected.",
    )

    if st.button(
        "🚨 CREATE INCIDENT",
        use_container_width=True,
    ):

        agent.incident_manager.create_incident(
            incident_type=incident_type,
            location=incident_location,
            description=incident_description,
            detected_at_step=(
                st.session_state.patrol_step
            ),
        )

        st.success(
            "Incident created."
        )

        st.rerun()


    st.divider()

    st.caption(
        "CSE276 • Artificial Intelligence Foundations"
    )


# ============================================================
# HERO
# ============================================================

hero_html = render_template(
    "hero.html"
)

if hero_html:

    render_html(hero_html)

else:

    st.title(
        "🛡️ Autonomous Campus Security"
    )


# ============================================================
# KPI DATA
# ============================================================

active_incidents = (
    agent.incident_manager
    .get_active_incidents()
)

unique_areas = len(
    set(agent.patrol_history)
)

battery_percentage = (
    agent.battery_manager
    .get_percentage()
)

current_location = (
    agent.current_location
)

total_distance = (
    agent.total_distance
)


# ============================================================
# KPI CARDS
# ============================================================

render_html(
    f"""
    <div class="kpi-grid">

        <div class="kpi-card">

            <div class="kpi-label">
                Current Location
            </div>

            <div class="kpi-value">
                {html.escape(current_location)}
            </div>

            <div class="kpi-description">
                Autonomous agent position
            </div>

        </div>


        <div class="kpi-card">

            <div class="kpi-label">
                Battery
            </div>

            <div class="kpi-value">
                {battery_percentage:.0f}%
            </div>

            <div class="kpi-description">
                Available energy
            </div>

        </div>


        <div class="kpi-card">

            <div class="kpi-label">
                Active Alerts
            </div>

            <div class="kpi-value">
                {len(active_incidents)}
            </div>

            <div class="kpi-description">
                Security incidents
            </div>

        </div>


        <div class="kpi-card">

            <div class="kpi-label">
                Distance
            </div>

            <div class="kpi-value">
                {total_distance}
            </div>

            <div class="kpi-description">
                Patrol distance
            </div>

        </div>


        <div class="kpi-card">

            <div class="kpi-label">
                Areas Visited
            </div>

            <div class="kpi-value">
                {unique_areas}
            </div>

            <div class="kpi-description">
                Unique campus areas
            </div>

        </div>

    </div>
    """
)


# ============================================================
# MAIN DASHBOARD COLUMNS
# ============================================================

left_column, right_column = st.columns(
    [1.8, 1],
    gap="large",
)


# ============================================================
# CAMPUS MAP
# ============================================================

with left_column:

    render_html(
        """
        <div class="panel">

            <div class="panel-title">
                🗺️ Live Campus Map
            </div>

            <div class="panel-subtitle">
                Autonomous patrol environment and security events
            </div>

        </div>
        """
    )


    positions = {

        "Main Gate": (0, 3),

        "Academic Block": (2, 4),

        "Library": (4, 4),

        "Hostel": (6, 2),

        "Canteen": (4, 2),

        "Parking": (2, 1),

        "Sports Ground": (4, 0),

        "Administration": (6, 4),

        "Security Office": (8, 3),
    }


    fig = go.Figure()


    # --------------------------------------------------------
    # CAMPUS PATHS
    # --------------------------------------------------------

    for start, end, data in (
        campus.graph.edges(data=True)
    ):

        x1, y1 = positions[start]

        x2, y2 = positions[end]

        fig.add_trace(
            go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",

                line=dict(
                    width=2,
                    color="#294258",
                ),

                hoverinfo="none",
                showlegend=False,
            )
        )


    # --------------------------------------------------------
    # CAMPUS NODES
    # --------------------------------------------------------

    node_x = []
    node_y = []
    node_text = []


    for location in campus.get_locations():

        x, y = positions[location]

        node_x.append(x)
        node_y.append(y)
        node_text.append(location)


    fig.add_trace(
        go.Scatter(

            x=node_x,
            y=node_y,

            mode="markers+text",

            text=node_text,

            textposition="top center",

            marker=dict(
                size=17,
                color="#35d9ff",

                line=dict(
                    width=2,
                    color="#071019",
                ),
            ),

            textfont=dict(
                color="#dceeff",
                size=11,
            ),

            hovertemplate=(
                "<b>%{text}</b>"
                "<extra></extra>"
            ),

            showlegend=False,
        )
    )


    # --------------------------------------------------------
    # CURRENT AI AGENT
    # --------------------------------------------------------

    agent_x, agent_y = positions[
        agent.current_location
    ]


    fig.add_trace(
        go.Scatter(

            x=[agent_x],
            y=[agent_y],

            mode="markers+text",

            text=["🤖 AI AGENT"],

            textposition="bottom center",

            marker=dict(
                size=25,
                color="#38e6a4",
                symbol="star",

                line=dict(
                    width=3,
                    color="#ffffff",
                ),
            ),

            textfont=dict(
                color="#38e6a4",
                size=12,
            ),

            hovertemplate=(
                "<b>Autonomous Agent</b><br>"
                f"Location: "
                f"{html.escape(agent.current_location)}"
                "<extra></extra>"
            ),

            showlegend=False,
        )
    )


    # --------------------------------------------------------
    # ACTIVE INCIDENTS
    # --------------------------------------------------------

    incident_x = []
    incident_y = []
    incident_names = []


    for incident in active_incidents:

        if incident.location in positions:

            x, y = positions[
                incident.location
            ]

            incident_x.append(x)

            incident_y.append(y)

            incident_names.append(
                f"🚨 {incident.incident_type}"
            )


    if incident_x:

        fig.add_trace(
            go.Scatter(

                x=incident_x,
                y=incident_y,

                mode="markers+text",

                text=incident_names,

                textposition="bottom center",

                marker=dict(
                    size=24,
                    color="#ff5577",
                    symbol="diamond",

                    line=dict(
                        width=2,
                        color="#ffffff",
                    ),
                ),

                textfont=dict(
                    color="#ff8da5",
                    size=10,
                ),

                showlegend=False,
            )
        )


    # --------------------------------------------------------
    # MAP LAYOUT
    # --------------------------------------------------------

    fig.update_layout(

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20,
        ),

        paper_bgcolor="#0d1520",

        plot_bgcolor="#070b12",

        xaxis=dict(
            visible=False,
            range=[-1, 9],
        ),

        yaxis=dict(
            visible=False,
            range=[-1, 5],
        ),

        showlegend=False,
    )


    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# AGENT STATUS
# ============================================================

with right_column:

    agent_html = render_template(
        "agent_status.html",
        {
            "CURRENT_LOCATION":
                agent.current_location,

            "BATTERY":
                f"{battery_percentage:.0f}",
        },
    )


    if agent_html:

        render_html(agent_html)


    render_html(
        """
        <div class="panel">

            <div class="panel-title">
                📡 System Telemetry
            </div>

        </div>
        """
    )


    telemetry_col1, telemetry_col2 = (
        st.columns(2)
    )


    with telemetry_col1:

        st.metric(
            "Battery",
            f"{battery_percentage:.0f}%",
        )


    with telemetry_col2:

        st.metric(
            "Distance",
            total_distance,
        )


    st.metric(
        "Active Incidents",
        len(active_incidents),
    )


    st.metric(
        "Unique Areas",
        unique_areas,
    )


# ============================================================
# AI DECISION ENGINE
# ============================================================

render_html(
    """
    <div class="ai-decision">

        <div class="panel-title">
            🧠 AI Decision Engine
        </div>

        <div class="panel-subtitle">
            Explainable utility-based destination selection
        </div>

    </div>
    """
)


decision = getattr(
    agent,
    "last_decision",
    {},
)


if decision:

    selected_destination = decision.get(
        "destination",
        st.session_state.last_destination,
    )


    utility_score = decision.get(
        "utility_score",
        0,
    )


    factors = decision.get(
        "factors",
        {},
    )


    render_html(
        f"""
        <div class="ai-decision">

            <div class="kpi-label">
                SELECTED DESTINATION
            </div>

            <div class="ai-destination">
                {html.escape(
                    str(selected_destination)
                )}
            </div>

            <div class="ai-score">
                Final Utility Score:
                <strong>
                    {float(utility_score):.2f}
                </strong>
            </div>

        </div>
        """
    )


    factor_rows = []


    for key, value in factors.items():

        if isinstance(
            value,
            (int, float),
        ):

            factor_rows.append(
                {
                    "Factor":
                        key.replace(
                            "_",
                            " ",
                        ).title(),

                    "Value":
                        value,
                }
            )


    if factor_rows:

        factor_df = pd.DataFrame(
            factor_rows
        )

        st.dataframe(
            factor_df,
            use_container_width=True,
            hide_index=True,
        )


else:

    st.info(
        "Run a patrol step to generate "
        "an explainable AI decision."
    )


# ============================================================
# UTILITY SCORE ANALYSIS
# ============================================================

if st.session_state.last_scores:

    st.subheader(
        "📊 Destination Utility Analysis"
    )


    score_df = pd.DataFrame(
        {
            "Location":
                list(
                    st.session_state
                    .last_scores
                    .keys()
                ),

            "Utility":
                list(
                    st.session_state
                    .last_scores
                    .values()
                ),
        }
    ).sort_values(
        "Utility",
        ascending=False,
    )


    fig_scores = px.bar(
        score_df,
        x="Location",
        y="Utility",
        title="Utility Score by Destination",
    )


    fig_scores.update_layout(
        paper_bgcolor="#0d1520",
        plot_bgcolor="#070b12",

        font=dict(
            color="#eef7ff"
        ),

        xaxis=dict(
            tickangle=-35,
        ),
    )


    st.plotly_chart(
        fig_scores,
        use_container_width=True,
    )


# ============================================================
# SECURITY INCIDENT CENTER
# ============================================================

st.subheader(
    "🚨 Security Incident Center"
)


all_incidents = (
    agent.incident_manager
    .active_incidents
)


if not all_incidents:

    st.info(
        "No incidents have been recorded yet."
    )


else:

    for incident in all_incidents:

        response_time = (
            incident.get_response_time()
        )


        if incident.active:

            incident_html = render_template(
                "incident_card.html",
                {
                    "INCIDENT_TYPE":
                        incident.incident_type,

                    "LOCATION":
                        incident.location,

                    "PRIORITY":
                        incident.priority,

                    "STATUS":
                        "ACTIVE",
                },
            )


            if incident_html:

                render_html(incident_html)


            st.warning(
                f"🚨 {incident.incident_type} — "
                f"{incident.location}"
            )


        else:

            st.success(
                f"✅ {incident.incident_type} — "
                f"{incident.location} | "
                f"Response time: "
                f"{response_time} patrol steps"
            )


# ============================================================
# INCIDENT RESPONSE METRICS
# ============================================================

st.subheader(
    "⏱️ Incident Response Metrics"
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

                "Response Time":
                    (
                        incident.get_response_time()
                        if not incident.active
                        else None
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
        "Incident response metrics will appear "
        "here after incidents are created."
    )


# ============================================================
# MULTI-AGENT COMMAND CENTER
# ============================================================

st.subheader(
    "👥 Multi-Agent Command Center"
)


multi_col1, multi_col2, multi_col3, multi_col4 = (
    st.columns(4)
)


agent_1 = multi_agent_system.agent_1

agent_2 = multi_agent_system.agent_2


agent_1_coverage = (
    multi_agent_system
    .calculate_coverage_percentage(
        "Agent 1"
    )
)


agent_2_coverage = (
    multi_agent_system
    .calculate_coverage_percentage(
        "Agent 2"
    )
)


total_coverage = (
    multi_agent_system
    .calculate_total_coverage()
)


with multi_col1:

    st.metric(
        "Campus Coverage",
        f"{total_coverage:.2f}%",
    )


with multi_col2:

    st.metric(
        "Agent 1 Coverage",
        f"{agent_1_coverage:.2f}%",
    )


with multi_col3:

    st.metric(
        "Agent 2 Coverage",
        f"{agent_2_coverage:.2f}%",
    )


with multi_col4:

    overlap = len(
        multi_agent_system
        .coverage["Agent 1"]
        &
        multi_agent_system
        .coverage["Agent 2"]
    )


    st.metric(
        "Overlap",
        overlap,
    )


# ============================================================
# MULTI-AGENT TERRITORIES
# ============================================================

territory_col1, territory_col2 = (
    st.columns(2)
)


with territory_col1:

    render_html(
        """
        <div class="agent-territory">

            <div class="panel-title">
                🤖 Agent 1 Territory
            </div>

        </div>
        """
    )


    st.write(
        sorted(
            multi_agent_system
            .territories["Agent 1"]
        )
    )


    st.write(
        "Visited:",
        sorted(
            multi_agent_system
            .coverage["Agent 1"]
        ),
    )


with territory_col2:

    render_html(
        """
        <div class="agent-territory">

            <div class="panel-title">
                🤖 Agent 2 Territory
            </div>

        </div>
        """
    )


    st.write(
        sorted(
            multi_agent_system
            .territories["Agent 2"]
        )
    )


    st.write(
        "Visited:",
        sorted(
            multi_agent_system
            .coverage["Agent 2"]
        ),
    )


# ============================================================
# STRATEGY PERFORMANCE ANALYSIS
# ============================================================

st.subheader(
    "📈 Patrol Strategy Performance"
)


results_file = (
    RESULTS_PATH /
    "patrol_results.csv"
)


if results_file.exists():

    try:

        results_df = pd.read_csv(
            results_file
        )


        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True,
        )


        # Do not show Strategy or Trial
        # as selectable performance metrics.

        excluded_columns = {
            "Strategy",
            "Trial",
        }


        numeric_columns = [

            column

            for column in results_df.columns

            if (
                column not in excluded_columns
                and pd.api.types.is_numeric_dtype(
                    results_df[column]
                )
            )
        ]


        if numeric_columns:

            selected_metric = st.selectbox(
                "Performance Metric",
                numeric_columns,
            )


            fig_strategy = px.bar(
                results_df,
                x="Strategy",
                y=selected_metric,
                title=(
                    f"{selected_metric} "
                    "by Patrol Strategy"
                ),
            )


            fig_strategy.update_layout(

                paper_bgcolor="#0d1520",

                plot_bgcolor="#070b12",

                font=dict(
                    color="#eef7ff"
                ),
            )


            st.plotly_chart(
                fig_strategy,
                use_container_width=True,
            )


    except Exception as exc:

        st.error(
            f"Could not load patrol results: {exc}"
        )


else:

    st.info(
        "Run the patrol evaluation experiment "
        "to display strategy comparisons."
    )


# ============================================================
# PATROL HISTORY
# ============================================================

st.subheader(
    "🧭 Patrol History"
)


history_df = pd.DataFrame(
    {
        "Step":
            range(
                len(
                    agent.patrol_history
                )
            ),

        "Location":
            agent.patrol_history,
    }
)


st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True,
)


# ============================================================
# AGENT STATUS DETAILS
# ============================================================

st.subheader(
    "🔎 Agent Status"
)


status_col1, status_col2, status_col3 = (
    st.columns(3)
)


with status_col1:

    st.metric(
        "Location",
        agent.current_location,
    )


with status_col2:

    st.metric(
        "Battery",
        f"{agent.battery}/"
        f"{agent.battery_manager.capacity}",
    )


with status_col3:

    st.metric(
        "Charging Station",
        agent.charging_station,
    )


# ============================================================
# FOOTER
# ============================================================

footer_html = render_template(
    "footer.html"
)


if footer_html:

    render_html(footer_html)