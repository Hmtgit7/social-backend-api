const { validationResult } = require('express-validator');

/**
 * Middleware to validate request against express-validator rules
 */
const validate = (req, res, next) => {
    const errors = validationResult(req);

    if (!errors.isEmpty()) {
        return res.status(400).json({
            error: 'Validation Error',
            details: errors.array().map(error => ({
                field: error.param,
                message: error.msg
            }))
        });
    }

    return next();
};

module.exports = {
    validate
};