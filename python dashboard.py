import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import base64
import io

PASS_MARK = 50
COURSE_NAME = "BCA"

# ---------- KPI CARD ----------
def kpi(title, value):
    return html.Div(
        [html.H4(title), html.H2(value)],
        style={
            "background": "#F28E9C",
            "padding": "20px",
            "borderRadius": "12px",
            "width": "22%",
            "textAlign": "center",
            "boxShadow": "0px 4px 8px rgba(0,0,0,0.1)"
        }
    )

# ---------- APP ----------
app = dash.Dash(__name__)
app.title = "BCA Student Dashboard"

# ---------- LAYOUT ----------
app.layout = html.Div([

    html.H1("📊 BCA Student Dashboard", style={"textAlign": "center"}),

    dcc.Upload(
        id="file-upload",
        children=html.Div("Drag & Drop or Click to Upload CSV / Excel"),
        style={
            "width": "98%", "height": "60px", "lineHeight": "60px",
            "borderWidth": "2px", "borderStyle": "dashed",
            "borderRadius": "10px", "textAlign": "center",
            "margin": "10px", "backgroundColor": "#F28E96"
        },
        multiple=False
    ),

    html.Div(id="upload-status"),
    dcc.Store(id="stored_data"),

    html.Br(),
    html.Label("Select Subject"),
    dcc.Dropdown(id="subject_dropdown", placeholder="Select Subject (BCA)"),

    html.Br(),
    html.Div(id="kpi_cards", style={"display": "flex", "gap": "20px"}),

    html.Br(),
    html.Div([
        dcc.Graph(id="gender_pie", style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(id="marks_hist", style={"width": "48%", "display": "inline-block"})
    ]),

    dcc.Graph(id="pass_fail_chart", style={"width": "48%", "margin": "auto"}),

    html.Div([
        dcc.Graph(id="pass_gender_pie", style={"width": "48%", "display": "inline-block"}),
        dcc.Graph(id="fail_gender_pie", style={"width": "48%", "display": "inline-block"})
    ])

], style={"backgroundColor": "#FFF9ED", "padding": "15px"})


# ---------- FILE UPLOAD ----------
@app.callback(
    Output("upload-status", "children"),
    Output("stored_data", "data"),
    Output("subject_dropdown", "options"),
    Input("file-upload", "contents"),
    Input("file-upload", "filename")
)
def upload_file(contents, filename):
    if contents is None:
        return "", None, []

    decoded = base64.b64decode(contents.split(",")[1])

    try:
        if filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        else:
            df = pd.read_excel(io.BytesIO(decoded))

        df.columns = df.columns.str.strip().str.replace(" ", "_")

        required = {"Course", "Gender", "Subject", "Internal_1", "Internal_2", "External"}
        if not required.issubset(df.columns):
            return "❌ Missing required columns", None, []

        df = df[df["Course"] == COURSE_NAME]
        df["Total_Marks"] = df["Internal_1"] + df["Internal_2"] + df["External"]

        subjects = [{"label": s, "value": s} for s in sorted(df["Subject"].unique())]

        return f"✅ Uploaded: {filename}", df.to_json(orient="split"), subjects

    except Exception as e:
        return f"❌ Error: {e}", None, []


# ---------- DASHBOARD UPDATE ----------
@app.callback(
    Output("kpi_cards", "children"),
    Output("gender_pie", "figure"),
    Output("marks_hist", "figure"),
    Output("pass_fail_chart", "figure"),
    Output("pass_gender_pie", "figure"),
    Output("fail_gender_pie", "figure"),
    Input("subject_dropdown", "value"),
    Input("stored_data", "data")
)
def update_dashboard(subject, stored_data):

    empty = px.scatter(title="Please select a subject")

    if not stored_data or not subject:
        return [kpi("Total Students", 0), kpi("Boys %", "0%"),
                kpi("Girls %", "0%"), kpi("Avg Marks", 0)], empty, empty, empty, empty, empty

    df = pd.read_json(stored_data, orient="split")
    d = df[df["Subject"] == subject].copy()

    d["Result"] = d["Total_Marks"].apply(lambda x: "Pass" if x >= PASS_MARK else "Fail")

    # ---------- MARK RANGES ----------
    bins = [0, 20, 40, 60, 70, 80, 90, 100]
    labels = ["0-20", "20-40", "40-60", "60-70", "70-80", "80-90", "90-100"]

    d["Mark_Range"] = pd.cut(
        d["Total_Marks"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    # ---------- KPI ----------
    total = len(d)
    boys = len(d[d["Gender"] == "Boy"])
    girls = len(d[d["Gender"] == "Girl"])

    kpis = [
        kpi("Total Students", total),
        kpi("Boys %", f"{boys/total*100:.1f}%"),
        kpi("Girls %", f"{girls/total*100:.1f}%"),
        kpi("Avg Marks", round(d["Total_Marks"].mean(), 2))
    ]

    # ---------- COLORS ----------
    gender_colors = {"Boy": "#90D999", "Girl": "#F28E9C"}
    mark_colors = {
        "0-20": "#969CE4",
        "20-40": "#C89DD6",
        "40-60": "#A5C2DE",
        "60-70": "#91D9A2",
        "70-80": "#DFE486",
        "80-90": "#E4A46F",
        "90-100": "#FE7674"
    }

    bg = "#FFF9ED"

    # ---------- CHARTS ----------
    gender_pie = px.pie(
        d, names="Gender", title="Gender Distribution",
        color="Gender", color_discrete_map=gender_colors
    )
    gender_pie.update_layout(plot_bgcolor=bg, paper_bgcolor=bg)
    gender_pie.update_traces(textinfo="percent+label")

    marks_hist = px.histogram(
        d,
        x="Mark_Range",
        title="Marks Distribution (Range-wise)",
        color="Mark_Range",
        category_orders={"Mark_Range": labels},
        color_discrete_map=mark_colors
    )
    marks_hist.update_layout(
        plot_bgcolor=bg,
        paper_bgcolor=bg,
        xaxis_title="Marks Range",
        yaxis_title="Number of Students"
    )

    pf = d.groupby("Result").size().reset_index(name="Count")
    pass_fail_chart = px.bar(
        pf, x="Result", y="Count", color="Result",
        color_discrete_map={"Pass": "#90D999", "Fail": "#F28E9C"},
        title="Pass vs Fail"
    )
    pass_fail_chart.update_layout(plot_bgcolor=bg, paper_bgcolor=bg)

    pass_gender_pie = px.pie(
        d[d["Result"] == "Pass"], names="Gender", hole=0.4,
        title="Passed Students", color="Gender",
        color_discrete_map=gender_colors
    )
    pass_gender_pie.update_layout(plot_bgcolor=bg, paper_bgcolor=bg)

    fail_gender_pie = px.pie(
        d[d["Result"] == "Fail"], names="Gender", hole=0.4,
        title="Failed Students", color="Gender",
        color_discrete_map=gender_colors
    )
    fail_gender_pie.update_layout(plot_bgcolor=bg, paper_bgcolor=bg)

    return kpis, gender_pie, marks_hist, pass_fail_chart, pass_gender_pie, fail_gender_pie


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True, port=8050)
