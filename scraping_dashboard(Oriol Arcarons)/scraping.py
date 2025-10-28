import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import time
import re
from urllib.parse import urljoin

# Configuración de la página
st.set_page_config(
    page_title="Books Scraper Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #3498db, #2c3e50);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .book-card {
        background: black;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        color: white;
    }
    .book-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    .book-image-container {
        width: 100%;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
        overflow: hidden;
        border-radius: 5px;
        background: #f8f9fa;
    }
    .book-image {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }
    .book-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: white;
        line-height: 1.3;
        height: 2.6em;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    .price-tag {
        background-color: #e74c3c;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 1.1rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .availability-badge {
        background-color: #27ae60;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-left: 0.5rem;
    }
    .out-of-stock {
        background-color: #95a5a6 !important;
    }
    .rating-stars {
        color: #f39c12;
        font-size: 1.2rem;
        margin: 0.5rem 0;
        letter-spacing: 2px;
    }
    .book-meta {
        font-size: 0.9rem;
        color: #bdc3c7;
        margin-bottom: 0.5rem;
    }
    .view-book-link {
        display: inline-block;
        background: red;
        color: white !important;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 0.5rem;
        transition: background 0.3s ease;
        text-decoration: none !important;

    }
    .view-book-link:hover {
        background: white;
        color: black !important;
        text-decoration: none;
    }
    .filter-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

def scrape_books_toscrape():
    """
    Scraper mejorado para books.toscrape.com que extrae hasta 1000 libros
    """
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    all_books = []
    page = 1
    max_books = 1000
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    status_placeholder = st.empty()
    
    with status_placeholder.container():
        st.info("🚀 Iniciando scraping... Esto puede tomar unos minutos.")
    
    while len(all_books) < max_books:
        try:
            url = base_url.format(page)
            status_text.text(f"📖 Escaneando página {page}... ({len(all_books)}/{max_books} libros encontrados)")
            
            response = requests.get(url, headers=headers, timeout=15)
            
            # Si recibimos un 404, significa que no hay más páginas
            if response.status_code == 404:
                with status_placeholder.container():
                    st.success(f"✅ ¡Completado! Se encontraron {len(all_books)} libros en {page-1} páginas.")
                break
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar todos los libros en la página
            book_elements = soup.find_all('article', class_='product_pod')
            
            if not book_elements:
                with status_placeholder.container():
                    st.success(f"✅ ¡Completado! Se encontraron {len(all_books)} libros en {page-1} páginas.")
                break
            
            for book_elem in book_elements:
                try:
                    # Extraer título
                    title_elem = book_elem.find('h3').find('a')
                    title = title_elem['title'] if title_elem and 'title' in title_elem.attrs else title_elem.get_text(strip=True)
                    
                    # Extraer precio
                    price_elem = book_elem.find('p', class_='price_color')
                    price_text = price_elem.get_text(strip=True) if price_elem else "£0.00"
                    price = float(re.sub(r'[^\d.]', '', price_text))
                    
                    # Extraer disponibilidad
                    availability_elem = book_elem.find('p', class_='instock availability')
                    availability = availability_elem.get_text(strip=True) if availability_elem else "Unknown"
                    
                    # Extraer rating
                    rating_elem = book_elem.find('p', class_='star-rating')
                    rating_classes = rating_elem.get('class', []) if rating_elem else []
                    rating = 0
                    for cls in rating_classes:
                        if cls == 'One':
                            rating = 1
                        elif cls == 'Two':
                            rating = 2
                        elif cls == 'Three':
                            rating = 3
                        elif cls == 'Four':
                            rating = 4
                        elif cls == 'Five':
                            rating = 5
                    
                    # Extraer imagen - CORREGIDO
                    img_elem = book_elem.find('img')
                    img_src = img_elem['src'] if img_elem and 'src' in img_elem.attrs else None
                    
                    # Convertir URL relativa a absoluta CORRECTAMENTE
                    if img_src:
                        # Usar urljoin para construir la URL absoluta correctamente
                        img_url = urljoin("https://books.toscrape.com/", img_src)
                    else:
                        img_url = None
                    
                    # Extraer enlace al libro - CORREGIDO
                    link_elem = book_elem.find('h3').find('a')
                    book_link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else None
                    
                    if book_link:
                        # Usar urljoin para construir la URL absoluta correctamente
                        book_url = urljoin("https://books.toscrape.com/catalogue/", book_link)
                    else:
                        book_url = None
                    
                    # ID único para cada libro
                    book_id = f"book_{len(all_books) + 1:04d}"
                    
                    all_books.append({
                        'book_id': book_id,
                        'title': title,
                        'price': price,
                        'availability': availability,
                        'rating': rating,
                        'image_url': img_url,
                        'book_url': book_url,
                        'page_number': page
                    })
                    
                    # Si alcanzamos el máximo, salir
                    if len(all_books) >= max_books:
                        break
                        
                except Exception as e:
                    continue
            
            # Actualizar barra de progreso
            progress = min(len(all_books) / max_books, 1.0)
            progress_bar.progress(progress)
            
            # Pequeña pausa para ser respetuoso con el servidor
            time.sleep(0.3)
            
            page += 1
            
        except Exception as e:
            with status_placeholder.container():
                st.error(f"❌ Error en página {page}: {str(e)}")
            break
    
    progress_bar.empty()
    status_text.empty()
    
    return all_books

