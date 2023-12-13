import pandas as pd


class Gemi:
        durum: dict = {}

        def __init__(self, gemi_adi, kapasite, gidecek_ulke):
            self.info = {
                "gemi_adi": gemi_adi,
                "kapasite": kapasite,
                "gidecek_ülke": gidecek_ulke
            }
            self.sira = gemi_adi
            self.mevcut_kapasite = 0

        def yukleme(self, yuk):
            self.mevcut_kapasite += yuk

        def gitmeye_hazirlar(self):
            return self.mevcut_kapasite / self.info["kapasite"] >= 0.95

        @staticmethod
        def okuma(path):
            a = pd.read_csv(path, encoding="cp1254")
            maksimum_t = 0
            for i in range(len(a)):
                gemi = a.iloc[i]
                Gemidurum = Gemi(
                    a.iloc[i]["gemi_adı"],
                    a.iloc[i]["kapasite"],
                    a.iloc[i]["gidecek_ülke"]
                )
                if Gemi.durum.get(gemi["geliş_zamanı"]) is None:
                    Gemi.durum[gemi["geliş_zamanı"]] = [Gemidurum]
                else:
                    Gemi.durum[gemi["geliş_zamanı"]].append(Gemidurum)
                maksimum_t = max(maksimum_t, gemi["geliş_zamanı"])
            return maksimum_t


class Tir:
    durum: dict = {}

    def __init__(self, plaka: str, ulke: str, ton20: int, ton30: int, yuk_miktari: int, maliyet: int):
        self.info = {
            "plaka": plaka,
            "ülke": ulke,
            "20_ton_adet": ton20,
            "30_ton_adet": ton30,
            "yük_miktarı": yuk_miktari,
            "maliyet": maliyet
        }
        self.sira = plaka.split("_")[-1]

    @staticmethod
    def okuma(path):
        a = pd.read_csv(path, encoding="cp1254")
        maksimum_t = 0
        for i in range(len(a)):
            tir = a.iloc[i]
            Tirdurum = Tir(
                a.iloc[i]["tır_plakası"],
                a.iloc[i]["ülke"],
                a.iloc[i]["20_ton_adet"],
                a.iloc[i]["30_ton_adet"],
                a.iloc[i]["yük_miktarı"],
                a.iloc[i]["maliyet"]
            )
            if Tir.durum.get(tir["geliş_zamanı"]) is None:
                Tir.durum[tir["geliş_zamanı"]] = [Tirdurum]
            else:
                Tir.durum[tir["geliş_zamanı"]].append(Tirdurum)
            maksimum_t = max(maksimum_t, tir["geliş_zamanı"])
        return maksimum_t

def istif_alan_yukleri(istif_alani):
    return sum(map(lambda x: x[0], istif_alani))

