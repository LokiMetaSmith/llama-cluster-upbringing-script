const express = require('express');
const { embed, similar } = require('@ternlight/base');

const app = express();
app.use(express.json({ limit: '10mb' }));

const PORT = process.env.PORT || 8000;

/**
 * Health check endpoint
 */
app.get('/health', (req, res) => {
  res.json({ status: 'ok', engine: 'ternlight' });
});

// Authentication middleware
const authenticate = (req, res, next) => {
  const expectedToken = process.env.TERNLIGHT_API_KEY;
  if (expectedToken) {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Missing or invalid Authorization header' });
    }
    const token = authHeader.split(' ')[1];
    if (token !== expectedToken) {
      return res.status(403).json({ error: 'Invalid API Key' });
    }
  }
  next();
};

/**
 * Embed text
 * POST /embed
 * Body: { text: string }
 */
app.post('/embed', authenticate, async (req, res) => {
  try {
    const { text } = req.body;
    if (!text) {
      return res.status(400).json({ error: 'Text is required' });
    }
    const embedding = await embed(text);
    res.json({ embedding });
  } catch (error) {
    console.error('Embedding error:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * Similarity search
 * POST /similar
 * Body: { query: string, documents: string[] | {content: string}[], topK: number }
 */
app.post('/similar', authenticate, async (req, res) => {
  try {
    const { query, documents, topK = 5 } = req.body;
    if (!query || !documents) {
      return res.status(400).json({ error: 'Query and documents are required' });
    }

    // Ternlight similar() takes (queryText, dataArray, options)
    // dataArray can be strings or objects with content
    const results = await similar(query, documents, { topK });
    res.json({ results });
  } catch (error) {
    console.error('Similarity search error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Ternlight service listening on port ${PORT}`);
});
