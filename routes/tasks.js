routes/tasks.js

const express = require('express');
const router = express.Router();
let tasks = require('../data/tasks');

// Feature 2: Add Task
router.post('/', (req, res) => {
    const task = req.body.task;
    tasks.push(task);

    res.json({
        message: "Task added successfully",
        tasks
    });
});

// View Tasks
router.get('/', (req, res) => {
    res.json(tasks);
});

module.exports = router;
