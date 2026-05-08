# BÁO CÁO ĐỒ ÁN MÔN HỌC
**(Đồ án phát triển ứng dụng)**
**Lớp:** IT003.Q21.CTTN  

### SINH VIÊN THỰC HIỆN
**Mã sinh viên:** 25521787  
**Họ và tên:** Võ Quốc Thịnh  

### TÊN ĐỀ TÀI: Game Pacman  

---

## CÁC NỘI DUNG CẦN BÁO CÁO:

### 1. Giới thiệu đồ án:
**a. Mô tả chung về ứng dụng:**
Dự án là một phiên bản mô phỏng (clone) của tựa game arcade kinh điển Pac-Man, được xây dựng bằng Python và thư viện Pygame. Trong tuần 2, trọng tâm phát triển là việc tích hợp **trí tuệ nhân tạo (AI) cho các bóng ma (Ghost)** sử dụng giải thuật **Tìm kiếm theo chiều rộng (BFS)** để truy đuổi Pac-Man trên lưới mê cung. Script `demo_tuan2.py` được xây dựng nhằm minh hoạ thuần tuý cơ chế AI tìm đường — bỏ qua menu và âm thanh — chỉ tập trung vào việc 4 Ghost dùng BFS ở chế độ Hard để bám đuổi người chơi.

**b. Các CTDL và giải thuật đã được sử dụng: (cần làm rõ các câu hỏi: what, why)**

- **Mảng 2 chiều (2D List / Matrix):**
  - **What:** Ma trận lưới `grid_matrix` kích thước 24×24, mỗi phần tử là một ký tự (`'1'` = tường, `'0'` = hạt (dot), `'P'` = Pac-Man, `'E'` = Ghost, `' '` = ô trống). Được parse từ mảng chuỗi `GAME_MAP` qua hàm `load_map_matrix()` (dòng 46 `demo_tuan2.py`).
  - **Why:** Cho phép truy xuất trạng thái bất kỳ ô nào với thời gian O(1) thông qua chỉ số `grid[row][col]`. Ma trận này đóng vai trò là **đồ thị không trọng số (unweighted graph)** — mỗi ô là một đỉnh, các ô kề nhau (trên/dưới/trái/phải) không phải tường là các cạnh — làm nền tảng cho thuật toán BFS hoạt động.

- **Hàng đợi (Queue / `collections.deque`):**
  - **What:** Cấu trúc dữ liệu hoạt động theo nguyên tắc **FIFO (First-In-First-Out)**, được khai báo trong hàm `bfs_shortest_path()` tại `algorithms.py` dưới dạng `queue = collections.deque([start])`. Dùng để lưu trữ các đỉnh (tọa độ lưới) đang chờ được duyệt.
  - **Why:** Hàng đợi đảm bảo thuật toán BFS duyệt các ô theo **từng cấp độ (level-order)** — tất cả các ô cách `start` đúng k bước được duyệt xong trước khi duyệt các ô cách k+1 bước. Thao tác `popleft()` và `append()` trên `deque` đều có thời gian O(1), giúp BFS hoạt động hiệu quả.

- **Từ điển (Dictionary / `parent_map`):**
  - **What:** Dictionary `parent_map = {start: None}` dùng để lưu vết đường đi: `parent_map[neighbor] = current` ghi nhận rằng `current` là ô cha dẫn đến `neighbor`. Đồng thời đóng vai trò tập **visited** — một ô đã có trong `parent_map` thì không được duyệt lại.
  - **Why:** Sau khi BFS tìm tới đích `target`, hàm dùng vòng lặp `while curr != start` để truy ngược từ đích về nguồn qua `parent_map`, xây dựng mảng `path[]`, sau đó trả về `path[0]` — **bước đi tiếp theo ngay lập tức** mà Ghost cần thực hiện. Việc dùng Dictionary thay vì 2 cấu trúc riêng biệt (visited + path) giúp tiết kiệm bộ nhớ và đơn giản hoá code.

- **Tập hợp (Set / `occupied_positions`):**
  - **What:** Tập hợp chứa toạ độ các Ghost khác, được truyền vào `get_valid_neighbors()` để loại bỏ các ô đã bị Ghost khác chiếm.
  - **Why:** Khi BFS mở rộng đỉnh, hàm `get_valid_neighbors()` kiểm tra `(nr, nc) not in occupied_positions` trên Set có thời gian trung bình O(1), ngăn nhiều Ghost chồng lên cùng một ô.

