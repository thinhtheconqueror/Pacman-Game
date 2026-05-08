# BÁO CÁO ĐỒ ÁN MÔN HỌC
**(Đồ án phát triển ứng dụng)**  
**Lớp:** IT003.Q21.CTTN

### SINH VIÊN THỰC HIỆN
**Mã sinh viên:** 25521787  
**Họ và tên:** Võ Quốc Thịnh

### TÊN ĐỀ TÀI: Game Pacman

---

## CÁC NỘI DUNG CẦN BÁO CÁO

### 1. Giới thiệu đồ án

**a. Mô tả chung về ứng dụng**

Dự án là một phiên bản mô phỏng trò chơi Pac-Man cổ điển, được xây dựng bằng ngôn ngữ Python và thư viện Pygame. Sau khi hoàn thành phần nền tảng điều khiển nhân vật và thuật toán tìm đường BFS cho Ghost ở tuần 2, trong tuần 3 nhóm tập trung hoàn thiện trải nghiệm chơi thực tế của chế độ Offline Mode, đồng thời bước đầu tích hợp khung ứng dụng tổng để chuẩn bị cho chế độ Multiplayer.

Các nội dung chính của tuần 3 gồm: hoàn thiện vòng lặp trạng thái game, bổ sung menu chọn chế độ chơi, cải thiện đồ họa theo phong cách arcade/neon, tích hợp âm thanh nhiều kênh, thêm hiệu ứng hạt và popup điểm số, xử lý trạng thái Frightened khi Pac-Man ăn Energizer, đồng thời xây dựng launcher trong `app.py` để người dùng có thể chọn Offline Mode, Host Multiplayer Server hoặc Join Multiplayer.

**b. Các cấu trúc dữ liệu, cơ chế và kỹ thuật đã sử dụng**

- **State Machine đơn giản cho vòng đời trò chơi**
  - **What:** Game được chia thành các trạng thái chính như Main Menu, In Game, Game Over, Win và quay lại Menu. Trong `main.py`, hàm `main_menu()` đảm nhiệm chọn độ khó và số lượng Ghost, còn `game_loop()` xử lý toàn bộ logic khi đang chơi.
  - **Why:** Việc tách trạng thái giúp chương trình dễ kiểm soát luồng chạy hơn. Người chơi có thể bắt đầu ván mới, thoát bằng phím `ESC`, quay lại menu hoặc reset game mà không làm rối logic xử lý trong cùng một vòng lặp.

- **Virtual Surface và Smooth Scaling**
  - **What:** Game được vẽ trước lên một `virtual_surface` có kích thước cố định theo cấu hình, sau đó dùng `pygame.transform.smoothscale()` để phóng to hoặc thu nhỏ vừa với màn hình thật.
  - **Why:** Cách làm này giúp toàn bộ tọa độ trong game vẫn ổn định theo lưới, không bị sai lệch khi chạy ở các độ phân giải khác nhau. Đồng thời game giữ được đúng tỉ lệ hiển thị và tránh tình trạng hình ảnh bị méo.

- **Pygame Mixer Channel cho âm thanh nhiều kênh**
  - **What:** Sử dụng `pygame.mixer.set_num_channels(8)` và phân tách các kênh âm thanh như `eat_channel`, `siren_channel`, `ghost_channel`. Các file âm thanh được dùng gồm `eating.mp3`, `eat-pill.mp3`, `eat-ghost.mp3`, `siren.mp3`.
  - **Why:** Trong game Pac-Man, nhiều âm thanh có thể xảy ra gần như cùng lúc: tiếng ăn hạt, tiếng còi nền, tiếng ăn Energizer, tiếng ăn Ghost. Nếu chỉ dùng một kênh phát âm thanh, hiệu ứng mới có thể ghi đè hiệu ứng cũ. Việc tách kênh giúp âm thanh rõ ràng, tự nhiên và không bị ngắt đột ngột.

- **Danh sách động cho Particle System và Floating Popup**
  - **What:** Trong `game_loop()`, hai danh sách `particles` và `popups` được dùng để lưu các hiệu ứng tạm thời. Mỗi phần tử particle chứa tọa độ, vận tốc, màu sắc, thời gian sống; mỗi popup chứa nội dung điểm, vị trí, thời gian hiển thị và màu chữ.
  - **Why:** Đây là cách đơn giản nhưng hiệu quả để tạo phản hồi thị giác khi Pac-Man ăn hạt, ăn Energizer hoặc ăn Ghost. Các hiệu ứng tự giảm vòng đời rồi bị xóa khỏi danh sách, giúp chương trình không giữ lại dữ liệu thừa.

- **Hàm sin và thời gian hệ thống cho animation**
  - **What:** Sử dụng `math.sin()` kết hợp `pygame.time.get_ticks()` để tạo các chuyển động lặp theo thời gian, ví dụ hiệu ứng nền synthwave, nhấp nháy vật phẩm hoặc dao động hình ảnh.
  - **Why:** Các chuyển động nhỏ làm màn hình bớt tĩnh, tạo cảm giác game đang chuyển động liên tục mà không cần thêm tài nguyên đồ họa phức tạp.

