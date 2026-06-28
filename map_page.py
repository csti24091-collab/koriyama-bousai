# -*- coding: utf-8 -*-
"""
郡山市マイ・タイムラインDX - 地図ページ
GPS位置情報取得 + Folium地図表示

機能:
  - ブラウザGPSで現在地取得
  - 指定避難場所をマップ上にピン表示
  - 現在地から近い順に避難場所を表示
  - 洪水浸水想定区域をWMS重ね表示
"""

import math
import folium
import streamlit as st
from streamlit_folium import st_folium

# ─────────────────────────────────────────
# 郡山市 指定避難場所データ
# 出典: 郡山市オープンデータ・国土地理院
# ─────────────────────────────────────────
SHELTERS = [
    # (名称, 緯度, 経度, 種別, 洪水対応)
    ("郡山市役所",              37.3941, 140.3877, "避難所",   False),
    ("金透小学校",              37.3978, 140.3794, "避難所",   True),
    ("芳山小学校",              37.4012, 140.3701, "避難所",   True),
    ("橘小学校",                37.3921, 140.3756, "避難所",   True),
    ("小原田小学校",            37.3867, 140.3712, "避難所",   True),
    ("開成小学校",              37.4089, 140.3823, "避難所",   True),
    ("芳賀小学校",              37.4156, 140.4012, "避難所",   False),
    ("桃見台小学校",            37.3856, 140.3945, "避難所",   True),
    ("赤木小学校",              37.3734, 140.3867, "避難所",   True),
    ("富田小学校",              37.4089, 140.4201, "避難所",   True),
    ("富田東小学校",            37.4134, 140.4312, "避難所",   True),
    ("富田西小学校",            37.4045, 140.4089, "避難所",   True),
    ("大槻小学校",              37.3712, 140.4123, "避難所",   False),
    ("薫小学校",                37.4023, 140.3634, "避難所",   True),
    ("東芳小学校",              37.4289, 140.4445, "避難所",   True),
    ("郡山市民文化センター",    37.3989, 140.3823, "避難所",   True),
    ("郡山北体育館",            37.4201, 140.3756, "避難所",   True),
    ("郡山西体育館",            37.3934, 140.3523, "避難所",   False),
    ("郡山南体育館",            37.3712, 140.3845, "避難所",   True),
    ("麓山公園",                37.3956, 140.3889, "緊急避難場所", False),
    ("開成山公園",              37.4045, 140.3812, "緊急避難場所", False),
    ("郡山市総合体育館",        37.3823, 140.3623, "避難所",   False),
    ("安積中学校",              37.3823, 140.3734, "避難所",   True),
    ("郡山第一中学校",          37.3989, 140.3845, "避難所",   True),
    ("郡山第二中学校",          37.4112, 140.3923, "避難所",   True),
    ("郡山第三中学校",          37.3867, 140.4056, "避難所",   True),
    ("郡山高校",                37.4023, 140.3756, "避難所",   True),
    ("安積高校",                37.3934, 140.3867, "避難所",   True),
    ("郡山女子大学",            37.4089, 140.3712, "避難所",   False),
    ("日本大学工学部",          37.3756, 140.3978, "避難所",   False),
]

# 郡山市の中心座標
KORIYAMA_CENTER = (37.3941, 140.3877)


