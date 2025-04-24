/**
 * Global error handler middleware
 */
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);

    // Handle validation errors
    if (err.name === 'ValidationError') {
        return res.status(400).json({
            error: 'Validation Error',
            details: err.errors
        });
    }

    // Handle duplicate key errors (PostgreSQL error code 23505)
    if (err.code === '23505') {
        return res.status(409).json({
            error: 'Conflict',
            message: 'A resource with that identifier already exists'
        });
    }

    // Handle JWT errors
    if (err.name === 'JsonWebTokenError') {
        return res.status(401).json({
            error: 'Unauthorized',
            message: 'Invalid token'
        });
    }

    if (err.name === 'TokenExpiredError') {
        return res.status(401).json({
            error: 'Unauthorized',
            message: 'Token expired'
        });
    }

    // Custom API error
    if (err.statusCode) {
        return res.status(err.statusCode).json({
            error: err.name || 'Error',
            message: err.message
        });
    }

    // Default to 500 server error
    return res.status(500).json({
        error: 'Internal Server Error',
        message: process.env.NODE_ENV === 'production'
            ? 'Something went wrong'
            : err.message
    });
};

module.exports = errorHandler;