- **Giải thuật Tìm kiếm theo chiều rộng (Breadth-First Search - BFS):**
  - **What:** Thuật toán duyệt đồ thị lưới trong hàm `bfs_shortest_path(start, target, grid)` tại `algorithms.py`. Bắt đầu từ vị trí Ghost, BFS lần lượt: (1) lấy đỉnh đầu hàng đợi (`popleft`), (2) kiểm tra có phải đích không, (3) thêm tất cả đỉnh kề chưa duyệt vào hàng đợi, (4) lặp lại cho đến khi tìm thấy đích hoặc hết đỉnh. Trong `demo_tuan2.py`, tất cả 4 Ghost đều chạy BFS ở chế độ Hard (dòng 72: `is_hard_mode=True`).
  - **Why:** Trong mê cung Pac-Man, mọi bước di chuyển đều có chi phí bằng 1 (đồ thị không trọng số). BFS **đảm bảo** tìm được đường đi ngắn nhất, giúp Ghost luôn chọn hướng tối ưu nhất để tiếp cận Pac-Man.
  - **Complexity:** Thời gian O(V + E) với V = số ô lưới, E = số cạnh hợp lệ. Không gian O(V) cho `parent_map` và `queue`.

- **Giải thuật Bước ngẫu nhiên (Random Walk Algorithm):**
  - **What:** Hàm `random_walk_algorithm(start, grid)` trong `algorithms.py`. Lấy danh sách ô kề hợp lệ qua `get_valid_neighbors()`, rồi dùng `random.choice(neighbors)` chọn ngẫu nhiên một ô để di chuyển đến.
  - **Why:** Được sử dụng làm **fallback** khi BFS không tìm được đường đến đích (mục tiêu bị bao kín hoàn toàn hoặc không thể tiếp cận). Trong `demo_tuan2.py`, Random Walk chỉ đóng vai trò dự phòng cho BFS.

### 2. Quá trình thực hiện
**a. Tuần 2: Xây dựng AI tìm đường (BFS) và script demo minh hoạ:**

- **Cài đặt module `algorithms.py` (được import bởi `demo_tuan2.py`):** Triển khai 3 hàm cốt lõi:
  - `get_valid_neighbors(pos, grid, occupied_positions)` — Tìm tất cả ô kề đi được (không phải tường `'1'`, không bị Ghost khác chiếm, có xử lý Tunnel Wrap Around khi `nc < 0` hoặc `nc >= len(grid[0])`).
  - `bfs_shortest_path(start, target, grid, occupied_positions)` — BFS tìm đường ngắn nhất, trả về bước đi tiếp theo.
  - `random_walk_algorithm(start, grid, occupied_positions)` — Chọn ngẫu nhiên ô kề hợp lệ, dùng làm fallback.

- **Thiết kế Entity (OOP) trong `entities.py` (được import bởi `demo_tuan2.py`):**
  - Lớp `Pacman` — Xử lý input di chuyển (queued direction), kiểm tra ăn hạt `check_eat_dot()`, animation há/ngậm miệng.
  - Lớp `Ghost` — Chứa logic AI trong phương thức `update()`: xác định `occupied_positions`, gọi `bfs_shortest_path()` để tính bước đi tiếp theo.

- **Xây dựng script `demo_tuan2.py`:**
  - **Khởi tạo (dòng 39-79):** Init Pygame fullscreen, load lưới `grid_matrix`, duyệt lưới để spawn Pacman (ô `'P'`) và 4 Ghost (ô `'E'`) với `is_hard_mode=True`.
  - **Game Loop (dòng 83-141):** Vòng lặp chính xử lý:
    1. **Input:** Bắt phím mũi tên/WASD để điều khiển Pac-Man, phím Q để thoát.
    2. **Update Pacman:** Gọi `pacman.update(grid_matrix)` di chuyển theo hướng đã chọn, `pacman.check_eat_dot(grid_matrix)` kiểm tra ăn hạt.
    3. **Update Ghost AI:** Gọi `ghost.update(pacman, grid_matrix, ghosts)` cho từng Ghost — bên trong sẽ chạy BFS tìm đường ngắn nhất đến Pac-Man. Kiểm tra va chạm Ghost-Pacman → nếu trùng toạ độ thì Game Over.
    4. **Render:** Vẽ lưới đơn giản (`draw_grid`: tường = `pygame.draw.rect` màu xanh, hạt = `pygame.draw.circle`), vẽ Pacman và Ghost, hiển thị overlay text (Score, chế độ AI, phím tắt).
    5. **Scaling:** Scale `virtual_surface` (600×650) lên kích thước màn hình thực tế, căn giữa.
  - **Hàm `draw_grid` (dòng 17-33):** Render lưới đơn giản — tường vẽ bằng `pygame.draw.rect` màu BLUE viền BLACK, hạt vẽ bằng `pygame.draw.circle` màu hồng nhạt.

