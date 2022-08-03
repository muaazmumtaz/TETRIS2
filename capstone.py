import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly as py
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import plotly.graph_objs as go
import plotly.express as px
from PIL import Image


st.set_page_config(layout="wide")
st.title("KORUPSI : Oknum atau Budaya")
st.markdown('Oleh : Muhammad Atqa Adzkia Zaldi')

# BAB I
st.header("BAB I : Korupsi di Dunia")

# Isi
'''
Korupsi merupakan salah satu masalah hal yang tidak akan pernah lepas apabila kita membahas suatu negara. 
Korupsi dapat terjadi karena adanya penyalahgunaan kekuasaan dan kepercayaan untuk keuntungan pribadi contohnya 
melakukan suap untuk mendapatkan keekslusifan akses publik hingga pencucian uang. Korupsi dapat menjadi masalah 
yang serius bagi masyarakat contohnya bantuan yang tidak sampai, infrastruktur minim spesifikasi dengan harga 
menggunung hingga monetisasi kesehatan yang menimbulkan kematian.\n

Salah satu parameter yang dapat dilihat untuk mengetahui tinggi rendahnya tingkat korupsi suatu negara yaitu 
melalui CPI (Corruption Perception Index) yang dirilis oleh organisasi anti-korupsi Transparency International. 
Data yang didapat merupakan CPI global dari tahun 2012 hingga 2021 dengan total 180 negara / teritori dengan skor yang 
ditampilkan memiliki skala 0 (sangat korup) hingga 100 (sangat bersih).
'''

# Ambil data CPI dan Cleaning
CPI = pd.read_excel('DATA/CPI_2012-2021.xlsx')
CPI_copy = CPI.copy()
CPI_copy = CPI_copy.drop(columns=['Sources 2021', 'Standard error 2021', 'Sources 2020', 'Standard error 2020',
                                  'Sources 2019', 'Standard error 2019', 'Sources 2018', 'Standard error 2018',
                                  'Sources 2017', 'Standard error 2017', 'Sources 2016', 'Standard error 2016',
                                  'Sources 2015', 'Standard error 2015', 'Sources 2014', 'Standard error 2014',
                                  'Sources 2013', 'Standard error 2013', 'Sources 2012', 'Standard error 2012'])
CPI_copy['Rank 2016'] = CPI_copy['CPI score 2016'].rank(method='min', ascending=False)
CPI_copy['Rank 2015'] = CPI_copy['CPI score 2015'].rank(method='min', ascending=False)
CPI_copy['Rank 2014'] = CPI_copy['CPI score 2014'].rank(method='min', ascending=False)
CPI_copy['Rank 2013'] = CPI_copy['CPI Score 2013'].rank(method='min', ascending=False)
CPI_copy['Rank 2012'] = CPI_copy['CPI Score 2012'].rank(method='min', ascending=False)
CPI_copy.rename(columns = {'CPI Score 2012':'CPI score 2012',
                           'CPI Score 2013':'CPI score 2013'}, inplace = True)
# Pilihan Tahun terbesar dan terkecil dan Data Tertinggi dan Terendah
tahun_cpi = st.selectbox(
                        "Pilih Tahun CPI",
                        ('2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012')
                        )
tertinggi = CPI_copy['Country / Territory'].loc[CPI_copy[f'Rank {tahun_cpi}'] == CPI_copy[f'Rank {tahun_cpi}'].min()].values[0]
val_tinggi = CPI_copy[f'CPI score {tahun_cpi}'].loc[CPI_copy[f'Rank {tahun_cpi}'] == CPI_copy[f'Rank {tahun_cpi}'].min()].values[0]
terendah = CPI_copy['Country / Territory'].loc[CPI_copy[f'Rank {tahun_cpi}'] == CPI_copy[f'Rank {tahun_cpi}'].max()].values[0]
val_rendah = CPI_copy[f'CPI score {tahun_cpi}'].loc[CPI_copy[f'Rank {tahun_cpi}'] == CPI_copy[f'Rank {tahun_cpi}'].max()].values[0]

cpi_tertinggi, cpi_terendah = st.columns(2)
with cpi_tertinggi:
    st.metric("Rank Pertama", tertinggi, val_tinggi, delta_color='off')
with cpi_terendah:
    st.metric("Rank Terakhir", terendah, val_rendah, delta_color='off')

