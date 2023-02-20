import pandas as pd

from utils.validators import PreparedData


def build_es_data(filmwork_id, df, df_fwg, df_fwp):
    df['rating'].fillna(-1.0, inplace=True)
    df_sub = df[df['id'] == filmwork_id]
    df_fwg_sub = df_fwg[df_fwg['id'] == filmwork_id]
    df_fwp_sub = df_fwp[df_fwp['id'] == filmwork_id]

    d = {}
    d['id'] = filmwork_id
    d['imdb_rating'] = df_sub['rating'].iloc[0]
    d['genre'] = df_fwg_sub['name'].unique().tolist()
    d['title'] = df_sub['title'].iloc[0] or ''
    d['description'] = df_sub['description'].iloc[0] or ''
    sub_actor = df_fwp_sub[df_fwp_sub['role'] == 'actor']
    if len(sub_actor) > 0:
        d['actors_names'] = ','.join(sub_actor['name'])
        d['actors'] = sub_actor[['id', 'name']].to_dict('records')
    else:
        d['actors_names'] = ''
        d['actors'] = []
    sub_writer = df_fwp_sub[df_fwp_sub['role'] == 'writer']
    if len(sub_writer) > 0:
        d['writers_names'] = ','.join(sub_writer['name'].values.tolist())
        d['writers'] = sub_writer[['id', 'name']].to_dict('records')
    else:
        d['writers_names'] = ''
        d['writers'] = []

    d_validated = PreparedData(**d).dict()

    return d_validated, df_sub['updated_at'].iloc[0]


def transform(df: pd.DataFrame, df_fwg: pd.DataFrame, df_fwp: pd.DataFrame) -> pd.DataFrame:
    data, l_updated_at = [], []
    for filmwork_id in df['id'].values:
        row, upd = build_es_data(filmwork_id, df, df_fwg, df_fwp)
        l_updated_at.append(upd)
        data.append(row)
    return data, l_updated_at
