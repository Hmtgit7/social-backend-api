const db = require('../config/db');

/**
 * Get current user profile
 * @route GET /api/users/me
 */
const getCurrentUser = async (req, res, next) => {
    try {
        const userId = req.user.id;

        const result = await db.query(
            'SELECT id, name, email, bio, created_at FROM users WHERE id = $1',
            [userId]
        );

        if (result.rows.length === 0) {
            return res.status(404).json({
                error: 'Not found',
                message: 'User not found'
            });
        }

        res.json({
            user: result.rows[0]
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Update current user profile
 * @route PUT /api/users/me
 */
const updateProfile = async (req, res, next) => {
    try {
        const userId = req.user.id;
        const { name, bio } = req.body;

        // Build dynamic query based on provided fields
        let updateFields = [];
        let queryParams = [];
        let paramCounter = 1;

        if (name !== undefined) {
            updateFields.push(`name = $${paramCounter}`);
            queryParams.push(name);
            paramCounter++;
        }

        if (bio !== undefined) {
            updateFields.push(`bio = $${paramCounter}`);
            queryParams.push(bio);
            paramCounter++;
        }

        // Add updated_at timestamp
        updateFields.push(`updated_at = CURRENT_TIMESTAMP`);

        // If no fields to update, return current user
        if (updateFields.length === 1) {
            return getCurrentUser(req, res, next);
        }

        // Add user ID to params
        queryParams.push(userId);

        const query = `
      UPDATE users
      SET ${updateFields.join(', ')}
      WHERE id = $${paramCounter}
      RETURNING id, name, email, bio, updated_at
    `;

        const result = await db.query(query, queryParams);

        res.json({
            message: 'Profile updated successfully',
            user: result.rows[0]
        });
    } catch (error) {
        next(error);
    }
};

/**
 * List all users except current user
 * @route GET /api/users
 */
const listUsers = async (req, res, next) => {
    try {
        const userId = req.user.id;
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 10;
        const offset = (page - 1) * limit;

        // Get total count for pagination
        const countResult = await db.query(
            'SELECT COUNT(*) FROM users WHERE id != $1',
            [userId]
        );

        const totalUsers = parseInt(countResult.rows[0].count);
        const totalPages = Math.ceil(totalUsers / limit);

        // Get users with pagination
        const result = await db.query(
            `SELECT id, name, email, bio, created_at FROM users
       WHERE id != $1
       ORDER BY name ASC
       LIMIT $2 OFFSET $3`,
            [userId, limit, offset]
        );

        res.json({
            users: result.rows,
            pagination: {
                total: totalUsers,
                page,
                limit,
                totalPages
            }
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Search users by name
 * @route GET /api/users/search
 */
const searchUsers = async (req, res, next) => {
    try {
        const userId = req.user.id;
        const searchName = req.query.name || '';
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 10;
        const offset = (page - 1) * limit;

        // Get total count for pagination
        const countResult = await db.query(
            `SELECT COUNT(*) FROM users 
       WHERE id != $1 AND name ILIKE $2`,
            [userId, `%${searchName}%`]
        );

        const totalUsers = parseInt(countResult.rows[0].count);
        const totalPages = Math.ceil(totalUsers / limit);

        // Get users with pagination
        const result = await db.query(
            `SELECT id, name, email, bio, created_at FROM users
       WHERE id != $1 AND name ILIKE $2
       ORDER BY name ASC
       LIMIT $3 OFFSET $4`,
            [userId, `%${searchName}%`, limit, offset]
        );

        res.json({
            users: result.rows,
            pagination: {
                total: totalUsers,
                page,
                limit,
                totalPages
            }
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Get user by ID
 * @route GET /api/users/:id
 */
const getUserById = async (req, res, next) => {
    try {
        const userId = parseInt(req.params.id);

        if (isNaN(userId)) {
            return res.status(400).json({
                error: 'Bad Request',
                message: 'Invalid user ID'
            });
        }

        const result = await db.query(
            'SELECT id, name, email, bio, created_at FROM users WHERE id = $1',
            [userId]
        );

        if (result.rows.length === 0) {
            return res.status(404).json({
                error: 'Not Found',
                message: 'User not found'
            });
        }

        res.json({
            user: result.rows[0]
        });
    } catch (error) {
        next(error);
    }
};

module.exports = {
    getCurrentUser,
    updateProfile,
    listUsers,
    searchUsers,
    getUserById
};