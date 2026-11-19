# Rebuild data/modular-sets.js from the parsed master Google Doc tables.
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
tables = json.load(open(sys.argv[1], encoding='utf-8'))
OUT = sys.argv[2]

CHECK = re.compile(r'\s*✔️?\s*')

# Doc heading -> (site villain name, group). Existing site names are kept so saved selections still work.
VILLAINS = {
    'RHINO': ('Rhino', 'Core Set'), 'KLAW': ('Klaw', 'Core Set'), 'ULTRON': ('Ultron', 'Core Set'),
    'RISKY BUSINESS': ('Risky Business', 'Green Goblin'), 'MUTAGEN FORMULA': ('Mutagen Formula', 'Green Goblin'),
    'WRECKING CREW': ('Wrecking Crew', 'The Wrecking Crew'),
    'CROSSBONES': ('Crossbones', 'The Rise of Red Skull'), 'ABSORBING MAN': ('Absorbing Man', 'The Rise of Red Skull'),
    'TASKMASTER': ('Taskmaster', 'The Rise of Red Skull'), 'ZOLA': ('Zola', 'The Rise of Red Skull'),
    'RED SKULL': ('Red Skull', 'The Rise of Red Skull'),
    'KANG': ('Kang', 'The Once and Future Kang'),
    'BROTHERHOOD OF BADOON (DRANG)': ('Brotherhood of Badoon (Drang)', "Galaxy's Most Wanted"),
    'INFILTRATE THE MUSEUM (COLLECTOR #1)': ('Infiltrate the Museum (Collector #1)', "Galaxy's Most Wanted"),
    'ESCAPE THE MUSEUM (COLLECTOR #2)': ('Escape the Museum (Collector #2)', "Galaxy's Most Wanted"),
    'NEBULA': ('Nebula', "Galaxy's Most Wanted"), 'RONAN THE ACCUSER': ('Ronan the Accuser', "Galaxy's Most Wanted"),
    'EBONY MAW': ('Ebony Maw', "The Mad Titan's Shadow"),
    'TOWER DEFENSE (PROXIMA/CORVUS)': ('Tower Defense (Proxima/Corvus)', "The Mad Titan's Shadow"),
    'THANOS': ('Thanos', "The Mad Titan's Shadow"), 'HELA': ('Hela', "The Mad Titan's Shadow"),
    'LOKI': ('Loki', "The Mad Titan's Shadow"),
    'THE HOOD [PAGE #1]': ('The Hood', 'The Hood'), 'THE HOOD [PAGE #2]': ('The Hood', 'The Hood'),
    'SANDMAN': ('Sandman', 'Sinister Motives'), 'VENOM': ('Venom', 'Sinister Motives'),
    'MYSTERIO': ('Mysterio', 'Sinister Motives'), 'THE SINISTER SIX': ('The Sinister Six', 'Sinister Motives'),
    'VENOM GOBLIN': ('Venom Goblin', 'Sinister Motives'),
    'SABRETOOTH': ('Sabretooth', 'Mutant Genesis'),
    'PROJECT WIDEAWAKE (SENTINELS)': ('Project Wideawake (Sentinels)', 'Mutant Genesis'),
    'MASTER MOLD': ('Master Mold', 'Mutant Genesis'), 'MANSION ATTACK': ('Mansion Attack', 'Mutant Genesis'),
    'MAGNETO': ('Magneto', 'Mutant Genesis'),
    'MAGOG': ('Magog', 'MojoMania'), 'SPIRAL': ('Spiral', 'MojoMania'), 'MOJO': ('Mojo', 'MojoMania'),
    'MORLOCK SIEGE': ('Morlock Siege', 'Next Evolution'), 'ON THE RUN': ('On the Run', 'Next Evolution'),
    'JUGGERNAUT': ('Juggernaut', 'Next Evolution'), 'MISTER SINISTER': ('Mister Sinister', 'Next Evolution'),
    'STRYFE': ('Stryfe', 'Next Evolution'),
    'UNUS': ('Unus', 'Age of Apocalypse'), 'FOUR HORSEMEN': ('Four Horsemen', 'Age of Apocalypse'),
    'APOCALYPSE': ('Apocalypse', 'Age of Apocalypse'), 'DARK BEAST': ('Dark Beast', 'Age of Apocalypse'),
    'EN SABAH NUR (APOCALYPSE #2)': ('En Sabah Nur (Apocalypse #2)', 'Age of Apocalypse'),
    'BLACK WIDOW': ('Black Widow', 'Agents of S.H.I.E.L.D.'), 'BATROC': ('Batroc', 'Agents of S.H.I.E.L.D.'),
    'M.O.D.O.K.': ('M.O.D.O.K.', 'Agents of S.H.I.E.L.D.'), 'THUNDERBOLTS': ('Thunderbolts', 'Agents of S.H.I.E.L.D.'),
    'BARON ZEMO': ('Baron Zemo', 'Agents of S.H.I.E.L.D.'),
    'ENCHANTRESS': ('Enchantress', 'Trickster Takeover'), 'GOD OF LIES (LOKI #2)': ('God of Lies (Loki #2)', 'Trickster Takeover'),
    'CUSTOM REGISTRATION COMBOS': ('Custom Registration Combos', 'Civil War'),
    'CUSTOM RESISTANCE COMBOS': ('Custom Resistance Combos', 'Civil War'),
    'IRON MAN': ('Iron Man', 'Civil War'), 'CAPTAIN MARVEL': ('Captain Marvel', 'Civil War'),
    'CAPTAIN AMERICA': ('Captain America', 'Civil War'), 'SPIDER-WOMAN': ('Spider-Woman', 'Civil War'),
    'SHE-HULK': ('She-Hulk', 'Synthezoid Smackdown'), 'VISION': ('Vision', 'Synthezoid Smackdown'),
}
FNE_GROUP = 'Fear No Evil'
for h in ['BULLSEYE', 'ELECTRO', 'HAMMERHEAD', 'PURPLE MAN', 'TYPHOID MARY', 'THE GETAWAY',
          'PROTECTION RACKET', 'THE RAFT BREAKOUT', 'STOP THE PRESSES!', 'KINGPIN']:
    name = ' '.join(w.capitalize() for w in h.lower().split()).replace('Stop The Presses!', 'Stop the Presses!')
    # The doc still tags these headings as unreleased; accept them with or without that tag.
    VILLAINS[h + ' [UNRELEASED / SPECULATIVE]'] = (name, FNE_GROUP)
    VILLAINS[h] = (name, FNE_GROUP)

