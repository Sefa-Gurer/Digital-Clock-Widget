from tkinter import *
from gui import Screen
import utils
import json
import os

class Play:
    def __init__(self):

        self.window_width = 420
        self.window_height = 220

        screen_horizontal_cell = 25
        screen_vertical_cell = 9
        self.screen_ratio = screen_horizontal_cell/screen_vertical_cell
        self.margin = 20

        self.old_digits_cells = [[],[],[],[]]

        # Ana pencereyi oluştur
        self.root = Tk()

        window_size = f"{self.window_width}x{self.window_height}"

        self.root.overrideredirect(True)

        # Pencere boyutunu ve şeffaflığını ayarla
        self.root.geometry(window_size)
        self.root.attributes('-alpha', 1)  # Pencereyi tam görünür yap
        self.root.wm_attributes('-transparentcolor', '#ab23ff')  # Bu rengi şeffaf yap

        # === EKLENEN: ayarları (konum + renk) config.json'dan yükle ===
        # Yazılabilir config %APPDATA%\DigitalClock altında tutulur; böylece
        # exe Startup klasörüne konsa bile config.json o klasörde durmaz
        # (yoksa Windows açılışta config dosyasını da açar).
        appdata = os.environ.get("APPDATA") or \
            os.path.dirname(os.path.abspath(__file__))
        config_dir = os.path.join(appdata, "DigitalClock")
        os.makedirs(config_dir, exist_ok=True)
        self.config_path = os.path.join(config_dir, "config.json")
        self.palette = ["lightsteelblue", "red", "orange", "yellow",
                        "lime green", "cyan", "white", "magenta"]
        config = self.load_config()

        # Renk: kayıtlı değer yoksa paletteki ilk renk kullanılır
        self.color = config.get("color", self.palette[0])
        if self.color not in self.palette:
            self.palette.insert(0, self.color)
        self.color_index = self.palette.index(self.color)

        # Boyut: temel ölçüyü sakla, kayıtlı scale ile orantılı ölçekle
        self.BASE_W = self.window_width
        self.BASE_H = self.window_height
        self.scale = config.get("scale", 1.0)
        self.window_width = int(self.BASE_W * self.scale)
        self.window_height = int(self.BASE_H * self.scale)

        # Konum: kayıtlı x/y varsa pencereyi oraya taşı, boyutu da uygula
        pos_x = config.get("x")
        pos_y = config.get("y")
        if pos_x is not None and pos_y is not None:
            self.root.geometry(
                f"{self.window_width}x{self.window_height}+{pos_x}+{pos_y}")
        else:
            self.root.geometry(f"{self.window_width}x{self.window_height}")

        # Düzenleme modu durum değişkenleri
        self.edit_mode = False
        self._press = None
        self._moved = False
        self._mode = None
        self._off_x = 0
        self._off_y = 0
        self._anchor = None  # boyutlandırmada sabit kalacak karşı köşe
        # === EKLENEN bölüm sonu ===

        # Canvas'ı oluştur
        self.canvas = Canvas(self.root, width=self.window_width, height=self.window_height, bg='#ab23ff', highlightthickness=0)
        self.canvas.pack()

        screen_size = self.find_screen_size()

        self.screen = Screen(self.canvas,
            square_corner_one=screen_size[0],
            square_corner_two=screen_size[1],
            horizontal_cell = screen_horizontal_cell,
            vertical_cell = screen_vertical_cell,
            square_color="red")

        # EKLENEN: saat ve dakika arasına iki nokta üst üste çiz
        self.draw_colon()

        # EKLENEN: düzenleme (taşıma/renk/kaydetme) olaylarını bağla
        self.setup_editing()

        self.run()

    def run(self):
        current_time = utils.get_current_time()
        digits = utils.divide_digits(current_time)
        digits_cells = utils.divide_cells(digits)

        if digits_cells != self.old_digits_cells:
            print("Saat değişti")

            add_item = utils.find_array_diff(digits_cells,self.old_digits_cells)
            delete_item = utils.find_array_diff(self.old_digits_cells,digits_cells)

            for i, value in enumerate(add_item, start=1):
                for j in value:
                    square_corner_one,square_corner_two = self.screen.digits[f"digit{i}"].cell[f"cell{j}"]
                    utils.draw_digit(self.canvas,square_corner_one,square_corner_two,self.color,tag=f"cell{i}{j}")

            for i, value in enumerate(delete_item, start=1):
                for j in value:
                    self.canvas.delete(f"cell{i}{j}")

        self.old_digits_cells = digits_cells
        # 1000 milisaniye (1 saniye) sonra tekrar run()'u çalıştır
        self.root.after(1000, self.run)

    def find_screen_size(self):
        if (self.window_height-(2*self.margin)) * self.screen_ratio <= (self.window_width-(2*self.margin)):
            screen_height = self.window_height-(2*self.margin)
            screen_width = screen_height * self.screen_ratio
        else:
            screen_width = self.window_width-(2*self.margin)
            screen_height = screen_width / self.screen_ratio

        corner_one = (self.window_width-screen_width)/2,(self.window_height-screen_height)/2
        corner_two = (self.window_width-corner_one[0]),(self.window_height-corner_one[1])

        return (corner_one,corner_two)

    # ================================================================
    #  EKLENEN BÖLÜM: konum taşıma, renk değiştirme ve kaydetme
    #  Düzenleme modu  : Ctrl tuşunu basılı tutup widget'a tıkla
    #    - Ctrl + sürükle  -> konumu taşı
    #    - Ctrl + tek tık  -> rengi değiştir
    #    - Ctrl + S        -> konum ve rengi config.json'a kaydet
    # ================================================================

    _EDIT_TEXT = "surukle=tasi  kose=boyut  tik=renk  Ctrl+S=kaydet"
    _DOT = 14   # köşe noktasının çapı (px)
    _HIT = 26   # köşeden boyutlandırma için yakalama alanı (px)

    def draw_colon(self):
        """Saat ve dakika arasına (digit5 alanına) iki nokta üst üste çizer.
        Projenin hücre mantığını kullanır: digit5 sütunu 1 hücre genişliğinde,
        iki nokta dikeyde 2-3 ve 6-7. hücrelere kare olarak yerleştirilir."""
        col = self.screen.digits["digit5"]
        left_x = col.corner_one[0]
        top_y = col.corner_one[1]
        cell = self.screen.horizontal_cell_size
        for v in (2, 6):  # üst nokta ve alt nokta
            utils.draw_digit(
                self.canvas,
                (left_x, top_y + cell * v),
                (left_x + cell, top_y + cell * (v + 1)),
                self.color,
                tag="colon")

    def load_config(self):
        """Kayıtlı ayarları %APPDATA%\\DigitalClock\\config.json'dan okur.
        Dosya yoksa boş döner; bu durumda koddaki varsayılanlar kullanılır."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, ValueError):
            return {}

    def save_config(self):
        """Mevcut konum ve rengi config.json'a yazar."""
        data = {
            "x": self.root.winfo_x(),
            "y": self.root.winfo_y(),
            "color": self.color,
            "scale": self.scale,
        }
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def setup_editing(self):
        """Düzenleme için klavye/fare olaylarını bağlar."""
        self.root.focus_force()
        self.root.bind("<Control-Button-1>", self.on_ctrl_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<KeyRelease-Control_L>", self.exit_edit_mode)
        self.root.bind("<KeyRelease-Control_R>", self.exit_edit_mode)
        self.root.bind("<Control-Key-s>", self.on_save)
        self.root.bind("<Control-Key-S>", self.on_save)
        # Ctrl basılıyken fare hareket edince köşe noktalarını göster,
        # Ctrl bırakılınca/pencereden çıkınca gizle
        self.root.bind("<Control-Motion>", self.on_ctrl_motion)
        self.root.bind("<Motion>", self.on_plain_motion)
        self.root.bind("<Leave>", self.on_leave)

    def enter_edit_mode(self):
        """Düzenleme modunu açar: tüm pencereyi opak yapan koyu arka plan +
        saatin 4 köşesine yeşil nokta çizer. Opak arka plan sayesinde şeffaf
        bölgeler de tıklanabilir olur (köşeler yakalanabilir, mod kapanmaz)."""
        if self.edit_mode:
            return
        self.edit_mode = True
        # Tüm pencereyi kaplayan koyu arka plan (rakamların altına gönderilir)
        self.canvas.create_rectangle(
            0, 0, self.window_width, self.window_height,
            fill="#1b1b1b", outline="", tags=("edit_ui", "edit_bg"))
        self.canvas.tag_lower("edit_bg")
        for (x, y) in self._corner_centers():
            r = self._DOT / 2
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill="#00ff00", outline="#007700", width=1,
                tags="edit_ui")
        self.canvas.create_text(
            self.window_width / 2, self._DOT + 2, text=self._EDIT_TEXT,
            fill="#00ff00", font=("Consolas", 7, "bold"),
            tags=("edit_ui", "edit_text"))

    def _corner_centers(self):
        """4 köşe noktasının merkez koordinatlarını döndürür."""
        m = self._DOT / 2 + 1
        W, H = self.window_width, self.window_height
        return [(m, m), (W - m, m), (m, H - m), (W - m, H - m)]

    def _on_corner(self, x, y):
        """Verilen widget koordinatı bir köşe yakalama alanında mı?"""
        W, H = self.window_width, self.window_height
        return (x <= self._HIT or x >= W - self._HIT) and \
               (y <= self._HIT or y >= H - self._HIT)

    def exit_edit_mode(self, event=None):
        """Düzenleme modunu kapatır ve göstergeyi siler."""
        self.edit_mode = False
        self._press = None
        self._anchor = None
        self.canvas.delete("edit_ui")

    def on_ctrl_press(self, event):
        """Ctrl + sol tık: köşedeyse boyutlandırma, değilse taşıma başlat."""
        self.root.focus_force()
        self.enter_edit_mode()
        self._press = (event.x_root, event.y_root)
        self._moved = False
        if self._on_corner(event.x, event.y):
            # Boyutlandırma: tutulan köşenin KARŞI köşesi sabit kalır (anchor).
            # Ölçek, anchor ile fare arasındaki uzaklık oranına göre değişir.
            self._mode = "resize"
            grabbed_left = event.x < self.window_width / 2
            grabbed_top = event.y < self.window_height / 2
            anchor_left = not grabbed_left
            anchor_top = not grabbed_top
            ax = self.root.winfo_x() + (0 if anchor_left else self.window_width)
            ay = self.root.winfo_y() + (0 if anchor_top else self.window_height)
            self._anchor = (ax, ay, anchor_left, anchor_top)
            dx, dy = event.x_root - ax, event.y_root - ay
            self._resize_d0 = max(8.0, (dx * dx + dy * dy) ** 0.5)
            self._resize_base = self.scale
        else:
            # Taşıma
            self._mode = "move"
            self._anchor = None
            self._off_x = event.x_root - self.root.winfo_x()
            self._off_y = event.y_root - self.root.winfo_y()

    def on_drag(self, event):
        """Düzenleme modunda sürükleme: köşeden boyutlandır, gövdeden taşı."""
        if not self.edit_mode or self._press is None:
            return
        if abs(event.x_root - self._press[0]) > 3 or \
           abs(event.y_root - self._press[1]) > 3:
            self._moved = True
        if self._mode == "resize":
            ax, ay = self._anchor[0], self._anchor[1]
            dx = event.x_root - ax
            dy = event.y_root - ay
            d1 = (dx * dx + dy * dy) ** 0.5
            self.apply_scale(self._resize_base * (d1 / self._resize_d0))
        else:
            new_x = event.x_root - self._off_x
            new_y = event.y_root - self._off_y
            self.root.geometry(
                f"{self.window_width}x{self.window_height}+{new_x}+{new_y}")

    def on_release(self, event):
        """Fare bırakıldığında: sürüklenmediyse rengi değiştir."""
        if not self.edit_mode or self._press is None:
            return
        if not self._moved and self._mode == "move":
            self.cycle_color()
        self._press = None
        self._mode = None
        self._anchor = None

    def cycle_color(self):
        """Palette'teki sıradaki renge geçer ve tüm hücreleri yeniden boyar."""
        self.color_index = (self.color_index + 1) % len(self.palette)
        self.color = self.palette[self.color_index]
        for item in self.canvas.find_all():
            if "edit_ui" in self.canvas.gettags(item):
                continue
            self.canvas.itemconfig(item, fill=self.color, outline=self.color)

    def on_ctrl_motion(self, event):
        """Ctrl basılıyken fare oynayınca köşe noktalarını göster."""
        self.enter_edit_mode()

    def on_plain_motion(self, event):
        """Ctrl bırakılınca köşe noktalarını gizle."""
        if self.edit_mode and not (event.state & 0x0004) and self._press is None:
            self.exit_edit_mode()

    def on_leave(self, event):
        """Pencereden çıkınca, sadece sürükleme yoksa ve Ctrl bırakılmışsa kapat."""
        if self._press is None and not (event.state & 0x0004):
            self.exit_edit_mode()

    def apply_scale(self, new_scale):
        """Widget'ı verilen ölçeğe göre yeniden boyutlandırır.
        Tüm geometri window_width/height'ten türediği için her şey orantılı
        büyür/küçülür; ekran ve rakamlar yeni boyuta göre yeniden çizilir."""
        new_scale = round(new_scale / 0.05) * 0.05  # titreşimi azaltmak için 0.05 adım
        new_scale = max(0.4, min(4.0, round(new_scale, 2)))
        if new_scale == self.scale:
            return
        self.scale = new_scale
        self.window_width = int(self.BASE_W * new_scale)
        self.window_height = int(self.BASE_H * new_scale)

        # Pencere ve canvas boyutunu güncelle. Boyutlandırmada karşı köşe
        # (anchor) sabit kalacak şekilde yeni sol-üst konumu hesaplanır.
        if self._anchor is not None:
            ax, ay, anchor_left, anchor_top = self._anchor
            x = ax if anchor_left else ax - self.window_width
            y = ay if anchor_top else ay - self.window_height
        else:
            x, y = self.root.winfo_x(), self.root.winfo_y()
        self.root.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")
        self.canvas.config(width=self.window_width, height=self.window_height)
        self.canvas.delete("all")

        # Ekran geometrisini yeni boyuta göre yeniden kur
        screen_size = self.find_screen_size()
        self.screen = Screen(self.canvas,
            square_corner_one=screen_size[0],
            square_corner_two=screen_size[1],
            horizontal_cell=25,
            vertical_cell=9,
            square_color="red")

        # Rakamları anında yeniden çiz (run döngüsünü beklemeden)
        cells = utils.divide_cells(utils.divide_digits(utils.get_current_time()))
        for i, value in enumerate(cells, start=1):
            for j in value:
                c1, c2 = self.screen.digits[f"digit{i}"].cell[f"cell{j}"]
                utils.draw_digit(self.canvas, c1, c2, self.color, tag=f"cell{i}{j}")
        self.old_digits_cells = cells

        # İki nokta ve (açıksa) düzenleme göstergesini yeniden çiz
        self.draw_colon()
        if self.edit_mode:
            self.edit_mode = False
            self.enter_edit_mode()

    def on_save(self, event=None):
        """Ctrl + S: konum, renk ve boyutu kaydeder, kısa bir onay gösterir."""
        self.save_config()
        if self.edit_mode:
            self.canvas.itemconfig(
                "edit_text", text="KAYDEDILDI", fill="#ffff00")
            self.root.after(900, self._restore_edit_text)

    def _restore_edit_text(self):
        if self.edit_mode:
            self.canvas.itemconfig(
                "edit_text", text=self._EDIT_TEXT, fill="#00ff00")

    # ================================================================
    #  EKLENEN bölüm sonu
    # ================================================================

if __name__ == '__main__':
    play = Play()
    # Ana pencereyi başlat
    play.root.mainloop()