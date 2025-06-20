import streamlit as st

# Fungsi untuk menghitung f(x) = x²e^(-x)
def f(x):
    """Menghitung nilai f(x) = x² × e^(-x)"""
    # Implementasi e^(-x) tanpa library
    e_neg_x = 1.0
    term = 1.0
    for k in range(1, 50):  # 50 iterasi untuk akurasi
        term *= -x / k
        e_neg_x += term
    
    return x * x * e_neg_x

# Fungsi interpolasi Lagrange
def interpolasi_lagrange(x_data, y_data, x):
    """Melakukan interpolasi Lagrange"""
    n = len(x_data)
    hasil = 0.0
    basis_values = []
    
    for i in range(n):
        # Hitung basis Lagrange Li(x)
        Li = 1.0
        for j in range(n):
            if i != j:
                Li *= (x - x_data[j]) / (x_data[i] - x_data[j])
        
        basis_values.append(Li)
        # Tambahkan yi * Li(x) ke hasil
        hasil += y_data[i] * Li
    
    return hasil, basis_values

# Fungsi untuk membuat plot sederhana menggunakan Streamlit
def plot_function_and_interpolation(x_points, y_points, x_min=0.3, x_max=2.2, n_points=100):
    # Generate titik-titik untuk plot
    x_plot = []
    y_actual = []
    y_interp = []
    
    step = (x_max - x_min) / n_points
    for i in range(n_points + 1):
        x = x_min + i * step
        x_plot.append(x)
        y_actual.append(f(x))
        y_interp.append(interpolasi_lagrange(x_points, y_points, x)[0])
    
    # Cari nilai max dan min untuk scaling
    all_values = y_actual + y_interp + list(y_points)
    y_min = min(all_values) - 0.1
    y_max = max(all_values) + 0.1
    
    # Buat data untuk Streamlit line_chart
    chart_data = {
        'x': x_plot + x_plot + list(x_points),
        'value': y_actual + y_interp + list(y_points),
        'type': ['Fungsi Asli'] * len(x_plot) + ['Interpolasi'] * len(x_plot) + ['Data Points'] * len(x_points)
    }
    
    return chart_data

