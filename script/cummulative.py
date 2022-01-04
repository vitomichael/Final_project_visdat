from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, Panel
from bokeh.layouts import column, row


def cummulative(df):
    def make_dataset(df):
        return ColumnDataSource(df)

    def style(plot):
        plot.title.align = "center"
        plot.title.text_font_size = "20pt"

        plot.xaxis.axis_label_text_font_size = "14pt"
        plot.xaxis.axis_label_text_font_style = "bold"
        plot.yaxis.axis_label_text_font_size = "14pt"
        plot.yaxis.axis_label_text_font_style = "bold"

        plot.xaxis.major_label_text_font_size = "12pt"
        plot.yaxis.major_label_text_font_size = "12pt"

        return plot

    def confirmed_plot(src):
        fig = figure(
            plot_width=1000,
            plot_height=400,
            title="Confirmed Cases",
            x_axis_label="Date",
            y_axis_label="Value",
            x_axis_type="datetime",
        )
        hover = HoverTool(
            tooltips=[("As at", "@Date{%F}"), ("Confirmed Cases", "@confirm")],
            formatters={"@Date": "datetime"},
            mode="vline",
        )

        fig.line("Date", "confirmed_cases", source=src, color="gray")
        fig.diamond(
            "Date",
            "confirmed_cases",
            source=src,
            fill_alpha=0.7,
            size=5,
            hover_fill_color="purple",
            hover_fill_alpha=1,
            color="cyan",
        )
        fig.add_tools(hover)

        fig = style(fig)

        return fig

    def recovered_plot(src):
        fig = figure(
            plot_width=800,
            plot_height=400,
            title="Recovered Cases",
            x_axis_label="Date",
            y_axis_label="Value",
            x_axis_type="datetime",
        )
        hover = HoverTool(
            tooltips=[("As at", "@Date{%F}"), ("Recovered Cases", "@recovered")],
            formatters={"@Date": "datetime"},
            mode="vline",
        )

        fig.line("Date", "recovered_cases", source=src, color="gray")
        fig.diamond(
            "Date",
            "recovered_cases",
            source=src,
            fill_alpha=0.7,
            size=5,
            hover_fill_color="purple",
            hover_fill_alpha=1,
            color="lime",
        )
        fig.add_tools(hover)

        fig = style(fig)

        return fig

    def death_plot(src):
        fig = figure(
            plot_width=800,
            plot_height=400,
            title="Confirmed Death",
            x_axis_label="Date",
            y_axis_label="Value",
            x_axis_type="datetime",
        )
        hover = HoverTool(
            tooltips=[("As at", "@Date{%F}"), ("Death Cases", "@death")],
            formatters={"@Date": "datetime"},
            mode="vline",
        )

        fig.line("Date", "death_cases", source=src, color="gray")
        fig.diamond(
            "Date",
            "death_cases",
            source=src,
            fill_alpha=0.7,
            size=5,
            hover_fill_color="purple",
            hover_fill_alpha=1,
            color="red",
        )
        fig.add_tools(hover)

        fig = style(fig)

        return fig

    def update(attr, old, new):
        country = menu.value

        df1 = df[df["Country"] == country]
        new_src = make_dataset(df1)

        src.data.update(new_src.data)

        return country

    option = list(df["Country"].value_counts().index)
    option.sort()

    menu = Select(options=option, value=option[0], title="Country")

    menu.on_change("value", update)

    controls = column(menu)

    country = menu.value

    df1 = df[df["Country"] == country]

    src = make_dataset(df1)
    c_plot = confirmed_plot(src)
    r_plot = recovered_plot(src)
    d_plot = death_plot(src)

    layout1 = row([controls, c_plot])
    layout2 = row([r_plot, d_plot], sizing_mode="scale_both")
    layout = column(layout1, layout2)

    tab = Panel(child=layout, title="Cummulative Progression")

    return tab
