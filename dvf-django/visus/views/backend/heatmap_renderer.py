from .df import get_df_by_year, geojson_departements, df_gares, df_gares_par_dpt
import plotly.express as px
import plotly.graph_objects as go


def heatmap_render(repr_id: int, zone_id: int, period_id: int):
    df = get_df_by_year(period_id)
    df, plotly_kwargs = get_df_by_zone(df if repr_id != 2 else df_gares_par_dpt, zone_id)
    fig = {
        0: render_prixmoyen,
        1: render_volume_foncier,
        2: render_nb_gares,
        3: render_nb_gares_par_prix,
        4: render_nb_gares_par_surface,
        5: render_nb_gares_par_volume,
        6: render_nb_transactions_par_nb_gares,
        7: render_gares,
    }[repr_id](df, plotly_kwargs)

    return fig.to_html(full_html=False, include_plotlyjs='cdn')


DPT_IDF = set(map(str, [75, 92, 93, 94, 77, 78, 91, 95]))


def get_df_by_zone(df, zone_id):
    plotly_kwargs = {
        'zoom': 4.5, 
        'center': {'lat': 46.7111, 'lon': 1.7191}, 
        # 'margin': {"r": 0, "t": 0, "l": 0, "b": 0}, 
        'height': 800
    }
    if zone_id == 1:
        plotly_kwargs.update({
            'center': {'lat': 48.8566, 'lon': 2.3522},
            'zoom': 7,
        })
        return df[df["Code departement"].isin(DPT_IDF)], plotly_kwargs

    elif zone_id == 2:
        return df[~df["Code departement"].isin(DPT_IDF)], plotly_kwargs

    else:
        return df, plotly_kwargs


def render_prixmoyen(df, plotly_kwargs):
    df_heatmap = df.groupby('Code departement')[
        'Prix au m2'].mean().reset_index()
    df_heatmap["Code departement"] = df_heatmap["Code departement"].astype(
        str).str.zfill(2)
    fig = px.choropleth_mapbox(df_heatmap, locations='Code departement', color='Prix au m2',
                               hover_name='Code departement', color_continuous_scale='Plasma', 
                               featureidkey='properties.code', geojson=geojson_departements, 
                               labels={'Prix au m2': 'Prix au m2 moyen'}, title='Prix au m2 moyen par département en France', mapbox_style='carto-positron',
                               opacity=1, **plotly_kwargs)
    return fig

def render_gares(df, plotly_kwargs):

    fig = render_prixmoyen(df, plotly_kwargs) # on utilse le fond de carte

    df_gares['lat'] = df_gares['geo_point_2d'].apply(lambda x: float(x.split(',')[0]))
    df_gares['lon'] = df_gares['geo_point_2d'].apply(lambda x: float(x.split(',')[1]))

    # rend transparents les départements précédents
    fig.update_traces(marker_opacity=0.0)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # cache la légende
    fig.update_layout(coloraxis_showscale=False)
    # affiche les gares
    fig.add_trace(go.Scattermapbox(
        lat=df_gares['lat'],
        lon=df_gares['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=5,
            color='rgb(255, 0, 0)',
            opacity=0.7
        ),
        text=df_gares['libelle'],
        hoverinfo='text',
        showlegend=False,
    ))

    return fig

def render_volume_foncier(df, plotly_kwargs):
    volume_foncier_total = df.groupby('Code departement')['Valeur fonciere'].sum().reset_index()
    volume_foncier_total.columns = ['Code departement', 'Volume foncier total']
    volume_foncier_total["Code departement"] = volume_foncier_total["Code departement"].astype(str).str.zfill(2)

    fig = px.choropleth_mapbox(volume_foncier_total, locations='Code departement', color='Volume foncier total',
                            hover_name='Code departement', color_continuous_scale='Plasma', featureidkey='properties.code', geojson=geojson_departements, title='Volume foncier total par département', mapbox_style='carto-positron',
                            opacity=1, **plotly_kwargs)
    
    return fig

