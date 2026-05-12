<div align="center">
  <h1>🕹️ Pac-Man Python Clone (AI & Multiplayer)</h1>
  <p>Một dự án tái hiện tựa game arcade kinh điển Pac-Man với trí tuệ nhân tạo (BFS) và chế độ nhiều người chơi (Multiplayer) qua mạng nội bộ.</p>
</div>

---

## 🌟 Giới thiệu

Dự án này là một phiên bản phát triển toàn diện mô phỏng (clone) tựa game **Pac-Man**, được xây dựng hoàn toàn bằng ngôn ngữ Python cùng thư viện đồ hoạ Pygame. 

Không chỉ tái hiện lại lối chơi gốc, dự án còn đi sâu vào việc áp dụng các **Cấu trúc dữ liệu và Giải thuật** (như BFS, Đồ thị, Hàng đợi), cũng như phát triển các kỹ thuật lập trình nâng cao (hệ thống State Machine, xử lý âm thanh đa kênh, lập trình mạng Socket TCP/Threading để hỗ trợ Multiplayer).

## ✨ Tính năng nổi bật

*   👻 **AI Tìm đường thông minh:** Sử dụng thuật toán Tìm kiếm theo chiều rộng (BFS) trên đồ thị lưới không trọng số để tính toán đường đi ngắn nhất cho ma (Ghost), tạo ra những màn rượt đuổi nghẹt thở trong chế độ Offline.
*   🕹️ **Cơ chế vật lý O(1):** Xử lý kiểm tra va chạm mượt mà dựa trên cấu trúc Mảng 2 Chiều (2D Array). Hỗ trợ cơ chế xếp hàng hướng đi (Turn-queueing) cho cả Pac-Man và Player Ghost để luồn lách qua các góc hẹp dễ dàng.
*   🌐 **Chế độ Multiplayer (LAN):** Trải nghiệm chơi cùng bạn bè với kiến trúc Client - Server sử dụng Socket và Multi-threading. Hỗ trợ 1 người làm Pac-Man và tối đa 4 người làm Ghost (không có AI Ghost xen vào để đảm bảo tính cạnh tranh thực tế).
*   🎨 **Đồ họa Retro/Neon:** Hình ảnh sắc nét, nền di chuyển synthwave, hệ thống hạt (Particle System) và số điểm nổi (Floating Popup).
*   🎵 **Âm thanh Đa kênh:** Sử dụng hệ thống 8 kênh âm thanh độc lập để phát tiếng ăn hạt, hú còi, và ăn ma cùng một lúc không bị đè tiếng.
*   💊 **Cơ chế Frightened:** Ăn viên sức mạnh (Energizer) để đảo ngược tình thế, khiến các con ma hoảng sợ và chậm lại!

## 🚀 Cài đặt và Sử dụng

### 1. Yêu cầu hệ thống
* Python 3.10 trở lên
* Pygame 2.x

### 2. Cài đặt thư viện
Clone repository này về máy và cài đặt các thư viện cần thiết:
```bash
git clone https://github.com/thinhtheconqueror/Pacman-Game
cd Pacman-Game
pip install -r requirements.txt
```

### 3. Chạy Game
Bạn chỉ cần chạy file `app.py` để khởi động Game Launcher:
```bash
python app.py
```

Tại màn hình chính, bạn có thể chọn:
- **Offline Mode:** Chơi một người với AI.
- **Host Multiplayer Server:** Tạo phòng chơi mạng nội bộ (LAN).
- **Join Multiplayer:** Nhập IP để tham gia vào phòng chơi mạng đã tạo.

## 📁 Cấu trúc thư mục

* `app.py`: Game Launcher chính, điều hướng chế độ Offline/Online.
* `main.py`: Chứa logic vòng lặp chính của chế độ Offline.
* `entities.py`: Định nghĩa các thực thể trong game (`Pacman`, `Ghost`).
* `algorithms.py`: Các thuật toán AI (BFS, Random Walk).
* `Multiplayer_Python/`: Thư mục chứa mã nguồn Server và Client cho chế độ Multiplayer.
* `docs/`: Tài liệu chi tiết về API và Docstrings của dự án.
* `Tai_Lieu_Bao_Cao/`: Các file báo cáo đồ án qua từng tuần.

## 🧠 Tài liệu tham khảo
Vui lòng xem trong thư mục [docs/](docs/) để đọc chi tiết về các Docstrings giải thuật và báo cáo tổng kết của dự án.

---
**Giảng viên hướng dẫn:** Nguyễn Thanh Sơn  
**Sinh viên thực hiện:** Võ Quốc Thịnh  
**Môn học:** Cấu trúc dữ liệu và giải thuật (IT003)
