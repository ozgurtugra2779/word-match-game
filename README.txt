WORD MATCH - PYTHON / STREAMLIT

1) Bu klasörde CMD açın.
2) Şunu çalıştırın:
   py -m pip install -r requirements.txt
3) Ardından:
   py -m streamlit run app.py

Tarayıcıda açılan adresten oynayın.
İnternet bağlantısı ilk kurulumda paketleri indirmek için gerekir.
Oyun başladıktan sonra kelimeler yerel vocabulary.json dosyasından okunur.

Puan:
- Doğru eşleşme: +50
- Yanlış eşleşme: -20
- Puan 0'ın altına inmez.
Süre oyun başladığında saymaya başlar.
Her ünitede toplam 20 kelime bulunur; ekranda aynı anda 12 çift görünür.