def lines(cell):
    return [l.strip() for l in cell.split('\n') if l.strip()]

def find_villain(ctx):
    for c in reversed(ctx):
        key = re.sub(r'\s+', ' ', c).strip()
        key = key.split('\n')[-1].strip()
        if key in VILLAINS: return key
        m = re.match(r'NOTE: (.+?) DOES NOT NORMALLY', key)
        if m and m.group(1) in VILLAINS: return m.group(1)
    return None

sets, groups, info, packs = [], {}, {}, {}

# Pack legend from the first table.
for cell in tables[0]['rows'][0]:
    for l in lines(cell):
        m = re.match(r'^([A-Z/]+)\s*=\s*(.+)$', l)
        if m: packs[m.group(1)] = m.group(2)

for t in tables[1:]:
    rows = t['rows']
    if not rows or rows[0][0] not in ('Name', 'Name + Main Schemes'): continue
    key = find_villain(t['context'])
    if not key:
        print('!! no villain for table with context', t['context'][-3:]); continue
    villain, group = VILLAINS[key]
    groups.setdefault(group, [])
    if villain not in groups[group]: groups[group].append(villain)

    # Villain info: themes, mechanics, required sets and notes from the text above the table.
    vi = info.setdefault(villain, {})
    notes = vi.setdefault('notes', [])
    for c in t['context']:
        c1 = re.sub(r'\s+', ' ', c).strip()
        if c1.startswith('Themes:'): vi['themes'] = c1[7:].strip()
        elif c1.startswith('Mechanics:'): vi['mechanics'] = c1[10:].strip()
        elif c1.startswith(('Required Modular', 'Interchangeable', 'Uses ONLY', 'Unofficially', "Add a modular", 'Shuffle four', '(Crime', 'NOTE:', 'BEYOND', 'Remember')):
            if c1 not in notes: notes.append(c1)
    legend = lines(rows[0][1])[1:] if rows and len(rows[0]) > 1 else []
    for l in legend:
        l = re.sub(r'\s*=\s*', ' = ', l)
        n = f'In Modular Sets, {l}.'
        if n not in notes: notes.append(n)
    if not notes: del vi['notes']

    header = rows[0]
    main_schemes_col = 'Main Schemes' in header
    name_has_schemes = header[0] == 'Name + Main Schemes'
    for r in rows[1:]:
        r = r + [''] * (6 - len(r))
        name_lines = lines(r[0])
        if not name_lines: continue
        name_text = name_lines[0]
        extra = name_lines[1:]
        # Names can wrap onto two lines; main schemes always end in "(1B)" / "(2B)" etc.
        while extra and not re.search(r'\(\d[AB]\)$', extra[0]):
            name_text += ' ' + extra.pop(0)
        recommended = '✔' in name_text
        name = CHECK.sub(' ', name_text).strip()
        e = {'villain': villain, 'name': name,
             'modulars': ', '.join(lines(r[1]))}
        if main_schemes_col:
            e['difficulty'] = ''
            e['mainSchemes'] = ', '.join(lines(r[2]))
        else:
            d = r[2].strip()
            e['difficulty'] = '+' + d if re.match(r'^0\??$', d) else d
        e['notes'] = ' '.join(lines(r[3]))
        e['packs'] = ', '.join(lines(r[4]))
        if name_has_schemes and extra: e['mainSchemes'] = ', '.join(extra)
        if recommended: e['recommended'] = True
        sets.append(e)

