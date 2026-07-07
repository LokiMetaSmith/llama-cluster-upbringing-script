/**
 * Ternlight Client-side Embedding and Search
 * Adapted for use in the Pipecat App Mission Control
 */

class TernlightClient {
    constructor(serviceUrl = null) {
        this.serviceUrl = serviceUrl || window.location.origin;
        this.isLoaded = false;
    }

    async init() {
        // In a real browser environment, we might load the 7MB model here via WASM or a script tag.
        // For this integration, we'll proxy to our Ternlight microservice if available,
        // or simulate the "Instant Search" if the microservice is not reachable.
        try {
            const resp = await fetch(`${this.serviceUrl}/health`);
            this.isLoaded = resp.ok;
        } catch (e) {
            console.warn("Ternlight microservice not reachable, falling back to mock mode.");
            this.isLoaded = false;
        }
        return this.isLoaded;
    }

    async search(query, documents, topK = 5) {
        if (!this.isLoaded) {
            // Mock search for demo purposes if service is down
            console.log("Mocking Ternlight search...");
            return documents
                .filter(doc => {
                    const content = typeof doc === 'string' ? doc : doc.content;
                    return content.toLowerCase().includes(query.toLowerCase());
                })
                .slice(0, topK);
        }

        try {
            const response = await fetch(`${this.serviceUrl}/similar`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query, documents, topK })
            });
            const data = await response.json();
            return data.results;
        } catch (e) {
            console.error("Ternlight search failed:", e);
            return [];
        }
    }
}

// Export for use in other scripts
window.TernlightClient = TernlightClient;
