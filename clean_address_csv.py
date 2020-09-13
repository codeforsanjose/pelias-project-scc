import csv, json

fin = csv.DictReader(open("AddressPoint_data.csv"))
fout = None

for row in fin:
    the_geom = row.pop("the_geom")
    assert the_geom.startswith("POINT (") and the_geom.endswith(")"), the_geom
    coords = the_geom[7:-1].split(' ')
    assert len(coords) == 2, the_geom
    row["lon"], row["lat"] = map(float, coords)

    row["ID"] = row.pop("OBJECTID")

    row["HOUSENUMBER"] = row.pop("HOUSENUMTEXT")
    
    fl = row.pop("FLOOR")
    row["addendum_json_scc"] = json.dumps({"floor": fl} if len(fl) > 0 else {})

    row["UNIT"] = row.pop("UNITNUMBER")
    
    street_components = [row.pop(cname) for cname in ["STREETPREFIX", "STREETNAME", "STREETTYPE", "STREETSUFFIX"]]
    street_components = [c for c in street_components if len(c) > 0]
    row["STREET"] = ' '.join(street_components)
    
    row["layer"] = "address"

    if fout is None:
        fout = csv.DictWriter(open("data/AddressPoint_pelias.csv", 'w'), row.keys())
        fout.writeheader()
    fout.writerow(row)