- **Frightened State cho Ghost**
  - **What:** Khi Pac-Man ăn Energizer, các Ghost gọi phương thức `frighten()`, thiết lập `frightened_timer`. Trong thời gian này Ghost đổi màu, nhấp nháy, di chuyển chậm hơn và có thể bị Pac-Man ăn.
  - **Why:** Đây là cơ chế quan trọng của Pac-Man gốc, giúp gameplay không chỉ là chạy trốn mà còn có nhịp phản công. Về mặt lập trình, trạng thái này cũng cho thấy cách quản lý hành vi đối tượng theo thời gian.

- **Socket, Thread và Pickle cho Multiplayer bước đầu**
  - **What:** Trong thư mục `Multiplayer_Python`, `server.py` dùng socket TCP, `threading` để xử lý nhiều client và `pickle` để đóng gói dữ liệu trạng thái game. `network.py` định nghĩa lớp `Network` cho client gửi input và nhận state từ server.
  - **Why:** Multiplayer cần một tiến trình trung tâm giữ trạng thái game thống nhất. Server chịu trách nhiệm cập nhật vị trí, điểm, Ghost, Pac-Man và gửi dữ liệu mới về các client. Cách này giúp tránh việc mỗi máy tự tính một trạng thái khác nhau.

### 2. Quá trình thực hiện

**Tuần 3: Hoàn thiện Offline Mode và tích hợp khung chạy ứng dụng**

- **Hoàn thiện menu và vòng lặp game**
  - Xây dựng `main_menu()` để hiển thị màn hình chờ, chọn độ khó Easy/Hard và chọn số lượng Ghost.
  - Xây dựng `game_loop()` để xử lý input, cập nhật Pac-Man, cập nhật Ghost, kiểm tra va chạm, kiểm tra thắng/thua và render toàn bộ màn chơi.
  - Bổ sung xử lý phím `ESC` để quay lại menu an toàn, đồng thời dừng âm thanh nền khi rời khỏi ván chơi.

- **Nâng cấp đồ họa**
  - Viết `create_wall_surface()` để vẽ tường bằng nhiều lớp đường thẳng có độ trong suốt khác nhau, tạo cảm giác phát sáng neon.
  - Viết `draw_synthwave_bg()` để tạo nền lưới chuyển động theo phong cách retro/synthwave.
  - Cải thiện hiển thị UI: điểm số, mạng còn lại, trạng thái thắng/thua và các thông tin trong màn hình menu.
  - Load sprite từ `spritesheet.png` thông qua `load_arcade_assets()` để tăng tính arcade cho Pac-Man và Ghost.

- **Tích hợp âm thanh**
  - Khởi tạo hệ thống âm thanh bằng `pygame.mixer.init()`.
  - Load các âm thanh chính: ăn hạt, ăn Energizer, ăn Ghost và siren nền.
  - Tách kênh phát âm thanh để tránh việc các hiệu ứng ghi đè lẫn nhau.
  - Dừng siren khi Game Over, khi chiến thắng, khi quay lại menu hoặc khi thoát game.

- **Bổ sung hiệu ứng phản hồi**
  - Khi ăn hạt thường, cộng 10 điểm, phát âm thanh ăn hạt, tạo particle nhỏ và popup `+10`.
  - Khi ăn Energizer, cộng 50 điểm, phát âm thanh đặc biệt, kích hoạt trạng thái Frightened cho Ghost, tạo particle và popup `+50`.
  - Khi ăn Ghost trong trạng thái Frightened, cộng 200 điểm, phát âm thanh ăn Ghost, tạo hiệu ứng mạnh hơn và thêm `hit_stop_frames` để tạo cảm giác va chạm rõ ràng.

- **Cải thiện hành vi Ghost**
  - Ghost tiếp tục sử dụng BFS để truy đuổi Pac-Man ở chế độ Hard.
  - Khi bị Frightened, Ghost chuyển sang di chuyển ngẫu nhiên và giảm tốc độ.
  - Sau khi bị Pac-Man ăn, Ghost có thể quay về vị trí xuất phát trước khi tham gia lại trò chơi.
  - Bổ sung xử lý tránh chồng vị trí giữa các Ghost thông qua tập hợp `occupied_positions`.

- **Tích hợp launcher trong `app.py`**
  - Tạo menu tổng cho ứng dụng với 3 lựa chọn: Offline Mode, Host Multiplayer Server và Join Multiplayer.
  - Tái sử dụng `game_loop()` và `main_menu()` của chế độ offline trong `app.py`.
  - Khi host multiplayer, chương trình tự chạy `Multiplayer_Python/server.py`, hiển thị IP máy chủ và cho phép người chơi tham gia vào phòng.
  - Khi join multiplayer, người chơi nhập IP server và chọn vai trò Pac-Man hoặc Ghost.

