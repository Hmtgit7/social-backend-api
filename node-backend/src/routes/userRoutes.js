const express = require('express');
const { authenticate } = require('../middleware/auth');
const { validate } = require('../middleware/validation');
const { updateProfileValidator, searchUserValidator } = require('../validators/userValidator');
const {
    getCurrentUser,
    updateProfile,
    listUsers,
    searchUsers,
    getUserById
} = require('../controllers/userController');

const router = express.Router();

// Apply authentication middleware to all routes
router.use(authenticate);

/**
 * @route GET /api/users/me
 * @desc Get current user profile
 * @access Private
 */
router.get('/me', getCurrentUser);

/**
 * @route PUT /api/users/me
 * @desc Update current user profile
 * @access Private
 */
router.put('/me', updateProfileValidator, validate, updateProfile);

/**
 * @route GET /api/users/search
 * @desc Search users by name
 * @access Private
 */
router.get('/search', searchUserValidator, validate, searchUsers);

/**
 * @route GET /api/users/:id
 * @desc Get user by ID
 * @access Private
 */
router.get('/:id', getUserById);

/**
 * @route GET /api/users
 * @desc List all users except current user
 * @access Private
 */
router.get('/', listUsers);

module.exports = router;