### 3. Kết quả đạt được
- Tích hợp thành công **thuật toán BFS** giúp 4 Ghost bám đuổi Pac-Man theo đường đi ngắn nhất ở chế độ Hard.
- Script `demo_tuan2.py` hoạt động độc lập, minh hoạ rõ ràng cơ chế AI tìm đường mà không bị phân tán bởi menu hay âm thanh.
- Cơ chế **tránh va chạm giữa các Ghost** hoạt động chính xác nhờ `occupied_positions` truyền vào BFS.
- Hệ thống phát hiện Game Over khi Ghost bắt được Pac-Man (trùng toạ độ lưới).

### 4. Tài liệu tham khảo
- Giáo trình Cấu trúc dữ liệu và Giải thuật (Nội dung: Đồ thị, BFS, Hàng đợi, Từ điển).
- Tài liệu lập trình thư viện Pygame (`pygame.display`, `pygame.draw`, `pygame.event`).
- Tài liệu Python `collections.deque`: [https://docs.python.org/3/library/collections.html#collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)

### 5. Phụ lục 1: Giới thiệu (demo) kết quả
[Chèn link video demo Youtube của bạn vào đây]

### 6. Phụ lục 2: Docstring các hàm trong demo

- **Hàm `main` (trong `demo_tuan2.py`):**
```python
"""
Week 2 AI pathfinding demo script.

Bypasses main menu and audio system for a pure algorithmic demonstration.
Focuses entirely on BFS-based ghost tracking in Hard Mode.

Flow:
1. Load and parse 2D grid matrix from map_data.
2. Spawn Pacman and 4 Ghosts (all Hard Mode / BFS).
3. Game loop: Handle input → Update Pacman → Update Ghost AI (BFS) → Render.
"""
```

- **Hàm `draw_grid` (trong `demo_tuan2.py`):**
```python
"""
Simplified grid rendering for demo purposes.

Draws walls as filled blue rectangles with black borders,
and dots as small pink circles at cell centers.
"""
```

- **Hàm `bfs_shortest_path` (trong `algorithms.py`, được gọi bởi Ghost AI):**
```python
"""
HARD DIFFICULTY AI (Breadth-First Search):
Logic: Level-order traversal to find the shortest path in an unweighted graph.

Guarantees the absolute shortest path to the target (Pacman) by exploring
all possible paths level-by-level using a Queue.

Data Structures: 
- Queue (collections.deque): For O(1) enqueue/dequeue operations.
- Dictionary (parent_map): To track visited nodes and reconstruct the path.

Args:
    start (tuple): The starting (row, col) position.
    target (tuple): The target (row, col) position (usually Pacman).
    grid (list[list[str]]): The 2D grid matrix.
    occupied_positions (set, optional): Positions of other ghosts.
    
Returns:
    tuple: The immediate next (row, col) position on the shortest path.
    
Complexity:
    Time: O(V + E) where V is the number of grid cells and E is the number of valid moves.
    Space: O(V) to store the visited nodes in the parent_map and queue.
"""
```

- **Hàm `random_walk_algorithm` (trong `algorithms.py`, dùng làm fallback):**
```python
"""
EASY DIFFICULTY AI / BFS FALLBACK:
Logic: Random selection of valid neighbors.

This algorithm picks a random valid direction at each step.
In demo_tuan2.py, it only activates as fallback when BFS
cannot find a path to the target (target fully enclosed).

Args:
    start (tuple): The current (row, col) position of the ghost.
    grid (list[list[str]]): The 2D grid matrix.
    occupied_positions (set, optional): Positions of other ghosts.
    
Returns:
    tuple: The next (row, col) position to move to.
    
Complexity:
    Time: O(1)
"""
```

- **Hàm `get_valid_neighbors` (trong `algorithms.py`, hàm phụ trợ cho BFS):**
```python
"""
Finds all navigable adjacent cells (Up, Down, Left, Right) from a given position.

A cell is considered navigable if it is within grid boundaries, not a wall ('1'),
and not currently occupied by another entity. Includes Tunnel Wrap Around logic.

Args:
    pos (tuple): The current (row, col) position.
    grid (list[list[str]]): The 2D grid matrix.
    occupied_positions (set, optional): Positions of other ghosts to avoid collision.
    
Returns:
    list[tuple]: A list of navigable (row, col) neighbor positions.
    
Complexity:
    Time: O(1) - Constant time as it only checks 4 directions.
"""
```