- **Xây dựng Multiplayer bước đầu**
  - `server.py` quản lý trạng thái tập trung của phòng chơi, danh sách Pac-Man, danh sách Ghost người chơi, AI Ghost và trạng thái bắt đầu game.
  - `client.py` nhận state từ server và render bản đồ, Pac-Man, Ghost, điểm số, màn hình chờ.
  - `network.py` đóng gói thao tác kết nối, gửi input và nhận dữ liệu phản hồi.
  - Server dùng thread riêng cho từng client để nhiều người chơi có thể kết nối cùng lúc.

### 3. Kết quả đạt được

- Hoàn thiện được chế độ Offline Mode với menu, gameplay, âm thanh, đồ họa, hiệu ứng điểm số và điều kiện thắng/thua.
- Ghost có thêm trạng thái Frightened, giúp gameplay giống Pac-Man gốc hơn và tạo thêm chiều sâu chiến thuật.
- Game có trải nghiệm nghe nhìn tốt hơn so với bản demo tuần 2: có nền động, tường neon, popup điểm, particle và âm thanh nhiều kênh.
- Ứng dụng có launcher tổng trong `app.py`, hỗ trợ chọn Offline Mode hoặc chuyển sang luồng Multiplayer.
- Xây dựng được nền tảng Multiplayer ban đầu bằng socket TCP: server giữ trạng thái game, client gửi input và nhận state để render.
- Mã nguồn được tổ chức rõ hơn theo các module: `main.py` cho offline, `app.py` cho launcher, `entities.py` cho thực thể, `algorithms.py` cho thuật toán, `Multiplayer_Python` cho phần mạng.

### 4. Khó khăn và hướng giải quyết

- **Đồng bộ âm thanh:** Ban đầu các âm thanh dễ bị ghi đè lẫn nhau. Hướng giải quyết là tách từng loại âm thanh quan trọng sang channel riêng.
- **Tỉ lệ màn hình:** Khi chạy fullscreen, nếu vẽ trực tiếp theo kích thước màn hình thật thì dễ lệch tọa độ lưới. Hướng giải quyết là dùng virtual surface rồi scale ra màn hình.
- **Quản lý nhiều hiệu ứng tạm thời:** Particle và popup nếu không xóa đúng lúc sẽ làm danh sách ngày càng lớn. Hướng giải quyết là mỗi hiệu ứng có `life/timer` và bị remove khi hết thời gian sống.
- **Đồng bộ multiplayer:** Khi nhiều client cùng gửi input, server cần là nơi quyết định trạng thái cuối cùng. Hướng giải quyết là đặt game state ở server và dùng lock để tránh lỗi khi nhiều thread cùng truy cập dữ liệu.

### 5. Tài liệu tham khảo

- Tài liệu Pygame Display và Surface: https://www.pygame.org/docs/ref/display.html
- Tài liệu Pygame Mixer: https://www.pygame.org/docs/ref/mixer.html
- Tài liệu Python Socket Programming: https://docs.python.org/3/library/socket.html
- Tài liệu Python Threading: https://docs.python.org/3/library/threading.html
- Giáo trình Cấu trúc dữ liệu và Giải thuật: nội dung về ma trận, hàng đợi, tập hợp, đồ thị và BFS.

### 6. Phụ lục 1: Giới thiệu demo kết quả

[Chèn link video demo Youtube của bạn vào đây]

### 7. Phụ lục 2: Docstring các hàm cốt lõi

- **Hàm `main_menu()` trong `main.py`:**

```python
"""
Displays the splash screen and difficulty selection menu.
Allows the player to choose game difficulty and number of ghosts
before entering the main game loop.
"""
```

- **Hàm `game_loop()` trong `main.py`:**

```python
"""
Runs the main offline Pac-Man gameplay loop.
Handles player input, entity updates, collision checks, scoring,
audio events, visual effects, win/lose states and rendering.
"""
```

- **Hàm `create_wall_surface()` trong `main.py`:**

```python
"""
Creates a static glowing surface for the map walls.
Draws wall connections with layered alpha lines to create
a neon glow effect while avoiding redrawing expensive wall
effects from scratch every frame.
"""
```

- **Hàm `draw_synthwave_bg()` trong `main.py`:**

```python
"""
Draws a moving synthwave grid background.
Uses time-based offsets to animate horizontal grid lines and
create a retro arcade visual style behind the map.
"""
```

- **Hàm `frighten()` trong `entities.py`:**

```python
"""
Activates frightened mode for a ghost.
During this state, the ghost becomes vulnerable, moves slower,
changes its visual appearance and can be eaten by Pac-Man.
"""
```

- **Lớp `Network` trong `Multiplayer_Python/network.py`:**

```python
"""
Client-side networking helper.
Connects to the game server, sends role selection and player input,
then receives the latest serialized game state from the server.
"""
```

- **Hàm `build_game_state()` trong `Multiplayer_Python/server.py`:**

```python
"""
Builds the authoritative game state dictionary on the server.
The state includes map data, Pac-Man players, Ghost players,
AI ghosts, score, room status and sound events for clients.
"""
```
