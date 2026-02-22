from sys import argv
from os import path
from litemapy import Schematic, Region, BlockState

def parse_bin(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return data

def generate_regions(data):
    # Define a north and south region per slice
    nregions = []
    sregions = []
    for i in range(8):
        (bx, by, bz) = (33+i%2, 17, 1+7*i)
        nregions.append(Region(bx, by, bz, -31, 16, 1))
        sregions.append(Region(bx, by, bz+2, -31, 16, 1))

    repeater_north = BlockState("minecraft:repeater", facing="north")
    repeater_south = BlockState("minecraft:repeater", facing="south")
    void = BlockState("minecraft:structure_void")
    
    # Iterate over slices (0 <= i <= 7)
    for nreg, sreg, i in zip(nregions, sregions, range(8)):
        # Iterate over bytes
        for j in range(16):
            byten = data[j + 32*i]
            bytes = data[(j+16) + 32*i]
            # Iterate over bits
            for k in range(8):
                nreg[-j*2,(j+1)%2 + 2*k,0] = repeater_north if byten & 0x1 else void
                sreg[-j*2,(j+1)%2 + 2*k,0] = repeater_south if bytes & 0x1 else void
                byten >>= 1
                bytes >>= 1

    all_regions = {f"Bytes[{i*16}:{(i+1)*16}]":reg for i,reg in enumerate(nregions + sregions)}
    return all_regions

def main():
    if len(argv) > 1:
        file_path = " ".join(argv[1:])
    else:
        file_path = input(".bin file to convert: ")
    if not file_path.endswith(".bin"):
        print("File must be .bin\nProgram exited.")
        return 1
    file_name = path.splitext(path.basename(file_path))[0]
    
    data = parse_bin(file_path)
    print(data.hex(sep="\t", bytes_per_sep=1))
    
    all_regions = generate_regions(data)
    
    ROM_SCHEMATIC = "256_byte_ROM.litematic"
    schem = Schematic.load(ROM_SCHEMATIC)
    schem.name = f"{file_name}_ROMdata"
    schem.author = schem.author + ", AMcD"
    schem.description = "ROM data generated from binary file"
    for name,region in all_regions.items():
        schem.regions[name] = region
    #schem = Schematic(name=f"{file_name}_ROM", author="AMcD", description="ROM data generated from binary file", regions=all_regions)
    
    # Save the schematic
    schem.save(f"{path.splitext(file_path)[0]}_ROMdata.litematic")
    return 0

if __name__ == "__main__":
    main()