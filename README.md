# BÁO CÁO ĐỒ ÁN MÔN HỌC: CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT

**Tên đề tài:** Ứng dụng Cấu trúc dữ liệu và Giải thuật trong việc phát triển mô phỏng trò chơi Pac-Man đa người chơi.

## 1. THÔNG TIN CHUNG
- **Trường:** Đại học Công nghệ Thông tin — ĐHQG TP.HCM (UIT)
- **Môn học:** Cấu trúc dữ liệu và Giải thuật (IT003)
- **Giảng viên hướng dẫn:** Nguyễn Thanh Sơn
- **Sinh viên thực hiện:** Võ Quốc Thịnh

---

## 2. GIỚI THIỆU ĐỀ TÀI

Dự án này là một phiên bản phát triển mô phỏng (clone) tựa game arcade kinh điển Pac-Man. Mục tiêu chính của đồ án không chỉ dừng lại ở việc tái hiện gameplay, mà còn tập trung vào việc áp dụng các kiến thức cốt lõi của môn học Cấu trúc dữ liệu và Giải thuật vào giải quyết các bài toán thực tế trong lập trình trò chơi.

Đồ án được chia làm hai phần chính:
1. **Chế độ Ngoại tuyến (Offline):** Tập trung vào việc xây dựng Trí tuệ nhân tạo (AI) cho các thực thể (Ghost) bằng các thuật toán duyệt đồ thị.
2. **Chế độ Trực tuyến (Multiplayer):** Phát triển cơ chế giao tiếp mạng nội bộ (LAN) dựa trên kiến trúc Client-Server, đảm bảo tính đồng bộ dữ liệu giữa nhiều người chơi.

---

## 3. CẤU TRÚC DỮ LIỆU VÀ GIẢI THUẬT ĐƯỢC ÁP DỤNG

### 3.1. Biểu diễn đồ thị bản đồ (Graph Representation)
Bản đồ trong trò chơi được mô hình hóa dưới dạng một đồ thị vô hướng không trọng số.
- **Cấu trúc dữ liệu:** Sử dụng Ma trận 2 chiều (2D Array) có kích thước 36 hàng x 28 cột.
- **Tính toán:** Mỗi ô vuông (cell) hợp lệ trên bản đồ được xem là một đỉnh (Vertex), và sự liền kề giữa các ô (trên, dưới, trái, phải) đại diện cho các cạnh (Edge) nối giữa chúng. Việc kiểm tra tính hợp lệ của đường đi (kiểm tra va chạm với tường) được thực hiện với độ phức tạp O(1) nhờ đặc tính truy xuất trực tiếp của mảng.

### 3.2. Thuật toán Tìm kiếm theo chiều rộng (Breadth-First Search - BFS)
Được sử dụng làm thuật toán lõi cho Trí tuệ nhân tạo (cho cả 2 chế độ Easy và Hard) của các Ghost để tính toán đường đi ngắn nhất đến vị trí mục tiêu.
- **Cấu trúc dữ liệu hỗ trợ:** 
  - `Queue` (Hàng đợi - triển khai bằng `collections.deque` trong Python) để duyệt các đỉnh theo từng mức (level-order) với thời gian O(1) cho các thao tác enqueue/dequeue.
  - `Dictionary` (Bảng băm) để lưu vết đường đi (parent map), phục vụ cho quá trình truy vết (backtracking) từ đích về điểm xuất phát.
  - `Set` (Tập hợp) dùng để lưu trữ tọa độ các con ma khác (chướng ngại vật động) giúp thuật toán kiểm tra đụng độ và tự động tránh va chạm với độ phức tạp O(1).
- **Độ phức tạp:** Thời gian O(V + E) và Không gian O(V), tối ưu cho đồ thị không trọng số như bản đồ lưới của Pac-Man.
- **Cải tiến chiến thuật (Điểm phân biệt độ khó):**
  - **Dễ (Easy):** Mục tiêu BFS luôn trỏ vào vị trí hiện tại của Pac-Man (Chỉ bám đuôi).
  - **Khó (Hard):** Tích hợp logic tìm hướng đón lõng cho một số Ghost đặc biệt (như Pinky - đặt mục tiêu chặn trước 4 ô theo hướng di chuyển của Pac-Man) để tạo ra thế gọng kìm vây bắt.

### 3.3. Thuật toán Đi ngẫu nhiên (Random Walk)
Được sử dụng khi Ghost ở trạng thái bị hoảng sợ (Frightened Mode) hoặc làm phương án dự phòng (Fallback).
- **Cơ chế:** Thuật toán duyệt qua các đỉnh kề hợp lệ hiện tại và thực hiện chọn ngẫu nhiên một đỉnh tiếp theo để di chuyển.
- **Sử dụng:** Được dùng để giả lập sự mất phương hướng, hoảng loạn chạy trốn khi bị Pac-Man ăn viên sức mạnh. Đồng thời làm phương án dự phòng (gỡ kẹt) khi thuật toán BFS đụng ngõ cụt.
- **Độ phức tạp:** Thời gian O(1) do số lượng đỉnh kề tối đa luôn <= 4.

---

## 4. KIẾN TRÚC HỆ THỐNG VÀ XỬ LÝ MẠNG

