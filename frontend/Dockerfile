# Koristi zvaničnu Node.js sliku za build
FROM node:18 AS builder

# Postavi radni direktorijum
WORKDIR /frontend-app

# Kopiraj package.json i install dependencies
COPY package*.json ./
RUN npm install

# Kopiraj ostatak aplikacije
COPY . .

# Izgradi aplikaciju
RUN npm run build --prod

# Koristi Nginx za posluživanje izgrađene aplikacije
FROM nginx:alpine
COPY --from=builder /frontend-app/dist/frontend/browser /usr/share/nginx/html

# Kopiraj Nginx konfiguraciju
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
