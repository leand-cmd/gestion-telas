FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

ARG VITE_API_URL
ARG VITE_GOOGLE_MAPS_API_KEY
ENV VITE_API_URL=${VITE_API_URL}
ENV VITE_GOOGLE_MAPS_API_KEY=${VITE_GOOGLE_MAPS_API_KEY}

RUN npm run build

FROM nginx:alpine

COPY nginx.conf /etc/nginx/templates/default.conf.template

COPY --from=builder /app/dist /usr/share/nginx/html

ENV PORT=3000
EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
