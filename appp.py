import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Hộp Oxyz Thông Minh - Pháo cối & Máy bay", layout="wide"
)

st.markdown("### 🎯 Mô hình 3D Oxyz: Pháo cối & Máy bay Cứu trợ")

# Chia giao diện thành 2 cột: Cột trái (Camera & Nhập tọa độ), Cột phải (Mô hình 3D)
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("📷 1. Camera Web & Tọa độ")
    img_file = st.camera_input("Chụp ảnh vị trí mục tiêu thực tế trên sa bàn")

    if img_file is not None:
        st.success("✅ Đã ghi nhận hình ảnh từ Camera Web!")

    st.markdown("#### ⚙️ Tọa độ các đối tượng:")

    # Tọa độ Pháo cối (Gốc xuất phát)
    st.markdown("**1. Vị trí Pháo cối**")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        x_phao = st.number_input("X pháo", value=1.0, step=0.5)
    with col_p2:
        y_phao = st.number_input("Y pháo", value=1.0, step=0.5)
    with col_p3:
        z_phao = st.number_input("Z pháo", value=0.0, step=0.5)

    # Tọa độ Máy bay (Mục tiêu trên không)
    st.markdown("**2. Vị trí Máy bay (Mục tiêu)**")
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        x_mb = st.number_input("X máy bay", value=8.0, step=0.5)
    with col_m2:
        y_mb = st.number_input("Y máy bay", value=7.0, step=0.5)
    with col_m3:
        z_mb = st.number_input("Z cao độ", value=6.0, step=0.5)

    # Khởi tạo vector mảng numpy
    Phao = np.array([x_phao, y_phao, z_phao])
    MayBay = np.array([x_mb, y_mb, z_mb])

    # Tính toán vector đường đạn và khoảng cách
    vec_duong_dan = MayBay - Phao
    khoang_cach = np.linalg.norm(vec_duong_dan)

    list_vec = [float(v) for v in vec_duong_dan]

    st.markdown("---")
    st.subheader("📊 Kết quả tính toán không gian")
    st.write(f"- **Vectơ đường đạn $\\vec{{PM}}$**: `{list_vec}`")
    st.write(f"- **Khoảng cách thực tế (tầm bắn)**: **{khoang_cach:.2f} km**")
    st.success("✔ Đã đồng bộ tọa độ giữa Pháo cối và Máy bay thành công!")

with col_right:
    st.subheader("🌐 Mô hình Không gian 3D Oxyz Chuẩn Sa Bàn")

    # Vẽ biểu đồ 3D bằng Plotly
    fig = go.Figure()

    # 1. Vẽ điểm Pháo cối
    fig.add_trace(
        go.Scatter3d(
            x=[Phao[0]],
            y=[Phao[1]],
            z=[Phao[2]],
            mode="markers+text",
            marker=dict(size=9, color="red"),
            text=["Pháo cối (P)"],
            textposition="top center",
            name="Pháo cối",
        )
    )

    # 2. Vẽ điểm Máy bay
    fig.add_trace(
        go.Scatter3d(
            x=[MayBay[0]],
            y=[MayBay[1]],
            z=[MayBay[2]],
            mode="markers+text",
            marker=dict(size=10, color="cyan", symbol="diamond"),
            text=["Máy bay (M)"],
            textposition="top center",
            name="Máy bay",
        )
    )

    # 3. Vẽ đường đạn nối thẳng từ Pháo cối đến Máy bay
    fig.add_trace(
        go.Scatter3d(
            x=[Phao[0], MayBay[0]],
            y=[Phao[1], MayBay[1]],
            z=[Phao[2], MayBay[2]],
            mode="lines+markers",
            line=dict(color="red", width=6),
            name="Quỹ đạo đường đạn",
        )
    )

    # Cấu hình khung không gian 3D với trục Oz thẳng đứng chính giữa chuẩn sa bàn
    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 11], title="Trục Ox (km)", zeroline=True),
            yaxis=dict(range=[0, 11], title="Trục Oy (km)", zeroline=True),
            zaxis=dict(range=[0, 11], title="Trục Oz (km)", zeroline=True),
            # Khóa góc nhìn camera chuẩn
            camera=dict(
                eye=dict(x=1.6, y=-1.6, z=1.2), up=dict(x=0, y=0, z=1)
            ),
        ),
        margin=dict(l=0, r=0, b=0, t=30),
        legend=dict(x=0.0, y=0.9),
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption(
    "💡 Mô hình rút gọn 2 đối tượng (Pháo cối & Máy bay) chạy mượt mà trên"
    " Streamlit Cloud."
)