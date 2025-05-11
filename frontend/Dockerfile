
FROM node:16-alpine

# Set working directory
WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application source
COPY . .

# Expose development port
EXPOSE 3000

# Ensure react-scripts is available
RUN npm install react-scripts

# Start development server
CMD ["npm", "start"]





# FROM node:16-alpine

# WORKDIR /app

# # Copy package files and install dependencies
# COPY package*.json ./
# RUN npm install

# # Copy the rest of the application
# COPY . .

# # Expose the port used by `npm start`
# EXPOSE 3000

# # Start the development server
# CMD ["npm", "start"]



# FROM node:16-alpine

# WORKDIR /app

# # Copy package files
# COPY package*.json ./
# RUN npm install

# # Copy the rest of the application
# COPY . .

# # Build the application
# RUN npm run build

# # Install serve to run the application
# RUN npm install -g serve

# EXPOSE 3000

# CMD ["serve", "-s", "build", "-l", "3000"]