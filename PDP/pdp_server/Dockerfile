
FROM node:latest
# Create app directory
WORKDIR /app

# Install app dependencies
COPY package.json  ./
RUN npm install 

# Bundle app source
COPY . .

# Declaring PROT in containers
EXPOSE 3000
CMD [ "npm", "start" ]