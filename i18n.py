# -*- coding: utf-8 -*-
"""
郡山市マイ・タイムラインDX 多言語翻訳辞書

対応言語:
  ja - 日本語（原文）
  en - English
  zh - 中文（簡体字）
  ko - 한국어
  vi - Tiếng Việt
  tl - Filipino（タガログ語）
  id - Bahasa Indonesia

使い方:
  from i18n import LANGUAGES, UI, PHASES, TASKS, t, t_phase, t_task
  lang = "en"
  t(lang, "title")            -> UIラベル翻訳
  t_phase(lang, phase_ja)      -> フェーズ名翻訳
  t_task(lang, task_text_ja)   -> タスク文翻訳
"""

# ─────────────────────────────────────────
# 対応言語一覧（表示名）
# ─────────────────────────────────────────
LANGUAGES = {
    "ja": "日本語",
    "en": "English",
    "zh": "中文",
    "ko": "한국어",
    "vi": "Tiếng Việt",
    "tl": "Filipino",
    "id": "Bahasa Indonesia",
}

# ─────────────────────────────────────────
# UIラベル翻訳
# ─────────────────────────────────────────
UI = {
    "app_title": {
        "ja": "郡山市 マイ・タイムライン DX",
        "en": "Koriyama City My Timeline DX",
        "zh": "郡山市 我的防灾时间表 DX",
        "ko": "고리야마시 마이 타임라인 DX",
        "vi": "Lịch trình cá nhân phòng chống thiên tai thành phố Koriyama",
        "tl": "My Timeline DX ng Lungsod ng Koriyama",
        "id": "My Timeline DX Kota Koriyama",
    },
    "app_subtitle": {
        "ja": "郡山市防災行動計画に基づく動的シミュレーター",
        "en": "Dynamic simulator based on Koriyama City's Disaster Action Plan",
        "zh": "基于郡山市防灾行动计划的动态模拟器",
        "ko": "고리야마시 방재 행동계획에 기반한 동적 시뮬레이터",
        "vi": "Trình mô phỏng động dựa trên Kế hoạch hành động phòng chống thiên tai của thành phố Koriyama",
        "tl": "Dynamic simulator batay sa Disaster Action Plan ng Lungsod ng Koriyama",
        "id": "Simulator dinamis berdasarkan Rencana Aksi Bencana Kota Koriyama",
    },
    "language_select": {
        "ja": "🌐 言語 / Language",
        "en": "🌐 Language / 言語",
        "zh": "🌐 语言 / Language",
        "ko": "🌐 언어 / Language",
        "vi": "🌐 Ngôn ngữ / Language",
        "tl": "🌐 Wika / Language",
        "id": "🌐 Bahasa / Language",
    },
    "font_size_select": {
        "ja": "🔠 文字サイズ",
        "en": "🔠 Text Size",
        "zh": "🔠 字体大小",
        "ko": "🔠 글자 크기",
        "vi": "🔠 Cỡ chữ",
        "tl": "🔠 Sukat ng Teksto",
        "id": "🔠 Ukuran Teks",
    },
    "font_size_normal": {
        "ja": "通常",
        "en": "Normal",
        "zh": "普通",
        "ko": "보통",
        "vi": "Bình thường",
        "tl": "Normal",
        "id": "Normal",
    },
    "font_size_large": {
        "ja": "大きい",
        "en": "Large",
        "zh": "大",
        "ko": "크게",
        "vi": "Lớn",
        "tl": "Malaki",
        "id": "Besar",
    },
    "household_status": {
        "ja": "👤 世帯の状況",
        "en": "👤 Household Status",
        "zh": "👤 家庭情况",
        "ko": "👤 가구 상황",
        "vi": "👤 Tình trạng hộ gia đình",
        "tl": "👤 Katayuan ng Sambahayan",
        "id": "👤 Status Rumah Tangga",
    },
    "has_elderly": {
        "ja": "高齢者・乳幼児がいる",
        "en": "Have elderly or infants",
        "zh": "家中有老人或婴幼儿",
        "ko": "고령자・영유아가 있음",
        "vi": "Có người già hoặc trẻ nhỏ",
        "tl": "May matatanda o sanggol",
        "id": "Ada lansia atau bayi",
    },
    "has_car": {
        "ja": "車で避難する",
        "en": "Evacuate by car",
        "zh": "开车避难",
        "ko": "차량으로 피난함",
        "vi": "Sơ tán bằng ô tô",
        "tl": "Lilikas gamit ang kotse",
        "id": "Evakuasi dengan mobil",
    },
    "mode_label": {
        "ja": "📌 モード",
        "en": "📌 Mode",
        "zh": "📌 模式",
        "ko": "📌 모드",
        "vi": "📌 Chế độ",
        "tl": "📌 Mode",
        "id": "📌 Mode",
    },
    "mode_normal": {
        "ja": "通常（手動選択）",
        "en": "Normal (Manual)",
        "zh": "常规（手动选择）",
        "ko": "일반（수동 선택）",
        "vi": "Thông thường (Chọn thủ công)",
        "tl": "Normal (Manual)",
        "id": "Normal (Manual)",
    },
    "mode_realtime": {
        "ja": "📡 リアルタイム水位連携",
        "en": "📡 Real-time Water Level",
        "zh": "📡 实时水位联动",
        "ko": "📡 실시간 수위 연동",
        "vi": "📡 Mực nước thời gian thực",
        "tl": "📡 Real-time na Antas ng Tubig",
        "id": "📡 Level Air Real-time",
    },
    "mode_weather": {
        "ja": "🌤️ 郡山市天気",
        "en": "🌤️ Koriyama Weather",
        "zh": "🌤️ 郡山市天气",
        "ko": "🌤️ 고리야마시 날씨",
        "vi": "🌤️ Thời tiết Koriyama",
        "tl": "🌤️ Panahon sa Koriyama",
        "id": "🌤️ Cuaca Koriyama",
    },
    "mode_task_manage": {
        "ja": "✏️ タスク管理",
        "en": "✏️ Task Management",
        "zh": "✏️ 任务管理",
        "ko": "✏️ 작업 관리",
        "vi": "✏️ Quản lý nhiệm vụ",
        "tl": "✏️ Pamamahala ng Gawain",
        "id": "✏️ Manajemen Tugas",
    },
    "select_phase": {
        "ja": "現在の災害フェーズを選択してください：",
        "en": "Please select the current disaster phase:",
        "zh": "请选择当前的灾害阶段：",
        "ko": "현재 재해 단계를 선택해 주세요：",
        "vi": "Vui lòng chọn giai đoạn thiên tai hiện tại:",
        "tl": "Piliin ang kasalukuyang yugto ng sakuna:",
        "id": "Silakan pilih fase bencana saat ini:",
    },
    "timeline_header": {
        "ja": "📋 あなた専用のマイ・タイムライン",
        "en": "📋 Your Personal Timeline",
        "zh": "📋 您的专属时间表",
        "ko": "📋 나만의 마이 타임라인",
        "vi": "📋 Lịch trình cá nhân của bạn",
        "tl": "📋 Ang Iyong Personal na Timeline",
        "id": "📋 Linimasa Pribadi Anda",
    },
    "current_phase": {
        "ja": "現在のフェーズ：",
        "en": "Current Phase: ",
        "zh": "当前阶段：",
        "ko": "현재 단계：",
        "vi": "Giai đoạn hiện tại: ",
        "tl": "Kasalukuyang Yugto: ",
        "id": "Fase Saat Ini: ",
    },
    "tasks_for_phase": {
        "ja": "フェーズ [ {phase} ] で実行すべき行動：",
        "en": "Actions to take in phase [ {phase} ]:",
        "zh": "在阶段 [ {phase} ] 中应采取的行动：",
        "ko": "단계 [ {phase} ]에서 실행해야 할 행동：",
        "vi": "Hành động cần thực hiện trong giai đoạn [ {phase} ]:",
        "tl": "Mga aksyon na gagawin sa yugto [ {phase} ]:",
        "id": "Tindakan yang harus dilakukan pada fase [ {phase} ]:",
    },
    "no_tasks": {
        "ja": "✨ このフェーズに対象タスクはありません。引き続き情報収集を続けてください。",
        "en": "✨ No tasks for this phase. Please continue gathering information.",
        "zh": "✨ 此阶段没有相关任务。请继续收集信息。",
        "ko": "✨ 이 단계에는 대상 작업이 없습니다. 계속 정보를 수집하세요.",
        "vi": "✨ Không có nhiệm vụ cho giai đoạn này. Vui lòng tiếp tục theo dõi thông tin.",
        "tl": "✨ Walang gawain para sa yugtong ito. Patuloy na mangalap ng impormasyon.",
        "id": "✨ Tidak ada tugas untuk fase ini. Harap terus mengumpulkan informasi.",
    },
    "progress_done": {
        "ja": "実施済み: {done} / {total} 件",
        "en": "Completed: {done} / {total}",
        "zh": "已完成：{done} / {total} 项",
        "ko": "완료됨: {done} / {total} 건",
        "vi": "Đã hoàn thành: {done} / {total}",
        "tl": "Natapos: {done} / {total}",
        "id": "Selesai: {done} / {total}",
    },
    "record_button": {
        "ja": "📝 チェック内容を記録する",
        "en": "📝 Save Checked Items",
        "zh": "📝 记录已勾选内容",
        "ko": "📝 체크 내용 기록하기",
        "vi": "📝 Lưu các mục đã chọn",
        "tl": "📝 I-save ang mga Naka-check",
        "id": "📝 Simpan Item yang Dicentang",
    },
    "record_saved": {
        "ja": "✅ {count}件のタスクを記録しました。（{time}）",
        "en": "✅ Saved {count} task(s). ({time})",
        "zh": "✅ 已记录 {count} 项任务。（{time}）",
        "ko": "✅ {count}건의 작업을 기록했습니다.（{time}）",
        "vi": "✅ Đã lưu {count} nhiệm vụ. ({time})",
        "tl": "✅ Na-save ang {count} na gawain. ({time})",
        "id": "✅ {count} tugas telah disimpan. ({time})",
    },
    "footer_links": {
        "ja": "📞 防災関連リンク・緊急連絡先",
        "en": "📞 Disaster Info Links & Emergency Contacts",
        "zh": "📞 防灾相关链接・紧急联系方式",
        "ko": "📞 방재 관련 링크・긴급 연락처",
        "vi": "📞 Liên kết phòng chống thiên tai & Liên hệ khẩn cấp",
        "tl": "📞 Mga Link Tungkol sa Sakuna at Emergency Contact",
        "id": "📞 Tautan Info Bencana & Kontak Darurat",
    },
    "google_translate_note": {
        "ja": "🌐 自動翻訳（Google翻訳）で確認する",
        "en": "🌐 View with Google Translate",
        "zh": "🌐 使用谷歌翻译查看",
        "ko": "🌐 구글 번역으로 보기",
        "vi": "🌐 Xem bằng Google Dịch",
        "tl": "🌐 Tingnan gamit ang Google Translate",
        "id": "🌐 Lihat dengan Google Translate",
    },
    "weather_warning_header": {
        "ja": "🌩️ 気象庁 警報・注意報（郡山市）",
        "en": "🌩️ JMA Warnings & Advisories (Koriyama City)",
        "zh": "🌩️ 气象厅 警报・注意报（郡山市）",
        "ko": "🌩️ 기상청 경보・주의보（고리야마시）",
        "vi": "🌩️ Cảnh báo & Khuyến cáo JMA (Thành phố Koriyama)",
        "tl": "🌩️ Babala ng JMA (Lungsod ng Koriyama)",
        "id": "🌩️ Peringatan JMA (Kota Koriyama)",
    },
    "no_warnings": {
        "ja": "✅ 現在、郡山市に発令中の警報・注意報はありません。",
        "en": "✅ No warnings or advisories currently issued for Koriyama City.",
        "zh": "✅ 目前郡山市没有发布警报或注意报。",
        "ko": "✅ 현재 고리야마시에 발령 중인 경보・주의보는 없습니다.",
        "vi": "✅ Hiện không có cảnh báo nào được ban hành cho thành phố Koriyama.",
        "tl": "✅ Walang kasalukuyang babala para sa Lungsod ng Koriyama.",
        "id": "✅ Saat ini tidak ada peringatan untuk Kota Koriyama.",
    },
    "weather_realtime_panel": {
        "ja": "📍 郡山市 現在の実況（AMeDAS）",
        "en": "📍 Koriyama Current Conditions (AMeDAS)",
        "zh": "📍 郡山市 当前实况（AMeDAS）",
        "ko": "📍 고리야마시 현재 실황（AMeDAS）",
        "vi": "📍 Tình hình hiện tại tại Koriyama (AMeDAS)",
        "tl": "📍 Kasalukuyang Kondisyon sa Koriyama (AMeDAS)",
        "id": "📍 Kondisi Terkini Koriyama (AMeDAS)",
    },
    "temperature": {
        "ja": "🌡️ 気温",
        "en": "🌡️ Temperature",
        "zh": "🌡️ 气温",
        "ko": "🌡️ 기온",
        "vi": "🌡️ Nhiệt độ",
        "tl": "🌡️ Temperatura",
        "id": "🌡️ Suhu",
    },
    "precipitation_1h": {
        "ja": "💧 1h降水量",
        "en": "💧 1h Precipitation",
        "zh": "💧 1小时降水量",
        "ko": "💧 1시간 강수량",
        "vi": "💧 Lượng mưa 1 giờ",
        "tl": "💧 Pag-ulan (1h)",
        "id": "💧 Curah Hujan 1 Jam",
    },
    "wind_speed": {
        "ja": "🌬️ 風速",
        "en": "🌬️ Wind Speed",
        "zh": "🌬️ 风速",
        "ko": "🌬️ 풍속",
        "vi": "🌬️ Tốc độ gió",
        "tl": "🌬️ Bilis ng Hangin",
        "id": "🌬️ Kecepatan Angin",
    },
    "wind_direction": {
        "ja": "🧭 風向",
        "en": "🧭 Wind Direction",
        "zh": "🧭 风向",
        "ko": "🧭 풍향",
        "vi": "🧭 Hướng gió",
        "tl": "🧭 Direksyon ng Hangin",
        "id": "🧭 Arah Angin",
    },
    "humidity": {
        "ja": "💦 湿度",
        "en": "💦 Humidity",
        "zh": "💦 湿度",
        "ko": "💦 습도",
        "vi": "💦 Độ ẩm",
        "tl": "💦 Halumigmig",
        "id": "💦 Kelembapan",
    },
    "river_select": {
        "ja": "表示する河川を選択：",
        "en": "Select river to display:",
        "zh": "选择要显示的河流：",
        "ko": "표시할 하천을 선택：",
        "vi": "Chọn sông để hiển thị:",
        "tl": "Piliin ang ipapakitang ilog:",
        "id": "Pilih sungai yang ditampilkan:",
    },
    "current_water_level": {
        "ja": "現在水位",
        "en": "Current Water Level",
        "zh": "当前水位",
        "ko": "현재 수위",
        "vi": "Mực nước hiện tại",
        "tl": "Kasalukuyang Antas ng Tubig",
        "id": "Level Air Saat Ini",
    },
    "fetch_failed": {
        "ja": "⚠️ データを取得できませんでした。",
        "en": "⚠️ Failed to retrieve data.",
        "zh": "⚠️ 无法获取数据。",
        "ko": "⚠️ 데이터를 가져올 수 없습니다.",
        "vi": "⚠️ Không thể lấy dữ liệu.",
        "tl": "⚠️ Hindi makuha ang data.",
        "id": "⚠️ Gagal mengambil data.",
    },
    "retry_button": {
        "ja": "🔄 再取得を試みる",
        "en": "🔄 Retry",
        "zh": "🔄 重新获取",
        "ko": "🔄 다시 가져오기",
        "vi": "🔄 Thử lại",
        "tl": "🔄 Subukan Ulit",
        "id": "🔄 Coba Lagi",
    },
    "emergency_contacts_text": {
        "ja": "🌊 福島県河川流域総合情報システム　🗾 国土交通省 川の防災情報　🏙️ 郡山市 防災情報　☎️ 災害用伝言ダイヤル: 171",
        "en": "🌊 Fukushima River Information System　🗾 MLIT River Disaster Info　🏙️ Koriyama City Disaster Info　☎️ Disaster Message Dial: 171",
        "zh": "🌊 福岛县河流信息系统　🗾 国土交通省河流防灾信息　🏙️ 郡山市防灾信息　☎️ 灾害留言专线：171",
        "ko": "🌊 후쿠시마현 하천정보시스템　🗾 국토교통성 하천 방재정보　🏙️ 고리야마시 방재정보　☎️ 재해용 메시지 다이얼: 171",
        "vi": "🌊 Hệ thống thông tin sông Fukushima　🗾 Thông tin thiên tai sông MLIT　🏙️ Thông tin thiên tai thành phố Koriyama　☎️ Đường dây tin nhắn thiên tai: 171",
        "tl": "🌊 Fukushima River Information System　🗾 MLIT River Disaster Info　🏙️ Koriyama City Disaster Info　☎️ Disaster Message Dial: 171",
        "id": "🌊 Sistem Informasi Sungai Fukushima　🗾 Info Bencana Sungai MLIT　🏙️ Info Bencana Kota Koriyama　☎️ Dial Pesan Bencana: 171",
    },
    "condition_elderly_prefix": {
        "ja": "【高齢者等】",
        "en": "[Elderly/Infants] ",
        "zh": "【老人・婴幼儿】",
        "ko": "【고령자 등】",
        "vi": "[Người già/Trẻ nhỏ] ",
        "tl": "[Matatanda/Sanggol] ",
        "id": "[Lansia/Bayi] ",
    },
    "condition_car_prefix": {
        "ja": "【車避難】",
        "en": "[Car Evacuation] ",
        "zh": "【车辆避难】",
        "ko": "【차량 피난】",
        "vi": "[Sơ tán bằng ô tô] ",
        "tl": "[Paglikas gamit ang Kotse] ",
        "id": "[Evakuasi Mobil] ",
    },
}


