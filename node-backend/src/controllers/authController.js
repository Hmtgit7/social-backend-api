const bcrypt = require('bcrypt');
const { OAuth2Client } = require('google-auth-library');
const db = require('../config/db');
const { generateToken } = require('../utils/jwtUtils');

// Google OAuth client for verifying tokens
const googleClient = process.env.GOOGLE_CLIENT_ID
    ? new OAuth2Client(process.env.GOOGLE_CLIENT_ID)
    : null;

/**
 * Register a new user
 * @route POST /api/auth/register
 */
const register = async (req, res, next) => {
    try {
        const { name, email, password } = req.body;

        // Check if user already exists
        const existingUser = await db.query(
            'SELECT * FROM users WHERE email = $1',
            [email]
        );

        if (existingUser.rows.length > 0) {
            return res.status(409).json({
                error: 'Registration failed',
                message: 'User with that email already exists'
            });
        }

        // Hash password
        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        // Create new user
        const result = await db.query(
            'INSERT INTO users (name, email, password) VALUES ($1, $2, $3) RETURNING id, name, email, created_at',
            [name, email, hashedPassword]
        );

        const user = result.rows[0];

        // Generate JWT token
        const token = generateToken(user);

        res.status(201).json({
            message: 'User registered successfully',
            user: {
                id: user.id,
                name: user.name,
                email: user.email,
                created_at: user.created_at
            },
            token
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Login a user
 * @route POST /api/auth/login
 */
const login = async (req, res, next) => {
    try {
        const { email, password } = req.body;

        // Find user by email
        const result = await db.query(
            'SELECT * FROM users WHERE email = $1',
            [email]
        );

        if (result.rows.length === 0) {
            return res.status(401).json({
                error: 'Authentication failed',
                message: 'Invalid email or password'
            });
        }

        const user = result.rows[0];

        // Check if user has a password (could be Google-auth only user)
        if (!user.password) {
            return res.status(401).json({
                error: 'Authentication failed',
                message: 'This account uses Google authentication'
            });
        }

        // Verify password
        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch) {
            return res.status(401).json({
                error: 'Authentication failed',
                message: 'Invalid email or password'
            });
        }

        // Generate JWT token
        const token = generateToken(user);

        res.json({
            message: 'Login successful',
            user: {
                id: user.id,
                name: user.name,
                email: user.email
            },
            token
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Google Authentication
 * @route POST /api/auth/google
 */
const googleAuth = async (req, res, next) => {
    try {
        // Make sure Google authentication is configured
        if (!googleClient) {
            return res.status(501).json({
                error: 'Not implemented',
                message: 'Google authentication is not configured'
            });
        }

        const { token } = req.body;

        // Verify Google token
        const ticket = await googleClient.verifyIdToken({
            idToken: token,
            audience: process.env.GOOGLE_CLIENT_ID
        });

        const payload = ticket.getPayload();
        const { sub: googleId, email, name } = payload;

        // Check if user exists
        const { rows } = await db.query(
            'SELECT * FROM users WHERE google_id = $1 OR email = $2',
            [googleId, email]
        );

        let user;

        if (rows.length > 0) {
            // User exists, update google_id if needed
            user = rows[0];

            if (!user.google_id) {
                await db.query(
                    'UPDATE users SET google_id = $1 WHERE id = $2',
                    [googleId, user.id]
                );
            }
        } else {
            // Create new user
            const result = await db.query(
                'INSERT INTO users (name, email, google_id) VALUES ($1, $2, $3) RETURNING *',
                [name, email, googleId]
            );

            user = result.rows[0];
        }

        // Generate JWT token
        const jwtToken = generateToken(user);

        res.json({
            message: 'Google authentication successful',
            user: {
                id: user.id,
                name: user.name,
                email: user.email
            },
            token: jwtToken
        });
    } catch (error) {
        next(error);
    }
};

module.exports = {
    register,
    login,
    googleAuth
};