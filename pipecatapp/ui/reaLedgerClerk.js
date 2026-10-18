// reaLedgerClerk.js — Drop-in REA Write-Ahead Clerk for EISPP SubmitButton
export async function commitPreferencesToREALedger({
  agentId,
  clerkId = "eispp:agent/lumina-nao",
  globalToggleState,
  stagedRowDiffs,
  scratchpadDragCount = 0
}) {
  // 1. Guard: Policy Resource check (Global Toggle)
  if (!globalToggleState.enabled || globalToggleState.lockChildren) {
    throw new Error("REA Policy Violation: Global toggle locks child preference mutations.");
  }

  const timestamp = new Date().toISOString();
  const processId = `eispp:process/submit-commit-${crypto.randomUUID()}`;

  // 2. Construct deterministic ValueFlows Bundle from ephemeral UI scratchpad
  const vfBundle = {
    "@context": "https://w3id.org/valueflows#",
    "@id": `urn:uuid:${crypto.randomUUID()}`,
    "@type": "vf:Bundle",
    "prov:generatedAtTime": timestamp,
    "vf:Process": {
      "@id": processId,
      "@type": "vf:Process",
      "eispp:discardedScratchpadIntents": scratchpadDragCount,
      "vf:hasInput": [
        {
          "@type": "vf:EconomicEvent",
          "vf:action": "cite",
          "vf:provider": agentId,
          "vf:resourceInventoriedAs": "eispp:resource/global-toggle-master",
          "vf:created": timestamp
        }
      ],
      "vf:hasOutput": stagedRowDiffs.map((diff) => ({
        "@id": `eispp:event/modify-${diff.rowId}-${Date.now()}`,
        "@type": "vf:EconomicEvent",
        "vf:action": "modify",
        "vf:provider": agentId,
        "vf:receiver": clerkId,
        "vf:resourceInventoriedAs": `eispp:resource/${diff.rowId}`,
        "vf:created": timestamp,
        "eispp:stateDiff": {
          from: diff.previousValue,
          to: diff.newValue
        }
      }))
    }
  };

  // 3. Emit to local append-only write-ahead log (or NAO Gateway endpoint)
  console.debug("[REA-Clerk] Committing vf:Bundle:", JSON.stringify(vfBundle, null, 2));
  return vfBundle;
}