# ─────────────────────────────────────────
# フェーズ名翻訳
# ─────────────────────────────────────────
PHASES = {
    "平時（備えの期間）": {
        "ja": "平時（備えの期間）",
        "en": "Normal Times (Preparation Period)",
        "zh": "平时（准备期）",
        "ko": "평시（대비 기간）",
        "vi": "Bình thường (Giai đoạn chuẩn bị)",
        "tl": "Normal (Yugto ng Paghahanda)",
        "id": "Normal (Periode Persiapan)",
    },
    "台風上陸の3日前（準備開始）": {
        "ja": "台風上陸の3日前（準備開始）",
        "en": "3 Days Before Typhoon Landfall (Start Preparation)",
        "zh": "台风登陆前3天（开始准备）",
        "ko": "태풍 상륙 3일 전（준비 시작）",
        "vi": "3 ngày trước khi bão đổ bộ (Bắt đầu chuẩn bị)",
        "tl": "3 Araw Bago Tumama ang Bagyo (Simula ng Paghahanda)",
        "id": "3 Hari Sebelum Topan Mendarat (Mulai Persiapan)",
    },
    "大雨・洪水注意報発表 (-24h)": {
        "ja": "大雨・洪水注意報発表 (-24h)",
        "en": "Heavy Rain/Flood Advisory Issued (-24h)",
        "zh": "发布大雨・洪水注意报 (-24h)",
        "ko": "대우・홍수 주의보 발표 (-24h)",
        "vi": "Ban hành khuyến cáo mưa lớn/lũ lụt (-24h)",
        "tl": "Naglabas ng Babala sa Malakas na Ulan/Pagbaha (-24h)",
        "id": "Peringatan Hujan Lebat/Banjir Dikeluarkan (-24h)",
    },
    "水防団待機水位到達 (4.00m)": {
        "ja": "水防団待機水位到達 (4.00m)",
        "en": "Flood Watch Standby Level Reached (4.00m)",
        "zh": "达到水防团待命水位 (4.00m)",
        "ko": "수방단 대기 수위 도달 (4.00m)",
        "vi": "Đạt mức nước chờ của đội phòng lũ (4.00m)",
        "tl": "Naabot ang Antas ng Standby ng Flood Watch (4.00m)",
        "id": "Level Siaga Tim Pencegah Banjir Tercapai (4.00m)",
    },
    "はん濫注意水位到達 (5.50m)": {
        "ja": "はん濫注意水位到達 (5.50m)",
        "en": "Flood Caution Level Reached (5.50m)",
        "zh": "达到泛滥注意水位 (5.50m)",
        "ko": "범람주의 수위 도달 (5.50m)",
        "vi": "Đạt mức nước cảnh báo lũ tràn (5.50m)",
        "tl": "Naabot ang Antas ng Caution sa Pagbaha (5.50m)",
        "id": "Level Peringatan Banjir Tercapai (5.50m)",
    },
    "警戒レベル3：高齢者等避難 発令 (5.70m)": {
        "ja": "警戒レベル3：高齢者等避難 発令 (5.70m)",
        "en": "Alert Level 3: Evacuation for Elderly Issued (5.70m)",
        "zh": "警戒级别3：发布老人等避难指示 (5.70m)",
        "ko": "경계레벨3：고령자 등 피난 발령 (5.70m)",
        "vi": "Mức cảnh báo 3: Ban hành lệnh sơ tán cho người già (5.70m)",
        "tl": "Antas ng Alerto 3: Inilabas ang Paglikas para sa Matatanda (5.70m)",
        "id": "Level Peringatan 3: Evakuasi untuk Lansia Dikeluarkan (5.70m)",
    },
    "警戒レベル4：避難指示 発令 (6.80m)": {
        "ja": "警戒レベル4：避難指示 発令 (6.80m)",
        "en": "Alert Level 4: Evacuation Order Issued (6.80m)",
        "zh": "警戒级别4：发布避难指示 (6.80m)",
        "ko": "경계레벨4：피난지시 발령 (6.80m)",
        "vi": "Mức cảnh báo 4: Ban hành lệnh sơ tán (6.80m)",
        "tl": "Antas ng Alerto 4: Inilabas ang Utos ng Paglikas (6.80m)",
        "id": "Level Peringatan 4: Perintah Evakuasi Dikeluarkan (6.80m)",
    },
    "最大水位到達 (10.01m)": {
        "ja": "最大水位到達 (10.01m)",
        "en": "Maximum Water Level Reached (10.01m)",
        "zh": "达到最高水位 (10.01m)",
        "ko": "최대수위 도달 (10.01m)",
        "vi": "Đạt mức nước tối đa (10.01m)",
        "tl": "Naabot ang Maximum na Antas ng Tubig (10.01m)",
        "id": "Level Air Maksimum Tercapai (10.01m)",
    },
}


