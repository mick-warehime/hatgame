FROM python:3.7
COPY requirements.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements.txt
ADD . /app
WORKDIR /app/server
EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]

FROM node:alpine AS node_builder
WORKDIR /app/client
RUN npm install
EXPOSE 8080
CMD [ "npm", "run", "prod" ]

# COPY --from=builder /app/client ./
# RUN npm install
# RUN npm run build