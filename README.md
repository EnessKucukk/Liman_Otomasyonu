# Gemi ve Tır Yükleme Yönetim Sistemi

Bu proje, gemi ve tır yükleme ve boşaltma süreçlerini yönetmek için geliştirilmiş bir Python uygulamasıdır. Uygulama, belirli bir tarihte gelen gemi ve tır bilgilerini okuyarak, yükleme alanlarını yönetir ve kargoları uygun taşıma araçlarına yönlendirir.

## Özellikler

- **Gemi Yönetimi**: Gemi bilgilerini okuyarak, gemilerin yükleme kapasitelerini takip eder.
- **Tır Yönetimi**: Tır bilgilerini okuyarak, tırların yükleme kapasitelerini takip eder.
- **Yükleme ve Boşaltma**: Yükleme alanını kullanarak, tır ve gemilerin yükleme işlemlerini gerçekleştirir.
- **Durum Takibi**: Her tarih için gelen tır ve gemi bilgilerini takip eder.

## Gereksinimler

- Python 3.x
- Pandas kütüphanesi

## Kurulum

1. **Gereksinimleri Yükleyin**:
   ```bash
   pip install pandas


Proje Dosyalarını İndirin: Proje dosyalarını bilgisayarınıza indirin veya klonlayın.

CSV Dosyalarını Hazırlayın:

olaylar.csv: Tır bilgilerini içeren bir CSV dosyası.
gemiler.csv: Gemi bilgilerini içeren bir CSV dosyası.
Kullanım
Ana Programı Çalıştırın:

Kopyala
python main.py