# Fungsi CPI Global
def cpi_global_plot(year = '2021'):
    data = dict(type = 'choropleth',
                locations = CPI_copy['Country / Territory'], 
                locationmode = 'country names',
                colorscale= 'blackbody',
                text= CPI_copy['ISO3'],
                z = CPI_copy[f'CPI score {year}'],
                colorbar = {'title':f'CPI Skor {year}'})
    chmap = go.Figure(data=[data])
    chmap.update_layout(
        title_text = f'CPI Global {year}',
        title_x = 0.5
    )
    return chmap

df_cpi, graph_cpi = st.columns([2, 5])

with df_cpi:
    df = CPI_copy[[f'Rank {tahun_cpi}', 'Country / Territory', f'CPI score {tahun_cpi}']]
    df = df.sort_values(by=[f'Rank {tahun_cpi}'])
    df = df.dropna()
    df[f'Rank {tahun_cpi}'] = df[f'Rank {tahun_cpi}'].astype('int')
    df[f'CPI score {tahun_cpi}'] = df[f'CPI score {tahun_cpi}'].astype('int')
    df = df.rename(columns= {f'CPI score {tahun_cpi}':'CPI'})
    df = df.set_index(f'Rank {tahun_cpi}')
    st.dataframe(df)

with graph_cpi:
    fig1 = cpi_global_plot(tahun_cpi)
    st.plotly_chart(fig1, use_container_width=True)

st.caption('Sumber : https://www.transparency.org/')

# Isi mengenai CPI Global
'''
Denmark merupakan negara yang mempertahankan peringkat CPI tertinggi selama 4 tahun terakhir dengan skor CPI ± 88. 
Indonesia pada tahun 2021 menempati peringkat 96 dari 180 negara dengan skor CPI sebesar 38 dengan rata-rata global CPI berada 
pada 43,27 yang menandakan Indonesia masih berada dibawah rata-rata negara dunia menurut skor CPI. Hal ini memberitahu 
kita bahwa permasalahan korupsi di Indonesia masih merupakan hal yang besar dan perlu untuk segera ditangani.
'''

# Fungsi CPI / Negara
negara_cpi = st.selectbox(
                        "Pilih Negara",
                        ('Afghanistan', 'Albania', 'Algeria', 'Angola', 'Argentina',
                         'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
                         'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Benin',
                         'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana',
                         'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso',
                         'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada',
                         'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia',
                         'Comoros', 'Congo', 'Costa Rica', "Cote d'Ivoire", 'Croatia',
                         'Cuba', 'Cyprus', 'Czechia', 'Democratic Republic of the Congo',
                         'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador',
                         'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
                         'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon',
                         'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada',
                         'Guatemala', 'Guinea', 'Guinea Bissau', 'Guyana', 'Haiti',
                         'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India',
                         'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy',
                         'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya',
                         'Korea, North', 'Korea, South', 'Kosovo', 'Kuwait', 'Kyrgyzstan',
                         'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
                         'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia',
                         'Maldives', 'Mali', 'Malta', 'Mauritania', 'Mauritius', 'Mexico',
                         'Moldova', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique',
                         'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand',
                         'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway',
                         'Oman', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay',
                         'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania',
                         'Russia', 'Rwanda', 'Saint Lucia',
                         'Saint Vincent and the Grenadines', 'Sao Tome and Principe',
                         'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
                         'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
                         'South Africa', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan',
                         'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan',
                         'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo',
                         'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan',
                         'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
                         'United States of America', 'Uruguay', 'Uzbekistan', 'Vanuatu',
                         'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe')
                        )

