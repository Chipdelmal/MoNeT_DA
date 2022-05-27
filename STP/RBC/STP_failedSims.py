import STP_aux as aux

files = (
    "E_03_04_00200_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_04_00400_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_04_00400_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_04_00600_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_04_00800_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_04_00800_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_04_01000_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_04_01000_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_00200_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_00400_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_00400_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_00600_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_00600_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_00800_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_00800_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_01000_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_08_01000_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00200_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00200_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00400_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00400_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00600_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00600_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00800_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00800_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_00800_001185000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_01000_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_12_01000_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_00200_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_00400_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_00400_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_00600_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_00600_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_00800_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_00800_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_01000_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_01000_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_16_01000_001185000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_00200_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_00200_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_00400_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_00400_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_00600_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_00600_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_00800_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_00800_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_01000_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_01000_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_20_01000_001185000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_00200_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_00200_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_00400_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_00400_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_00600_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_00600_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_00800_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_00800_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_01000_000000000000_000100000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_01000_000395000000_000001000000_0021875_0008775_0000000_0100000_0071700",
    "E_03_24_01000_001185000000_000100000000_0021875_0008775_0000000_0100000_0071700"
)

scalers = list(aux.DATA_SCA.values())

file = files[0]
splits = file.split("_")[1:]
[int(i)/s for (i, s) in zip(splits, scalers)]