const ms = require("ms");

const raw = process.argv[2];
const payload = raw ? JSON.parse(raw) : {};

const name = payload.name || "World";
const start = Date.now();

// Simulate a tiny bit of work
const result = {
  message: `Hello, ${name}!`,
  elapsed: ms(Date.now() - start || 1),
};

process.stdout.write(JSON.stringify(result) + "\n");
