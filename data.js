/* Tables d'addition — donnees de l'app.
 *
 * Tout ce qu'on peut vouloir regler sans toucher a la logique (app.js).
 */
window.APP_DATA = {
  title: "Tables d'Addition",

  // Une « table de N » = N + 1, N + 2, ... N + 10.
  tables: { min: 1, max: 10, defaults: [2, 3, 4, 5] },
  terms: { min: 1, max: 10 },

  // Au-dela, une bonne reponse compte comme une hesitation (a revoir).
  slowMs: 4000,

  // Plus grande somme possible = 20 -> 2 chiffres.
  maxDigits: 2,

  // Une question ratee revient entre 1 et `requeueSpan` questions plus loin.
  requeueSpan: 4,

  mascots: ['🦊', '🐸', '🦁', '🐼', '🦄', '🐯', '🐧', '🦋'],

  // Du meilleur au moins bon ; {rate} = taux de reussite en %.
  tiers: [
    { min: 100, emoji: '🏆', title: 'Parfait !', sub: 'Tu as tout bon du premier coup, champion !' },
    { min: 80, emoji: '⭐', title: 'Excellent !', sub: '{rate}% de réussite, c\'est super !' },
    { min: 60, emoji: '👍', title: 'Bien joué !', sub: '{rate}% de réussite, continue à t\'entraîner !' },
    { min: 0, emoji: '💪', title: 'Courage !', sub: '{rate}% — pratique encore, tu vas y arriver !' },
  ],
};
