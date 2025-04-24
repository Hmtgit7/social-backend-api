/**
 * Database initialization script
 * Run with: node scripts/init-db.js
 */

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const { Pool } = require('pg');

// Create database connection
const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT || 5432
});

async function initializeDatabase() {
    try {
        console.log('Starting database initialization...');

        // Read SQL initialization file
        const sqlFilePath = path.join(__dirname, '..', 'db', 'init.sql');
        const sqlScript = fs.readFileSync(sqlFilePath, 'utf8');

        // Execute SQL script
        await pool.query(sqlScript);

        console.log('Database initialized successfully!');
    } catch (error) {
        console.error('Error initializing database:', error);
    } finally {
        // Close pool
        await pool.end();
    }
}

// Run initialization
initializeDatabase();