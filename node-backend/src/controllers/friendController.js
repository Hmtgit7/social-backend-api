const db = require('../config/db');

/**
 * Send friend request
 * @route POST /api/friends/request
 */
const sendFriendRequest = async (req, res, next) => {
    try {
        const requesterId = req.user.id;
        const addresseeId = parseInt(req.body.userId);

        // Validate addressee ID
        if (isNaN(addresseeId)) {
            return res.status(400).json({
                error: 'Bad Request',
                message: 'Invalid user ID'
            });
        }

        // Check if target user exists
        const userResult = await db.query(
            'SELECT id FROM users WHERE id = $1',
            [addresseeId]
        );

        if (userResult.rows.length === 0) {
            return res.status(404).json({
                error: 'Not Found',
                message: 'User not found'
            });
        }

        // Check if requesting self
        if (requesterId === addresseeId) {
            return res.status(400).json({
                error: 'Bad Request',
                message: 'Cannot send friend request to self'
            });
        }

        // Check if request already exists
        const existingResult = await db.query(
            `SELECT * FROM friends 
       WHERE (requester_id = $1 AND addressee_id = $2)
       OR (requester_id = $2 AND addressee_id = $1)`,
            [requesterId, addresseeId]
        );

        if (existingResult.rows.length > 0) {
            const existing = existingResult.rows[0];

            if (existing.requester_id === requesterId && existing.status === 'pending') {
                return res.status(409).json({
                    error: 'Conflict',
                    message: 'Friend request already sent'
                });
            }

            if (existing.addressee_id === requesterId && existing.status === 'pending') {
                return res.status(409).json({
                    error: 'Conflict',
                    message: 'This user has already sent you a friend request'
                });
            }

            if (existing.status === 'accepted') {
                return res.status(409).json({
                    error: 'Conflict',
                    message: 'You are already friends with this user'
                });
            }

            if (existing.status === 'rejected') {
                // Update the existing rejected request
                await db.query(
                    `UPDATE friends 
           SET requester_id = $1, addressee_id = $2, status = 'pending', updated_at = CURRENT_TIMESTAMP
           WHERE id = $3`,
                    [requesterId, addresseeId, existing.id]
                );

                return res.status(201).json({
                    message: 'Friend request sent successfully',
                    requestId: existing.id
                });
            }
        }

        // Create new friend request
        const result = await db.query(
            `INSERT INTO friends (requester_id, addressee_id, status)
       VALUES ($1, $2, 'pending')
       RETURNING id`,
            [requesterId, addresseeId]
        );

        res.status(201).json({
            message: 'Friend request sent successfully',
            requestId: result.rows[0].id
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Respond to friend request (accept/reject)
 * @route PUT /api/friends/request/:requestId
 */
const respondToFriendRequest = async (req, res, next) => {
    try {
        const userId = req.user.id;
        const requestId = parseInt(req.params.requestId);
        const { action } = req.body;

        // Get the friend request
        const requestResult = await db.query(
            'SELECT * FROM friends WHERE id = $1',
            [requestId]
        );

        if (requestResult.rows.length === 0) {
            return res.status(404).json({
                error: 'Not Found',
                message: 'Friend request not found'
            });
        }

        const request = requestResult.rows[0];

        // Check if user is the addressee
        if (request.addressee_id !== userId) {
            return res.status(403).json({
                error: 'Forbidden',
                message: 'Not authorized to respond to this request'
            });
        }

        // Check if request is pending
        if (request.status !== 'pending') {
            return res.status(409).json({
                error: 'Conflict',
                message: `This request has already been ${request.status}`
            });
        }

        // Update request status
        await db.query(
            `UPDATE friends
       SET status = $1, updated_at = CURRENT_TIMESTAMP
       WHERE id = $2`,
            [action, requestId]
        );

        res.json({
            message: `Friend request ${action}ed successfully`
        });
    } catch (error) {
        next(error);
    }
};

/**
 * List friends
 * @route GET /api/friends
 */
const listFriends = async (req, res, next) => {
    try {
        const userId = req.user.id;
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 10;
        const offset = (page - 1) * limit;

        // Get total count for pagination
        const countResult = await db.query(
            `SELECT COUNT(*) FROM friends
       WHERE (requester_id = $1 OR addressee_id = $1)
       AND status = 'accepted'`,
            [userId]
        );

        const totalFriends = parseInt(countResult.rows[0].count);
        const totalPages = Math.ceil(totalFriends / limit);

        // Get friends with pagination
        const result = await db.query(
            `SELECT f.id AS friendship_id, f.created_at AS friendship_date,
              CASE
                WHEN f.requester_id = $1 THEN f.addressee_id
                ELSE f.requester_id
              END AS friend_id,
              u.name, u.email, u.bio
       FROM friends f
       JOIN users u ON (
         CASE
           WHEN f.requester_id = $1 THEN u.id = f.addressee_id
           ELSE u.id = f.requester_id
         END
       )
       WHERE (f.requester_id = $1 OR f.addressee_id = $1)
       AND f.status = 'accepted'
       ORDER BY u.name ASC
       LIMIT $2 OFFSET $3`,
            [userId, limit, offset]
        );

        res.json({
            friends: result.rows,
            pagination: {
                total: totalFriends,
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
 * List pending friend requests (both sent and received)
 * @route GET /api/friends/requests
 */
const listFriendRequests = async (req, res, next) => {
    try {
        const userId = req.user.id;

        // Get received requests
        const receivedResult = await db.query(
            `SELECT f.id, f.requester_id, f.created_at, f.status, 
              u.name, u.email
       FROM friends f
       JOIN users u ON f.requester_id = u.id
       WHERE f.addressee_id = $1 AND f.status = 'pending'
       ORDER BY f.created_at DESC`,
            [userId]
        );

        // Get sent requests
        const sentResult = await db.query(
            `SELECT f.id, f.addressee_id, f.created_at, f.status,
              u.name, u.email
       FROM friends f
       JOIN users u ON f.addressee_id = u.id
       WHERE f.requester_id = $1 AND f.status = 'pending'
       ORDER BY f.created_at DESC`,
            [userId]
        );

        res.json({
            received: receivedResult.rows,
            sent: sentResult.rows
        });
    } catch (error) {
        next(error);
    }
};

/**
 * Get friend suggestions
 * @route GET /api/friends/suggestions
 */
const getFriendSuggestions = async (req, res, next) => {
    try {
        const userId = req.user.id;
        const limit = 5; // Limit to 5 suggestions

        // Get IDs of current friends and pending requests
        const existingConnectionsResult = await db.query(
            `SELECT 
        CASE
          WHEN requester_id = $1 THEN addressee_id
          ELSE requester_id
        END AS connected_user_id
       FROM friends
       WHERE (requester_id = $1 OR addressee_id = $1)`,
            [userId]
        );

        // Extract user IDs to exclude (self + connections)
        const excludeIds = [userId];
        existingConnectionsResult.rows.forEach(row => {
            excludeIds.push(row.connected_user_id);
        });

        // Get random suggestions excluding connections
        const suggestionsResult = await db.query(
            `SELECT id, name, email, bio
       FROM users
       WHERE id != ALL($1)
       ORDER BY RANDOM()
       LIMIT $2`,
            [excludeIds, limit]
        );

        res.json({
            suggestions: suggestionsResult.rows
        });
    } catch (error) {
        next(error);
    }
};

module.exports = {
    sendFriendRequest,
    respondToFriendRequest,
    listFriends,
    listFriendRequests,
    getFriendSuggestions
};