def render_nb_gares(df, plotly_kwargs):
    fig = px.choropleth_mapbox(df, locations='Code departement', color='Nombre de gares',
                            hover_name='Code departement', color_continuous_scale='Plasma', featureidkey='properties.code', geojson=geojson_departements, labels={'Nombre de gares': 'Nombre de gares'}, title='Nombre de gares par département en France', mapbox_style='carto-positron',
                            opacity=1, **plotly_kwargs)
    return fig

def render_nb_gares_par_prix(df, plotly_kwargs):
    df_heatmap = df.groupby('Code departement')['Prix au m2'].mean().reset_index()
    df_heatmap['Code departement'] = df_heatmap['Code departement'].astype(str).str.zfill(2)
    df_heatmap = df_heatmap.merge(df_gares_par_dpt, on='Code departement')
    df_heatmap['Gare par prix au m2'] = df_heatmap['Nombre de gares']/df_heatmap['Prix au m2']

    fig = px.choropleth_mapbox(df_heatmap, locations='Code departement', color='Gare par prix au m2',
                                hover_name='Code departement', color_continuous_scale='Plasma', featureidkey='properties.code', geojson=geojson_departements, labels={'Gare par prix au m2': 'Gare par prix au m2'}, title='Nombre de gares par prix au m2 en France', mapbox_style='carto-positron',
                                opacity=1, **plotly_kwargs)
    return fig

def render_nb_gares_par_surface(df, plotly_kwargs):
    df_heatmap = df.groupby('Code departement')['Surface Carrez Total'].sum().reset_index()
    df_heatmap['Code departement'] = df_heatmap['Code departement'].astype(str).str.zfill(2)
    df_heatmap = df_heatmap.merge(df_gares_par_dpt, on='Code departement')
    df_heatmap['Gare par surface vendue totale'] = df_heatmap['Nombre de gares']/df_heatmap['Surface Carrez Total']


    fig = px.choropleth_mapbox(df_heatmap, locations='Code departement', color='Gare par surface vendue totale',
                                hover_name='Code departement', color_continuous_scale='Plasma', featureidkey='properties.code', geojson=geojson_departements, title="Départements avec le plus grand nombre de gares en fonction de la surface carrez totale vendue dans l'année", mapbox_style='carto-positron',
                                opacity=1, **plotly_kwargs)
    return fig

def render_nb_gares_par_volume(df, plotly_kwargs):
    df_heatmap = df.groupby('Code departement')['Valeur fonciere'].sum().reset_index()
    df_heatmap['Code departement'] = df_heatmap['Code departement'].astype(str).str.zfill(2)
    df_heatmap = df_heatmap.merge(df_gares_par_dpt, on='Code departement')
    df_heatmap['Gare par volume foncier total'] = df_heatmap['Nombre de gares']/df_heatmap['Valeur fonciere']


    fig = px.choropleth_mapbox(df_heatmap, locations='Code departement', color='Gare par volume foncier total',
                                hover_name='Code departement', color_continuous_scale='Plasma', featureidkey='properties.code', geojson=geojson_departements, title="Départements avec le plus grand nombre de gares en fonction du volume foncier total", mapbox_style='carto-positron',
                                opacity=1, **plotly_kwargs)
    return fig

def render_nb_transactions_par_nb_gares(df, plotly_kwargs):
    df_heatmap = df.groupby('Code departement')['Prix au m2'].count().reset_index()
    df_heatmap['Code departement'] = df_heatmap['Code departement'].astype(str).str.zfill(2)
    df_heatmap = df_heatmap.merge(df_gares_par_dpt, on='Code departement')
    df_heatmap['Transactions par gare'] = df_heatmap['Prix au m2']/df_heatmap['Nombre de gares']


    fig = px.choropleth_mapbox(df_heatmap, locations='Code departement', color='Transactions par gare',
                                hover_name='Code departement', color_continuous_scale='Plasma', featureidkey='properties.code', geojson=geojson_departements, title="Nombre de transactions par nombre de gares", mapbox_style='carto-positron',
                                opacity=1, **plotly_kwargs)
    return fig