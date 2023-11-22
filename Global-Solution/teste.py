import json

with open("Global-Solution/json/clinica.json", "r", encoding="utf-8") as file:
    clinicas = json.load(file)

with open("Global-Solution/json/hospitais.json", "r", encoding="utf-8") as file:
    hospitais = json.load(file)

with open("Global-Solution/json/imagemlaboratorio.json", "r", encoding="utf-8") as file:
    imagem = json.load(file)

with open("Global-Solution/json/notredame.json", "r", encoding="utf-8") as file:
    notredame = json.load(file)

with open("Global-Solution/json/outras.json", "r", encoding="utf-8") as file:
    outras = json.load(file)

with open("Global-Solution/json/pa.json", "r", encoding="utf-8") as file:
    pa = json.load(file)

# print(f"Clínicas: {len(clinicas['clinicas'])}")
# print(f"Hospitais: {len(hospitais['hospital'])}")
# print(f"imagem: {len(imagem['imagemlaboratorio'])}")
# print(f"Notredame: {len(notredame['unidades'])}")
# print(f"Outras: {len(outras['outras'])}")
# print(f"PA: {len(pa['prontoatendimento'])}")
# print(f"Soma: {len(clinicas['clinicas']) + len(hospitais['hospital']) + len(imagem['imagemlaboratorio']) + len(notredame['unidades']) + len(outras['outras']) + len(pa['prontoatendimento'])}")

count_clinicas = 0
count_hospitais = 0
count_imagem = 0
count_notredame = 0
count_outras = 0
count_pa = 0

for unidade in clinicas["clinicas"]:
    if unidade["estado"] == "SP":
        count_clinicas += 1

for h in hospitais["hospital"]:
    if h["estado"] == "SP":
        count_hospitais += 1

for i in imagem["imagemlaboratorio"]:
    if i["estado"] == "SP":
        count_imagem += 1

for n in notredame["unidades"]:
    if n["estado"] == "SP":
        count_notredame += 1

for o in outras["outras"]:
    if o["estado"] == "SP":
        count_outras += 1

for p in pa["prontoatendimento"]:
    if p["estado"] == "SP":
        count_pa += 1

print(count_clinicas)
print(count_hospitais)
print(count_imagem)
print(count_notredame)
print(count_outras)
print(count_pa)
print(count_clinicas + count_hospitais + count_imagem + count_notredame + count_outras + count_pa)

