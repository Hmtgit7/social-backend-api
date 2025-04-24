const express = require('express');
const passport = require('passport');
const { validate } = require('../middleware/validation');
const { registerValidator, loginValidator } = require('../validators/authValidator');
const { register, login, googleAuth } = require('../controllers/authController');

const router = express.Router();

/**
 * @route POST /api/auth/register
 * @desc Register a new user
 * @access Public
 */
router.post('/register', registerValidator, validate, register);

/**
 * @route POST /api/auth/login
 * @desc Login a user and return JWT token
 * @access Public
 */
router.post('/login', loginValidator, validate, login);

/**
 * @route POST /api/auth/google
 * @desc Authenticate with Google ID token
 * @access Public
 */
router.post('/google', googleAuth);

/**
 * @route GET /api/auth/google/callback
 * @desc Handle Google OAuth callback (for web flow)
 * @access Public
 */
router.get(
    '/google/callback',
    passport.authenticate('google', { session: false }),
    (req, res) => {
        // Create JWT token
        const token = require('../utils/jwtUtils').generateToken(req.user);

        // Redirect to frontend with token (adjust URL as needed)
        res.redirect(`${process.env.FRONTEND_URL || '/'}/auth/callback?token=${token}`);
    }
);

module.exports = router;