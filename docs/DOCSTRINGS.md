# 📚 Tài Liệu API & Logic Trò Chơi (Docstrings)

Tài liệu này giải thích chi tiết chức năng, tham số và độ phức tạp của các thuật toán cũng như các hàm cốt lõi được sử dụng trong hệ thống Game Pac-Man (bao gồm cả AI và Multiplayer).

---

## 1. Trí Tuệ Nhân Tạo (AI) - `algorithms.py`

### 🔹 `bfs_shortest_path(start, target, grid, occupied_positions)`
**Mô tả:** Thuật toán Tìm kiếm theo chiều rộng (BFS). Được sử dụng làm AI ở mức độ Khó (Hard). Đảm bảo tìm ra đường đi ngắn nhất để các bóng ma (Ghost) tiếp cận Pac-Man.
* **Logic:** Duyệt qua đồ thị không trọng số (mảng 2 chiều) theo từng cấp độ (level-order traversal). Sử dụng Hàng đợi (Queue) để lưu các đỉnh chờ duyệt và Từ điển (Dictionary) để lưu vết đường đi.
* **Tham số:**
  * `start` *(tuple)*: Tọa độ `(row, col)` bắt đầu của Ghost.
  * `target` *(tuple)*: Tọa độ `(row, col)` mục tiêu (thường là vị trí của Pac-Man).
  * `grid` *(list[list[str]])*: Ma trận 2D biểu diễn mê cung.
  * `occupied_positions` *(set, optional)*: Tập hợp các vị trí đang bị chiếm bởi Ghost khác (để AI tránh đi đè lên nhau).
* **Trả về:** `tuple` - Tọa độ `(row, col)` bước đi tối ưu tiếp theo.
* **Độ phức tạp:** Thời gian `O(V + E)`, Không gian `O(V)`. (Với V là số đỉnh, E là số cạnh).

### 🔹 `random_walk_algorithm(start, grid, occupied_positions)`
**Mô tả:** Thuật toán bước ngẫu nhiên. Được sử dụng làm AI mức độ Dễ hoặc làm phương án dự phòng (fallback) khi BFS không thể tìm được đường.
* **Logic:** Lấy tất cả các ô liền kề (không bị vướng tường) và chọn ngẫu nhiên một hướng để di chuyển.
* **Tham số:** Giống như hàm BFS.
* **Trả về:** `tuple` - Tọa độ bước đi tiếp theo.
* **Độ phức tạp:** Thời gian `O(1)`.

### 🔹 `get_valid_neighbors(pos, grid, occupied_positions)`
**Mô tả:** Hàm phụ trợ tìm tất cả các ô liền kề hợp lệ (Lên, Xuống, Trái, Phải) từ một tọa độ cho trước.
* **Logic:** Bỏ qua các ô chứa tường (`'1'`), các ô nằm ngoài bản đồ, và các ô đã có Ghost khác đứng. Tích hợp cơ chế đi xuyên hầm (Tunnel Wrap Around).
* **Trả về:** `list[tuple]` - Danh sách các tọa độ hợp lệ.

---

## 2. Hệ Thống Thực Thể (Entities) - `entities.py`

### 🔹 `Ghost.frighten()`
**Mô tả:** Kích hoạt trạng thái Hoảng Sợ (Frightened Mode) cho bóng ma khi Pac-Man ăn viên sức mạnh (Energizer).
* **Hiệu ứng:** 
  * Ma thay đổi giao diện (chuyển sang màu xanh dương và nhấp nháy liên tục).
  * Tốc độ di chuyển giảm xuống đáng kể.
  * Tạm thời bị thay đổi thuật toán di chuyển (chuyển sang đi ngẫu nhiên).
  * Pac-Man có thể đuổi theo "ăn" ma để lấy điểm thưởng.

---

## 3. Vòng Lặp Trò Chơi (Game Loop) - `main.py`

### 🔹 `main_menu()`
**Mô tả:** Hiển thị giao diện màn hình chờ chính của trò chơi (Splash screen).
* **Chức năng:** Cho phép người chơi lựa chọn độ khó của AI (Easy/Hard) và tùy chỉnh số lượng Ghost xuất hiện trên bản đồ trước khi tiến vào ván đấu.

### 🔹 `game_loop()`
**Mô tả:** Vòng lặp vòng đời trò chơi của chế độ chơi Offline.
* **Chức năng:** Xử lý toàn bộ logic liên tục trong 1 giây (Frame by frame): Nhận tín hiệu điều khiển từ người chơi, cập nhật vị trí các thực thể, kiểm tra va chạm (ăn hạt, ăn ma, bị ma bắt), quản lý điểm số, gọi hệ thống âm thanh, và vẽ (render) hình ảnh lên màn hình.

### 🔹 `create_wall_surface()`
**Mô tả:** Khởi tạo giao diện đồ họa tĩnh cho mê cung.
* **Chức năng:** Vẽ các đường viền với độ trong suốt (alpha) theo nhiều lớp chồng lên nhau để tạo hiệu ứng tường phát sáng neon (Neon Glow Effect). Chức năng này chỉ chạy 1 lần lúc khởi tạo màn chơi, giúp tối ưu hóa FPS so với việc vẽ lại trên mỗi khung hình.

---

## 4. Mạng và Đa Người Chơi (Multiplayer) - `Multiplayer_Python/`

### 🔹 Class `Network` (`network.py`)
**Mô tả:** Đối tượng quản lý kết nối socket từ phía Client.
* **Chức năng:** Kết nối và duy trì đường truyền đến Server, liên tục gửi thông tin điều khiển (input bàn phím) của người chơi và nhận về dữ liệu trạng thái game mới nhất (GameState) đã được mã hoá bằng `pickle`.

### 🔹 `build_game_state()` (`server.py`)
**Mô tả:** Hàm đóng gói toàn bộ trạng thái đồng bộ của phòng chơi tại phía Server.
* **Chức năng:** Thu thập dữ liệu vị trí thực tế của tất cả người chơi (Pac-Man và Ghost), dữ liệu đường đi của AI, điểm số, hạt đậu còn lại trên bản đồ, các hiệu ứng âm thanh (event còi, tiếng ăn hạt)... thành một `Dictionary` hoàn chỉnh để đẩy về tất cả các Client đang kết nối nhằm tránh giật lag hay mất đồng bộ.
