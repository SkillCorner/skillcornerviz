"""
Markos Bontozoglou
14/06/24
A class that holds various constants used for run types, metrics, color palettes,
average strings, meta information strings, and player positions. These include the
translations to Spanish, French, Italian, and Portuguese.
"""

from skillcornerviz.utils import skillcorner_colors


RUN_TYPES = ['cross_receiver_runs',
             'runs_in_behind',
             'runs_ahead_of_the_ball',
             'overlap_runs',
             'underlap_runs',
             'support_runs',
             'coming_short_runs',
             'dropping_off_runs',
             'pulling_half_space_runs',
             'pulling_wide_runs']

RUN_METRICS_PER_30_TIP = ['count_' + i + '_per_30_tip' for i in RUN_TYPES]

# Palette
TEXT_COLOR = skillcorner_colors.primary_colors_hex_codes['PITCH SHADOW']

BASE_COLOR = skillcorner_colors.primary_colors_hex_codes['INNOVATION']
DARK_BASE_COLOR = skillcorner_colors.greens['DIGITAL PITCH']['80% SHADOW HEX']

PRIMARY_HIGHLIGHT_COLOR = skillcorner_colors.primary_colors_hex_codes['PHYSICAL PITCH']
DARK_PRIMARY_HIGHLIGHT_COLOR = skillcorner_colors.primary_colors_hex_codes['DIGITAL PITCH']

SECONDARY_HIGHLIGHT_COLOR = skillcorner_colors.greens['PHYSICAL PITCH']['40% SHADOW HEX']
DARK_SECONDARY_HIGHLIGHT_COLOR = skillcorner_colors.greens['DIGITAL PITCH']['40% SHADOW HEX']

# COLORS PALLET
FIVE_COLORS = [skillcorner_colors.greens['PHYSICAL PITCH']['40% SHADOW HEX'],
               skillcorner_colors.sec_col_hex_codes['Yellow'],
               skillcorner_colors.sec_col_hex_codes['Red'],
               skillcorner_colors.sec_col_hex_codes['Blue'],
               skillcorner_colors.sec_col_hex_codes['Teal']
               ]


GREEN_TO_RED_SCALE = [skillcorner_colors.red_hex_codes['SCREEN HEX'],
                      skillcorner_colors.red_hex_codes['40% TINT HEX'],
                      BASE_COLOR,
                      skillcorner_colors.greens['PHYSICAL PITCH']['40% TINT HEX'],
                      skillcorner_colors.greens['PHYSICAL PITCH']['BASE']]
DARK_GREEN_TO_RED_SCALE = [skillcorner_colors.red_hex_codes['SCREEN HEX'],
                           skillcorner_colors.red_hex_codes['40% SHADOW HEX'],
                           DARK_BASE_COLOR,
                           skillcorner_colors.greens['DIGITAL PITCH']['40% SHADOW HEX'],
                           skillcorner_colors.greens['DIGITAL PITCH']['BASE']]

# Average String
AVERAGE_STRINGS = {
    'ENG': {
        'Average': 'Average',
        'Player Av.': 'Player Av.',
        'Sample Average': 'Sample Average',
        'Av. of Top 5 Performances': 'Av. of Top 5 Performances',
        'Season Average': 'Season Average',
        'Single Performance': 'Single Performance',
        'High': 'High',
        'Very High': 'Very High',
        'Low': 'Low',
        'Very Low': 'Very Low'
    },
    'ESP': {
        'Average': 'Media',
        'Player Av.': 'Media del jugador',
        'Sample Average': 'Media de la muestra',
        'Av. of Top 5 Performances': 'Media de los 5 mejores partidos',
        'Season Average': 'Media de la temporada',
        'Single Performance': 'Partido individual',
        'High': 'Alto',
        'Very High': 'Muy alto',
        'Low': 'Bajo',
        'Very Low': 'Muy bajo'
    },
    'FRA': {
        'Average': 'Moyenne',
        'Player Av.': 'Moyenne des performances',
        'Sample Average': "Moyenne de l'échantillon",
        'Av. of Top 5 Performances': 'Moyenne des 5 meilleurs performances',
        'Season Average': 'Moyenne de la saison',
        'Single Performance': 'Performance sur un match',
        'High': 'Haut',
        'Very High': 'Très haut',
        'Low': 'Basse',
        'Very Low': 'Très basse'
    },
    'ITA': {
        'Average': 'Media',
        'Player Av.': 'Media del giocatore',
        'Sample Average': 'Media campione',
        'Av. of Top 5 Performances': 'Media delle prime 5 prestazioni',
        'Season Average': 'Media stagionale',
        'Single Performance': 'Spettacolo singolo',
        'High': 'Alto',
        'Very High': 'Molto alto',
        'Low': 'Basso',
        'Very Low': 'Molto Basso'
    },
    'POR': {
        'Average': 'Média',
        'Player Av.': ' Média do jogador',
        'Sample Average': 'Média da amostra',
        'Av. of Top 5 Performances': 'Média dos 5 melhores desempenhos',
        'Season Average': 'Média da temporada',
        'Single Performance': 'Desempenho único',
        'High': 'Alto',
        'Very High': 'Muito alto',
        'Low': 'Baixo',
        'Very Low': 'Muito baixo'
    }
}

