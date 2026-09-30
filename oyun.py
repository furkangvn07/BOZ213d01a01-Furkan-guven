"""
Ders: Nesne Tabanlı Programlama (OOP)
Proje: Zindan Hazine Avcısı (Tkinter Grafik Arayüzlü)
Özellikler: Kalıtım, Kapsülleme, Durum Yönetimi, Butonlar ve Grafik Arayüz
"""

import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# ==========================================
# 1. OOP MANTIĞI: VERİ VE OYUN VARLIKLARI
# ==========================================


class Varlik:
    """Temel sınıf: Kalıtım (Inheritance) ve Kapsülleme örneği."""

    def __init__(self, isim: str, can: int = 100):
        self.isim = isim
        self._can = can  # Kapsülleme (Encapsulation)
        self.maks_can = can

    @property
    def can(self) -> int:
        return self._can

    @can.setter
    def can(self, deger: int):
        # Can 0 ile maksimum can arasında sınırlanır
        self._can = max(0, min(self.maks_can, deger))

    def hayatta_mi(self) -> bool:
        return self._can > 0


class Oyuncu(Varlik):
    """Varlik sınıfından türetilen Oyuncu sınıfı."""

    def __init__(self, isim: str):
        super().__init__(isim, can=100)
        self.skor = 0
        self.iksir_sayisi = 1

    def hasar_al(self, miktar: int):
        self.can -= miktar

    def iksir_kullan(self) -> bool:
        if self.iksir_sayisi > 0 and self.can < self.maks_can:
            self.iksir_sayisi -= 1
            self.can += 30
            return True
        return False


class Kapi:
    """Odaları ve kapı arkasındaki olayları yöneten sınıf."""

    def __init__(self, kapi_no: int):
        self.kapi_no = kapi_no

    def kapiyi_ac(self, oyuncu: Oyuncu, pencere_referans=None) -> str:
        """Kapının arkasındaki rastgele olayı belirler ve oyuncuyu etkiler."""
        olay = random.choice(["hazine", "tuzak", "bilmece"])

        if olay == "hazine":
            puan = random.randint(25, 50)
            oyuncu.skor += puan
            oyuncu.iksir_sayisi += 1
            return (
                f"✨ HAZİNE BULDUN!\n"
                f"Muazzam bir sandık açtın. +{puan} Puan ve 1 Can İksiri kazandın!"
            )

        elif olay == "tuzak":
            hasar = random.randint(15, 30)
            oyuncu.hasar_al(hasar)
            return (
                f"💥 ZİNDAN TUZAĞI!\n"
                f"Yerden fırlayan oklar sana isabet etti: {hasar} Hasar aldın!"
            )

        elif olay == "bilmece":
            gizli_sayi = random.randint(1, 5)
            # Grafik arayüzü üzerinden kullanıcıdan sayı isteme
            tahmin = simpledialog.askinteger(
                "Muhafızın Bilmecesi",
                "🧙 Muhafız: 'Geçmek için aklımdaki sayıyı bil (1 ile 5 arası)!'",
                parent=pencere_referans,
                minvalue=1,
                maxvalue=5,
            )

            if tahmin is not None and tahmin == gizli_sayi:
                oyuncu.skor += 40
                return f"🎉 BİLMECYİ BİLDİN!\nMuhafızın sayısı {gizli_sayi} idi. Geçiş izni ve +40 Puan aldın!"
            else:
                oyuncu.hasar_al(20)
                return f"❌ YANLIŞ TAHMİN!\nDoğru sayı {gizli_sayi} idi. Muhafız sana saldırdı! (-20 Can)"


# ==========================================
# 2. GRAFİK ARAYÜZ (GUI) VE OYUN MOTORU
# ==========================================