def get_star_rating(rating):
    """
    Convierte un rating numérico a estrellas HTML
    """
    if not rating or rating == 0:
        return '<div class="rating-stars">No rating</div>'
    
    stars = "★" * rating + "☆" * (5 - rating)
    return f'<div class="rating-stars">{stars} ({rating}/5)</div>'

def get_availability_badge(availability):
    """
    Devuelve el badge de disponibilidad con clase CSS apropiada
    """
    if "out of stock" in availability.lower():
        return f'<span class="availability-badge out-of-stock">{availability}</span>'
    else:
        return f'<span class="availability-badge">{availability}</span>'

def main():
    st.markdown('<h1 class="main-header">📚 Books Scraper Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("### Extracción de libros de books.toscrape.com")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔧 Controles")
        
        if st.button("🔄 Iniciar Scraping", use_container_width=True, type="primary"):
            st.session_state.pop('books_data', None)
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Información")
        st.markdown("""
        - **Fuente**: books.toscrape.com
        - **Objetivo**: 1000 libros
        - **Páginas**: Automáticas
        - **Datos**: Título, precio, rating, disponibilidad, imagen
        """)
    
    # Scraping de datos
    if 'books_data' not in st.session_state:
        st.info("👆 Haz clic en 'Iniciar Scraping' para comenzar a extraer datos de books.toscrape.com")
        if st.button("Iniciar Scraping", key="init_scraping"):
            with st.spinner('🚀 Iniciando scraping de libros...'):
                books_data = scrape_books_toscrape()
                st.session_state.books_data = books_data
                if books_data:
                    df = pd.DataFrame(books_data)
                    st.session_state.df = df
                else:
                    st.session_state.df = pd.DataFrame()
            st.rerun()
    else:
        df = st.session_state.df
        
        if df.empty:
            st.error("No se pudieron extraer datos. Intenta nuevamente.")
            return
        
        # Mostrar información en sidebar
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**✅ Libros extraídos:** {len(df)}")
        st.sidebar.markdown(f"**💰 Precio promedio:** £{df['price'].mean():.2f}")
        st.sidebar.markdown(f"**⭐ Rating promedio:** {df['rating'].mean():.1f}/5")
        st.sidebar.markdown(f"**📄 Páginas escaneadas:** {df['page_number'].max()}")
        
        # Métricas principales
        st.markdown("## 📈 Resumen General")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">Total Libros</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_price = df['price'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">£{avg_price:.2f}</div>
                <div class="metric-label">Precio Promedio</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_rating = df['rating'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_rating:.1f}/5</div>
                <div class="metric-label">Rating Promedio</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            available_books = len(df[df['availability'].str.contains('stock', case=False, na=False)])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{available_books}</div>
                <div class="metric-label">En Stock</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Filtros
        st.markdown("## 🔍 Filtros")
        
        with st.container():
            st.markdown('<div class="filter-section">', unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                price_range = st.slider(
                    "💰 Rango de Precio (£)",
                    min_value=float(df['price'].min()),
                    max_value=float(df['price'].max()),
                    value=(float(df['price'].min()), float(df['price'].max()))
                )
            
            with col2:
                rating_filter = st.multiselect(
                    "⭐ Rating",
                    options=sorted(df['rating'].unique()),
                    default=[]
                )
            
            with col3:
                availability_options = sorted(df['availability'].unique())
                availability_filter = st.multiselect(
                    "📦 Disponibilidad",
                    options=availability_options,
                    default=availability_options
                )
            
            with col4:
                # Ordenamiento
                sort_option = st.selectbox(
                    "📊 Ordenar por",
                    options=[
                        "Precio (Mayor a Menor)", 
                        "Precio (Menor a Mayor)", 
                        "Rating (Mayor a Menor)", 
                        "Rating (Menor a Mayor)", 
                        "Título A-Z",
                        "Página"
                    ]
                )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Aplicar filtros
        filtered_df = df.copy()
        
        # Filtro de precio
        filtered_df = filtered_df[
            (filtered_df['price'] >= price_range[0]) & 
            (filtered_df['price'] <= price_range[1])
        ]
        
        # Filtro de rating
        if rating_filter:
            filtered_df = filtered_df[filtered_df['rating'].isin(rating_filter)]
        
        # Filtro de disponibilidad
        if availability_filter:
            filtered_df = filtered_df[filtered_df['availability'].isin(availability_filter)]
        
        # Aplicar ordenamiento
        if sort_option == "Precio (Mayor a Menor)":
            filtered_df = filtered_df.sort_values('price', ascending=False)
        elif sort_option == "Precio (Menor a Mayor)":
            filtered_df = filtered_df.sort_values('price', ascending=True)
        elif sort_option == "Rating (Mayor a Menor)":
            filtered_df = filtered_df.sort_values('rating', ascending=False)
        elif sort_option == "Rating (Menor a Mayor)":
            filtered_df = filtered_df.sort_values('rating', ascending=True)
        elif sort_option == "Título A-Z":
            filtered_df = filtered_df.sort_values('title')
        elif sort_option == "Página":
            filtered_df = filtered_df.sort_values('page_number')
        
        # Pestañas
        tab1, tab2, tab3, tab4 = st.tabs(["📚 Libros", "📊 Análisis", "💰 Precios", "💾 Datos"])
        
        with tab1:
            st.markdown(f"### 📚 Catálogo de Libros ({len(filtered_df)} encontrados)")
            
            # Mostrar libros en grid responsive
            books_per_row = 4
            books = filtered_df.to_dict('records')
            
            for i in range(0, len(books), books_per_row):
                cols = st.columns(books_per_row)
                for j in range(books_per_row):
                    if i + j < len(books):
                        book = books[i + j]
                        with cols[j]:
                            # Badge de disponibilidad
                            availability_badge = get_availability_badge(book['availability'])
                            
                            # Estrellas de rating
                            stars = get_star_rating(book['rating'])
                            
                            st.markdown(f"""
                            <div class="book-card" data-testid="{book['book_id']}">
                                <div class="book-image-container">
                                    <img src="{book['image_url']}" class="book-image" alt="{book['title']}" 
                                         onerror="this.src='https://via.placeholder.com/150x200?text=No+Image'">
                                </div>
                                <div class="book-title">{book['title']}</div>
                                <div class="price-tag">£{book['price']:.2f}</div>
                                {availability_badge}
                                {stars}
                                <div class="book-meta">Página {book['page_number']}</div>
                                <a href="{book['book_url']}" target="_blank" class="view-book-link">Ver Libro</a>
                            </div>
                            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### 📊 Análisis de Datos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribución de ratings
                rating_counts = filtered_df['rating'].value_counts().sort_index()
                fig1 = px.bar(
                    x=rating_counts.index,
                    y=rating_counts.values,
                    title="Distribución de Ratings",
                    labels={'x': 'Rating', 'y': 'Cantidad de Libros'},
                    color=rating_counts.index,
                    color_continuous_scale='viridis'
                )
                # Añadir espacio entre barras
                fig1.update_layout(bargap=0.3)
                st.plotly_chart(fig1, use_container_width=True)
                
                # Libros por página
                page_counts = filtered_df['page_number'].value_counts().sort_index()
                fig2 = px.line(
                    x=page_counts.index,
                    y=page_counts.values,
                    title="Libros por Página",
                    labels={'x': 'Página', 'y': 'Cantidad de Libros'}
                )
                st.plotly_chart(fig2, use_container_width=True)
            
            with col2:
                # Distribución de precios - MEJORADO con barras separadas
                fig3 = px.histogram(
                    filtered_df,
                    x='price',
                    nbins=30,  # Más bins para mejor distribución
                    title="Distribución de Precios",
                    labels={'price': 'Precio (£)'},
                    color_discrete_sequence=['#3498db'],
                    opacity=0.8
                )
                # Ajustar el espaciado entre barras
                fig3.update_traces(marker=dict(line=dict(width=1, color='white')))
                fig3.update_layout(
                    bargap=0.1,  # Espacio entre barras
                    xaxis_title="Precio (£)",
                    yaxis_title="Cantidad de Libros"
                )
                st.plotly_chart(fig3, use_container_width=True)
                
                # Disponibilidad
                availability_counts = filtered_df['availability'].value_counts()
                fig4 = px.pie(
                    values=availability_counts.values,
                    names=availability_counts.index,
                    title="Distribución por Disponibilidad",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig4, use_container_width=True)
        
        with tab3:
            st.markdown("### 💰 Análisis de Precios")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Precio vs Rating - SIN LOWESS
                fig5 = px.scatter(
                    filtered_df,
                    x='rating',
                    y='price',
                    title="Relación Precio vs Rating",
                    labels={'rating': 'Rating', 'price': 'Precio (£)'},
                    color='rating',
                    color_continuous_scale='viridis'
                )
                st.plotly_chart(fig5, use_container_width=True)
            
            with col2:
                # Precios por rating
                fig6 = px.box(
                    filtered_df,
                    x='rating',
                    y='price',
                    title="Distribución de Precios por Rating",
                    labels={'rating': 'Rating', 'price': 'Precio (£)'},
                    color='rating',
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig6, use_container_width=True)
            
            # Gráfico adicional: Precio promedio por rating
            st.markdown("#### 📊 Precio Promedio por Rating")
            avg_price_by_rating = filtered_df.groupby('rating')['price'].mean().reset_index()
            fig7 = px.bar(
                avg_price_by_rating,
                x='rating',
                y='price',
                title="Precio Promedio por Rating",
                labels={'rating': 'Rating', 'price': 'Precio Promedio (£)'},
                color='rating',
                color_continuous_scale='viridis'
            )
            # Añadir espacio entre barras
            fig7.update_layout(bargap=0.3)
            st.plotly_chart(fig7, use_container_width=True)
            
            # Top libros más caros
            st.markdown("#### 📈 Top 10 Libros Más Caros")
            top_expensive = filtered_df.nlargest(10, 'price')[['title', 'price', 'rating', 'availability', 'page_number']]
            top_expensive = top_expensive.rename(columns={
                'title': 'Título', 
                'price': 'Precio (£)', 
                'rating': 'Rating', 
                'availability': 'Disponibilidad',
                'page_number': 'Página'
            })
            st.dataframe(top_expensive, use_container_width=True)
        
        with tab4:
            st.markdown("### 💾 Datos Completos")
            
            # Mostrar dataframe con nombres de columnas en español
            display_df = filtered_df[['title', 'price', 'rating', 'availability', 'page_number', 'book_url']].copy()
            display_df = display_df.rename(columns={
                'title': 'Título',
                'price': 'Precio (£)',
                'rating': 'Rating',
                'availability': 'Disponibilidad',
                'page_number': 'Página',
                'book_url': 'URL del Libro'
            })
            
            st.dataframe(display_df, use_container_width=True)
            
            st.markdown("#### Exportar Datos")
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Descargar CSV",
                data=csv,
                file_name="books_toscrape.csv",
                mime="text/csv",
                use_container_width=True
            )

if __name__ == "__main__":
    main()