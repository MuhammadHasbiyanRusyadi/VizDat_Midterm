import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import re

#-----------------------------------------------------------------------------------
# Konfigurasi Aplikasi (Warna & Daftar Artis)
#-----------------------------------------------------------------------------------
P3_BLUE = "#3A86FF"
P3_YELLOW = "#FFD700"
P3_RED = "#FF4500"
P3_PINK = "#FF69B4"
P3_DARK_NAVY = "#0A1931"
P3_BLACK = "#111111"
P3_WHITE = "#FFFFFF"

# Daftar artis J-Pop, J-Rock, J-Idol sebagai basis standarisasi
J_POP_ARTISTS = [
 'Aimer', 'LiSA', 'YOASOBI', 'Kenshi Yonezu', 'Eve', 'Yorushika', 'Official HIGE DANDism', 'King Gnu', 'Aimyon', 'RADWIMPS', 'Daoko', 'Yui', 'Utada Hikaru', 'Ayumi Hamasaki', 'Namie Amuro', 'Milet', 'Nana Mizuki', 'Kumi Koda', 'Ado', 'Reol', 'MAISONdes', 'Kana Nishino', 'Zutomayo', 'Ikimono Gakari', 'Perfume', 'Back Number', 'Sekai no Owari', 'Supercell', 'GARNiDELiA', 'Scandal', 'Flow', 'Nissy', 'MIYAVI', 'Hoshimachi Suisei', 'Yo Hitoto', 'Ryoko Moriyama', 'Megumi Hayashibara', 'ClariS', 'Angela', 'Aira Mitsuki', 'Hikaru Utada', 'Fujii Kaze', 'iri', 'Vickeblanka', 'Tatsuya Kitani', 'Man with a Mission', 'Mrs. GREEN APPLE', 'KANA-BOON', 'Orange Range', 'UVERworld', 'LArc~en~Ciel', 'BUMP OF CHICKEN', 'Glay', 'Spitz', 'Asian Kung-Fu Generation', 'The Oral Cigarettes', 'Novelbright', 'indigo la End', 'Daichi Miura', 'Hoshino Gen', 'Yuuri', 'Riria', 'Saucy Dog', 'Ketsumeishi', 'FUNKY MONKEY BABYS', 'Yuzu', 'SMAP', 'Arashi', 'Hey! Say! JUMP',
 'Dreams Come True', 'Every Little Thing', 'Do As Infinity', 'Globe', 'MAX', 'SPEED', 'The Brilliant Green', 'ZONE', 'Morning Musume', 'Wada Kouji', 'TM Revolution', 'Gackt', 'Luna Sea', 'X Japan', 'Buck-Tick', 'BZ', 'Mr.Children', 'Chemistry', 'EXILE', 'AAA', 'Da Pump', 'Monkey Majik', 'Porno Graffitti', 'Remioromen', 'Hitomi', 'Mika Nakashima', 'Rie fu', 'Angela Aki', 'Ken Hirai', 'Toshinobu Kubota', 'Kuwata Keisuke', 'Southern All Stars', 'Shogo Hamada', 'Seiko Matsuda', 'Yumi Matsutoya', 'Chisato Moritaka', 'Anri', 'Takako Matsu', 'Yutaka Ozaki'
]
J_ROCK_ARTISTS = [
 'LArc~en~Ciel', 'X Japan', 'Luna Sea', 'Dir En Grey', 'the GazettE', 'BZ', 'GLAY', 'Asian Kung-Fu Generation', 'BUMP OF CHICKEN', 'ONE OK ROCK', 'UVERworld', 'SPYAIR', 'FLOW', 'RADWIMPS', 'Man with a Mission', 'The Oral Cigarettes', 'Alexandros', 'SiM', 'Survive Said The Prophet', 'Fear and Loathing in Las Vegas', 'Crossfaith', 'Coldrain', 'SCANDAL', '9mm Parabellum Bullet', 'Ling Tosite Sigure', 'Nothings Carved In Stone', 'Base Ball Bear', 'ELLEGARDEN', 'Hi-STANDARD', 'The Pillows', 'Straightener', 'GRANRODEO', 'abingdon boys school', 'TM Revolution', 'MIYAVI', 'HYDE', 'Sugizo', 'YOSHIKI', 'Takahiro Moriuchi', 'ReoNa', 'Eve', 'Tatsuya Kitani', 'KANA-BOON', 'Mrs. GREEN APPLE', 'King Gnu', 'Official HIGE DANDism', 'ORANGE RANGE', 'DOES', 'NICO Touches the Walls', 'Buck-Tick', 'The Yellow Monkey', 'ZIGGY', 'Janne Da Arc', 'Acid Black Cherry', 'SIAM SHADE', 'Penicillin', 'Gackt', 'Malice Mizer', 'Versailles', 'The Brilliant Green', 'The Back Horn', 'ROOKIEZ is PUNKD', 'Nano', 'ORESAMA', 'BLUE ENCOUNT', 'Shonen Knife', 'Boris', 'Maximum the Hormone', 'POLYSICS', 'NUMBER GIRL', 'tricot', 'toe', 'MONO', 'Envy', 'Plastic Tree', 'MUCC', 'Girugamesh', 'Alice Nine', 'DespairsRay', 'NoGoD', 'SID', 'Granrodeo', 'NIGHTMARE', 'Inoran', 'Kuroyume', 'Lynch', 'TOTALFAT', 'dustbox', 'Good Morning America', 'Brian the Sun', 'My First Story'
]
J_IDOL_ARTISTS = [
    'Nogizaka46', 'Sakurazaka46', 'Hinatazaka46', 'AKB48', 'NMB48', 'HKT48', 'STU48', 'SKE48',
    'Morning Musume', 'ANGERME', 'Juice=Juice',
    'Momoiro Clover Z', 'Shiritsu Ebisu Chugaku',
    'BiSH', 'BiS', 'EMPiRE', 'GANG PARADE',
    'JO1', 'INI', 'BE:FIRST',
    'Perfume',
    'Arashi', 'Hey! Say! JUMP', 'V6', 'TOKIO', 'KAT-TUN', 'NEWS', 'Kanjani8', 'KinKi Kids', 'SMAP'
]

