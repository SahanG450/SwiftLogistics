FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy shared utilities
COPY ../../shared /app/shared

# Copy source code
COPY src ./src

# Expose port
EXPOSE 3001

# Start the application
CMD ["npm", "start"]
