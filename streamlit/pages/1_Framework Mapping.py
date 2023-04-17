import networkx as nx 
import streamlit as st
import pandas as pd
import os 
from PIL import Image
from bokeh.models import (WheelPanTool, BoxZoomTool, ResetTool,  Circle, HoverTool,
                          MultiLine, NodesAndLinkedEdges, Plot, TapTool, WheelZoomTool)
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues5

# sidebar
image = Image.open(os.getcwd()+'\\streamlit\\imgs\\deloitte-logo-black.png')
st.sidebar.image(image)
st.sidebar.header("S&C Reg Navigator v0.9")


def out_df(
    # makes df of requirements for export
        df,
        geog,
        reg,
        sub_reg,
        industry,
        sector
    ):
    output = df.loc[
    (df["Geographies"].isin(geog)) &
    (df["Framework"].isin(reg)) &
    (df["Industry"].isin(industry)) &
    (df["Sector"].isin(sector)) 
    ]
    cols = list(output.columns)
    cols.remove('ProductCategories_AssetClasses')
    return output[cols].to_csv()


def make_digraph(
    # uses networkx to produce a digraph of the regs
    # need to add subreg once we have subreg -> industry mapping
    geog,
    reg,
    sub_reg,
    industry,
    sector
    ):
        G = nx.DiGraph()
        col_dict = {}
        hierachy_dict = {}
        color_palette = Blues5[::-1]

        # iterate through each df mapping, and draw edges, appending detail to dicts
        for index, row in df_geo_reg.iterrows():
            if (row["Geographies"] in geog) & (row['Framework'] in reg):
                G.add_edge(str(row["Geographies"]), str(row["Framework"]))
                col_dict[str(row["Geographies"])] = color_palette[0]
                hierachy_dict[str(row["Geographies"])] = 'Geography'
                col_dict[str(row["Framework"])] =  color_palette[1]
                hierachy_dict[str(row["Framework"])] =  'Framework'

        ##  uncomment this later when we have mapping for sub regulatory framework
        # if sub_reg:
        #     for index, row in df_reg_subreg.iterrows():
        #         if (row["Framework"] in reg) & (row["Framework Subcategory"] in sub_reg):
        #             G.add_edge(str(row["Framework"]), str(row["Framework Subcategory"]))
        #     for index, row in df_sub_reg_indus.iterrows():
        #         if (row["Framework Subcategory"] in reg) & (row["Industry"] in industry):
        #             G.add_edge(str(row["Framework Subcategory"]), str(row["Industry"]))
        # else:
        for index, row in df_reg_indus.iterrows():
            if (row["Framework"] in reg) & (row["Industry"] in industry):
                G.add_edge(str(row["Framework"]), str(row["Industry"]))
                col_dict[str(row["Framework"])] = color_palette[1]
                hierachy_dict[str(row["Framework"])] =  'Framework'
                col_dict[str(row["Industry"])] =  color_palette[2]
                hierachy_dict[str(row["Industry"])] =  'Industry'

        for index, row in df_indus_sector.iterrows():
            if (row["Industry"] in industry) & (row["Sector"] in sector):
                G.add_edge(str(row["Industry"]), str(row["Sector"]))
                col_dict[str(row["Industry"])] =  color_palette[2]
                hierachy_dict[str(row["Industry"])] =  'Industry'
                col_dict[str(row["Sector"])] =  color_palette[3]
                hierachy_dict[str(row["Sector"])] =  'Sector'
        for index, row in df_sector_product.iterrows():
            if row["Sector"] in sector:
                G.add_edge(str(row["Sector"]), str(row["Asset_Class"]))
                col_dict[str(row["Sector"])] =  color_palette[3]
                hierachy_dict[str(row["Sector"])] =  'Sector'
                col_dict[str(row["Asset_Class"])] =  color_palette[4]
                hierachy_dict[str(row["Asset_Class"])] =  'Asset Class'

        # scale node size by degree centrality measure of nodes
        degrees = dict(nx.degree(G))
        for k in degrees.keys():
            degrees[k] = degrees[k]+10

        # set attrs for colure, hierachy and size
        nx.set_node_attributes(G, name='degree', values=degrees)
        nx.set_node_attributes(G, name='cat_col', values=col_dict)
        nx.set_node_attributes(G, name='hierachy', values=hierachy_dict)

        # use graphviz layout for node positions
        pos=nx.nx_agraph.graphviz_layout(G)
        plot = Plot()
        plot.title.text = "(hover to see detailed information)"
        plot.add_tools(BoxZoomTool(), ResetTool(), TapTool())
        
        # render bokeh graph
        graph_renderer = from_networkx(G, pos)
        # default node color
        graph_renderer.node_renderer.glyph = Circle(size='degree', fill_color='cat_col')
        
        # node highlight formatting
        graph_renderer.node_renderer.selection_glyph = Circle(size='degree', fill_color='cat_col', line_width=2)
        graph_renderer.node_renderer.hover_glyph = Circle(size='degree', fill_color='cat_col', line_width=2)

        graph_renderer.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=5)
        # edge highlight formatting
        graph_renderer.edge_renderer.selection_glyph = MultiLine(line_color='#1d1d1f', line_width=5)
        graph_renderer.edge_renderer.hover_glyph = MultiLine(line_color='#1d1d1f', line_width=5)

        # interaction hover allow
        graph_renderer.selection_policy = NodesAndLinkedEdges()
        graph_renderer.inspection_policy = NodesAndLinkedEdges()
        plot.renderers.append(graph_renderer)

        node_hover_tool = HoverTool(tooltips=[
            ("Class", "@hierachy"),
            ("Name", "@index"),
        ])
        plot.add_tools(node_hover_tool,WheelPanTool(), WheelZoomTool())
        return plot


