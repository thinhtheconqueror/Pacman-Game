# BÁO CÁO TỔNG KẾT ĐỒ ÁN MÔN HỌC
**(Đồ án phát triển ứng dụng)**

**TÊN ĐỀ TÀI:** Phát triển Game Pac-Man (Tích hợp AI và Multiplayer)
**Giảng viên hướng dẫn:** Nguyễn Thanh Sơn
**Sinh viên thực hiện:** Võ Quốc Thịnh (25521787)
**Lớp:** IT003.Q21.CTTN

---

## 1. Giới thiệu tổng quan đồ án
Dự án là một phiên bản phát triển toàn diện mô phỏng (clone) tựa game arcade kinh điển **Pac-Man**, được xây dựng hoàn toàn bằng ngôn ngữ Python cùng thư viện đồ hoạ Pygame. 

Mục tiêu của dự án không chỉ dừng lại ở việc tái hiện lại lối chơi gốc mà còn áp dụng sâu rộng các **Cấu trúc dữ liệu và Giải thuật** (như BFS, Đồ thị, Hàng đợi), cũng như phát triển các kỹ thuật lập trình nâng cao (hệ thống State Machine, xử lý âm thanh đa kênh, lập trình mạng Socket TCP/Threading để hỗ trợ Multiplayer).

Quá trình thực hiện dự án được chia làm 3 giai đoạn (3 tuần), đi từ xây dựng nền tảng vật lý 2D, tích hợp AI thông minh, đến hoàn thiện hiệu ứng nghe-nhìn và kiến trúc đa người chơi.

---

## 2. Quá trình phát triển và Các tính năng chính

### Giai đoạn 1: Xây dựng nền tảng đồ họa và cơ chế di chuyển (Tuần 1)
*   **Thiết lập môi trường:** Khởi tạo Game Loop cơ bản với Pygame.
*   **Mô hình hóa bản đồ:** Sử dụng **Mảng 2 chiều (2D Array)** để biểu diễn lưới mê cung.
*   **Cơ chế di chuyển và va chạm:** Tọa độ của Pac-Man được ánh xạ trực tiếp lên ma trận lưới. Nhờ đó, việc kiểm tra va chạm với tường và các vật thể (hạt đậu) diễn ra với độ phức tạp **O(1)**, tối ưu hóa đáng kể hiệu suất trò chơi.

### Giai đoạn 2: Tích hợp Trí tuệ nhân tạo (AI) cho Ghost (Tuần 2)
*   **AI bám đuổi thông minh:** Cài đặt giải thuật **Tìm kiếm theo chiều rộng (BFS)** để các bóng ma (Ghost) có khả năng tính toán đường đi ngắn nhất bám đuổi Pac-Man (Hard Mode).
*   **Hệ thống phòng tránh va chạm:** Sử dụng cấu trúc **Tập hợp (Set)** để lưu trữ vị trí hiện tại của các Ghost, giúp chúng tự động né tránh và không đi đè lên nhau.
*   **Cơ chế dự phòng:** Bổ sung thuật toán **Random Walk** làm giải pháp fallback khi BFS không thể tìm được đường (ví dụ: Pac-Man bị bao vây kín).
*   **Thiết kế Hướng đối tượng (OOP):** Chia tách rõ ràng cấu trúc code thành các thực thể độc lập (`Pacman`, `Ghost`) để dễ quản lý.

### Giai đoạn 3: Hoàn thiện trải nghiệm (Đồ họa, Âm thanh) và Multiplayer (Tuần 3)
*   **Luồng trò chơi (State Machine):** Xây dựng hoàn chỉnh các màn hình UI: *Main Menu (chọn độ khó, số lượng ma), In-game, Game Over, và Win*. 
*   **Cơ chế Frightened (Hoảng sợ):** Thêm tính năng ăn viên sức mạnh (Energizer). Khi đó Ghost sẽ đổi màu, chậm lại, di chuyển ngẫu nhiên và Pac-Man có thể "ăn" Ghost để lấy điểm thưởng.
*   **Nâng cấp Hiệu ứng Nghe - Nhìn:**
    *   **Thị giác:** Cải thiện đồ hoạ theo phong cách Retro/Neon Synthwave. Tường phát sáng (neon glow), nền lưới chuyển động, tích hợp hệ thống hạt (Particle System) và số điểm nổi (Floating Popup) khi ăn hạt/ghost. Sử dụng *Virtual Surface* để chống méo hình khi scale màn hình.
    *   **Thính giác:** Tích hợp hệ thống âm thanh **Đa kênh (Multi-channel)** (`pygame.mixer` 8 kênh) để các âm thanh như tiếng ăn hạt, còi nền, ăn Ghost được phát ra đồng thời mà không bị tắt hay đè lên nhau.
*   **Kiến trúc Đa người chơi (Multiplayer):** 
    *   Thiết kế hệ thống **Client - Server** qua thư viện `socket` và `threading`. Server chịu trách nhiệm lưu giữ trạng thái chung, Client gửi input và nhận trạng thái về để render.
    *   Tích hợp Launcher tổng trong `app.py` cho phép người chơi dễ dàng điều hướng giữa: Chơi Offline, Host Server, hoặc Join vào phòng chơi mạng.

---

## 3. Các Cấu trúc dữ liệu và Giải thuật cốt lõi đã áp dụng

Để game hoạt động mượt mà và thông minh, dự án đã áp dụng thực tiễn các kiến thức môn học:
1.  **Mảng 2D (Matrix):** Đóng vai trò là đồ thị không trọng số của bản đồ, giúp kiểm tra va chạm cực nhanh **O(1)**.
2.  **Hàng đợi (Queue - `collections.deque`):** Sử dụng cho giải thuật BFS giúp duyệt các đỉnh kề theo từng cấp độ với thao tác thêm/xóa O(1).
3.  **Từ điển (Dictionary) & Tập hợp (Set):** 
    *   Dictionary (`parent_map`) dùng để đánh dấu điểm đã duyệt và lưu vết đường đi nhằm truy xuất lại hướng di chuyển tối ưu cho AI.
    *   Set (`occupied_positions`) cho phép dò tìm va chạm giữa các Ghost trong thời gian O(1).
4.  **Giải thuật Đồ thị (BFS):** Giúp 4 Ghost bám đuổi Pac-Man bằng đường đi ngắn nhất, tạo độ khó cao cho game.
5.  **Multi-threading (Đa luồng):** Ứng dụng phía Server để phục vụ nhiều kết nối Socket từ các Client cùng lúc mà không làm gián đoạn trò chơi.

---

## 4. Kết quả đạt được của dự án

*   **Về mặt Sản phẩm:** Hoàn thiện một tựa game Pac-Man có thể chơi được với đầy đủ các quy tắc gốc, đồ hoạ đẹp mắt, âm thanh sống động, hiệu suất khung hình cao (nhờ các thuật toán tối ưu).
*   **Về mặt Tính năng mở rộng:** Trò chơi có độ thử thách cao nhờ AI tìm đường BFS. Đặc biệt, game không chỉ giới hạn ở việc chơi đơn trên một máy mà đã có nền tảng mạng kết nối đa thiết bị (Multiplayer LAN/Internet).
*   **Về mặt Kỹ thuật:** Thể hiện được khả năng tổ chức mã nguồn tốt (chia tách các Module `main.py`, `app.py`, `entities.py`, `algorithms.py`, `network.py`), hiểu và áp dụng chính xác các cấu trúc dữ liệu, giải thuật vào các tình huống thực tế của việc phát triển phần mềm và game.