# Meta Information Strings
META_STRINGS = {
    'ENG': {
        'Player Name': 'Player Name',
        'Team': 'Team',
        'Position Group': 'Position Group',
        'Position': 'Position',
        'Date Of Birth': 'Date Of Birth',
        'Matches': 'Matches',
        'Season': 'Season'},
    'ESP': {
        'Player Name': 'Nombre del jugador',
        'Team': 'Equipo',
        'Position Group': 'Grupo de Posición',
        'Position': 'Posición',
        'Date Of Birth': 'Fecha de nacimiento',
        'Matches': 'Partidos',
        'Season': 'Temporada'},
    'FRA': {
        'Player Name': 'Nom de joueur',
        'Team': 'Équipe',
        'Position Group': 'Groupe de postes',
        'Position': 'Position',
        'Date Of Birth': 'Date de naissance',
        'Matches': 'Matchs',
        'Season': 'Saison'},
    'ITA': {
        'Player Name': 'Nome del giocatore',
        'Team': 'Squadra',
        'Position Group': 'Gruppo posizionale',
        'Position': 'Ruolo',
        'Date Of Birth': 'Data di nascita',
        'Matches': 'Partite',
        'Season': 'Stagione'},
    'POR': {
        'Player Name': 'Nome do jogador',
        'Team': 'Equipa',
        'Position Group': 'Grupo posicional',
        'Position': 'Posição',
        'Date Of Birth': 'Data de nascimento',
        'Matches': 'Jogos',
        'Season': 'Temporada'},
}

# Position Names

PLAYER_POSITION_GROUP_READABLE = {
    'ENG': {
        'Goalkeeper': 'Goalkeeper',
        'Central Defender': 'Central Defender',
        'Full Back': 'Full Back',
        'Defender': 'Defender',
        'Midfield': 'Midfield',
        'Forward': 'Forward',
        'Winger': 'Winger'
    },
    'FRA': {
        'Goalkeeper': 'Gardien de but',
        'Central Defender': 'Défenseur central',
        'Full Back': 'Arrière latéral',
        'Defender': 'Défenseur',
        'Midfield': 'Milieu de terrain',
        'Forward': 'Attaquant',
        'Winger': 'Ailier'
    },
    'ESP': {
        'Goalkeeper': 'Portero',
        'Central Defender': 'Defensor central',
        'Full Back': 'Lateral',
        'Defender': 'Defensor',
        'Midfield': 'Centrocampista',
        'Forward': 'Delantero',
        'Winger': 'Extremo'
    },
    'POR': {
        'Goalkeeper': 'Goleiro',
        'Central Defender': 'Zagueiro central',
        'Full Back': 'Lateral',
        'Defender': 'Defensor',
        'Midfield': 'Meio-campista',
        'Forward': 'Atacante',
        'Winger': 'Ponta'
    },
    'ITA': {
        'Goalkeeper': 'Portiere',
        'Central Defender': 'Difensore centrale',
        'Full Back': 'Terzino',
        'Defender': 'Difensore',
        'Midfield': 'Centrocampista',
        'Forward': 'Attaccante',
        'Winger': 'Ala'
    }
}

PLAYER_POSITION_READABLE = {
    'ENG': {'GK': 'GK', 'CB': 'CB', 'LCB': 'LCB', 'RCB': 'RCB', 'FB': 'FB', 'LWB': 'LWB', 'RWB': 'RWB', 'DM': 'DM',
            'CM': 'CM', 'LM': 'LM', 'RM': 'RM', 'LW': 'LW', 'RW': 'RW', 'AM': 'AM', 'CF': 'CF', 'LF': 'LF',
            'RF': 'RF', 'ST': 'ST'},
    'FRA': {'GK': 'GB', 'CB': 'DC', 'LCB': 'DCG', 'RCB': 'DCD', 'FB': 'LAT', 'LWB': 'LATG', 'RWB': 'LATD', 'DM': 'MDC',
            'CM': 'MC', 'LM': 'MG', 'RM': 'MD', 'LW': 'AG', 'RW': 'AD', 'AM': 'MOC', 'CF': 'ATC', 'LF': 'ATG',
            'RF': 'ATD', 'ST': 'BU'},
    'ESP': {'GK': 'POR', 'CB': 'DFC', 'LCB': 'DCL', 'RCB': 'DCR', 'FB': 'LD', 'LWB': 'LI', 'RWB': 'LD', 'DM': 'MCD',
            'CM': 'MC', 'LM': 'MI', 'RM': 'MD', 'LW': 'EI', 'RW': 'ED', 'AM': 'MAC', 'CF': 'DC', 'LF': 'EI',
            'RF': 'ED', 'ST': 'DL'},
    'POR': {'GK': 'GR', 'CB': 'DC', 'LCB': 'DCI', 'RCB': 'DCD', 'FB': 'LD', 'LWB': 'LE', 'RWB': 'LD', 'DM': 'MDC',
            'CM': 'MC', 'LM': 'ME', 'RM': 'MD', 'LW': 'AE', 'RW': 'AD', 'AM': 'MAC', 'CF': 'AC', 'LF': 'AE',
            'RF': 'AD', 'ST': 'PL'},
    'ITA': {'GK': 'POR', 'CB': 'DC', 'LCB': 'DCS', 'RCB': 'DCD', 'FB': 'TD', 'LWB': 'TS', 'RWB': 'TD', 'DM': 'CCD',
            'CM': 'CC', 'LM': 'CS', 'RM': 'CD', 'LW': 'AS', 'RW': 'AD', 'AM': 'CAM', 'CF': 'ACC', 'LF': 'AS',
            'RF': 'AD', 'ST': 'ATT'}
}
