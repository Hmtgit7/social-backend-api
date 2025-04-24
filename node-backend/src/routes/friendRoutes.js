const express = require('express');
const { authenticate } = require('../middleware/auth');
const { validate } = require('../middleware/validation');
const {
    friendRequestValidator,
    friendResponseValidator,
    friendListValidator
} = require('../validators/friendValidator');
const {
    sendFriendRequest,
    respondToFriendRequest,
    listFriends,
    listFriendRequests,
    getFriendSuggestions
} = require('../controllers/friendController');

const router = express.Router();

// Apply authentication middleware to all routes
router.use(authenticate);

/**
 * @route POST /api/friends/request
 * @desc Send a friend request
 * @access Private
 */
router.post('/request', friendRequestValidator, validate, sendFriendRequest);

/**
 * @route PUT /api/friends/request/:requestId
 * @desc Respond to a friend request (accept/reject)
 * @access Private
 */
router.put('/request/:requestId', friendResponseValidator, validate, respondToFriendRequest);

/**
 * @route GET /api/friends/requests
 * @desc List pending friend requests (both sent and received)
 * @access Private
 */
router.get('/requests', listFriendRequests);

/**
 * @route GET /api/friends/suggestions
 * @desc Get friend suggestions
 * @access Private
 */
router.get('/suggestions', getFriendSuggestions);

/**
 * @route GET /api/friends
 * @desc List all friends
 * @access Private
 */
router.get('/', friendListValidator, validate, listFriends);

module.exports = router;