def display_fig_download(df, geog, reg, sub_reg, industry, sector):
    st.download_button(
    "Export Fully Mapped Attributes to Excel",
    out_df(df, geog, reg, sub_reg, industry, sector),
    "sc_reg_attributes.csv",
    "text/csv",
    key='download-csv'
    )
    with st.expander('''Show/Hide Mapping Network'''): 
        st.bokeh_chart(make_digraph(
            geog,
            reg,
            sub_reg,
            industry,
            sector
            ), use_container_width=True)
    return

# load data
prefix=os.getcwd()+'/streamlit/data/'
df_all = pd.read_csv(prefix+'S&C REG-DATA Mapping V2.csv')
df_geo_reg = pd.read_csv(prefix+'Rel_Geo_Framework.csv')
df_reg_subreg = pd.read_csv(prefix+'Rel_Framework_Framework_Subcategory.csv')
df_reg_indus = pd.read_csv(prefix+'Rel_Framework_Industry.csv')
df_indus_sector = pd.read_csv(prefix+'Rel_Industry_Sector.csv')
df_sector_product = pd.read_csv(prefix+'Rel_Sector_Product.csv')
df_asset_subasset = pd.read_csv(prefix+'Rel_Asset_SubAsset.csv')
ms = 10

st.title('Framework Mapping Tool')
st.divider()
st.caption('''This app aims to decompose complex regulatory documents into digestable 
controls and requirements which we can then simplify into physical data attributes''')

# cascading select with filters
geos = df_all['Geographies'].unique()
geo_choice = st.multiselect('Geography', geos, )

if geo_choice:
    regs = df_all["Framework"].loc[df_all["Geographies"].isin(geo_choice)].unique()
    reg_choice = st.multiselect('Framework', regs, max_selections=ms)
    
    if reg_choice:
        sub_regs = df_all["Framework Sub-Category"].loc[df_all["Framework"].isin(reg_choice)]

        if not sub_regs.dropna().empty:
            sub_regs = sub_regs.dropna().unique()
            sub_reg_choice = st.multiselect('Framework Subcategory', sub_regs, max_selections=ms)

            industries = df_all['Industry'].loc[df_all["Framework Sub-Category"].isin(sub_reg_choice)].unique()
            industry_choice = st.multiselect('Industry', industries,max_selections=ms)
            
            if industry_choice:
                sector = df_all['Sector'].loc[df_all['Industry'].isin(industry_choice)].unique()
                sector_choice = st.multiselect('Sector', sector, max_selections=ms)
                
                if sector_choice:
                    display_fig_download(
                        df_all,
                        geo_choice,
                        reg_choice,
                        sub_reg_choice,
                        industry_choice,
                        sector_choice
                    )
    
        else:
            sub_reg_choice = reg_choice

            industries = df_all['Industry'].loc[df_all["Framework"].isin(sub_reg_choice)].unique()
            industry_choice = st.multiselect('Industry', industries, max_selections=ms)
            
            if industry_choice:
                sector = df_all['Sector'].loc[df_all['Industry'].isin(industry_choice)].unique()
                sector_choice = st.multiselect('Sector', sector, max_selections=ms)
                
                if sector_choice:
                    display_fig_download(
                        df_all,
                        geo_choice,
                        reg_choice,
                        None,
                        industry_choice,
                        sector_choice
                    )
    