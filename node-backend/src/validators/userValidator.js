const { body, query } = require('express-validator');

// Validation rules for updating user profile
const updateProfileValidator = [
    body('name')
        .optional()
        .trim()
        .isLength({ min: 2, max: 100 })
        .withMessage('Name must be between 2 and 100 characters'),

    body('bio')
        .optional()
        .trim()
        .isLength({ max: 500 })
        .withMessage('Bio must not exceed 500 characters')
];

// Validation rules for search query
const searchUserValidator = [
    query('name')
        .optional()
        .trim()
        .isLength({ min: 1 })
        .withMessage('Search term must not be empty'),

    query('page')
        .optional()
        .isInt({ min: 1 })
        .withMessage('Page must be a positive integer'),

    query('limit')
        .optional()
        .isInt({ min: 1, max: 100 })
        .withMessage('Limit must be between 1 and 100')
];

module.exports = {
    updateProfileValidator,
    searchUserValidator
};