if __name__ == "__main__":
    tir_max_t = Tir.okuma("olaylar.csv")
    gemi_max_t = Gemi.okuma("gemiler.csv")

    gemi_bekletme_bolgesi = []
    tir_bekletme_bolgesi = []
    istif_alani = [[], []]

    for t in range(1, max(tir_max_t, gemi_max_t) + 1):
        print(f"{t} tarihi için işlemler başlatıldı")
        vinc_kullanma_miktari = 0
        if Tir.durum.get(t) is not None:
            for tir in Tir.durum[t]:
                tir_bekletme_bolgesi.append(tir)
                print(f"\t{t} tarihinde {tir.info['plaka']} plakalı tır bekletme alanına geldi")
            tir_bekletme_bolgesi.sort(key=lambda tir: tir.sira)

        if Gemi.durum.get(t) is not None:
            for gemi in Gemi.durum[t]:
                gemi_bekletme_bolgesi.append(gemi)
                print(f"\t{t} tarihinde {gemi.info['gemi_adi']} adlı gemi bekletme alanına getirildi")
            gemi_bekletme_bolgesi.sort(key=lambda gemi: gemi.sira)

        while istif_alan_yukleri(istif_alani[0]) < 750 and vinc_kullanma_miktari < 20:
            if len(tir_bekletme_bolgesi) == 0:
                break
            tir = tir_bekletme_bolgesi.pop(0)
            yuk = tir.info["20_ton_adet"] * 20 + tir.info["30_ton_adet"] * 30
            if istif_alan_yukleri(istif_alani[0]) + yuk > 750:
                tir_bekletme_bolgesi = [tir] + tir_bekletme_bolgesi
                break
            else:
                istif_alani[0].append([yuk, tir.info["ülke"]])
                vinc_kullanma_miktari += 1
                print(
                    f"\t{t} tarihinde {tir.info['plaka']} plakalı tır  1 nolu istif alanından {tir.info['ülke']}adlı ülkeye gidecek kargo yukledi")

        if istif_alan_yukleri(istif_alani[0]) == 750 and vinc_kullanma_miktari < 20:
            print(f"\t{t} tarihinde 750 tonluk 1 nolu istif alanı doldu")

        while istif_alan_yukleri(istif_alani[1]) < 750:
            if len(tir_bekletme_bolgesi) == 0:
                break
            tir = tir_bekletme_bolgesi.pop(0)
            yuk = tir.info["20_ton_adet"] * 20 + tir.info["30_ton_adet"] * 30
            if istif_alan_yukleri(istif_alani[1]) + yuk > 750:
                tir_bekletme_bolgesi = [tir] + tir_bekletme_bolgesi
                break
            else:
                istif_alani[1].append(yuk)
                vinc_kullanma_miktari += 1
                print(
                    f"\t{t} tarihinde {tir.info['plaka']} plakalı tır 2 nolu istif alanindan {tir.info['ülke']} adlı ülkeye gidecek kargo yukledi")

        if istif_alan_yukleri(istif_alani[1]) == 750:
            print(f"\t{t} tarihinde 750 tonluk 2 nolu istif alanı dolmuştur")

        index = 0
        while istif_alan_yukleri(istif_alani[0]) > 0 and index < len(gemi_bekletme_bolgesi) and vinc_kullanma_miktari < 20:
            if len(gemi_bekletme_bolgesi) == 0:
                break
            gemi = gemi_bekletme_bolgesi[index]
            gidilecek_ulke = gemi.info["gidecek_ülke"]
            kargo_listesi = list(filter(lambda x: x[1] == gidilecek_ulke, istif_alani[0]))
            for k in kargo_listesi:
                gemi.yukleme(k[0])
                vinc_kullanma_miktari += 1
                istif_alani[0].remove(k)
                print(
                    f"\t{t} tarihinde {k[0]} tonluk kargo 1 nolu istif alaninda {gemi.info['gemi_adi']} gemisine  yüklendi")
                if gemi.gitmeye_hazirlar():
                    print(f"\t{t} tarihinde {gemi.info['gemi_adi']} adlı gemi {gidilecek_ulke} ülkesine doğru harekete geçti")
                    gemi_bekletme_bolgesi.pop(index)
                    index -= 1
                    break
            index += 1

        if istif_alan_yukleri(istif_alani[0]) == 0:
            print(f"\t{t} tarihinde 1 nolu istif alanı boşaltıldı ")

        index = 0
        while istif_alan_yukleri(istif_alani[1]) > 0 and index < len(gemi_bekletme_bolgesi) and vinc_kullanma_miktari < 20:
            if len(gemi_bekletme_bolgesi) == 0:
                break
            gemi = gemi_bekletme_bolgesi[index]
            gidilecek_ulke = gemi.info["gidecek_ülke"]
            kargo_listesi = list(filter(lambda x: x[1] == gidilecek_ulke, istif_alani[1]))
            for k in kargo_listesi:
                gemi.yukleme(k[0])
                istif_alani[1].remove(k)
                vinc_kullanma_miktari += 1
                print(
                    f"\t{t} tarihinde {gemi.info['gemi_adi']} adlı gemi 2 nolu istif alanına {k[0]} tonluk kargo yükledi")
                if gemi.gitmeye_hazirlar():
                    print(f"\t{t} tarihinde {gemi.info['gemi_adi']} adlı gemi {gidilecek_ulke} ülkesine doğru harekete geçti ")
                    gemi_bekletme_bolgesi.pop(index)
                    index -= 1
                    break
            index += 1

        if istif_alan_yukleri(istif_alani[1]) == 0:
            print(f"\t{t} tarihinde 2 nolu istif alanı boşaltıldı")

        print(f"{t} tarihli işlemler sonlandırıldı")