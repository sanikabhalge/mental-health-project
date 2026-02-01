const RISK_PHRASES = [
  "i want to die",
  "i can't go on",
  "kill myself",
];

export function checkRiskPhrases(text) {
  if (!text || typeof text !== "string") return false;
  const lower = text.toLowerCase().trim();
  return RISK_PHRASES.some((phrase) => lower.includes(phrase));
}