def cpi_negara(negara_):
    data = dict(negara = negara_,
                tahun = [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
                CPI = [float(CPI_copy['CPI score 2012'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2013'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2014'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2015'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2016'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2017'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2018'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2019'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2020'].loc[CPI_copy['Country / Territory'] == negara_]),
                       float(CPI_copy['CPI score 2021'].loc[CPI_copy['Country / Territory'] == negara_]),],
                rerata = [CPI_copy['CPI score 2012'].mean(),
                          CPI_copy['CPI score 2013'].mean(),
                          CPI_copy['CPI score 2014'].mean(),
                          CPI_copy['CPI score 2015'].mean(),
                          CPI_copy['CPI score 2016'].mean(),
                          CPI_copy['CPI score 2017'].mean(),
                          CPI_copy['CPI score 2018'].mean(),
                          CPI_copy['CPI score 2019'].mean(),
                          CPI_copy['CPI score 2020'].mean(),
                          CPI_copy['CPI score 2021'].mean()]
                )
    data_cpi = pd.DataFrame(data)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data_cpi["tahun"], 
                  y=data_cpi["CPI"],
                  name=f'CPI Skor {negara_}'))
    fig2.add_trace(go.Scatter(x=data_cpi["tahun"], 
                  y=data_cpi["rerata"],
                  name='Rata-Rata CPI Skor Global'))
    fig2.update_layout(
                       title_text=f'CPI Skor {negara_} vs Rata-Rata CPI Skor Global',
                       title_x = 0.5
                      )
    fig2.update_xaxes(title_text="Tahun")
    fig2.update_yaxes(title_text="CPI Skor")
    return fig2

st.plotly_chart(cpi_negara(negara_cpi), use_container_width=True)
st.caption('Sumber : https://www.transparency.org/')


# BAB II
st.header("BAB II : Korupsi di Indonesia")

# Plot Indonesia
korupsi = pd.read_excel('DATA/TREN_KORUPSI.xlsx')
# CPI Index Indonesia
fig_cpi = cpi_negara("Indonesia")
st.plotly_chart(fig_cpi, use_container_width=True)
st.caption('Sumber : https://www.transparency.org/')

'''
Selama 10 tahun terakhir, skor CPI Indonesia selalu dibawah rata-rata CPI global. 
CPI Indonesia tertinggi pada tahun 2019 dengan skor 40 dan terendah pada tahun 2012 dan 2013 dengan skor 32. Hal ini 
menandakan bahwa tindak korupsi di Indonesia masih lebih tinggi dibandingkan dengan rata-rata tindak korupsi global 
selama 10 tahun terakhir.
'''
# Kerugian Negara
fig_kerugian = px.line(korupsi, x="Tahun", y="Kerugian Negara (Miliar)")
fig_kerugian.update_layout(title_text='Kerugian Negara Akibat Korupsi',
                           title_x = 0.5
                          )
st.plotly_chart(fig_kerugian, use_container_width=True)
st.caption('Sumber : https://www.antikorupsi.org/')

'''
Setiap terjadi korupsi akan mengakibatkan kerugian negara. Terjadi lonjakan yang sangat signifikan pada tahun 2020 
sebesar 472% yaitu kerugian negara sebesar Rp. 56,7 triliun dari tahun 2019 dengan jumlah kerugian sebesar Rp. 12 triliun. 
Pada tahun 2021 terjadi kenaikan jumlah kerugian korupsi sebesar 5% dari tahun 2020 yaitu Rp. 62,9 triliun yang mana nilai kerugian 
ini merupakan kerugian negara terbesar karena korupsi selama 6 tahun terakhir dengan korupsi terbesar dilakukan oleh Raden Priyono sebagai 
kepala BP Migas yaitu korupsi kondensat migas PT Trans Pacific Petrochemical Indonesia senilai Rp. 36 triliun kemudian Fakhri Hilmi sebagai 
kepala Departemen Pengawasan OJK yaitu korupsi Jiwasraya sebesar Rp. 16 triliun.
'''

# Terdakwa vs Perkara
fig_pt = go.Figure()
fig_pt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Perkara'],
    name='Jumlah Perkara',
    marker_color='indianred'
))
fig_pt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Terdakwa'],
    name='Jumlah Terdakwa',
    marker_color='blue'
))
fig_pt.update_layout(barmode='group',
                     xaxis_tickangle=-45,
                     title_text='Jumlah Perkara dan Terdakwa Korupsi',
                     title_x = 0.5
                    )
fig_pt.update_xaxes(title_text="Tahun")
st.plotly_chart(fig_pt, use_container_width=True)
st.caption('Sumber : https://www.antikorupsi.org/')

# Isi Perkara VS Terdakwa
'''
Pada kasus jumlah perkara dan terdakwa korupsi menunjukkan terjadi kenaikan selama 3 tahun terakhir dengan jumlah 
perkara dan terdakwa tertinggi terjadi di tahun 2021 yaitu 1282 perkara dan 1404 terdakwa yang merupakan jumlah perkara
dan terdakwa tertinggi selama 6 tahun terakhir. Ini menunjukkan bahwa pada beberapa tahun terakhir ini korupsi makin merajalela 
di Indonesia.
'''

