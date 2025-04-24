const passport = require('passport');

/**
 * Authentication middleware using Passport JWT strategy
 */
const authenticate = (req, res, next) => {
    passport.authenticate('jwt', { session: false }, (err, user, info) => {
        if (err) {
            return next(err);
        }

        if (!user) {
            return res.status(401).json({
                error: 'Unauthorized',
                message: info ? info.message : 'Authentication required'
            });
        }

        // Attach the authenticated user to the request object
        req.user = user;
        return next();
    })(req, res, next);
};

module.exports = {
    authenticate
};