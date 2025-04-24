const { body, param, query } = require('express-validator');

// Validation rules for sending friend request
const friendRequestValidator = [
    body('userId')
        .notEmpty()
        .withMessage('User ID is required')
        .isInt({ min: 1 })
        .withMessage('User ID must be a valid integer')
];

// Validation rules for responding to a friend request
const friendResponseValidator = [
    param('requestId')
        .notEmpty()
        .withMessage('Request ID is required')
        .isInt({ min: 1 })
        .withMessage('Request ID must be a valid integer'),

    body('action')
        .notEmpty()
        .withMessage('Action is required')
        .isIn(['accept', 'reject'])
        .withMessage('Action must be either "accept" or "reject"')
];

// Validation rules for friend list pagination
const friendListValidator = [
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
    friendRequestValidator,
    friendResponseValidator,
    friendListValidator
};