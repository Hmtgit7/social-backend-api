const passport = require('passport');
const { Strategy: JwtStrategy, ExtractJwt } = require('passport-jwt');
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const db = require('./db');

// Configure JWT Strategy
const jwtOptions = {
    jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
    secretOrKey: process.env.JWT_SECRET || 'your-secret-key'
};

passport.use(
    new JwtStrategy(jwtOptions, async (jwtPayload, done) => {
        try {
            const { rows } = await db.query(
                'SELECT id, name, email FROM users WHERE id = $1',
                [jwtPayload.id]
            );

            if (rows.length > 0) {
                return done(null, rows[0]);
            }
            return done(null, false);
        } catch (error) {
            return done(error, false);
        }
    })
);

// Configure Google Strategy (if GOOGLE credentials are provided)
if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
    passport.use(
        new GoogleStrategy(
            {
                clientID: process.env.GOOGLE_CLIENT_ID,
                clientSecret: process.env.GOOGLE_CLIENT_SECRET,
                callbackURL: '/api/auth/google/callback',
                scope: ['profile', 'email']
            },
            async (accessToken, refreshToken, profile, done) => {
                try {
                    // Check if user exists
                    const { rows } = await db.query(
                        'SELECT * FROM users WHERE google_id = $1 OR email = $2',
                        [profile.id, profile.emails[0].value]
                    );

                    if (rows.length > 0) {
                        // User exists, update google_id if needed
                        if (!rows[0].google_id) {
                            await db.query(
                                'UPDATE users SET google_id = $1 WHERE id = $2',
                                [profile.id, rows[0].id]
                            );
                        }
                        return done(null, rows[0]);
                    }

                    // Create new user
                    const newUser = {
                        name: profile.displayName,
                        email: profile.emails[0].value,
                        google_id: profile.id
                    };

                    const result = await db.query(
                        'INSERT INTO users (name, email, google_id) VALUES ($1, $2, $3) RETURNING *',
                        [newUser.name, newUser.email, newUser.google_id]
                    );

                    return done(null, result.rows[0]);
                } catch (error) {
                    return done(error, false);
                }
            }
        )
    );
}