# ─────────────────────────────────────────
# タスク文翻訳（日本語原文 → 各言語）
# ─────────────────────────────────────────
TASKS = {
    "ハザードマップで自宅・職場の浸水想定区域を確認する": {
        "en": "Check the flood-risk areas of your home and workplace using the hazard map",
        "zh": "通过防灾地图确认家中和工作场所的洪水风险区域",
        "ko": "재해지도로 자택・직장의 침수 예상 구역을 확인하기",
        "vi": "Kiểm tra khu vực có nguy cơ ngập lụt tại nhà và nơi làm việc bằng bản đồ thiên tai",
        "tl": "Suriin ang mga lugar na may panganib sa pagbaha sa tahanan at trabaho gamit ang hazard map",
        "id": "Periksa area rawan banjir di rumah dan tempat kerja menggunakan peta bahaya",
    },
    "避難場所・避難経路を家族で確認しておく": {
        "en": "Check evacuation sites and routes with your family in advance",
        "zh": "提前与家人一起确认避难场所和避难路线",
        "ko": "피난장소・피난경로를 가족과 함께 미리 확인해 두기",
        "vi": "Cùng gia đình kiểm tra trước nơi và lộ trình sơ tán",
        "tl": "Suriin nang maaga ang mga evacuation site at ruta kasama ang pamilya",
        "id": "Periksa lokasi dan jalur evakuasi bersama keluarga sebelumnya",
    },
    "非常用持ち出し袋（3日分）を準備する": {
        "en": "Prepare an emergency go-bag (3 days' worth of supplies)",
        "zh": "准备应急逃生包（3天份）",
        "ko": "비상용 대피 가방（3일분）을 준비하기",
        "vi": "Chuẩn bị túi đồ khẩn cấp (đủ dùng cho 3 ngày)",
        "tl": "Maghanda ng emergency go-bag (sapat para sa 3 araw)",
        "id": "Siapkan tas darurat (cukup untuk 3 hari)",
    },
    "緊急連絡先を家族全員で共有する": {
        "en": "Share emergency contact information with all family members",
        "zh": "与全家人共享紧急联系方式",
        "ko": "긴급 연락처를 가족 모두와 공유하기",
        "vi": "Chia sẻ thông tin liên hệ khẩn cấp với tất cả thành viên gia đình",
        "tl": "Ibahagi ang emergency contact sa lahat ng pamilya",
        "id": "Bagikan kontak darurat dengan seluruh anggota keluarga",
    },
    "【高齢者等】福祉避難所の場所と利用方法を確認する": {
        "en": "[Elderly/Infants] Check the location and usage of welfare evacuation shelters",
        "zh": "【老人・婴幼儿】确认福利避难所的位置和使用方法",
        "ko": "【고령자 등】복지피난소의 위치와 이용방법을 확인하기",
        "vi": "[Người già/Trẻ nhỏ] Kiểm tra vị trí và cách sử dụng nơi trú ẩn phúc lợi",
        "tl": "[Matatanda/Sanggol] Suriin ang lokasyon at paggamit ng welfare evacuation shelter",
        "id": "[Lansia/Bayi] Periksa lokasi dan cara penggunaan tempat pengungsian khusus",
    },
    "【車避難】渋滞を避けた避難ルートを複数確認しておく": {
        "en": "[Car Evacuation] Check multiple evacuation routes avoiding traffic jams in advance",
        "zh": "【车辆避难】提前确认多条避开拥堵的避难路线",
        "ko": "【차량 피난】교통혼잡을 피한 피난경로를 여러 개 확인해 두기",
        "vi": "[Sơ tán bằng ô tô] Kiểm tra trước nhiều lộ trình sơ tán tránh tắc đường",
        "tl": "[Paglikas gamit ang Kotse] Suriin nang maaga ang iba't ibang ruta na walang traffic",
        "id": "[Evakuasi Mobil] Periksa beberapa rute evakuasi yang menghindari kemacetan",
    },
    "気象情報・台風進路予報を確認し、今後の動向に注意する": {
        "en": "Check weather information and typhoon path forecasts, and stay alert to upcoming developments",
        "zh": "确认气象信息和台风路径预报，注意今后的动向",
        "ko": "기상정보・태풍 진로예보를 확인하고 앞으로의 동향에 주의하기",
        "vi": "Kiểm tra thông tin khí tượng và dự báo đường đi của bão, theo dõi diễn biến tiếp theo",
        "tl": "Suriin ang impormasyon sa panahon at forecast ng bagyo, at maging alerto sa mga susunod na pangyayari",
        "id": "Periksa informasi cuaca dan prakiraan jalur topan, dan waspadai perkembangan selanjutnya",
    },
    "非常用持ち出し袋の内容を点検・補充する": {
        "en": "Inspect and replenish the contents of your emergency go-bag",
        "zh": "检查并补充应急逃生包的内容",
        "ko": "비상용 대피 가방의 내용을 점검・보충하기",
        "vi": "Kiểm tra và bổ sung nội dung túi đồ khẩn cấp",
        "tl": "Suriin at dagdagan ang mga nilalaman ng emergency go-bag",
        "id": "Periksa dan lengkapi isi tas darurat",
    },
    "食料・飲料水（3〜7日分）の備蓄を確認・補充する": {
        "en": "Check and replenish food and drinking water stockpiles (3-7 days' worth)",
        "zh": "确认并补充食品和饮用水储备（3~7天份）",
        "ko": "식료품・음료수（3~7일분）의 비축을 확인・보충하기",
        "vi": "Kiểm tra và bổ sung lương thực và nước uống dự trữ (đủ dùng từ 3-7 ngày)",
        "tl": "Suriin at dagdagan ang reserba ng pagkain at inuming tubig (sapat para sa 3-7 araw)",
        "id": "Periksa dan lengkapi persediaan makanan dan air minum (cukup untuk 3-7 hari)",
    },
    "スマートフォンのモバイルバッテリーを充電しておく": {
        "en": "Charge your smartphone's mobile battery in advance",
        "zh": "提前给手机的移动电源充电",
        "ko": "스마트폰의 모바일 배터리를 충전해 두기",
        "vi": "Sạc đầy pin dự phòng cho điện thoại trước",
        "tl": "I-charge nang maaga ang mobile battery ng smartphone",
        "id": "Isi daya power bank smartphone Anda sebelumnya",
    },
    "【車避難】ガソリンを満タンにしておく": {
        "en": "[Car Evacuation] Fill up your gas tank in advance",
        "zh": "【车辆避难】提前将汽油加满",
        "ko": "【차량 피난】휘발유를 가득 채워 두기",
        "vi": "[Sơ tán bằng ô tô] Đổ đầy bình xăng trước",
        "tl": "[Paglikas gamit ang Kotse] Punuin nang maaga ang tangke ng gas",
        "id": "[Evakuasi Mobil] Isi penuh tangki bensin sebelumnya",
    },
    "【高齢者等】要介護者の状態と避難介助方法を事前に確認する": {
        "en": "[Elderly/Infants] Check in advance the condition of those requiring care and how to assist with evacuation",
        "zh": "【老人・婴幼儿】提前确认需要照护者的状态和避难协助方法",
        "ko": "【고령자 등】요양자의 상태와 피난 보조방법을 사전에 확인하기",
        "vi": "[Người già/Trẻ nhỏ] Kiểm tra trước tình trạng người cần chăm sóc và cách hỗ trợ sơ tán",
        "tl": "[Matatanda/Sanggol] Suriin nang maaga ang kondisyon ng nangangailangan ng pag-aalaga at paraan ng tulong sa paglikas",
        "id": "[Lansia/Bayi] Periksa kondisi orang yang membutuhkan perawatan dan cara membantu evakuasi sebelumnya",
    },
    "郡山市・気象庁の最新情報を継続的に確認する": {
        "en": "Continuously check the latest information from Koriyama City and the Japan Meteorological Agency",
        "zh": "持续确认郡山市・气象厅的最新信息",
        "ko": "고리야마시・기상청의 최신 정보를 계속 확인하기",
        "vi": "Liên tục theo dõi thông tin mới nhất từ thành phố Koriyama và Cơ quan Khí tượng",
        "tl": "Patuloy na suriin ang pinakabagong impormasyon mula sa Lungsod ng Koriyama at JMA",
        "id": "Terus periksa informasi terbaru dari Kota Koriyama dan Badan Meteorologi Jepang",
    },
    "避難場所の開設状況を市公式SNS・防災メールで確認する": {
        "en": "Check the opening status of evacuation sites via the city's official SNS or disaster email",
        "zh": "通过市官方SNS・防灾邮件确认避难场所的开设情况",
        "ko": "피난장소 개설상황을 시 공식 SNS・방재메일로 확인하기",
        "vi": "Kiểm tra tình trạng mở cửa của các nơi sơ tán qua SNS chính thức hoặc email phòng chống thiên tai của thành phố",
        "tl": "Suriin ang status ng pagbukas ng evacuation site sa opisyal na SNS o disaster email ng lungsod",
        "id": "Periksa status pembukaan tempat evakuasi melalui SNS resmi atau email bencana kota",
    },
    "浴槽・ポリタンクに生活用水を確保する": {
        "en": "Secure household water in your bathtub and water tanks",
        "zh": "在浴缸・塑料水桶中储备生活用水",
        "ko": "욕조・물탱크에 생활용수를 확보하기",
        "vi": "Trữ nước sinh hoạt vào bồn tắm và bình chứa nước",
        "tl": "Magtipon ng tubig sa bathtub at water tank para gamiting pang-araw-araw",
        "id": "Simpan air untuk kebutuhan rumah tangga di bathtub dan tangki air",
    },
    "【車避難】車を浸水しにくい高台の駐車場に移動させる": {
        "en": "[Car Evacuation] Move your car to a parking lot on higher ground that is less likely to flood",
        "zh": "【车辆避难】将车移动到不易被淹的高地停车场",
        "ko": "【차량 피난】차를 침수되기 어려운 고지대 주차장으로 이동시키기",
        "vi": "[Sơ tán bằng ô tô] Di chuyển xe đến bãi đỗ xe trên cao, ít có khả năng bị ngập",
        "tl": "[Paglikas gamit ang Kotse] Ilipat ang kotse sa parking lot sa mataas na lugar na hindi madaling malubog",
        "id": "[Evakuasi Mobil] Pindahkan mobil ke tempat parkir di dataran tinggi yang tidak mudah tergenang",
    },
    "【高齢者等】避難に時間がかかるため、早めの避難開始を検討する": {
        "en": "[Elderly/Infants] Since evacuation takes time, consider starting to evacuate early",
        "zh": "【老人・婴幼儿】因避难需要时间，请考虑提早开始避难",
        "ko": "【고령자 등】피난에 시간이 걸리므로 조기 피난 시작을 검토하기",
        "vi": "[Người già/Trẻ nhỏ] Vì sơ tán cần nhiều thời gian, hãy xem xét bắt đầu sơ tán sớm",
        "tl": "[Matatanda/Sanggol] Dahil matagal ang paglikas, isaalang-alang ang maagang paglikas",
        "id": "[Lansia/Bayi] Karena evakuasi membutuhkan waktu, pertimbangkan untuk mulai evakuasi lebih awal",
    },
    "阿武隈川の水位情報を10分ごとに確認する": {
        "en": "Check the Abukuma River water level information every 10 minutes",
        "zh": "每10分钟确认一次阿武隈川的水位信息",
        "ko": "아부쿠마강의 수위정보를 10분마다 확인하기",
        "vi": "Kiểm tra thông tin mực nước sông Abukuma mỗi 10 phút",
        "tl": "Suriin ang antas ng tubig ng Abukuma River bawat 10 minuto",
        "id": "Periksa informasi level air Sungai Abukuma setiap 10 menit",
    },
    "避難の準備を整え、いつでも出発できる状態にする": {
        "en": "Complete evacuation preparations so you can leave at any time",
        "zh": "做好避难准备，随时可以出发",
        "ko": "피난준비를 마치고 언제든지 출발할 수 있는 상태로 해 두기",
        "vi": "Hoàn tất chuẩn bị sơ tán để có thể xuất phát bất cứ lúc nào",
        "tl": "Kumpletuhin ang paghahanda sa paglikas upang makaalis anumang oras",
        "id": "Selesaikan persiapan evakuasi agar dapat berangkat kapan saja",
    },
    "隣近所・地域の要配慮者に声がけを開始する": {
        "en": "Start checking in with neighbors and people in the community who may need extra support",
        "zh": "开始与邻居・社区中需要关怀的人取得联系",
        "ko": "이웃・지역의 배려가 필요한 사람에게 안내를 시작하기",
        "vi": "Bắt đầu liên lạc với hàng xóm và những người cần hỗ trợ trong khu vực",
        "tl": "Magsimulang makipag-ugnayan sa mga kapitbahay at taong nangangailangan ng tulong sa komunidad",
        "id": "Mulai menyapa tetangga dan orang yang membutuhkan perhatian di komunitas",
    },
    "【高齢者等】早期避難を開始する（次のフェーズを待たない）": {
        "en": "[Elderly/Infants] Begin evacuating early (do not wait for the next phase)",
        "zh": "【老人・婴幼儿】开始提早避难（不要等待下一阶段）",
        "ko": "【고령자 등】조기 피난을 시작하기（다음 단계를 기다리지 않음）",
        "vi": "[Người già/Trẻ nhỏ] Bắt đầu sơ tán sớm (không chờ đến giai đoạn tiếp theo)",
        "tl": "[Matatanda/Sanggol] Magsimulang lumikas nang maaga (hindi na maghintay sa susunod na yugto)",
        "id": "[Lansia/Bayi] Mulai evakuasi lebih awal (jangan menunggu fase berikutnya)",
    },
    "郡山市の避難情報（避難指示・緊急安全確保）を随時確認する": {
        "en": "Continuously check Koriyama City's evacuation information (evacuation orders, emergency safety measures)",
        "zh": "随时确认郡山市的避难信息（避难指示・紧急安全确保）",
        "ko": "고리야마시의 피난정보（피난지시・긴급안전확보）를 수시로 확인하기",
        "vi": "Liên tục kiểm tra thông tin sơ tán của thành phố Koriyama (lệnh sơ tán, đảm bảo an toàn khẩn cấp)",
        "tl": "Patuloy na suriin ang impormasyon sa paglikas ng Lungsod ng Koriyama (utos ng paglikas, emergency safety)",
        "id": "Terus periksa informasi evakuasi Kota Koriyama (perintah evakuasi, keselamatan darurat)",
    },
    "外出は極力控え、自宅待機または避難先で待機する": {
        "en": "Avoid going outside as much as possible, and stay at home or at your evacuation location",
        "zh": "尽量避免外出，在家中或避难处待命",
        "ko": "외출은 최대한 자제하고 자택대기 또는 피난처에서 대기하기",
        "vi": "Hạn chế tối đa việc ra ngoài, ở yên tại nhà hoặc nơi sơ tán",
        "tl": "Iwasan ang pag-alis sa labas, manatili sa tahanan o sa lugar ng paglikas",
        "id": "Hindari keluar rumah sebisa mungkin, tetap di rumah atau di tempat evakuasi",
    },
    "非常用持ち出し袋を玄関に置き、すぐ持ち出せるようにする": {
        "en": "Place your emergency go-bag by the entrance so you can grab it immediately",
        "zh": "将应急逃生包放在门口，以便随时取走",
        "ko": "비상용 대피 가방을 현관에 두고 바로 가지고 나갈 수 있도록 하기",
        "vi": "Đặt túi đồ khẩn cấp ở lối ra vào để có thể mang theo ngay",
        "tl": "Ilagay ang emergency go-bag malapit sa pintuan para madaling dalhin",
        "id": "Letakkan tas darurat di pintu masuk agar bisa segera dibawa",
    },
    "【車避難】この段階以降の車避難は浸水リスクあり、徒歩避難も検討": {
        "en": "[Car Evacuation] From this stage, car evacuation carries a flood risk; also consider evacuating on foot",
        "zh": "【车辆避难】此阶段以后开车避难存在被淹风险，请同时考虑步行避难",
        "ko": "【차량 피난】이 단계 이후의 차량 피난은 침수 위험이 있으므로 도보 피난도 검토하기",
        "vi": "[Sơ tán bằng ô tô] Từ giai đoạn này, sơ tán bằng ô tô có nguy cơ ngập nước, hãy xem xét sơ tán bằng đi bộ",
        "tl": "[Paglikas gamit ang Kotse] Mula sa yugtong ito, may panganib ng pagbaha sa paglikas gamit ang kotse, isaalang-alang din ang paglakad",
        "id": "[Evakuasi Mobil] Sejak fase ini, evakuasi dengan mobil berisiko terendam, pertimbangkan juga evakuasi berjalan kaki",
    },
    "📢 高齢者等避難 発令！高齢者・障がい者・乳幼児は直ちに避難する": {
        "en": "📢 Evacuation for Elderly Issued! Elderly persons, people with disabilities, and infants should evacuate immediately",
        "zh": "📢 已发布老人等避难指示！老人・残障人士・婴幼儿请立即避难",
        "ko": "📢 고령자 등 피난 발령！고령자・장애인・영유아는 즉시 피난하기",
        "vi": "📢 Đã ban hành lệnh sơ tán cho người già! Người già, người khuyết tật và trẻ nhỏ hãy sơ tán ngay lập tức",
        "tl": "📢 Inilabas ang Paglikas para sa Matatanda! Ang matatanda, may kapansanan, at sanggol ay agad na lumikas",
        "id": "📢 Evakuasi untuk Lansia Dikeluarkan! Lansia, penyandang disabilitas, dan bayi harus segera evakuasi",
    },
    "避難場所に向かう。安全が確認できない場合は2階以上へ垂直避難": {
        "en": "Head to an evacuation site. If you cannot confirm safety, evacuate vertically to the 2nd floor or higher",
        "zh": "前往避难场所。如无法确认安全，请向二楼以上垂直避难",
        "ko": "피난장소로 향하기. 안전을 확인할 수 없는 경우 2층 이상으로 수직피난하기",
        "vi": "Đi đến nơi sơ tán. Nếu không thể đảm bảo an toàn, hãy sơ tán theo chiều thẳng đứng lên tầng 2 hoặc cao hơn",
        "tl": "Pumunta sa evacuation site. Kung hindi makumpirma ang kaligtasan, lumikas pataas sa ika-2 palapag o mas mataas",
        "id": "Menuju ke tempat evakuasi. Jika keselamatan tidak dapat dipastikan, evakuasi vertikal ke lantai 2 atau lebih tinggi",
    },
    "【高齢者等】直ちに避難を開始する。介助者は最優先で行動する": {
        "en": "[Elderly/Infants] Begin evacuating immediately. Caregivers should act as the top priority",
        "zh": "【老人・婴幼儿】立即开始避难。照护者请优先行动",
        "ko": "【고령자 등】즉시 피난을 시작하기. 보조자는 최우선으로 행동하기",
        "vi": "[Người già/Trẻ nhỏ] Bắt đầu sơ tán ngay lập tức. Người hỗ trợ hành động với mức ưu tiên cao nhất",
        "tl": "[Matatanda/Sanggol] Agad na lumikas. Ang tagapag-alaga ay aksyon kaagad bilang pinakaprayoridad",
        "id": "[Lansia/Bayi] Mulai evakuasi segera. Pendamping harus bertindak dengan prioritas utama",
    },
    "【車避難】冠水した道路への進入は絶対に避ける（30cm超で車が流される）": {
        "en": "[Car Evacuation] Absolutely avoid entering flooded roads (a car can be swept away in water over 30cm)",
        "zh": "【车辆避难】绝对避免进入被淹道路（超过30cm车辆会被冲走）",
        "ko": "【차량 피난】침수된 도로로의 진입은 절대 피하기（30cm 초과시 차가 떠내려감）",
        "vi": "[Sơ tán bằng ô tô] Tuyệt đối tránh đi vào đường bị ngập (xe có thể bị cuốn trôi nếu nước sâu trên 30cm)",
        "tl": "[Paglikas gamit ang Kotse] Iwasan nang lubusan ang pagpasok sa mga baradong kalsada (matatangay ang kotse kung lampas 30cm ang tubig)",
        "id": "[Evakuasi Mobil] Hindari sama sekali memasuki jalan yang tergenang (mobil dapat terbawa arus jika air lebih dari 30cm)",
    },
    "🚨 避難指示 発令！全員が直ちに避難を開始する": {
        "en": "🚨 Evacuation Order Issued! Everyone must begin evacuating immediately",
        "zh": "🚨 已发布避难指示！所有人请立即开始避难",
        "ko": "🚨 피난지시 발령！전원 즉시 피난을 시작하기",
        "vi": "🚨 Đã ban hành lệnh sơ tán! Tất cả mọi người phải bắt đầu sơ tán ngay lập tức",
        "tl": "🚨 Inilabas ang Utos ng Paglikas! Lahat ay dapat agad na lumikas",
        "id": "🚨 Perintah Evakuasi Dikeluarkan! Semua orang harus segera evakuasi",
    },
    "避難場所への移動が困難な場合は近隣の頑丈な建物の上層階へ垂直避難": {
        "en": "If moving to an evacuation site is difficult, evacuate vertically to the upper floors of a nearby sturdy building",
        "zh": "若难以前往避难场所，请向附近坚固建筑物的高层垂直避难",
        "ko": "피난장소로의 이동이 어려운 경우 인근의 견고한 건물의 상층으로 수직피난하기",
        "vi": "Nếu khó di chuyển đến nơi sơ tán, hãy sơ tán thẳng lên các tầng trên của một tòa nhà chắc chắn gần đó",
        "tl": "Kung mahirap pumunta sa evacuation site, lumikas pataas sa itaas na palapag ng matibay na gusali sa malapit",
        "id": "Jika sulit menuju tempat evakuasi, evakuasi vertikal ke lantai atas bangunan kokoh terdekat",
    },
    "家族の安否確認・集合場所を確認し、連絡手段を確保する": {
        "en": "Check on family members' safety, confirm a meeting place, and secure means of communication",
        "zh": "确认家人安全・集合地点，并确保联络方式",
        "ko": "가족의 안부확인・집합장소를 확인하고 연락수단을 확보하기",
        "vi": "Kiểm tra an toàn của các thành viên gia đình, xác nhận điểm tập trung và đảm bảo phương tiện liên lạc",
        "tl": "Suriin ang kaligtasan ng pamilya, kumpirmahin ang meeting place, at tiyakin ang paraan ng komunikasyon",
        "id": "Periksa keselamatan keluarga, konfirmasi tempat berkumpul, dan amankan sarana komunikasi",
    },
    "【高齢者等】介助者と合流し、福祉避難所への移動を優先する": {
        "en": "[Elderly/Infants] Join up with caregivers and prioritize moving to a welfare evacuation shelter",
        "zh": "【老人・婴幼儿】与照护者会合，优先前往福利避难所",
        "ko": "【고령자 등】보조자와 합류하여 복지피난소로의 이동을 우선시하기",
        "vi": "[Người già/Trẻ nhỏ] Hợp sức với người hỗ trợ và ưu tiên di chuyển đến nơi trú ẩn phúc lợi",
        "tl": "[Matatanda/Sanggol] Sumama sa tagapag-alaga at unahin ang paglipat sa welfare evacuation shelter",
        "id": "[Lansia/Bayi] Bergabung dengan pendamping dan utamakan pindah ke tempat pengungsian khusus",
    },
    "⛔ 屋外への移動は生命の危険があります。今いる場所で安全確保": {
        "en": "⛔ Moving outdoors is life-threatening. Secure your safety where you currently are",
        "zh": "⛔ 在户外移动有生命危险。请在当前所在地确保安全",
        "ko": "⛔ 실외로의 이동은 생명의 위험이 있습니다. 현재 위치에서 안전을 확보하기",
        "vi": "⛔ Di chuyển ra ngoài có nguy hiểm đến tính mạng. Hãy đảm bảo an toàn tại vị trí hiện tại",
        "tl": "⛔ Mapanganib ang pag-alis sa labas. Tiyakin ang kaligtasan sa kasalukuyang lokasyon",
        "id": "⛔ Bergerak ke luar membahayakan jiwa. Pastikan keselamatan di lokasi Anda saat ini",
    },
    "建物の上層階・屋根など、最も高い場所へ移動する（垂直避難）": {
        "en": "Move to the highest point available, such as upper floors or the roof (vertical evacuation)",
        "zh": "请移动至建筑物高层・屋顶等最高处（垂直避难）",
        "ko": "건물의 상층・지붕 등 가장 높은 곳으로 이동하기（수직피난）",
        "vi": "Di chuyển đến nơi cao nhất có thể, như tầng trên hoặc trên mái nhà (sơ tán theo chiều thẳng đứng)",
        "tl": "Lumipat sa pinakamataas na bahagi, tulad ng itaas na palapag o bubong (vertical evacuation)",
        "id": "Pindah ke tempat tertinggi yang tersedia, seperti lantai atas atau atap (evakuasi vertikal)",
    },
    "救助要請：171（災害用伝言ダイヤル）、119番または110番に連絡": {
        "en": "Request rescue: contact 171 (Disaster Message Dial), 119 (fire/ambulance), or 110 (police)",
        "zh": "请求救援：联系171（灾害留言专线）、119或110",
        "ko": "구조요청：171（재해용 메시지 다이얼）、119번 또는 110번으로 연락하기",
        "vi": "Yêu cầu cứu hộ: liên hệ 171 (Đường dây tin nhắn thiên tai), 119 hoặc 110",
        "tl": "Humingi ng saklolo: tumawag sa 171 (Disaster Message Dial), 119, o 110",
        "id": "Minta penyelamatan: hubungi 171 (Dial Pesan Bencana), 119, atau 110",
    },
    "窓やドアを開けず、水位上昇に備え常に上方向への逃げ場を確保する": {
        "en": "Do not open windows or doors; always keep an escape route upward in case the water level rises further",
        "zh": "请不要打开窗户或门，为应对水位上升请始终确保向上的逃生通道",
        "ko": "창문이나 문을 열지 말고, 수위 상승에 대비해 항상 위쪽으로의 도피처를 확보하기",
        "vi": "Không mở cửa sổ hoặc cửa ra vào; luôn đảm bảo có lối thoát hướng lên trong trường hợp nước tiếp tục dâng",
        "tl": "Huwag buksan ang mga bintana o pintuan; laging tiyakin ang daan paitaas kung sakaling tumaas pa ang tubig",
        "id": "Jangan membuka jendela atau pintu; selalu pastikan ada jalur pelarian ke atas jika air terus naik",
    },
}