# Pekerjaan Terdakwa
fig_pkt = go.Figure()
fig_pkt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Perangkat Desa'],
    name='Perangkat Desa',
    marker_color='indianred'
))
fig_pkt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Perangkat Daerah'],
    name='Perangkat Daerah',
    marker_color='blue'
))
fig_pkt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Kepala Daerah'],
    name='Kepala Daerah',
    marker_color='green'
))
fig_pkt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Swasta'],
    name='Swasta',
    marker_color='purple'
))
fig_pkt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['BUMN/BUMD'],
    name='BUMN/BUMD',
    marker_color='yellow'
))
fig_pkt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Kementrian/Lembaga'],
    name='Kementrian/Lembaga',
    marker_color='pink'
))
fig_pkt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Legislatif'],
    name='Legislatif',
    marker_color='cyan'
))
fig_pkt.add_trace(go.Bar(
    x=korupsi['Tahun'],
    y=korupsi['Penegak Hukum'],
    name='Penegak Hukum',
    marker_color='red'
))
fig_pkt.update_layout(barmode='group',
                      xaxis_tickangle=-45,
                      title_text='Terdakwa Korupsi Berdasarkan Pekerjaan',
                      title_x = 0.5,
                      legend_title_text = "Jenis Pekerjaan Terdakwa"
                     )
st.plotly_chart(fig_pkt, use_container_width=True)
st.caption('Sumber : https://www.antikorupsi.org/')

'''
Menurut pekerjaan terdakwa, perangkat desa dan perangkat daerah merupakan pelaku korupsi terbanyak disusul oleh swasta. Hal ini dikarenakan 
perangkat desa dan perangkat daerah memiliki jumlah yang banyak dan tersebar di Indonesia. Pada BUMN/BUMD dan Kementrian/Lembaga terdapat peningkatan 
jumlah terdakwa selama 3 tahun terakhir dan memiliki lonjakan jumlah terdakwa tertinggi pada tahun 2020 yaitu 196% pada 
BUMN/BUMD dengan 47 terdakwa dari 24 terdakwa di tahun 2019 dan 300% pada Kementrian/Lembaga dengan 39 terdakwa dari 
13 terdakwa di tahun 2019.
'''

# BAB III
st.header("BAB III : Solusi")

'''
Dari berbagai grafik yang ditampilkan lonjakan tertinggi korupsi terjadi pada tahun 2020 dimana pandemi COVID-19 sedang 
terjadi. Disaat negara dan masyarakat memiliki masalah terhadap ekonomi disitu pulalah para tikus mencari mangsanya. 
Apabila dibiarkan korupsi akan benar-benar menjadi masalah serius bagi kelangsungan hidup suatu negara seperti Sri Lanka 
yang mengalami "Bangkrut" dikarenakan korupsi para otoritas negaranya sehingga berbagai solusi dibutuhkan untuk menurunkan 
hingga menghilangkan korupsi di negara ini.
'''

st.subheader('Transparansi')

img1 = Image.open('Data/transparansi.jpg')

gambar1, isi1 = st.columns([1,3])

with gambar1 :
    st.image(img1)

with isi1 :
    '''
    Transparansi ekonomi dan sumber daya manusia merupakan hal yang sangat dibutuhkan untuk memberantas tindak korupsi 
    terutama pada pihak pemegang kekuasaan. Dengan ini akan meningkatkan akuntabilitas pemegang kekuasaan dalam pengelolaan
    sumber daya negara dan sumber daya manusia serta memberikan akses terhadap informasi dan berbagai hal yang lebih 
    memberikan kesempatan masyarakat luas untuk berpartisipasi di bidang ekonomi. Salah satu organisasi anti-korupsi seperti
    Indonesia Corruption Watch (ICW) setiap tahun mengeluarkan laporan tindak korupsi di Indonesia yang mana hal ini dapat 
    menyadarkan masyarakat tentang bahaya korupsi bagi kelangsungan negara.
    '''
st.subheader('Hukuman')

img2 = Image.open('Data/ditangkap.jpg')

gambar2, isi2 = st.columns([1,3])

with gambar2 :
    st.image(img2, caption='Fakhri Hilmi korupsi Jiwasraya dengan Kerugian Negara Rp. 16 Triliun')

