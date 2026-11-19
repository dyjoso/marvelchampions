// The Gauntlet: a five-scenario hero test. Each scenario tests a different skill.
// Modular set choices come from VillainTheory's "Every Villain's Best Modular Sets".
window.GAUNTLET = {
    scenarios: [
        {
            id: 'mutagen',
            villain: 'Mutagen Formula',
            mode: 'Standard III',
            test: 'Minion swarm',
            modulars: 'Goblin Gang: A Mess of Things (+1)',
            packs: 'The Green Goblin',
            summary: 'Goblins keep coming, and Gang-Up punishes you for letting them pile up. Can your hero control the board, or do they get buried?',
        },
        {
            id: 'mojo',
            villain: 'Mojo',
            mode: 'Standard III',
            test: 'Threat race',
            modulars: 'Two MojoMania sets (required in solo). Pick a fixed pair, e.g. Horror + Western, and always use the same pair.',
            packs: 'MojoMania',
            summary: 'Mass threat, a tempo race and changing TV genres. Can your hero thwart fast enough while still pushing damage? This is the most story-driven fight.',
        },
        {
            id: 'juggernaut',
            villain: 'Juggernaut',
            mode: 'Standard III',
            test: 'Big hits and protecting an ally',
            modulars: 'Smash Bros: Wrecking Crew (+0, ✔) + Hope Summers (required)',
            packs: 'NeXt Evolution, The Hood',
            summary: 'Huge attacks, large brute minions, and Hope Summers to keep alive. Can your hero defend, soak damage and protect someone else?',
            scoringTip: 'If Hope Summers survives, include her remaining HP in "Hero + Ally HP".',
        },
        {
            id: 'mysterio',
            villain: 'Mysterio',
            mode: 'Expert I',
            test: 'Deck disruption',
            modulars: 'The Sinister Seven: Sinister Assault (+1, ✔) + Personal Nightmare (required)',
            packs: 'Sinister Motives',
            summary: 'Illusions are shuffled into your deck and clog your hand, alongside large minions with high boosts. Does your hero\'s engine still work when the draws go bad?',
        },
        {
            id: 'redskull',
            villain: 'Red Skull',
            mode: 'Expert I',
            test: 'Final boss: side schemes',
            modulars: 'Caught Red-Handed: Sinister Syndicate + Iron Spider\'s Sinister Six (+1, ✔), used as side-scheme sets',
            packs: 'The Rise of Red Skull, The Hood, SP//dr hero pack',
            summary: 'A separate side-scheme deck keeps opening new fronts, with attachments and mixed minions. It tests everything at once.',
            alternative: 'No SP//dr? Use the default modular sets (Hydra Assault + Hydra Patrol), which are the same +0 difficulty.',
        },
    ],
    rules: [
        'Use the same modular sets, difficulty and MojoMania pair every run.',
        'The first attempt at each scenario counts. Retries are just for fun.',
        'Nothing carries over between scenarios. Each fight starts fresh and is scored separately.',
        'Optional "Iron" variant: carry your hero\'s remaining HP into the next scenario, like an Expert campaign. Scores are only comparable with other Iron runs.',
    ],
    scoringTips: [
        'Villain Total HP: add up the printed HP of the stages you actually play. Standard uses stages I + II and Expert uses stages II + III, at solo values.',
        'Total Threat Pool: add up the threat thresholds of every main scheme stage.',
        'The campaign score is the total of all five. The individual scores show each hero\'s strengths and weaknesses.',
    ],
};