# Streamlit App
def main():
    st.set_page_config(page_title="Interpolasi Lagrange - Kelompok 5", layout="wide")
    
    # Header
    st.title("🔢 Interpolasi Lagrange - Proyek Akhir Metode Numerik")
    st.markdown("**Kelompok 5 - Fungsi: f(x) = x² × e^(-x)**")
    st.markdown("---")
    
    # Sidebar untuk kontrol
    st.sidebar.header("⚙️ Pengaturan")
    
    # Pilihan mode
    mode = st.sidebar.radio("Pilih Mode:", ["Demo dengan 4 Titik Default", "Input Titik Manual"])
    
    if mode == "Demo dengan 4 Titik Default":
        # Titik default
        x_points = [0.5, 1.0, 1.5, 2.0]
        y_points = [f(x) for x in x_points]
    else:
        st.sidebar.subheader("Input Titik Data")
        n_points = st.sidebar.number_input("Jumlah titik:", min_value=2, max_value=10, value=4)
        
        x_points = []
        y_points = []
        
        for i in range(n_points):
            col1, col2 = st.sidebar.columns(2)
            with col1:
                x = st.number_input(f"x{i}:", value=0.5 + i*0.5, key=f"x{i}")
                x_points.append(x)
            with col2:
                y = f(x)
                st.text_input(f"y{i}:", value=f"{y:.6f}", disabled=True, key=f"y{i}")
                y_points.append(y)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📊 Data Titik-titik")
        
        # Tampilkan tabel data
        data_display = []
        for i in range(len(x_points)):
            data_display.append({
                "i": i,
                "xi": f"{x_points[i]:.2f}",
                "yi = f(xi)": f"{y_points[i]:.6f}"
            })
        st.table(data_display)
        
        # Tampilkan bentuk polinom
        st.subheader("📝 Bentuk Polinom Lagrange")
        st.latex(r"P(x) = \sum_{i=0}^{n} y_i \cdot L_i(x)")
        
        with st.expander("Lihat bentuk eksplisit polinom"):
            for i in range(len(x_points)):
                st.write(f"**Suku ke-{i}:**")
                
                # Bentuk basis Lagrange
                pembilang = []
                penyebut = 1.0
                for j in range(len(x_points)):
                    if i != j:
                        pembilang.append(f"(x - {x_points[j]:.1f})")
                        penyebut *= (x_points[i] - x_points[j])
                
                basis_str = " × ".join(pembilang)
                st.write(f"{y_points[i]:.6f} × [{basis_str}] / {penyebut:.6f}")
    
    with col2:
        st.subheader("🧮 Evaluasi Interpolasi")
        
        # Input nilai x untuk evaluasi
        x_eval = st.number_input("Masukkan nilai x untuk dievaluasi:", 
                                min_value=0.0, max_value=3.0, value=1.25, step=0.05)
        
        # Hitung interpolasi
        p_x, basis_values = interpolasi_lagrange(x_points, y_points, x_eval)
        f_x = f(x_eval)
        error = abs(p_x - f_x)
        
        # Tampilkan hasil
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("P(x)", f"{p_x:.6f}")
        with col_b:
            st.metric("f(x) Sebenarnya", f"{f_x:.6f}")
        with col_c:
            st.metric("Error", f"{error:.6f}")
        
        # Detail perhitungan
        with st.expander("Lihat detail perhitungan"):
            st.write(f"**Evaluasi di x = {x_eval}**")
            
            for i in range(len(x_points)):
                st.write(f"\n**Basis Lagrange L{i}({x_eval}):**")
                
                # Hitung dan tampilkan detail
                pembilang_vals = []
                pembilang_result = 1.0
                penyebut = 1.0
                
                for j in range(len(x_points)):
                    if i != j:
                        nilai = x_eval - x_points[j]
                        pembilang_vals.append(f"({x_eval} - {x_points[j]}) = {nilai:.3f}")
                        pembilang_result *= nilai
                        penyebut *= (x_points[i] - x_points[j])
                
                st.write("Pembilang:", " × ".join(pembilang_vals))
                st.write(f"= {pembilang_result:.6f}")
                st.write(f"Penyebut: {penyebut:.6f}")
                st.write(f"L{i}({x_eval}) = {basis_values[i]:.6f}")
            
            st.write("\n**Hasil akhir:**")
            terms = []
            for i in range(len(x_points)):
                term = y_points[i] * basis_values[i]
                terms.append(f"{y_points[i]:.6f} × {basis_values[i]:.6f} = {term:.6f}")
            
            st.write("P(x) = " + " + ".join(terms))
            st.write(f"P({x_eval}) = {p_x:.6f}")
    
    # Visualisasi
    st.subheader("📈 Visualisasi")
    
    # Generate data untuk plot
    chart_data = plot_function_and_interpolation(x_points, y_points)
    
    # Buat plot menggunakan Streamlit
    # Karena st.line_chart tidak support multiple series dengan baik,
    # kita akan menggunakan pendekatan alternatif
    
    # Plot fungsi asli
    st.write("**Grafik Perbandingan:**")
    info_text = """
    - 🔵 Fungsi asli f(x) = x²e^(-x)
    - 🔴 Polinom interpolasi P(x)
    - ⚫ Titik-titik data
    """
    st.info(info_text)
    
    # Karena keterbatasan Streamlit tanpa library lain, 
    # kita tampilkan nilai-nilai dalam bentuk yang lebih sederhana
    
    # Verifikasi interpolasi
    st.subheader("✅ Verifikasi")
    st.write("Polinom interpolasi harus melewati semua titik data:")
    
    verif_data = []
    for i in range(len(x_points)):
        p_xi = interpolasi_lagrange(x_points, y_points, x_points[i])[0]
        selisih = abs(y_points[i] - p_xi)
        verif_data.append({
            "x": f"{x_points[i]:.1f}",
            "y data": f"{y_points[i]:.6f}",
            "P(x)": f"{p_xi:.6f}",
            "Selisih": f"{selisih:.2e}"
        })
    
    st.table(verif_data)
    
    # Test pada beberapa nilai
    st.subheader("🧪 Test Interpolasi")
    test_values = [0.75, 1.25, 1.75]
    
    test_results = []
    for x_test in test_values:
        p_test = interpolasi_lagrange(x_points, y_points, x_test)[0]
        f_test = f(x_test)
        error_test = abs(p_test - f_test)
        test_results.append({
            "x": f"{x_test:.2f}",
            "P(x)": f"{p_test:.6f}",
            "f(x)": f"{f_test:.6f}",
            "Error": f"{error_test:.6f}",
            "Error %": f"{(error_test/f_test)*100:.2f}%"
        })
    
    st.table(test_results)
    
    # Footer dengan informasi
    st.markdown("---")
    
    # Informasi Proyek
    with st.expander("📋 Informasi Proyek Akhir", expanded=True):
        st.markdown("""
        ## Proyek Akhir Mata Kuliah Metode Numerik:
        
        Buatlah Program tentang
        1. **Interpolasi Lagrange (Nomor Kelompok Ganjil)**
        2. Interpolasi newton (Nomor Kelompok Genap)
        
        Dan berikan contoh penerapannya (secara manual dan program). Pilih polinom derajat 3 dengan pilih 4 titik sebarang.
        1. f(x)=Sec(x);(x1=..,x2=...,...)
        2. f(x)=cosec(x)
        3. f(x)=ln(x²+1)
        4. f(x)=x^(sin x)
        5. **f(x)=x2^(-x)**
        6. f(x)=e^(x³)
        7. f(x)=e^(1-x²)
        8. f(x)=ln(1+e^x)
        
        **Syarat & Ketentuan:**
        
        Proyek tidak menggunakan import library perhitungan.
        
        ---
        
        **Anggota Kelompok 5:**
        
        1. Lyon Ambrosio Djuanda / 2304130098
        2. Fikri Achmad Fadilah / 2304130116
        3. Faizal Rifky Abdilah / 2304130128
        4. Muhammad Khoirul Ihsan / 2304130131
        5. Arina Tira Sabela / 2304130133
        """)
    
    # Perhitungan Manual
    with st.expander("📝 Perhitungan Manual Lengkap"):
        st.markdown("""
        ## Perhitungan Manual
        Untuk f(x) = x²e^(-x), kita pilih 4 titik:
        
        - (x₀, y₀) = (0.5, 0.151633)
        - (x₁, y₁) = (1.0, 0.367879)
        - (x₂, y₂) = (1.5, 0.502129)
        - (x₃, y₃) = (2.0, 0.541341)
        
        ---
        
        ### Langkah 1: Hitung Basis Lagrange
        
        **L₀(x) = [(x-1)(x-1.5)(x-2)] / [(0.5-1)(0.5-1.5)(0.5-2)]**
        
        = [(x-1)(x-1.5)(x-2)] / [(-0.5)(-1)(-1.5)]
        
        = [(x-1)(x-1.5)(x-2)] / (-0.75)
        
        **L₁(x) = [(x-0.5)(x-1.5)(x-2)] / [(1-0.5)(1-1.5)(1-2)]**
        
        = [(x-0.5)(x-1.5)(x-2)] / [(0.5)(-0.5)(-1)]
        
        = [(x-0.5)(x-1.5)(x-2)] / 0.25
        
        **L₂(x) = [(x-0.5)(x-1)(x-2)] / [(1.5-0.5)(1.5-1)(1.5-2)]**
        
        = [(x-0.5)(x-1)(x-2)] / [(1)(0.5)(-0.5)]
        
        = [(x-0.5)(x-1)(x-2)] / (-0.25)
        
        **L₃(x) = [(x-0.5)(x-1)(x-1.5)] / [(2-0.5)(2-1)(2-1.5)]**
        
        = [(x-0.5)(x-1)(x-1.5)] / [(1.5)(1)(0.5)]
        
        = [(x-0.5)(x-1)(x-1.5)] / 0.75
        
        ---
        
        ### Langkah 2: Bentuk Polinom Lagrange
        
        P(x) = 0.151633 × L₀(x) + 0.367879 × L₁(x) + 0.502129 × L₂(x) + 0.541341 × L₃(x)
        
        ---
        
        ### Langkah 3: Evaluasi Lengkap di Semua Titik Uji
        
        #### A. Evaluasi di x = 0.75
        
        **L₀(0.75)** = [(0.75-1)(0.75-1.5)(0.75-2)] / [(0.5-1)(0.5-1.5)(0.5-2)]
        
        = [(-0.25)(-0.75)(-1.25)] / [(-0.5)(-1)(-1.5)]
        
        = -0.234375 / (-0.75) = 0.3125
        
        **L₁(0.75)** = [(0.75-0.5)(0.75-1.5)(0.75-2)] / [(1-0.5)(1-1.5)(1-2)]
        
        = [(0.25)(-0.75)(-1.25)] / [(0.5)(-0.5)(-1)]
        
        = 0.234375 / 0.25 = 0.9375
        
        **L₂(0.75)** = [(0.75-0.5)(0.75-1)(0.75-2)] / [(1.5-0.5)(1.5-1)(1.5-2)]
        
        = [(0.25)(-0.25)(-1.25)] / [(1)(0.5)(-0.5)]
        
        = 0.078125 / (-0.25) = -0.3125
        
        **L₃(0.75)** = [(0.75-0.5)(0.75-1)(0.75-1.5)] / [(2-0.5)(2-1)(2-1.5)]
        
        = [(0.25)(-0.25)(-0.75)] / [(1.5)(1)(0.5)]
        
        = 0.046875 / 0.75 = 0.0625
        
        **P(0.75)** = 0.151633×(0.3125) + 0.367879×(0.9375) + 0.502129×(-0.3125) + 0.541341×(0.0625)
        
        = 0.047385 + 0.344887 - 0.156915 + 0.033834
        
        = **0.269191**
        
        ---
        
        #### B. Evaluasi di x = 1.25
        
        **L₀(1.25)** = [(1.25-1)(1.25-1.5)(1.25-2)] / [(0.5-1)(0.5-1.5)(0.5-2)]
        
        = [(0.25)(-0.25)(-0.75)] / [(-0.5)(-1)(-1.5)]
        
        = 0.046875 / (-0.75) = -0.0625
        
        **L₁(1.25)** = [(1.25-0.5)(1.25-1.5)(1.25-2)] / [(1-0.5)(1-1.5)(1-2)]
        
        = [(0.75)(-0.25)(-0.75)] / [(0.5)(-0.5)(-1)]
        
        = 0.140625 / 0.25 = 0.5625
        
        **L₂(1.25)** = [(1.25-0.5)(1.25-1)(1.25-2)] / [(1.5-0.5)(1.5-1)(1.5-2)]
        
        = [(0.75)(0.25)(-0.75)] / [(1)(0.5)(-0.5)]
        
        = -0.140625 / (-0.25) = 0.5625
        
        **L₃(1.25)** = [(1.25-0.5)(1.25-1)(1.25-1.5)] / [(2-0.5)(2-1)(2-1.5)]
        
        = [(0.75)(0.25)(-0.25)] / [(1.5)(1)(0.5)]
        
        = -0.046875 / 0.75 = -0.0625
        
        **P(1.25)** = 0.151633×(-0.0625) + 0.367879×(0.5625) + 0.502129×(0.5625) + 0.541341×(-0.0625)
        
        = -0.009477 + 0.206932 + 0.282447 - 0.033834
        
        = **0.446068**
        
        ---
        
        #### C. Evaluasi di x = 1.75
        
        **L₀(1.75)** = [(1.75-1)(1.75-1.5)(1.75-2)] / [(0.5-1)(0.5-1.5)(0.5-2)]
        
        = [(0.75)(0.25)(-0.25)] / [(-0.5)(-1)(-1.5)]
        
        = -0.046875 / (-0.75) = 0.0625
        
        **L₁(1.75)** = [(1.75-0.5)(1.75-1.5)(1.75-2)] / [(1-0.5)(1-1.5)(1-2)]
        
        = [(1.25)(0.25)(-0.25)] / [(0.5)(-0.5)(-1)]
        
        = -0.078125 / 0.25 = -0.3125
        
        **L₂(1.75)** = [(1.75-0.5)(1.75-1)(1.75-2)] / [(1.5-0.5)(1.5-1)(1.5-2)]
        
        = [(1.25)(0.75)(-0.25)] / [(1)(0.5)(-0.5)]
        
        = -0.234375 / (-0.25) = 0.9375
        
        **L₃(1.75)** = [(1.75-0.5)(1.75-1)(1.75-1.5)] / [(2-0.5)(2-1)(2-1.5)]
        
        = [(1.25)(0.75)(0.25)] / [(1.5)(1)(0.5)]
        
        = 0.234375 / 0.75 = 0.3125
        
        **P(1.75)** = 0.151633×(0.0625) + 0.367879×(-0.3125) + 0.502129×(0.9375) + 0.541341×(0.3125)
        
        = 0.009477 - 0.114962 + 0.470746 + 0.169169
        
        = **0.534430**
        """)
    
    st.markdown("---")
    st.markdown("""
    ### 📚 Tentang Interpolasi Lagrange
    
    Interpolasi Lagrange adalah metode untuk menemukan polinom berderajat n yang melewati n+1 titik data.
    
    **Formula:**
    """)
    st.latex(r"P(x) = \sum_{i=0}^{n} y_i \cdot L_i(x)")
    st.latex(r"L_i(x) = \prod_{j=0, j \neq i}^{n} \frac{x - x_j}{x_i - x_j}")
    
    st.markdown("""
    **Kelebihan:**
    - Mudah diimplementasikan
    - Menghasilkan polinom unik yang melewati semua titik
    - Tidak memerlukan sistem persamaan linear
    
    **Kekurangan:**
    - Dapat mengalami fenomena Runge untuk derajat tinggi
    - Sensitif terhadap perubahan data
    - Komputasi ulang diperlukan jika ada titik baru
    """)

if __name__ == "__main__":
    main()