# ─────────────────────────────────────────
# ヘルパー関数
# ─────────────────────────────────────────

def t(lang: str, key: str, **kwargs) -> str:
    """UIラベルを翻訳する。見つからない場合は日本語を返す。"""
    entry = UI.get(key)
    if not entry:
        return key
    text = entry.get(lang, entry.get("ja", key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def t_phase(lang: str, phase_ja: str) -> str:
    """フェーズ名を翻訳する。見つからない場合は原文を返す。"""
    entry = PHASES.get(phase_ja)
    if not entry:
        return phase_ja
    return entry.get(lang, phase_ja)


def t_task(lang: str, task_ja: str) -> str:
    """タスク文を翻訳する。見つからない場合（lang=jaまたは未登録）は原文を返す。"""
    if lang == "ja":
        return task_ja
    entry = TASKS.get(task_ja)
    if not entry:
        return task_ja
    return entry.get(lang, task_ja)


def google_translate_url(text: str, target_lang: str) -> str:
    """指定テキストをGoogle翻訳で開くURLを生成する（原文=日本語想定）。"""
    import urllib.parse
    gt_lang_map = {
        "en": "en", "zh": "zh-CN", "ko": "ko",
        "vi": "vi", "tl": "tl", "id": "id", "ja": "ja",
    }
    tl = gt_lang_map.get(target_lang, "en")
    q = urllib.parse.quote(text)
    return f"https://translate.google.com/?sl=ja&tl={tl}&text={q}&op=translate"