DATA_FILE_PATH = 'datasetspotifytracks.csv'

# Skala Warna Grafik (3 Genre)
GENRE_COLORS = alt.Scale(domain=['J-Pop', 'J-Rock', 'J-Idol'],
                         range=[P3_BLUE, P3_RED, P3_PINK])

#-----------------------------------------------------------------------------------
# Styling CSS
#-----------------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    /* General styling */
    .main .block-container, [data-testid="stSidebar"] {{
        background-color: {P3_BLACK};
        color: {P3_WHITE};
        font-family: 'Poppins', sans-serif;
    }}
    h1, h2, h3, p, label, .st-emotion-cache-16txtl3, .st-emotion-cache-qbe2hs,
    .st-emotion-cache-1gjd1a4, .st-emotion-cache-1cypcdb,
    .st-emotion-cache-1jicfl2, .st-emotion-cache-z3ycr7,
    .st-emotion-cache-aw8l5d, .st-emotion-cache-ue6h4q {{
        color: {P3_WHITE} !important;
        font-family: 'Poppins', sans-serif;
    }}

    /* Widget styling */
    .st-emotion-cache-1629p8f, .st-emotion-cache-s49nzw,
    .st-emotion-cache-76cxyh, [data-testid="stSelectbox"] div[data-baseweb="select"],
    [data-testid="stMultiselect"] {{
        background-color: {P3_DARK_NAVY};
        border-color: {P3_BLUE};
        color: {P3_WHITE};
        font-family: 'Poppins', sans-serif;
    }}
    .st-emotion-cache-1g6gooi, .st-emotion-cache-1flf0i5 {{
        color: {P3_WHITE};
        font-family: 'Poppins', sans-serif;
    }}

    /* Metric styling */
    [data-testid="stMetricLabel"] {{
        color: #AAAAAA;
        font-family: 'Poppins', sans-serif;
    }}
    [data-testid="stMetricValue"] {{
        color: {P3_WHITE};
        font-family: 'Poppins', sans-serif;
    }}

    /* Insight box styling */
    .insight-box {{
        background-color: {P3_DARK_NAVY};
        border-left: 5px solid {P3_YELLOW};
        padding: 15px; margin-bottom: 15px; border-radius: 5px;
    }}
    .insight-box h4 {{ color: {P3_YELLOW}; margin-top: 0; font-family: 'Poppins', sans-serif; }}
    .insight-box p {{ color: {P3_WHITE}; font-family: 'Poppins', sans-serif; }}

    /* Dataframe styling */
     .stDataFrame {{ font-family: 'Poppins', sans-serif; }}
