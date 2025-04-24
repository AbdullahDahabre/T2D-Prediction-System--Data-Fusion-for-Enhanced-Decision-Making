#!/bin/bash

# Create main project directory
mkdir -p my-backend
cd my-backend

# Initialize npm project
npm init -y

# Install dependencies
npm install express cors body-parser mongoose jsonwebtoken dotenv
npm install nodemon --save-dev

# Update package.json to include start scripts
sed -i.bak '/"scripts": {/a\
    "start": "node server.js",\
    "dev": "nodemon server.js",
' package.json
rm package.json.bak

# Create directory structure
mkdir -p config controllers middleware models routes/api

# Create .env file
cat > .env << EOL
MONGO_URI=mongodb://localhost:27017/your_database
JWT_SECRET=your_jwt_secret
PORT=5000
EOL

# Create .gitignore
cat > .gitignore << EOL
node_modules/
.env
package-lock.json
.DS_Store
EOL

# Create config/db.js
cat > config/db.js << EOL
const mongoose = require('mongoose');
require('dotenv').config();

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
    console.log('MongoDB connected');
  } catch (err) {
    console.error('Database connection error:', err.message);
    process.exit(1);
  }
};

module.exports = connectDB;
EOL

# Create middleware/auth.js
cat > middleware/auth.js << EOL
const jwt = require('jsonwebtoken');
require('dotenv').config();

module.exports = function(req, res, next) {
  // Get token from header
  const token = req.header('x-auth-token');

  // Check if no token
  if (!token) {
    return res.status(401).json({ msg: 'No token, authorization denied' });
  }

  // Verify token
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded.user;
    next();
  } catch (err) {
    res.status(401).json({ msg: 'Token is not valid' });
  }
};
EOL

# Create routes/api/users.js
cat > routes/api/users.js << EOL
const express = require('express');
const router = express.Router();

// @route   POST api/users/register
// @desc    Register a user
// @access  Public
router.post('/register', (req, res) => {
  // Registration logic will go here
  res.send('User registration route');
});

// @route   POST api/users/login
// @desc    Authenticate user & get token
// @access  Public
router.post('/login', (req, res) => {
  // Authentication logic will go here
  res.send('User login route');
});

module.exports = router;
EOL

# Create server.js
cat > server.js << EOL
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');
require('dotenv').config();

// Initialize express app
const app = express();
const PORT = process.env.PORT || 5000;

// Connect to database
connectDB();

// Middleware
app.use(express.json({ extended: false }));
app.use(cors());

// Define Routes
app.use('/api/users', require('./routes/api/users'));

// Basic test route
app.get('/', (req, res) => {
  res.send('API Running');
});

// Start server
app.listen(PORT, () => {
  console.log(\`Server running on port \${PORT}\`);
});
EOL

echo "Backend structure created successfully!"
echo "To start your