def calc_distance(lat1, lon1, lat2, lon2) -> float:
    """2点間の距離をメートルで返す（ハバーサイン公式）"""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def render_map_page(lang: str = "ja") -> None:
    """地図ページ全体を描画する"""

    st.header("🗺️ 避難場所マップ" if lang == "ja" else "🗺️ Evacuation Map")
    st.caption(
        "現在地から近い避難場所を地図上に表示します。" if lang == "ja"
        else "Shows nearby evacuation sites from your current location."
    )

    # ─── GPS取得UI ──────────────────────────────────
    st.subheader("📍 現在地を取得" if lang == "ja" else "📍 Get Current Location")

    # JavaScript でブラウザGPSを取得
    gps_html = """
    <div id="gps-status" style="padding:8px;border-radius:6px;background:#e8eaf6;
         color:#1a237e;font-size:0.9rem;margin-bottom:8px;">
      📍 位置情報を取得中...
    </div>
    <button onclick="getLocation()" style="
      background:#1a237e;color:white;border:none;border-radius:8px;
      padding:10px 20px;font-size:1rem;cursor:pointer;font-weight:600;">
      🔍 現在地を取得する
    </button>
    <div id="coords" style="margin-top:8px;font-size:0.85rem;color:#546e7a;"></div>

    <script>
    function getLocation() {
      var status = document.getElementById('gps-status');
      status.style.background = '#fff3e0';
      status.style.color = '#e65100';
      status.innerHTML = '⏳ GPS取得中... （スマートフォンの場合、位置情報の許可が必要です）';

      if (!navigator.geolocation) {
        status.innerHTML = '❌ このブラウザはGPSに対応していません';
        return;
      }
      navigator.geolocation.getCurrentPosition(
        function(pos) {
          var lat = pos.coords.latitude.toFixed(6);
          var lon = pos.coords.longitude.toFixed(6);
          var acc = Math.round(pos.coords.accuracy);
          status.style.background = '#e8f5e9';
          status.style.color = '#1b5e20';
          status.innerHTML = '✅ 位置情報を取得しました！下の入力欄に自動入力します';
          document.getElementById('coords').innerHTML =
            '緯度: ' + lat + ' / 経度: ' + lon + ' / 精度: ±' + acc + 'm';
          // Streamlitへの橋渡し（テキストとしてコピー用）
          document.getElementById('lat-display').value = lat;
          document.getElementById('lon-display').value = lon;
        },
        function(err) {
          status.style.background = '#ffebee';
          status.style.color = '#b71c1c';
          var msg = '❌ 位置情報の取得に失敗しました：';
          if (err.code === 1) msg += '位置情報の許可が必要です';
          else if (err.code === 2) msg += 'GPS信号を取得できません';
          else msg += 'タイムアウト';
          status.innerHTML = msg;
        },
        {enableHighAccuracy: true, timeout: 10000}
      );
    }

    // 自動で取得開始
    window.onload = function() { getLocation(); };
    </script>

    <input type="text" id="lat-display" placeholder="緯度" readonly
      style="margin-top:6px;padding:4px 8px;border:1px solid #c5cae9;
             border-radius:4px;width:140px;font-size:0.85rem;">
    <input type="text" id="lon-display" placeholder="経度" readonly
      style="padding:4px 8px;border:1px solid #c5cae9;
             border-radius:4px;width:140px;font-size:0.85rem;margin-left:6px;">
    """

    st.components.v1.html(gps_html, height=160)

    st.caption(
        "⚠️ StreamlitではGPS座標を直接受け取れないため、上に表示された緯度・経度を下の欄に手動入力してください。"
        if lang == "ja" else
        "⚠️ Please manually enter the latitude/longitude shown above into the fields below."
    )

    # ─── 座標入力（GPS取得後に手動入力 or デフォルト郡山市役所）──
    st.markdown("**📌 現在地の座標を入力**" if lang == "ja" else "**📌 Enter Your Coordinates**")

    col1, col2 = st.columns(2)
    with col1:
        user_lat = st.number_input(
            "緯度 (Latitude)" if lang == "ja" else "Latitude",
            value=37.3941, format="%.6f", step=0.0001,
            help="GPS取得後に表示された緯度を入力",
        )
    with col2:
        user_lon = st.number_input(
            "経度 (Longitude)" if lang == "ja" else "Longitude",
            value=140.3877, format="%.6f", step=0.0001,
            help="GPS取得後に表示された経度を入力",
        )

    # ─── フィルター設定 ────────────────────────────────
    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        show_flood_only = st.checkbox(
            "🌊 洪水対応施設のみ" if lang == "ja" else "🌊 Flood-ready only",
            value=False,
        )
    with col_f2:
        radius_km = st.slider(
            "📏 表示範囲（km）" if lang == "ja" else "📏 Radius (km)",
            1, 10, 5,
        )
    with col_f3:
        show_wms = st.checkbox(
            "🌊 浸水想定区域を表示" if lang == "ja" else "🌊 Show flood zone",
            value=False,
        )

    # ─── Folium地図を生成 ──────────────────────────────
    m = folium.Map(
        location=[user_lat, user_lon],
        zoom_start=13,
        tiles="OpenStreetMap",
    )

    # 浸水想定区域WMSレイヤー（国土交通省ハザードマップポータル）
    if show_wms:
        folium.WmsTileLayer(
            url="https://disaportal.gsi.go.jp/maps/wmts/1.0.0/WMTSCapabilities.xml",
            name="浸水想定区域",
            fmt="image/png",
            layers="01001_natl_60m_suibotu_mesh_newcolor",
            transparent=True,
            overlay=True,
            control=True,
            opacity=0.5,
        ).add_to(m)

    # 現在地マーカー（青い人アイコン）
    folium.Marker(
        location=[user_lat, user_lon],
        popup=folium.Popup("📍 現在地" if lang == "ja" else "📍 Your Location", max_width=200),
        tooltip="現在地" if lang == "ja" else "Your Location",
        icon=folium.Icon(color="blue", icon="user", prefix="fa"),
    ).add_to(m)

    # 現在地を中心に指定範囲の円を表示
    folium.Circle(
        location=[user_lat, user_lon],
        radius=radius_km * 1000,
        color="#1a237e",
        fill=True,
        fill_opacity=0.03,
        weight=1,
        popup=f"半径 {radius_km}km" if lang == "ja" else f"Radius {radius_km}km",
    ).add_to(m)

    # 避難場所マーカーを追加
    nearby_shelters = []
    for name, lat, lon, kind, flood_ok in SHELTERS:
        dist = calc_distance(user_lat, user_lon, lat, lon)
        if dist > radius_km * 1000:
            continue
        if show_flood_only and not flood_ok:
            continue

        nearby_shelters.append((dist, name, lat, lon, kind, flood_ok))

        # マーカー色：緊急避難場所=緑、避難所=orange、洪水対応=赤アイコン
        color = "green" if kind == "緊急避難場所" else "orange"
        icon_name = "home"
        flood_label = "🌊 洪水対応" if flood_ok else "⚠️ 洪水非対応"

        popup_html = f"""
        <div style="font-family:sans-serif;min-width:180px;">
          <b style="font-size:1rem;">{name}</b><br>
          <span style="color:#546e7a;">{kind}</span><br>
          <span style="color:{'#1565c0' if flood_ok else '#b71c1c'};">{flood_label}</span><br>
          <b>📏 {dist/1000:.2f} km</b>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=220),
            tooltip=f"{name}（{dist/1000:.1f}km）",
            icon=folium.Icon(color=color, icon=icon_name, prefix="fa"),
        ).add_to(m)

    # レイヤーコントロール
    folium.LayerControl().add_to(m)

    # ─── 地図表示 ──────────────────────────────────────
    st.subheader("🗺️ 避難場所マップ" if lang == "ja" else "🗺️ Evacuation Map")
    map_data = st_folium(m, width="100%", height=520, returned_objects=[])

    # ─── 近い順リスト ─────────────────────────────────
    st.markdown("---")
    st.subheader(
        f"📋 近くの避難場所（{radius_km}km以内・{len(nearby_shelters)}件）"
        if lang == "ja" else
        f"📋 Nearby Shelters (within {radius_km}km: {len(nearby_shelters)} sites)"
    )

    if not nearby_shelters:
        st.warning(
            "指定した範囲に避難場所が見つかりません。範囲を広げてください。"
            if lang == "ja" else
            "No shelters found within the specified range. Please increase the radius."
        )
    else:
        nearby_shelters.sort()  # 距離順
        for dist, name, lat, lon, kind, flood_ok in nearby_shelters:
            flood_badge = (
                '<span style="background:#1565c0;color:white;padding:2px 6px;'
                'border-radius:4px;font-size:0.75rem;">🌊 洪水対応</span>'
                if flood_ok else
                '<span style="background:#ef9a9a;color:#b71c1c;padding:2px 6px;'
                'border-radius:4px;font-size:0.75rem;">⚠️ 洪水非対応</span>'
            )
            kind_badge = (
                '<span style="background:#e8f5e9;color:#2e7d32;padding:2px 6px;'
                'border-radius:4px;font-size:0.75rem;">緊急避難場所</span>'
                if kind == "緊急避難場所" else
                '<span style="background:#fff3e0;color:#e65100;padding:2px 6px;'
                'border-radius:4px;font-size:0.75rem;">避難所</span>'
            )
            gmap_url = f"https://maps.google.com/maps?q={lat},{lon}"
            st.markdown(
                f'<div style="background:#f8f9ff;border:1px solid #e8eaf6;'
                f'border-radius:8px;padding:10px 14px;margin-bottom:6px;">'
                f'<b style="font-size:1rem;">{name}</b>　'
                f'{kind_badge}　{flood_badge}<br>'
                f'<span style="color:#1a237e;font-weight:600;">📏 {dist/1000:.2f} km</span>　'
                f'<a href="{gmap_url}" target="_blank" '
                f'style="color:#1565c0;font-size:0.85rem;">Googleマップで開く →</a>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ─── 凡例 ──────────────────────────────────────────
    st.markdown("---")
    st.caption(
        "🟢 緑ピン：指定緊急避難場所　🟠 オレンジピン：指定避難所　"
        "🌊 洪水対応：洪水発生時も使用可能な施設"
    )
    st.caption(
        "避難場所データ出典：郡山市オープンデータ　地図：OpenStreetMap"
        if lang == "ja" else
        "Data: Koriyama City Open Data / Map: OpenStreetMap"
    )