with isi2 :
    '''
    Setiap tindak pidana korupsi memiliki hukuman yang diatur oleh undang-undang seperti UU Nomor 31 Tahun 1999 Tentang 
    Pemberantasan Tindak Pidana Korupsi. Tetapi kemudian, akan menjadi pertanyaan kenapa walaupun dengan adanya undang-undang tindak 
    pidana korupsi, korupsi masih terjadi di Indonesia. Dilansir dari Pusat Edukasi Antikorupsi KPK biaya kerugian negara 
    akibat korupsi masih jauh lebih besar dibandingkan hukuman bagi koruptor. Catatan KPK, dalam rentang tahun 2001 - 2012 
    kerugian negara akibat korupsi mencapai Rp. 168 triliun sedangkan hukuman final terhadap koruptor hanya menghasilkan 
    Rp. 15 triliun yang mana sisa Rp. 153 triliun ditanggung uang pajak rakyat. Jadi, secara tidak langsung justru rakyat banyak 
    menanggung kerugian yang diakibatkan oleh koruptor.
    '''
'''
Hukuman bagi para koruptor juga tidak mampu memberikan efek jera dan tidak dapat merefleksikan dampak korupsi yang jauh 
lebih besar. Vonis bagi koruptor memang sudah menjatuhkan hukuman seumur hidup dan hukuman denda, ditambah hukuman pengganti. Bahkan, 
hakim juga dapat mencabut hak politik bagi terpidana korupsi. Namun hukuman pengganti sangat terbatas dan sebagian koruptor 
yang diberikan hukuman pengganti justru tidak membayar dan lebih memilih ditahan sehingga hukuman bagi koruptor masih belum 
dapat memberikan efek jera. Belum lagi, biaya yang dikeluarkan negara untuk memproses penegakan hukum ini tidak sedikit dan mahal.\n
Salah satu cara yang dapat dilakukan yaitu koruptor harus membayar semua biaya sosial yang diakibatkan dari perbuatannya 
hingga jika perlu dapat sampai dimiskinkan. Dengan cara ini koruptor tidak akan dapat hidup mewah dari hasil korupsinya selepas 
dari penjara sesuai asas hukum *malis non expediat malos esse*, yaitu pelaku kejahatan tidak boleh menikmati hasil kejahatannya. 
Membebankan seluruh biaya sosial pada koruptor selain dapat mengganti kerugian negara juga dapat mengembalikan kepercayaan 
pemegang kekuasaan dan rasa keadilan bagi masyarakat serta diharapkan dapat memberikan efek jera bagi pelaku korupsi.
'''
st.subheader('Revolusi Mental')

img3 = Image.open('Data/stop.png')

gambar3, isi3 = st.columns([1,5])

with gambar3 :
    st.image(img3)

with isi3 :
    '''
    Korupsi tidak hanya dilakukan oleh orang yang berada pada tingkat pemerintahan yang tinggi seperti Kementrian hingga 
    penegak hukum tetapi juga dilakukan pada tingkat pemerintahan yang rendah seperti desa. Dari grafik yang ada kita ketahui 
    bahwa mayoritas terdakwa korupsi berada pada lingkup perangkat desa dan daerah. Hal ini menunjukkan bahwa pada level 
    pemerintahan terendah saja korupsi sudah marak dilakukan. Salah satu lembaga riset Bertelsmann Stiftung yang merilis 
    Bertelsmann Transformation Index (BTI) yaitu penilaian terhadap suatu negara berdasarkan transformasi politik, ekonomi dan 
    indeks pemerintahan memberikan gambaran terhadap Indonesia dalam satu kalimat.
    '''
'''
“Indonesia's policymakers have become dependent on siphoning state funds or receiving money from oligarchs to pay for 
their political operations and have often prioritized their own monetary interests over those of the general public.”\n
Kalimat tersebut merupakan tamparan keras bagi pelaku politik di Indonesia. Seolah-olah bahwa hal tersebut merupakan 
suatu yang lumrah untuk dilakukan di dunia politk. Sehingga perlu adanya edukasi menyeluruh bagi rakyat Indonesia 
tentang bahaya korupsi dari dini. Dimulai dari diri sendiri, keluarga hingga masyarakat luas.
'''

# Referensi
st.markdown('##### Referensi')

'''
[1] https://www.transparency.org/\n
[2] https://www.antikorupsi.org/\n
[3] https://aclc.kpk.go.id/\n
[4] https://bti-project.org/\n
'''
