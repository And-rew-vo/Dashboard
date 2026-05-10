from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc

from pages import age_structure, economy, migration, overview
from ui import APP_TITLE, HEADER_TABS, TOPBAR_BUTTON


external_stylesheets = [dbc.themes.YETI]
app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = APP_TITLE


def build_header() -> html.Header:
    nav_links = [
        dcc.Link(
            tab["label"],
            href=tab["href"],
            className="top-nav-link",
            id=tab["id"],
        )
        for tab in HEADER_TABS
    ]

    return html.Header(
        [
            html.Div(
                [
                    html.Div("Д", className="brand-mark"),
                    html.Div(APP_TITLE, className="brand-text"),
                ],
                className="brand-block",
            ),
            html.Nav(nav_links, className="top-nav"),
            dbc.Button(
                TOPBAR_BUTTON,
                color="light",
                className="export-button",
                disabled=True,
            ),
        ],
        className="app-header",
    )


app.layout = html.Div(
    [
        dcc.Location(id="url"),
        build_header(),
        html.Main(id="page-content", className="page-shell"),
    ],
    className="app-root",
)


@app.callback(
    Output("nav-overview", "className"),
    Output("nav-age", "className"),
    Output("nav-migration", "className"),
    Output("nav-economy", "className"),
    Input("url", "pathname"),
)
def highlight_nav(pathname: str):
    current = pathname or "/"
    active_map = {
        "nav-overview": current in {"/", "/overview"},
        "nav-age": current == "/age-structure",
        "nav-migration": current == "/migration",
        "nav-economy": current == "/economy",
    }
    return tuple(
        "top-nav-link active" if active_map[tab["id"]] else "top-nav-link"
        for tab in HEADER_TABS
    )


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname: str):
    routes = {
        "/": overview.layout,
        "/overview": overview.layout,
        "/age-structure": age_structure.layout,
        "/migration": migration.layout,
        "/economy": economy.layout,
    }
    return routes.get(pathname or "/", overview.layout)


if __name__ == "__main__":
    app.run(debug=True)
