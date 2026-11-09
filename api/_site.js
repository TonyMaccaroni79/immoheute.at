// Seitenspezifische Einstellungen fuer die Formulare von immoheute.at.
// Einwilligungstexte exakt wie auf der Seite; Version erhoehen, wenn ein Text geaendert wird.
export const SITE = {
  name: 'immoheute', domain: 'immoheute.at', base: 'https://immoheute.at',
  anliegen: ['verkauf', 'bewertung', 'erbe', 'trennung', 'steuer', 'anderes'],
  einwilligung: {
    newsletter: ['v1', 'Ja, ich möchte neue Ratgeber und Steuer-Änderungen rund um den Immobilienverkauf per E-Mail (höchstens einmal im Monat, jederzeit abbestellbar). Ich bekomme dazu eine Bestätigungs-E-Mail.'],
    anfrage: ['v1', 'Ich möchte, dass immoheute (FRABANTO AUSTRIA GmbH) mich zu meiner Anfrage kontaktiert und meine Angaben dafür speichert. Ich kann das jederzeit widerrufen.'],
    partner: ['v1', 'Freiwillig: Wenn es passt, darf immoheute meine Anfrage an einen geprüften Partner (z. B. Makler oder Gutachter) weitergeben. Welcher Partner das ist, erfahre ich vorher und kann dann noch ablehnen.'],
  },
};
