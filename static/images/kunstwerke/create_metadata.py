import os

data = []
with open('./metadata_with_links.txt', 'r') as f:
    for line in f:
        if not 'NO. ' in line:
            line.replace('NO.', 'NO. ')
        split = line.split(' ')
        
        filename = split[0].split('/')[-1].replace('jpg', 'ini')
        title = split[2]
        year = split[4]
        if year not in title:
            title = year + "-" + title
        material_end_index = split.index('FORMAT')
        material_index_start = split.index('MATERIAL') + 1
        material = " ".join(split[material_index_start: material_end_index])
        format_end_index = split.index('STATUS') if 'STATUS' in split else -1
        format = " ".join(split[material_end_index + 1: format_end_index])
        if not ' x ' in format:
            format = format.replace('x', ' x ')
        if 'CM' in format:
            format = format.replace('CM', 'cm')
        if not ' cm' in format:
            format = format.replace('cm', ' cm')
        status = ''
        if 'STATUS' in split:
            status_index = split.index('STATUS')+1
            status = split[status_index:][0].replace('\n', '')
        if not format.lower().endswith('cm'):
            format = format + ' cm'
        data.append({
            'filename': filename,
            'title': title,
            'year': year,
            'material': material,
            'format': format,
            'status': status
        })

for d in data:
    with open(f'./{d["year"]}/{d["filename"]}', 'w') as f:
        f.write(f'[Metadata]\nTitle={d["title"]}\nYear={d["year"]}\nMaterial={d["material"]}\nFormat={d["format"]}\nStatus={d["status"]}\n')

        

    
        