class ZindanOyunuGUI:
    """Tüm arayüzü ve oyun döngüsünü kontrol eden ana sınıf."""

    def __init__(self, master):
        self.master = master
        self.master.title("🏰 Zindan Hazine Avcısı - OOP Oyunu")
        self.master.geometry("650x580")
        self.master.resizable(False, False)
        self.master.config(bg="#1e1e2e")

        self.tur = 1
        self.hedef_tur = 5

        # Başlangıçta oyuncu oluştur
        self.oyuncu = None
        self._baslangic_ekrani()

    def _baslangic_ekrani(self):
        """Kullanıcıdan isim alma ekranı."""
        for widget in self.master.winfo_children():
            widget.destroy()

        baslik = tk.Label(
            self.master,
            text="🏰 ZİNDAN HAZİNE AVCISI 🏰",
            font=("Arial", 20, "bold"),
            fg="#f38ba8",
            bg="#1e1e2e",
        )
        baslik.pack(pady=40)

        aciklama = tk.Label(
            self.master,
            text="Zindandan kaçmak için 5 odayı başarıyla geçmelisin!\nLütfen kahramanının adını gir:",
            font=("Arial", 12),
            fg="#cdd6f4",
            bg="#1e1e2e",
        )
        aciklama.pack(pady=10)

        self.isim_kutusu = tk.Entry(
            self.master, font=("Arial", 14), justify="center"
        )
        self.isim_kutusu.insert(0, "Gezgin")
        self.isim_kutusu.pack(pady=15, ipady=4)
        self.isim_kutusu.focus()

        basla_butonu = tk.Button(
            self.master,
            text="Maceraya Başla ⚔️",
            font=("Arial", 12, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            padx=20,
            pady=8,
            command=self._oyunu_kur,
        )
        basla_butonu.pack(pady=20)

    def _oyunu_kur(self):
        isim = self.isim_kutusu.get().strip() or "Bilinmeyen Savaşçı"
        self.oyuncu = Oyuncu(isim)
        self.tur = 1
        self._ana_oyun_ekrani()

    def _ana_oyun_ekrani(self):
        """Kartlar, butonlar ve canlı can paneli."""
        for widget in self.master.winfo_children():
            widget.destroy()

        # Üst Panel (Durum Barı)
        durum_cercevesi = tk.Frame(self.master, bg="#313244", pady=10)
        durum_cercevesi.pack(fill="x", padx=15, pady=10)

        self.lbl_oyuncu = tk.Label(
            durum_cercevesi,
            text=f"👤 {self.oyuncu.isim}",
            font=("Arial", 11, "bold"),
            fg="#cdd6f4",
            bg="#313244",
        )
        self.lbl_oyuncu.grid(row=0, column=0, padx=15)

        self.lbl_tur = tk.Label(
            durum_cercevesi,
            text=f"📍 Oda: {self.tur}/{self.hedef_tur}",
            font=("Arial", 11, "bold"),
            fg="#fab387",
            bg="#313244",
        )
        self.lbl_tur.grid(row=0, column=1, padx=15)

        self.lbl_can = tk.Label(
            durum_cercevesi,
            text=f"❤️ Can: {self.oyuncu.can}/100",
            font=("Arial", 11, "bold"),
            fg="#f38ba8",
            bg="#313244",
        )
        self.lbl_can.grid(row=0, column=2, padx=15)

        self.lbl_skor = tk.Label(
            durum_cercevesi,
            text=f"⭐ Skor: {self.oyuncu.skor}",
            font=("Arial", 11, "bold"),
            fg="#f9e2af",
            bg="#313244",
        )
        self.lbl_skor.grid(row=0, column=3, padx=15)

        # Olay Bildirim Kutusu (Hikaye Paneli)
        self.lbl_olay = tk.Label(
            self.master,
            text="Önünde 3 adet kapı belirdi. Birini seçerek ilerle!",
            font=("Arial", 12, "italic"),
            fg="#cdd6f4",
            bg="#181825",
            wraplength=550,
            height=4,
            relief="ridge",
            bd=2,
        )
        self.lbl_olay.pack(fill="x", padx=25, pady=15)

        # Kapı Seçim Alanı (Görsel Butonlar)
        kapi_cercevesi = tk.Frame(self.master, bg="#1e1e2e")
        kapi_cercevesi.pack(pady=10)

        for i in range(1, 4):
            btn_kapi = tk.Button(
                kapi_cercevesi,
                text=f"🚪\nKAPI {i}",
                font=("Arial", 14, "bold"),
                bg="#89b4fa",
                fg="#11111b",
                width=8,
                height=4,
                cursor="hand2",
                command=lambda k=i: self._kapi_sec(k),
            )
            btn_kapi.pack(side="left", padx=15)

        # Alt Araç Çubuğu (İksir ve Çıkış)
        alt_panel = tk.Frame(self.master, bg="#1e1e2e")
        alt_panel.pack(pady=20)

        self.btn_iksir = tk.Button(
            alt_panel,
            text=f"🧪 İksir Kullan ({self.oyuncu.iksir_sayisi})",
            font=("Arial", 11, "bold"),
            bg="#eba0ac",
            fg="#11111b",
            padx=10,
            command=self._iksir_bas,
        )
        self.btn_iksir.pack(side="left", padx=10)

    def _kapi_sec(self, kapi_no: int):
        kapi = Kapi(kapi_no)
        sonuc_mesaji = kapi.kapiyi_ac(self.oyuncu, self.master)

        self.lbl_olay.config(text=sonuc_mesaji)
        self.tur += 1

        self._arayuz_guncelle()
        self._durum_kontrol()

    def _iksir_bas(self):
        if self.oyuncu.iksir_kullan():
            self.lbl_olay.config(
                text="🧪 Bir can iksiri içtin! +30 Can yenilendi."
            )
        else:
            self.lbl_olay.config(
                text="❌ İksirin yok veya canın zaten tamamen dolu!"
            )
        self._arayuz_guncelle()

    def _arayuz_guncelle(self):
        self.lbl_can.config(text=f"❤️ Can: {self.oyuncu.can}/100")
        self.lbl_skor.config(text=f"⭐ Skor: {self.oyuncu.skor}")
        self.lbl_tur.config(
            text=f"📍 Oda: {min(self.tur, self.hedef_tur)}/{self.hedef_tur}"
        )
        self.btn_iksir.config(
            text=f"🧪 İksir Kullan ({self.oyuncu.iksir_sayisi})"
        )

    def _durum_kontrol(self):
        # 1. Ölüm Kontrolü
        if not self.oyuncu.hayatta_mi():
            messagebox.showerror(
                "💀 Öldün!",
                f"Zindanın karanlıklarında can verdin!\nToplam Skor: {self.oyuncu.skor}",
            )
            self._baslangic_ekrani()
            return

        # 2. Zafer Kontrolü
        if self.tur > self.hedef_tur:
            messagebox.showinfo(
                "🏆 Zafer!",
                f"Tebrikler {self.oyuncu.isim}! Tüm odaları geçtin ve zindandan kaçtın!\nToplam Skorun: {self.oyuncu.skor}",
            )
            self._baslangic_ekrani()


# ==========================================
# 3. UYGULAMAYI BAŞLAT
# ==========================================
if __name__ == "__main__":
    pencere = tk.Tk()
    app = ZindanOyunuGUI(pencere)
    pencere.mainloop()
