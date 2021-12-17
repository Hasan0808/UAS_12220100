#NAMA : Rafiyuddin Hasan
#NIM : 12220100

### --- IMPORT
import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

st.set_page_config(page_title="UAS_12220100",
                   page_icon=":bar_chart:",
                   layout="wide")
def header_web():
    st.image('https://patra.itb.ac.id/wp-content/themes/patra/images/logo.png',width=200)
    st.header('Data Produksi Minyak Tahun 1971-2015')



### --- MASUKKAN DATA
data_minyak = pd.read_csv('produksi_minyak_mentah.csv')
data_negara = pd.read_json('kode_negara_lengkap.json')
data_negara = data_negara.loc[:,['name','alpha-3','region','sub-region']]

### --- UBAH DATA TO MENJADI FRAME
dfm = pd.DataFrame(data_minyak)
dfn = pd.DataFrame(data_negara)

### --- GABUNGKAN DATA FRAME
merged_df = pd.merge(dfn,dfm, left_on='alpha-3',right_on='kode_negara')
#merged_df = pd.merge(dfn,merged_df, left_on='sub-region',right_on='kode_negara')
list_negara = merged_df['name'].unique().tolist() #ubah df menjadi list dan menghapus data yg duplikat
list_tahun = merged_df['tahun'].unique().tolist()

def mainmenu():
    header_web()
    st.header('Selamat Datang !')
    st.subheader('Silahkan PIlih Fitur Dengan Memilih Salah Satu Menu Pada SideBar')
def biodata():
    header_web()
    a, b, c = st.columns(3)
    with a:
        st.header(' Biodata Creator ')
        image = Image.open('fotodiri.jpg')
        st.image(image,width = 250)
        st.caption('Nama  :Rafiyuddin Hasan')
        st.caption('NIM   :12220100')
        st.caption('Kelas :IF2112 Pemrograman Komputer K-02')
        st.caption('Dosen :Habibur Muhaimin ST,M.Sc.')

### --- A. GRAFIK PRDUKSI NEGARA (N) TERHADAP TAHUN
def fungsi_A():
    header_web()
    col1,col2,col3=st.columns(3)
    pilihan_negara = st.selectbox('Pilih Negara:',list_negara)
    dataA = merged_df[merged_df['name'] == pilihan_negara]
    #Buat grafik

    st.subheader(f'Grafik Jumlah Produksi Minyak {pilihan_negara}')
    grafik_a = px.line(dataA, x="tahun", y="produksi",template="plotly_white",
                       labels={"tahun": "Tahun",
                               "produksi":" Jumlah minyak (BO)" })
    #menampilkan tabel
    tabel_a = dataA.set_index('tahun').rename(columns={'produksi': "Jumlah Produksi Minyak"})['Jumlah Produksi Minyak']
    #output
    left,right = st.columns(2)
    with left:
        st.plotly_chart(grafik_a)
    with right:
        st.write(tabel_a)


### --- B. GRAFIK NEGARA PRODUKSI MINYAK TERBESAR PADA TAHUN TERTENTU
def fungsi_B():
    header_web()
    pilihan_tahun = st.selectbox('Pilih Tahun:',list_tahun)
    tahun = merged_df[merged_df['tahun']==pilihan_tahun]
    banyak_negara = st.number_input('Banyak Negara:',0,136)
    df_tahun = tahun.nlargest(banyak_negara,'produksi')
    st.subheader(f'{banyak_negara} Negara Dengan Produksi Minyak Terbesar Pada Tahun {pilihan_tahun}')

    #buat GRAFIK
    grafik_b = px.bar(df_tahun,x='name',y='produksi',color='name',
                      labels={"name": "Negara",
                              "produksi": "Jumlah minyak (BO)" })
    #menampilkan tabel
    tabel_b = df_tahun.set_index('name').rename(columns={'produksi': "Jumlah Produksi Minyak"})['Jumlah Produksi Minyak']
    #output
    left,right = st.columns(2)
    with left:
        st.plotly_chart(grafik_b)
    with right:
        st.write(tabel_b)

### --- C.GRAFIK NEGARA PRODUKSI MINYAK TERBESAR KUMULATIF
def fungsi_C():
    header_web()
    banyak_negara = st.number_input('Banyak Negara:',0,136)
    df_C = merged_df[['name','produksi']].groupby(['name'])['produksi'].sum().reset_index().reset_index(drop=True)
    df_C = df_C.nlargest(banyak_negara,'produksi')
    st.subheader(f'{banyak_negara} Negara Dengan Produksi Minyak Terbesar Pada Tahun 1971-2015')
    #buat GRAFIK
    grafik_C = px.bar(df_C,x="name",y="produksi",template="plotly_white",color="name",
                      labels={"name": "Negara",
                              "produksi": "Jumlah minyak (BO)"},)
    #menampilkan tabel
    tabel_C = df_C.set_index('name').rename(columns={'produksi': "Jumlah Produksi Minyak"})['Jumlah Produksi Minyak']
    #output
    left,right = st.columns(2)
    with left:
        st.plotly_chart(grafik_C)
    with right:
        st.write(tabel_C)

