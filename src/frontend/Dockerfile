# Dockerfile multi-stage para desenvolvimento e produção
# Para desenvolvimento: docker build --target development
# Para produção: docker build --target production

# Stage 1: Base com Node.js
FROM node:18-alpine as base
WORKDIR /app
COPY package*.json ./

# Stage 2: Desenvolvimento
FROM base as development
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# Stage 3: Build para produção
FROM base as build
RUN npm ci --only=production --silent
COPY . .
RUN npm run build

# Stage 4: Produção com nginx
FROM nginx:alpine as production
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