### 4.1. Mô hình Client - Server
Chế độ nhiều người chơi (Multiplayer) được xây dựng hoàn toàn bằng thư viện Socket thuần của Python sử dụng giao thức TCP.
- **Server:** Đóng vai trò là nguồn dữ liệu chuẩn (Authoritative Server). Mọi tính toán về va chạm, logic vật lý, tính điểm đều được thực hiện tại đây.
- **Client:** Đóng vai trò render đồ họa và gửi tín hiệu điều khiển (Input) lên Server.

### 4.2. Xử lý đa luồng (Multi-threading)
Sử dụng thư viện `threading` để cho phép Server chấp nhận và xử lý nhiều kết nối từ Client cùng lúc mà không bị nghẽn (blocking).
- Một luồng (Thread) độc lập chạy vòng lặp tính toán trạng thái game (Game Loop) ở tốc độ 60 FPS.
- Các luồng phụ trách tiếp nhận tín hiệu điều khiển từ từng Client.

### 4.3. Quản lý trạng thái và Đồng bộ dữ liệu
- **Cấu trúc dữ liệu đóng gói:** Toàn bộ trạng thái trò chơi được lưu trữ trong một `Dictionary` lớn tại Server, bao gồm danh sách các thực thể, điểm số, và trạng thái hạt.
- **Serialization:** Sử dụng thư viện `pickle` của Python để tuần tự hóa (serialize) cấu trúc dữ liệu này thành luồng byte và truyền qua mạng (Socket), đảm bảo quá trình giải mã tại Client diễn ra chính xác và khôi phục lại cấu trúc dữ liệu ban đầu.

---

## 5. CẤU TRÚC MÃ NGUỒN

- `app.py`: Tệp thực thi chính, quản lý giao diện chuyển đổi giữa các chế độ Offline và Online.
- `main.py`: Vòng lặp chính của chế độ chơi đơn (Offline).
- `entities.py`: Định nghĩa các đối tượng Pacman, Ghost theo hướng Đối tượng (OOP).
- `algorithms.py`: Triển khai các thuật toán đồ thị và AI (BFS, Random Walk).
- `map_data.py`: Khởi tạo và lưu trữ ma trận bản đồ.
- `Multiplayer_Python/`: Thư mục chứa kiến trúc mạng (server.py, client.py, network.py) và các logic vật lý riêng cho chế độ trực tuyến.
- `docs/DOCSTRINGS.md`: Tài liệu đặc tả kỹ thuật chi tiết các hàm và API trong dự án.

---

## 6. HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG

### 6.1. Môi trường yêu cầu
- Môi trường thực thi: Python 3.10 trở lên.
- Các thư viện phụ thuộc: Được định nghĩa trong tệp tin `requirements.txt` (chủ yếu là thư viện `pygame`).

### 6.2. Tải mã nguồn và cài đặt hệ thống
Bước 1: Tải mã nguồn đồ án từ kho lưu trữ (repository) thông qua lệnh Git:
```cmd
git clone https://github.com/thinhtheconqueror/Pacman-Game
cd Pacman-Game
```
Bước 2: Đảm bảo Command Prompt (cmd) hoặc Terminal đang trỏ vào thư mục `Pacman-Game` vừa tải về.
Bước 3: Thực thi lệnh sau để cài đặt các thư viện phụ thuộc cần thiết:
```cmd
pip install -r requirements.txt
```

### 6.3. Hướng dẫn khởi chạy
Từ thư mục gốc của dự án, khởi chạy tệp tin `app.py` để mở menu chính (Game Launcher):
```cmd
python app.py
```

### 6.4. Tương tác với hệ thống
- **Chế độ Ngoại tuyến (Offline Mode):**
  - Tại menu chính, nhấn phím `1`.
  - Chọn độ khó của thuật toán AI và số lượng thực thể Ghost mong muốn.
  - Sử dụng các phím mũi tên hoặc cụm phím `W`, `A`, `S`, `D` để điều hướng đối tượng Pac-Man.
- **Chế độ Trực tuyến (Host Multiplayer):**
  - Nhấn phím `2` để khởi tạo máy chủ phòng chơi cục bộ.
  - Một tiến trình Server sẽ tự động chạy ngầm và hệ thống sẽ cung cấp địa chỉ IPv4 của máy Host.
  - Lựa chọn vai trò điều khiển (Pac-Man hoặc Ghost). Người điều khiển Pac-Man (khi đã đủ người) có quyền nhấn phím `SPACE` để bắt đầu trò chơi.
- **Chế độ Trực tuyến (Join Multiplayer):**
  - Nhấn phím `3` để tham gia phòng chơi hiện có.
  - Nhập chính xác địa chỉ IPv4 của máy Host và chọn vai trò tham gia.
  - (Yêu cầu kỹ thuật: Các máy tính tham gia kết nối phải nằm trong cùng một mạng nội bộ LAN/Wi-Fi).

---

## 7. KẾT LUẬN

Dự án đã hoàn thành các mục tiêu ứng dụng trực tiếp những cấu trúc dữ liệu căn bản (Mảng 2D, Hàng đợi, Bảng băm) và các giải thuật kinh điển (Duyệt đồ thị theo chiều rộng) vào việc giải quyết bài toán tìm đường và tối ưu hóa hệ thống vật lý trong trò chơi. Đồng thời, dự án cũng mở rộng được khả năng lập trình ứng dụng phân tán thông qua kiến trúc mạng Client-Server cơ bản.