### --- Da
def fungsi_Da():
    header_web()
    #berdasarkan tahun
    #Produksi Terbesar
    pilihan_tahun = st.selectbox('Pilih Tahun:',list_tahun)
    df_Db = merged_df[merged_df['tahun']==pilihan_tahun]
    df_Db = df_Db.groupby(['name', 'region', 'sub-region','kode_negara'])['produksi'].sum().reset_index().reset_index(drop=True)
    tahun_terbesar = df_Db.nlargest(1,'produksi')
    negara_terbesar = tahun_terbesar['name'].to_string(index=False)
    jumlah_terbesar = merged_df[merged_df['name'] == negara_terbesar]['produksi'].sum()
    #Produksi Terkecil
    tahun_terkecil = df_Db[df_Db['produksi']!=0].groupby(['name','region','sub-region','kode_negara'])['produksi'].sum().reset_index().reset_index(drop=True)
    tahun_terkecil = tahun_terkecil.nsmallest(1,'produksi')
    negara_terkecil = tahun_terkecil['name'].to_string(index=False)
    jumlah_terkecil = merged_df[merged_df['name'] == negara_terkecil]['produksi'].sum()

    jumlah_keseluruhan = merged_df.groupby('name').sum().reset_index()
    #Produksi = 0
    tahun_nol = df_Db[df_Db['produksi']==0]
    jumlah_keseluruhan = jumlah_keseluruhan[jumlah_keseluruhan['name'].isin(tahun_nol['name'])]
   
    a,b,c = st.columns(3)
    with b:
        st.subheader(f'Jumlah produksi pada tahun {pilihan_tahun}')
    left_column,right_column = st.columns(2)

    with left_column:
        st.subheader(f'Produksi Terbanyak')
        st.caption(f'Negara: {tahun_terbesar.name.to_string(index=False)} ')
        st.caption(f'Kode Negara: {tahun_terbesar["kode_negara"].to_string(index=False)}')
        st.caption(f'Region: {tahun_terbesar.region.to_string(index=False)}')
        st.caption(f'Sub-region: {tahun_terbesar["sub-region"].to_string(index=False)}')
        st.caption(f'Jumlah Produksi Tahun {pilihan_tahun}: {tahun_terbesar["produksi"].to_string(index=False)} BO')
        
    with right_column:
        st.subheader(f'Produksi Terkecil')
        st.caption(f'Negara: {tahun_terkecil.name.to_string(index=False)} ')
        st.caption(f'Kode Negara: {tahun_terkecil["kode_negara"].to_string(index=False)}')
        st.caption(f'Region: {tahun_terkecil.region.to_string(index=False)}')
        st.caption(f'Sub-region: {tahun_terkecil["sub-region"].to_string(index=False)}')
        st.caption(f'Jumlah Produksi Tahun {pilihan_tahun}: {tahun_terkecil["produksi"].to_string(index=False)} BO')
    
    st.subheader(f'Negara yang Tidak Memproduksi Minyak Pada Tahun {pilihan_tahun}')
    st.write(tahun_nol.style.hide_index())

### --- Db
def fungsi_Db():
    header_web()
    #keseluruhan tahun
    df_Dk = merged_df.groupby(['name', 'region', 'sub-region','kode_negara'])['produksi'].sum().reset_index().reset_index(drop=True)
    #Produksi Terbesar
    tahun_terbesar_kumulatif = df_Dk.nlargest(1,'produksi')
    negara_terbesar_kumulatif = tahun_terbesar_kumulatif['name'].to_string(index=False)
    #Produksi Terkecil
    tahun_terkecil_kumulatif = merged_df[merged_df['produksi']!=0].groupby(['name','region','sub-region','kode_negara'])['produksi'].sum().reset_index().reset_index(drop=True)
    tahun_terkecil_kumulatif = tahun_terkecil_kumulatif.nsmallest(1,'produksi')
    negara_terkecil_kumulatif = tahun_terbesar_kumulatif['name'].to_string(index=False)
    #Produksi = 0 
    tahun_nol_kumulatif = df_Dk[df_Dk['produksi']==0]
    a,b,c = st.columns(3)
    with b:
        st.subheader(f'Jumlah Produksi Keseluruhan Tahun')
    left_column,right_column = st.columns(2)

    with left_column:
        st.subheader(f'Produksi Terbanyak')
        st.caption(f'Negara: {tahun_terbesar_kumulatif.name.to_string(index=False)} ')
        st.caption(f'Kode Negara: {tahun_terbesar_kumulatif["kode_negara"].to_string(index=False)}')
        st.caption(f'Region: {tahun_terbesar_kumulatif.region.to_string(index=False)}')
        st.caption(f'Sub-region: {tahun_terbesar_kumulatif["sub-region"].to_string(index=False)}')
        st.caption(f'Jumlah Produksi: {tahun_terbesar_kumulatif["produksi"].to_string(index=False)} BO')
    with right_column:
        st.subheader(f'Produksi Terkecil')
        st.caption(f'Negara: {tahun_terkecil_kumulatif.name.to_string(index=False)} ')
        st.caption(f'Kode Negara: {tahun_terkecil_kumulatif["kode_negara"].to_string(index=False)}')
        st.caption(f'Region: {tahun_terkecil_kumulatif.region.to_string(index=False)}')
        st.caption(f'Sub-region: {tahun_terkecil_kumulatif["sub-region"].to_string(index=False)}')
        st.caption(f'Jumlah Produksi: {tahun_terkecil_kumulatif["produksi"].to_string(index=False)} BO')

    st.subheader(f'Negara yang Tidak Memproduksi Minyak Keseluruhan')
    st.write(tahun_nol_kumulatif.style.hide_index())

### --- keluaran

list_menu = ['Main Menu','Biodata','Produksi Minyak Sebuah Negara','Produksi Terbesar Tahun Tertentu','Produksi Terbesar Keseluruhan','Produksi Tahun Tertentu','Produksi Keseluruhan']

menu = st.sidebar.selectbox('Menu',list_menu)
if menu == list_menu[0]:
    mainmenu()
elif menu == list_menu[1]:
    biodata()
elif menu == list_menu[2]:
    fungsi_A()
elif menu == list_menu[3]:
    fungsi_B()
elif menu == list_menu[4]:
    fungsi_C()
elif menu == list_menu[5]:
    fungsi_Da()
elif menu == list_menu[6]:
    fungsi_Db()