import pandas as pd

print("\n--- PANDAS SIFIR KİLOMETRE TESTİ ---")

test_data = {
    "Yazılımcı": ["Sen", "Ben"],
    "Rol": ["Pilot", "Pit Duvarı"],
    "Durum": ["Nizamî", "Hazır"]
}

df = pd.DataFrame(test_data)
print(df)
print("------------------------------------\n")

print("\n--- 2. AŞAMA: KOORDİNAT TESTLERİ ---")

print(f"0,0 Koordinatındaki Eleman: {df.iloc[0, 0]}")

print(f"0,1 Koordinatındaki Eleman: {df.iloc[0, 1]}")

print(f"1,2 Koordinatındaki Eleman: {df.iloc[1, 2]}")

print("\n--- TABLOYA YENİ SÜTUN EKLEME ---")

df["Puan"] = [90, 85]

print("Güncellenmiş Yeni Tablo:")
print(df)