</style>
""", unsafe_allow_html=True)


#-----------------------------------------------------------------------------------
# Persiapan Regex untuk Standarisasi Data
#-----------------------------------------------------------------------------------
# Membuat mapping Regex ke nama standar, urutan penting untuk prioritas genre
artist_map = {}
for artist in J_IDOL_ARTISTS:
    pattern = r'\b' + re.escape(artist) + r'\b'
    artist_map[pattern] = artist
for artist in J_ROCK_ARTISTS:
    pattern = r'\b' + re.escape(artist) + r'\b'
    artist_map[pattern] = artist
for artist in J_POP_ARTISTS:
    pattern = r'\b' + re.escape(artist) + r'\b'
    if pattern not in artist_map: # Hindari overwrite genre J-Idol/J-Rock
        artist_map[pattern] = artist

# Pattern regex gabungan untuk memfilter data awal
ALL_JP_ARTIST_PATTERN = '|'.join(artist_map.keys())
# Pattern terpisah untuk menentukan genre bersih
J_ROCK_PATTERN_LIST = [r'\b' + re.escape(artist) + r'\b' for artist in J_ROCK_ARTISTS]
J_IDOL_PATTERN_LIST = [r'\b' + re.escape(artist) + r'\b' for artist in J_IDOL_ARTISTS]
J_ROCK_PATTERN = '|'.join(J_ROCK_PATTERN_LIST)
J_IDOL_PATTERN = '|'.join(J_IDOL_PATTERN_LIST)


#-----------------------------------------------------------------------------------
# Fungsi Load & Clean Data
#-----------------------------------------------------------------------------------
@st.cache_data # Cache data untuk performa
def load_and_clean_data(file_path):
    """
    Memuat data Spotify, membersihkan, menstandarisasi,
    dan menghitung metrik baru berdasarkan daftar artis _J-Music_.
    """
    try:
        df = pd.read_csv(file_path, sep=';')
    except Exception as e:
        st.error(f"Error membaca file: {e}. Cek path & separator.")
        return pd.DataFrame()

    # Pastikan kolom esensial ada
    essential_cols = ['track_id', 'artists', 'album_name', 'track_name', 'popularity', 'duration_ms', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature', 'track_genre']
    if not all(col in df.columns for col in ['track_genre', 'artists']):
        st.error("Kolom 'track_genre' atau 'artists' tidak ditemukan.")
        return pd.DataFrame()
    df = df.loc[:, df.columns.isin(essential_cols)]

    # 1. Filter Awal: Ambil lagu berdasarkan daftar artis _J-Music_
    df_jp_music = df[df['artists'].str.contains(ALL_JP_ARTIST_PATTERN, case=False, na=False, regex=True)].copy()
    if df_jp_music.empty:
        st.error("Tidak ada lagu dari artis _J-Music_ yang ditemukan.")
        return pd.DataFrame()

    # 2. Standarisasi Genre: Buat kolom genre bersih (J-Idol -> J-Rock -> J-Pop)
    conditions = [
        df_jp_music['artists'].str.contains(J_IDOL_PATTERN, case=False, na=False, regex=True),
        df_jp_music['artists'].str.contains(J_ROCK_PATTERN, case=False, na=False, regex=True),
    ]
    choices = ['J-Idol', 'J-Rock']
    df_jp_music['track_genre'] = np.select(conditions, choices, default='J-Pop')

    # 3. Standarisasi Artis: Buat kolom artis utama yang konsisten
    def find_main_artist(artist_string):
        if not isinstance(artist_string, str): return np.nan
        for pattern, standard_name in artist_map.items():
            if re.search(pattern, artist_string, re.IGNORECASE):
                return standard_name
        return np.nan # Fallback
    df_jp_music['artist_utama'] = df_jp_music['artists'].apply(find_main_artist)

    # 4. Standarisasi Explicit: Ubah string ke boolean
    if 'explicit' in df_jp_music.columns:
        df_jp_music['explicit'] = df_jp_music['explicit'].map({'TRUE': True, 'FALSE': False, True: True, False: False}).fillna(False)
    else:
        st.error("Kolom 'explicit' tidak ditemukan.")
        return pd.DataFrame()

    # 5. Koreksi Tipe Data Numerik: Tangani koma desimal & konversi
    cols_to_convert = ['popularity', 'danceability', 'energy', 'loudness', 'valence', 'tempo', 'acousticness', 'instrumentalness', 'speechiness', 'liveness', 'duration_ms']
    for col in cols_to_convert:
        if col in df_jp_music.columns:
            if df_jp_music[col].dtype == 'object':
                df_jp_music[col] = df_jp_music[col].astype(str).str.replace(',', '.', regex=False)
            df_jp_music[col] = pd.to_numeric(df_jp_music[col], errors='coerce') # Nilai error jadi NaN

    # 6. Handle Missing Values: Hapus baris dengan NaN di kolom kunci
    key_columns = ['track_name', 'artists', 'artist_utama', 'explicit', 'popularity', 'danceability', 'energy', 'valence', 'duration_ms']
    rows_before = len(df_jp_music)
    df_jp_music = df_jp_music.dropna(subset=key_columns)
    rows_after = len(df_jp_music)
    st.session_state.cleaning_info = f"Pembersihan Data: {rows_before - rows_after} baris data tidak valid dihapus. Genre & Artis distandarisasi." # Info cleaning

    # 7. Final Type Conversion: Pastikan tipe data sesuai
    if not df_jp_music.empty:
      df_jp_music['popularity'] = df_jp_music['popularity'].astype(int)

    # 8. Feature Engineering: Buat metrik baru
    df_jp_music['duration_min'] = (df_jp_music['duration_ms'] / 60000).round(2)
    df_jp_music['positivity_index'] = (df_jp_music['energy'] * df_jp_music['valence']).round(3)

    return df_jp_music

#-----------------------------------------------------------------------------------
# Fungsi Pembuat Visualisasi & Insight
#-----------------------------------------------------------------------------------
# (Fungsi-fungsi chart tidak perlu komentar detail karena self-explanatory dengan Altair)
def create_top_artists_chart(df_filtered):
    df_top_artists = df_filtered.groupby(['artist_utama', 'track_genre'])['popularity'].mean().reset_index()
    df_top_artists = df_top_artists.sort_values('popularity', ascending=False).head(10)
    chart = alt.Chart(df_top_artists).mark_bar(opacity=0.8).encode(
        x=alt.X('popularity:Q', title='Popularitas Global Rata-rata (Skor Spotify)'),
        y=alt.Y('artist_utama:N', title='Artis Utama', sort='-x'),
        color=alt.Color('track_genre:N', title="Genre", scale=GENRE_COLORS),
        tooltip=['artist_utama', 'track_genre', alt.Tooltip('popularity:Q', format='.2f')]
    ).properties(title='Top 10 Artis _J-Music_ Berdasarkan Popularitas Global Rata-rata').interactive()
    return chart, df_top_artists

def create_danceability_density(df_filtered):
    chart = alt.Chart(df_filtered).transform_density(
        'danceability', as_=['danceability_value', 'density'], groupby=['track_genre']
    ).mark_area(orient='horizontal', opacity=0.5).encode(
        y=alt.Y('danceability_value:Q', title='Skor Danceability'),
        x=alt.X('density:Q', stack='center', title='Kepadatan Distribusi', axis=None),
        color=alt.Color('track_genre:N', title="Genre", scale=GENRE_COLORS),
        tooltip=['track_genre', alt.Tooltip('danceability_value:Q', format='.2f')]
    ).properties(title='Distribusi Danceability per Genre').interactive()
    return chart

def create_tempo_boxplot(df_filtered):
    chart = alt.Chart(df_filtered).mark_boxplot().encode(
        x=alt.X('track_genre:N', title='Genre'),
        y=alt.Y('tempo:Q', title='Tempo (BPM)'),
        color=alt.Color('track_genre:N', title="Genre", scale=GENRE_COLORS),
        tooltip=['track_genre', alt.Tooltip('tempo:Q', title='Tempo (BPM)')]
    ).properties(title='Perbandingan Tempo & Anomali per Genre').interactive()
    return chart

def create_energy_valence_scatter(df_filtered):
    chart = alt.Chart(df_filtered).mark_circle(opacity=0.6, size=60).encode(
        x=alt.X('energy:Q', title='Energi Lagu', scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('valence:Q', title='Nuansa Positif (Valence)', scale=alt.Scale(domain=[0, 1])),
        tooltip=['track_name', 'artists', 'artist_utama', 'track_genre',
                    alt.Tooltip('energy:Q', format='.2f'), alt.Tooltip('valence:Q', format='.2f')],
        color=alt.Color('track_genre:N', title="Genre", scale=GENRE_COLORS)
    ).properties(title='Pemetaan Energi vs. Nuansa Positif Lagu _J-Music_').interactive()
    return chart

def display_insights(df_filtered, df_top_artists):
    """Menampilkan bagian Insight & Rekomendasi."""
    st.header("💡 Insight Kunci & Rekomendasi Kolaborasi untuk Menggaet Pasar Internasional")
    st.caption("Bagaimana temuan ini membantu Anda memilih partner kolaborasi Musik Jepang (_J-Music_) dengan potensi global?")

    # Insight 1: Artis Populer
    top_jpop = df_top_artists[df_top_artists['track_genre'] == 'J-Pop']['artist_utama'].iloc[0] if not df_top_artists[df_top_artists['track_genre'] == 'J-Pop'].empty else None
    top_jrock = df_top_artists[df_top_artists['track_genre'] == 'J-Rock']['artist_utama'].iloc[0] if not df_top_artists[df_top_artists['track_genre'] == 'J-Rock'].empty else None
    top_jidol = df_top_artists[df_top_artists['track_genre'] == 'J-Idol']['artist_utama'].iloc[0] if not df_top_artists[df_top_artists['track_genre'] == 'J-Idol'].empty else None
    artis_populer_text = "Grafik Top 10 menyoroti artis dengan popularitas global tertinggi"
    if top_jpop: artis_populer_text += f", seperti <strong>{top_jpop}</strong> (_J-Pop_)"
    if top_jrock: artis_populer_text += f", <strong>{top_jrock}</strong> (_J-Rock_)"
    if top_jidol: artis_populer_text += f", dan <strong>{top_jidol}</strong> (_J-Idol_)"
    artis_populer_text += ". Ketenaran global mereka adalah modal kuat untuk menggaet pasar internasional."
    st.markdown(f"""<div class="insight-box"><h4>Insight 1: Identifikasi Artis Berdaya Tarik Global</h4><p>{artis_populer_text}</p><p><strong>Rekomendasi Actionable:</strong> Prioritaskan artis dari Top 10 ini. Popularitas global mereka meningkatkan peluang lagu kolaborasi diterima baik di Indonesia maupun pasar internasional lainnya.</p></div>""", unsafe_allow_html=True)

    # Insight 2: Karakteristik Audio
    avg_dance_pop = df_filtered[df_filtered['track_genre'] == 'J-Pop']['danceability'].mean()
    avg_dance_rock = df_filtered[df_filtered['track_genre'] == 'J-Rock']['danceability'].mean()
    avg_dance_idol = df_filtered[df_filtered['track_genre'] == 'J-Idol']['danceability'].mean()
    insight_dance = "Perbandingan _danceability_ antar genre menunjukkan variasi:"
    rekomendasi_dance = "Rekomendasi terkait ritme kolaborasi:"
    dance_means = []
    if not pd.isna(avg_dance_pop): dance_means.append(("J-Pop", avg_dance_pop))
    if not pd.isna(avg_dance_rock): dance_means.append(("J-Rock", avg_dance_rock))
    if not pd.isna(avg_dance_idol): dance_means.append(("J-Idol", avg_dance_idol))
    dance_means.sort(key=lambda item: item[1], reverse=True)
    if len(dance_means) > 1:
        insight_dance += f" Genre paling _danceable_ adalah <strong>{dance_means[0][0]}</strong> ({dance_means[0][1]:.2f}), terendah adalah <strong>{dance_means[-1][0]}</strong> ({dance_means[-1][1]:.2f})."
        if dance_means[0][0] == 'J-Idol' or dance_means[0][0] == 'J-Pop':
             rekomendasi_dance += f" Kolaborasi dengan artis {dance_means[0][0]} dapat menonjolkan elemen *upbeat*."
        elif dance_means[0][0] == 'J-Rock':
             rekomendasi_dance += f" Kolaborasi J-Rock bisa mempertahankan beat kuatnya atau beradaptasi."
    else:
         insight_dance = "Distribusi _danceability_ (lihat grafik density) menunjukkan preferensi ritme."
         rekomendasi_dance = "Sesuaikan ritme lagu kolaborasi berdasarkan target spesifik Anda."
    st.markdown(f"""<div class="insight-box"><h4>Insight 2: Sesuaikan Karakteristik Audio dengan Target Pasar</h4><p>{insight_dance} Scatter plot Energi vs. Valence juga memvisualisasikan klaster 'mood'.</p><p><strong>Rekomendasi Actionable:</strong> {rekomendasi_dance} Manfaatkan scatter plot untuk memahami 'signature mood' tiap genre dan cari kombinasi unik.</p></div>""", unsafe_allow_html=True)

#-----------------------------------------------------------------------------------
# === BAGIAN UTAMA APLIKASI STREAMLIT ===
#-----------------------------------------------------------------------------------

# Load data menggunakan fungsi di atas
df = load_and_clean_data(DATA_FILE_PATH)

# Hentikan jika data gagal dimuat/dibersihkan
if df.empty:
    st.stop()

# --- Render Sidebar ---
st.sidebar.header('⚙️ Filter Dashboard')
all_genres = sorted(df['track_genre'].unique())
selected_genres = st.sidebar.multiselect('Pilih Genre:', all_genres, default=all_genres)
min_pop = int(df['popularity'].min()) if not df['popularity'].empty else 0
max_pop = int(df['popularity'].max()) if not df['popularity'].empty else 100
selected_popularity = st.sidebar.slider('Pilih Rentang Popularitas (Global):', min_pop, max_pop, (min_pop, max_pop))
st.sidebar.markdown("---")
if 'cleaning_info' in st.session_state: st.sidebar.info(st.session_state.cleaning_info)

# --- Filter Dataframe berdasarkan input sidebar ---
df_filtered = df[(df['popularity'] >= selected_popularity[0]) & (df['popularity'] <= selected_popularity[1])]
if selected_genres:
    df_filtered = df_filtered[df_filtered['track_genre'].isin(selected_genres)]
else:
    df_filtered = pd.DataFrame(columns=df.columns) # Kosongkan jika tidak ada genre dipilih

# Hentikan jika hasil filter kosong
if df_filtered.empty:
    st.warning("Tidak ada data __J-Music__ yang cocok dengan filter Anda.")
    st.stop()

# --- Render Tampilan Utama ---
st.title('🎵 Analisis _J-Music_: Memilih Partner Kolaborasi yang Memiliki Daya tarik Global')
st.caption("Dashboard Ini Menganalisis Popularitas Global dan Karakteristik Musik dari Genre _J-Pop, J-Rock,_ dan _J-Idol_ untuk Membantu Produser/Artis Indonesia Menemukan Partner Kolaborasi dengan Potensi Pasar Internasional.")

# --- Render KPI Cards ---
st.markdown("---")
st.subheader("Ringkasan Data")
total_tracks = len(df_filtered)
avg_popularity = df_filtered['popularity'].mean() if total_tracks > 0 else 0
avg_danceability = df_filtered['danceability'].mean() if total_tracks > 0 else 0
avg_positivity = df_filtered['positivity_index'].mean() if total_tracks > 0 else 0
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Lagu Dianalisis", f"{total_tracks} 🎶")
with col2: st.metric("Rata-rata Popularitas (Global)", f"{avg_popularity:.2f} 🔥")
with col3: st.metric("Rata-rata Danceability", f"{avg_danceability:.2f} 💃")
with col4: st.metric("Rata-rata Positivity", f"{avg_positivity:.2f} 😊")
st.markdown("---")

# --- Render Visualisasi ---
st.header('Pertanyaan 1: Artis Jepang Mana yang Populer Secara Global?')
st.caption("Siapa saja artis _J-Music_ dengan jangkauan internasional terluas ? Grafik ini menunjukkan 10 Artis teratas berdasarkan popularitas global rata-rata mereka pada Spotify.")
chart1, df_top_artists_for_insight = create_top_artists_chart(df_filtered)
st.altair_chart(chart1, use_container_width=True)

st.markdown("---")
st.header("Pertanyaan 2: Bagaimana Karakteristik Audio _J-Music_ Dibandingkan Antar Genre?")
st.caption("Apakah ada 'formula' untuk sebuah genre musik populer? Grafik density dibawah membandingkan _danceability_, Box plot membandingkan tempo & anomali.")
col_a, col_b = st.columns(2)
with col_a:
    chart2 = create_danceability_density(df_filtered)
    st.altair_chart(chart2, use_container_width=True)
with col_b:
    chart4 = create_tempo_boxplot(df_filtered)
    st.altair_chart(chart4, use_container_width=True)

st.markdown("---")
st.header('Pertanyaan 3: Di Mana Posisi "Mood" _J-Music_ di Peta Musik Global?')
st.caption("Bagaimana _mood_ khas yang dimiliki  tiap genre _J-Music_ (Energi vs Nuansa Positif) ? Grafik ini membantu merancang lagu kolaborasi yang dapat memberikan kesan unik.")
chart3 = create_energy_valence_scatter(df_filtered)
st.altair_chart(chart3, use_container_width=True)

st.markdown("---")

# --- Render Insight & Rekomendasi ---
display_insights(df_filtered, df_top_artists_for_insight)

st.markdown("---")

# --- Render Data Mentah (dalam expander) ---
with st.expander("📊 Tampilkan Detail Data Lagu", expanded=False):
    st.subheader("Data Lagu _J-Music_ yang Telah Melalui Proses Filterisasi")
    df_display = df_filtered[['track_name', 'artists', 'artist_utama', 'track_genre', 'popularity', 'explicit', 'danceability', 'energy', 'valence', 'duration_min', 'positivity_index']].copy()
    df_display.index = np.arange(1, len(df_display) + 1) # Index mulai dari 1
    st.dataframe(df_display, use_container_width=True)