def js(v): return json.dumps(v, ensure_ascii=False)

def entry(e):
    order = ['villain', 'name', 'modulars', 'mainSchemes', 'difficulty', 'notes', 'packs', 'recommended', 'unreleased']
    return '{ ' + ', '.join(f'{k}: {js(e[k])}' for k in order if k in e) + ' }'

out = ['// VillainTheory\'s "Every Villain\'s Best Modular Sets", one entry per suggestion.',
       '// Source: https://docs.google.com/document/d/1AOED4MPkrEGIOAVzV4VJaFAc4bWHfhstOSVTqhSpvHU/edit',
       '// The villain name must match a name in MODULAR_GROUPS below.',
       '// recommended: true = the doc\'s ✔️ quick recommendation. Add unreleased: true to label a suggestion as speculative.',
       '// mainSchemes is only used by the Civil War / Synthezoid Smackdown villains.',
       'window.MODULAR_SETS = [']
last = None
for e in sets:
    if e['villain'] != last:
        out.append(f'    // {e["villain"].upper()}')
        last = e['villain']
    out.append(f'    {entry(e)},')
out.append('];\n')

# Tidy the villain notes: join wrapped lines and replace the all-caps NOTE lines with plain sentences.
NO_EXTRA = {
    'Wrecking Crew': 'Wrecking Crew does not normally contain any modular sets.',
    'The Sinister Six': 'The Sinister Six does not normally contain additional modular sets.',
    'Spiral': 'Spiral does not normally contain additional modular sets beyond the required MojoMania sets.',
    'Mojo': 'Mojo does not normally contain additional modular sets beyond the required MojoMania sets.',
    'Thunderbolts': 'Thunderbolts does not normally contain additional modular sets beyond the required sets with an Elite Thunderbolts.',
}
for villain, vi in info.items():
    notes = vi.get('notes')
    if not notes: continue
    tidy = []
    for n in notes:
        if n.startswith('BEYOND'): continue
        if n.startswith('NOTE:'):
            n = NO_EXTRA.get(villain) or sys.exit(f'unhandled NOTE for {villain}: {n}')
        elif n.startswith('(Crime') and tidy:
            tidy[-1] += ' ' + n
            continue
        elif n in ("Add a modular set to each Villain's deck",) or n.startswith('Shuffle four'):
            n = '• ' + n
        tidy.append(n)
    vi['notes'] = tidy

# The doc lists Thunderbolt minion sets in a small extra table after the Thunderbolts suggestions.
for t in tables:
    rows = t['rows']
    if rows and rows[0] and rows[0][0].startswith('Mod Sets that contain other Thunderbolt'):
        names = [c for r in rows[1:] for c in r if c.strip()]
        info['Thunderbolts'].setdefault('notes', []).append(
            'Mod sets that contain other Thunderbolt minions (in comic lore), pick 1 or 2: ' + ', '.join(names) + '.')

out.append('// Which villains belong to each box, in release order.')
out.append('window.MODULAR_GROUPS = {')
out += [f'    {js(g)}: {js(v)},' for g, v in groups.items()]
out.append('};\n')
out.append('// Themes, mechanics and setup notes shown above each villain\'s suggestions.')
out.append('window.MODULAR_VILLAIN_INFO = {')
out += [f'    {js(k)}: {js(v)},' for k, v in info.items() if v]
out.append('};\n')
out.append('// Pack codes used in the "Packs" field.')
out.append('window.MODULAR_PACKS = {')
out += [f'    {js(k)}: {js(v)},' for k, v in packs.items()]
out.append('};')
open(OUT, 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print(len(sets), 'suggestions,', sum(len(v) for v in groups.values()), 'villains,', len(groups), 'groups,', len(packs), 'pack codes')
